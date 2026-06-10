from pathlib import Path

import pandas as pd


def _ensure_parent_dir(path) -> Path:
    """
    Ensure that the parent directory of a file path exists.
    """
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def export_csv(
    df: pd.DataFrame,
    path,
    sep: str = ";",
    index: bool = False,
    encoding: str = "utf-8",
    **kwargs,
) -> Path:
    """
    Export a DataFrame to CSV.

    Defaults:
    - sep=";"
    - index=False
    - encoding="utf-8"
    """
    path = _ensure_parent_dir(path)

    df.to_csv(
        path,
        sep=sep,
        index=index,
        encoding=encoding,
        **kwargs,
    )

    return path


def export_excel(
    df: pd.DataFrame,
    path,
    sheet_name: str = "data",
    index: bool = False,
    **kwargs,
) -> Path:
    """
    Export a DataFrame to Excel.

    Defaults:
    - sheet_name="data"
    - index=False
    """
    path = _ensure_parent_dir(path)

    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(
            writer,
            sheet_name=sheet_name,
            index=index,
            **kwargs,
        )

    return path


def export_parquet(
    df: pd.DataFrame,
    path,
    engine: str = "pyarrow",
    compression: str = "zstd",
    index: bool = False,
    **kwargs,
) -> Path:
    """
    Export a DataFrame to Parquet.

    Defaults:
    - engine="pyarrow"
    - compression="zstd"
    - index=False
    """
    path = _ensure_parent_dir(path)

    df.to_parquet(
        path,
        engine=engine,
        compression=compression,
        index=index,
        **kwargs,
    )

    return path


def export_parquet_partitioned(
    df: pd.DataFrame,
    dataset_dir,
    partition_cols,
    engine: str = "pyarrow",
    compression: str = "zstd",
    index: bool = False,
    **kwargs,
) -> Path:
    """
    Export a DataFrame as a partitioned Parquet dataset.

    Notes:
    - This writes a directory, not a single file.
    - Useful for data lake style workflows.
    """
    dataset_dir = Path(dataset_dir)
    dataset_dir.mkdir(parents=True, exist_ok=True)

    df.to_parquet(
        dataset_dir,
        engine=engine,
        compression=compression,
        index=index,
        partition_cols=partition_cols,
        **kwargs,
    )

    return dataset_dir