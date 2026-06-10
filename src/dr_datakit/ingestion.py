from pathlib import Path
from datetime import datetime, date
import calendar
import re
import warnings

import pandas as pd


SUPPORTED_EXTENSIONS = ("csv", "xlsx", "xls", "txt", "parquet")


def _read_file(
    path,
    sep: str = ";",
    usecols=None,
    dtype=str,
    parquet_as_str: bool = False,
    **kwargs,
) -> pd.DataFrame:
    """
    Read a file based on its extension.

    Supported formats:
    - CSV
    - TXT
    - Excel
    - Parquet
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if not path.is_file():
        raise ValueError(f"Path is not a file: {path}")

    suffix = path.suffix.lower()

    if suffix in [".xlsx", ".xls"]:
        return pd.read_excel(
            path,
            dtype=dtype,
            usecols=usecols,
            **kwargs,
        )

    if suffix == ".parquet":
        df = pd.read_parquet(path, **kwargs)

        if usecols is not None:
            df = df[usecols]

        if parquet_as_str:
            df = df.astype(str)

        return df

    if suffix in [".csv", ".txt"]:
        try:
            return pd.read_csv(
                path,
                sep=sep,
                encoding="utf-8",
                dtype=dtype,
                usecols=usecols,
                **kwargs,
            )
        except UnicodeDecodeError:
            return pd.read_csv(
                path,
                sep=sep,
                encoding="ISO-8859-1",
                dtype=dtype,
                usecols=usecols,
                **kwargs,
            )

    raise ValueError(
        f"Unsupported file extension: {suffix}. "
        f"Supported extensions are: {SUPPORTED_EXTENSIONS}"
    )


def _extract_date_from_filename(filename) -> date | None:
    """
    Extract a YYYYMMDD date from the last block of a filename.

    Examples
    --------
    transactions_20260107.csv -> 2026-01-07
    transactions_2026-01-07.csv -> 2026-01-07
    """
    base = Path(filename).stem.split("_")[-1]
    base = re.sub(r"[-_]", "", base)

    try:
        return datetime.strptime(base, "%Y%m%d").date()
    except ValueError:
        return None


def _normalize_date(date_input) -> str:
    """
    Normalize date input to YYYYMMDD string.

    Accepted inputs:
    - datetime.date
    - string YYYY-MM-DD
    - string YYYYMMDD
    """
    if isinstance(date_input, date):
        return date_input.strftime("%Y%m%d")

    if isinstance(date_input, str):
        value = date_input.strip().replace("-", "")

        try:
            datetime.strptime(value, "%Y%m%d")
        except ValueError as exc:
            raise ValueError(
                "date_input must be a valid date in YYYY-MM-DD or YYYYMMDD format"
            ) from exc

        return value

    raise TypeError("date_input must be datetime.date or string")


def load_file(
    path,
    sep: str = ";",
    usecols=None,
    dtype=str,
    parquet_as_str: bool = False,
    **kwargs,
) -> pd.DataFrame:
    """
    Load a dataset from a file path.

    By default:
    - CSV/TXT files are read with sep=";"
    - CSV/TXT/Excel files are read as strings
    - Parquet files preserve their original schema
    """
    return _read_file(
        path,
        sep=sep,
        usecols=usecols,
        dtype=dtype,
        parquet_as_str=parquet_as_str,
        **kwargs,
    )


def load_prefix(
    path,
    prefix: str,
    extensions=SUPPORTED_EXTENSIONS,
    sep: str = ";",
    usecols=None,
    dtype=str,
    parquet_as_str: bool = False,
    **kwargs,
) -> pd.DataFrame:
    """
    Load the first file found that starts with a given prefix.
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Folder not found: {path}")

    files = sorted(
        f for f in path.iterdir()
        if f.is_file()
        and f.name.startswith(prefix)
        and f.suffix[1:].lower() in extensions
    )

    if not files:
        raise FileNotFoundError(
            f"No files found with prefix '{prefix}' in {path}"
        )

    return _read_file(
        files[0],
        sep=sep,
        usecols=usecols,
        dtype=dtype,
        parquet_as_str=parquet_as_str,
        **kwargs,
    )


def load_date(
    path,
    base_name: str,
    date_value,
    extensions=SUPPORTED_EXTENSIONS,
    sep: str = ";",
    usecols=None,
    dtype=str,
    parquet_as_str: bool = False,
    **kwargs,
) -> pd.DataFrame:
    """
    Load a file with one of these filename patterns:

    - base_name_YYYYMMDD.ext
    - base_name_YYYY-MM-DD.ext
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Folder not found: {path}")

    date_str = _normalize_date(date_value)

    possible_names = [
        f"{base_name}_{date_str}",
        f"{base_name}_{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}",
    ]

    for name in possible_names:
        for ext in extensions:
            file_path = path / f"{name}.{ext}"

            if file_path.exists():
                return _read_file(
                    file_path,
                    sep=sep,
                    usecols=usecols,
                    dtype=dtype,
                    parquet_as_str=parquet_as_str,
                    **kwargs,
                )

    raise FileNotFoundError(
        f"No file found for '{base_name}' with date {date_value} in {path}"
    )


def load_history(
    path,
    name_filter: str | None = None,
    start_date=None,
    end_date=None,
    extensions=SUPPORTED_EXTENSIONS,
    sep: str = ";",
    add_file_date: bool = True,
    usecols=None,
    dtype=str,
    parquet_as_str: bool = False,
    **kwargs,
) -> pd.DataFrame:
    """
    Load and concatenate historical files from a folder.

    Files must contain a valid date at the end of the filename.

    Optional filters:
    - name_filter: string that must be present in the filename
    - start_date: minimum file date
    - end_date: maximum file date
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Folder not found: {path}")

    dataframes = []
    skipped_files = []

    start = (
        datetime.strptime(_normalize_date(start_date), "%Y%m%d").date()
        if start_date else None
    )

    end = (
        datetime.strptime(_normalize_date(end_date), "%Y%m%d").date()
        if end_date else None
    )

    files = sorted(
        f for f in path.iterdir()
        if f.is_file()
        and f.suffix[1:].lower() in extensions
    )

    for file_path in files:
        if name_filter and name_filter not in file_path.name:
            continue

        file_date = _extract_date_from_filename(file_path.name)

        if not file_date:
            if start or end:
                skipped_files.append(file_path.name)
            continue

        if start and file_date < start:
            continue

        if end and file_date > end:
            continue

        df = _read_file(
            file_path,
            sep=sep,
            usecols=usecols,
            dtype=dtype,
            parquet_as_str=parquet_as_str,
            **kwargs,
        )

        if add_file_date:
            df["file_date"] = file_date

        dataframes.append(df)

    if skipped_files:
        warnings.warn(
            "Some files were skipped because no valid date was found "
            f"at the end of the filename: {skipped_files}",
            stacklevel=2,
        )

    if not dataframes:
        return pd.DataFrame()

    return pd.concat(dataframes, ignore_index=True)


def load_month(
    path,
    name_filter: str,
    date_value,
    extensions=SUPPORTED_EXTENSIONS,
    sep: str = ";",
    add_file_date: bool = True,
    usecols=None,
    dtype=str,
    parquet_as_str: bool = False,
    **kwargs,
) -> pd.DataFrame:
    """
    Load historical files for the month of a given date.
    """
    current_date = pd.to_datetime(date_value).date()
    year = current_date.year
    month = current_date.month

    end_day = calendar.monthrange(year, month)[1]

    start_date = f"{year}-{month:02d}-01"
    end_date = f"{year}-{month:02d}-{end_day}"

    return load_history(
        path=path,
        name_filter=name_filter,
        start_date=start_date,
        end_date=end_date,
        extensions=extensions,
        sep=sep,
        add_file_date=add_file_date,
        usecols=usecols,
        dtype=dtype,
        parquet_as_str=parquet_as_str,
        **kwargs,
    )