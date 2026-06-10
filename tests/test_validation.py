import pandas as pd
import pytest

from dr_datakit.validation import (
    validate_not_empty,
    validate_columns_exist,
    validate_required_columns,
    validate_not_null,
    validate_unique,
    validate_zero_diff,
    validate_non_negative,
    validate_allowed_values,
    validate_between,
)


def test_validate_not_empty_success():
    df = pd.DataFrame({"id": [1]})

    validate_not_empty(df)


def test_validate_not_empty_fail():
    df = pd.DataFrame()

    with pytest.raises(ValueError):
        validate_not_empty(df)


def test_validate_columns_exist_success():
    df = pd.DataFrame({
        "id": [1],
        "amount": [100],
    })

    validate_columns_exist(df, ["id", "amount"])


def test_validate_columns_exist_fail():
    df = pd.DataFrame({
        "id": [1],
    })

    with pytest.raises(ValueError):
        validate_columns_exist(df, ["id", "amount"])


def test_validate_required_columns_success():
    df = pd.DataFrame({
        "id": [1],
        "amount": [100],
    })

    validate_required_columns(df, ["id", "amount"])


def test_validate_not_null_success():
    df = pd.DataFrame({
        "id": [1, 2],
        "amount": [100, 200],
    })

    validate_not_null(df, ["id", "amount"])


def test_validate_not_null_fail():
    df = pd.DataFrame({
        "id": [1, None],
        "amount": [100, 200],
    })

    with pytest.raises(ValueError):
        validate_not_null(df, ["id"])


def test_validate_unique_success():
    df = pd.DataFrame({
        "id": [1, 2, 3],
    })

    validate_unique(df, "id")


def test_validate_unique_fail():
    df = pd.DataFrame({
        "id": [1, 1, 2],
    })

    with pytest.raises(ValueError):
        validate_unique(df, "id")


def test_validate_unique_composite_key_success():
    df = pd.DataFrame({
        "client_id": [1, 1, 2],
        "invoice_id": [10, 11, 10],
    })

    validate_unique(df, ["client_id", "invoice_id"])


def test_validate_zero_diff_success():
    df = pd.DataFrame({
        "diff": [0, 0.5, -0.5],
    })

    validate_zero_diff(df, "diff", tol=1)


def test_validate_zero_diff_fail():
    df = pd.DataFrame({
        "diff": [0, 2, -0.5],
    })

    with pytest.raises(ValueError):
        validate_zero_diff(df, "diff", tol=1)


def test_validate_non_negative_success():
    df = pd.DataFrame({
        "amount": [0, 100, 200],
    })

    validate_non_negative(df, "amount")


def test_validate_non_negative_fail():
    df = pd.DataFrame({
        "amount": [100, -10, 200],
    })

    with pytest.raises(ValueError):
        validate_non_negative(df, "amount")


def test_validate_allowed_values_success():
    df = pd.DataFrame({
        "status": ["paid", "pending", "cancelled"],
    })

    validate_allowed_values(
        df,
        "status",
        ["paid", "pending", "cancelled"],
    )


def test_validate_allowed_values_fail():
    df = pd.DataFrame({
        "status": ["paid", "pending", "invalid_status"],
    })

    with pytest.raises(ValueError):
        validate_allowed_values(
            df,
            "status",
            ["paid", "pending", "cancelled"],
        )


def test_validate_between_success():
    df = pd.DataFrame({
        "rate": [0.0, 0.5, 1.0],
    })

    validate_between(
        df,
        "rate",
        min_value=0,
        max_value=1,
    )


def test_validate_between_fail():
    df = pd.DataFrame({
        "rate": [0.0, 1.5, 0.5],
    })

    with pytest.raises(ValueError):
        validate_between(
            df,
            "rate",
            min_value=0,
            max_value=1,
        )