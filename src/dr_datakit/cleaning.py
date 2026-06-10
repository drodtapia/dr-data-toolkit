import pandas as pd


def _ensure_list(cols):
    """
    Ensure that a column input is returned as a list.
    """
    if cols is None:
        return []

    if isinstance(cols, str):
        return [cols]

    return list(cols)


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalize DataFrame column names.

    Rules:
    - strip leading/trailing spaces
    - lowercase
    - replace spaces with underscores
    - replace hyphens with underscores
    """
    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )

    return df


def strip_strings(df: pd.DataFrame, cols=None) -> pd.DataFrame:
    """
    Strip leading and trailing whitespace from string columns.
    """
    df = df.copy()

    if cols is None:
        cols = df.select_dtypes(include=["object", "string"]).columns
    else:
        cols = _ensure_list(cols)

    for col in cols:
        if col not in df.columns:
            continue

        df[col] = df[col].astype("string").str.strip()

    return df


def drop_empty_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Drop rows where all values are missing.
    """
    return df.dropna(how="all").copy()


def to_float(df: pd.DataFrame, cols) -> pd.DataFrame:
    """
    Convert one or more columns to float.

    Accepts comma or dot as decimal separator.
    Invalid values are converted to NaN.
    """
    cols = _ensure_list(cols)
    df = df.copy()

    for col in cols:
        if col not in df.columns:
            continue

        values = (
            df[col]
            .astype("string")
            .str.strip()
            .str.replace(",", ".", regex=False)
        )

        df[col] = pd.to_numeric(values, errors="coerce")

    return df


def to_int(df: pd.DataFrame, cols) -> pd.DataFrame:
    """
    Convert one or more columns to nullable integer (Int64).

    Invalid values are converted to <NA>.
    """
    cols = _ensure_list(cols)
    df = df.copy()

    for col in cols:
        if col not in df.columns:
            continue

        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    return df


def to_date(
    df: pd.DataFrame,
    cols,
    min_year=None,
    max_year=None,
    dayfirst: bool = False,
) -> pd.DataFrame:
    """
    Convert one or more columns to normalized datetime64[ns] dates.

    Invalid values are converted to NaT.
    """
    cols = _ensure_list(cols)
    df = df.copy()

    for col in cols:
        if col not in df.columns:
            continue

        dates = pd.to_datetime(
            df[col],
            errors="coerce",
            dayfirst=dayfirst,
        )

        if min_year is not None or max_year is not None:
            min_y = min_year if min_year is not None else dates.dt.year.min()
            max_y = max_year if max_year is not None else dates.dt.year.max()

            dates = dates.where(dates.dt.year.between(min_y, max_y))

        df[col] = dates.dt.normalize()

    return df


def to_datetime(
    df: pd.DataFrame,
    cols,
    min_year=None,
    max_year=None,
    dayfirst: bool = False,
) -> pd.DataFrame:
    """
    Convert one or more columns to datetime64[ns].

    Invalid values are converted to NaT.
    """
    cols = _ensure_list(cols)
    df = df.copy()

    for col in cols:
        if col not in df.columns:
            continue

        dates = pd.to_datetime(
            df[col],
            errors="coerce",
            dayfirst=dayfirst,
        )

        if min_year is not None or max_year is not None:
            min_y = min_year if min_year is not None else dates.dt.year.min()
            max_y = max_year if max_year is not None else dates.dt.year.max()

            dates = dates.where(dates.dt.year.between(min_y, max_y))

        df[col] = dates

    return df


def clean_df(
    df: pd.DataFrame,
    rename_cols=None,
    cols_float=None,
    cols_int=None,
    cols_date=None,
    cols_datetime=None,
    date_min_year=None,
    date_max_year=None,
    dayfirst: bool = False,
    normalize_columns: bool = True,
    strip_strings_all: bool = True,
    drop_empty: bool = True,
) -> pd.DataFrame:
    """
    Apply a basic and consistent cleaning pipeline to a DataFrame.

    Steps:
    - normalize column names
    - strip strings
    - drop empty rows
    - validate rename columns
    - rename columns
    - convert selected columns to float
    - convert selected columns to int
    - convert selected columns to date
    - convert selected columns to datetime
    """
    df = df.copy()

    rename_cols = rename_cols or {}
    cols_float = _ensure_list(cols_float)
    cols_int = _ensure_list(cols_int)
    cols_date = _ensure_list(cols_date)
    cols_datetime = _ensure_list(cols_datetime)

    if normalize_columns:
        df = clean_column_names(df)

    if strip_strings_all:
        df = strip_strings(df)

    if drop_empty:
        df = drop_empty_rows(df)

    missing = [col for col in rename_cols if col not in df.columns]

    if missing:
        raise ValueError(f"Columns not found in DataFrame: {missing}")

    df = df.rename(columns=rename_cols)

    if cols_float:
        df = to_float(df, cols_float)

    if cols_int:
        df = to_int(df, cols_int)

    if cols_date:
        df = to_date(
            df,
            cols_date,
            min_year=date_min_year,
            max_year=date_max_year,
            dayfirst=dayfirst,
        )

    if cols_datetime:
        df = to_datetime(
            df,
            cols_datetime,
            min_year=date_min_year,
            max_year=date_max_year,
            dayfirst=dayfirst,
        )

    return df