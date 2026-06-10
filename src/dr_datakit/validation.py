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


def validate_not_empty(df: pd.DataFrame, name: str = "DataFrame") -> None:
    """
    Validate that a DataFrame is not empty.
    """
    if df.empty:
        raise ValueError(f"{name} is empty")


def validate_columns_exist(df: pd.DataFrame, cols) -> None:
    """
    Validate that selected columns exist in the DataFrame.
    """
    cols = _ensure_list(cols)

    missing = [col for col in cols if col not in df.columns]

    if missing:
        raise ValueError(f"Columns not found in DataFrame: {missing}")


def validate_required_columns(df: pd.DataFrame, cols) -> None:
    """
    Validate that required columns exist in the DataFrame.

    Alias-style function for semantic clarity.
    """
    validate_columns_exist(df, cols)


def validate_not_null(df: pd.DataFrame, cols) -> None:
    """
    Validate that selected columns do not contain null values.
    """
    cols = _ensure_list(cols)

    validate_columns_exist(df, cols)

    null_counts = {
        col: int(df[col].isna().sum())
        for col in cols
        if df[col].isna().any()
    }

    if null_counts:
        raise ValueError(f"Null values detected: {null_counts}")


def validate_unique(df: pd.DataFrame, cols) -> None:
    """
    Validate that selected columns define unique records.
    """
    cols = _ensure_list(cols)

    validate_columns_exist(df, cols)

    duplicated = df.duplicated(subset=cols)

    if duplicated.any():
        raise ValueError(
            f"Duplicates detected for {cols}: {int(duplicated.sum())} rows"
        )


def validate_zero_diff(df: pd.DataFrame, col: str, tol: float = 0) -> None:
    """
    Validate that absolute values in a column are within tolerance.

    Useful for reconciliation checks.
    """
    validate_columns_exist(df, col)

    values = pd.to_numeric(df[col], errors="coerce")

    invalid = values.abs() > tol

    if invalid.any():
        raise ValueError(
            f"Values outside tolerance {tol} detected in column '{col}': "
            f"{int(invalid.sum())} rows"
        )


def validate_non_negative(df: pd.DataFrame, cols) -> None:
    """
    Validate that selected numeric columns do not contain negative values.
    """
    cols = _ensure_list(cols)

    validate_columns_exist(df, cols)

    negative_counts = {}

    for col in cols:
        values = pd.to_numeric(df[col], errors="coerce")
        count = int((values < 0).sum())

        if count > 0:
            negative_counts[col] = count

    if negative_counts:
        raise ValueError(f"Negative values detected: {negative_counts}")


def validate_allowed_values(df: pd.DataFrame, col: str, allowed_values) -> None:
    """
    Validate that a column only contains allowed values.

    Null values are ignored. Use validate_not_null separately if needed.
    """
    validate_columns_exist(df, col)

    allowed_values = set(_ensure_list(allowed_values))

    invalid_values = sorted(
        set(df[col].dropna().unique()) - allowed_values
    )

    if invalid_values:
        raise ValueError(
            f"Invalid values detected in column '{col}': {invalid_values}. "
            f"Allowed values are: {sorted(allowed_values)}"
        )


def validate_between(
    df: pd.DataFrame,
    col: str,
    min_value=None,
    max_value=None,
) -> None:
    """
    Validate that numeric values are within a range.

    Null values are ignored. Use validate_not_null separately if needed.
    """
    validate_columns_exist(df, col)

    values = pd.to_numeric(df[col], errors="coerce")

    invalid = pd.Series(False, index=df.index)

    if min_value is not None:
        invalid = invalid | (values < min_value)

    if max_value is not None:
        invalid = invalid | (values > max_value)

    if invalid.any():
        raise ValueError(
            f"Values outside allowed range detected in column '{col}': "
            f"{int(invalid.sum())} rows"
        )