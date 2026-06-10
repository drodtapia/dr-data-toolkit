import pandas as pd
import pytest

from dr_datakit.cleaning import (
    clean_column_names,
    strip_strings,
    drop_empty_rows,
    to_float,
    to_int,
    to_date,
    to_datetime,
    clean_df,
)


def test_clean_column_names():
    df = pd.DataFrame({
        " Fecha Compra ": [1],
        "Monto-Total": [100],
        " Estado Pago ": ["paid"],
    })

    df_clean = clean_column_names(df)

    assert list(df_clean.columns) == [
        "fecha_compra",
        "monto_total",
        "estado_pago",
    ]


def test_strip_strings():
    df = pd.DataFrame({
        "status": [" paid ", " pending "],
        "amount": [100, 200],
    })

    df_clean = strip_strings(df)

    assert df_clean["status"].tolist() == ["paid", "pending"]


def test_drop_empty_rows():
    df = pd.DataFrame({
        "id": [1, None, 3],
        "amount": [100, None, 300],
    })

    df_clean = drop_empty_rows(df)

    assert df_clean.shape == (2, 2)


def test_to_float_comma_and_dot():
    df = pd.DataFrame({
        "amount": ["100,5", "200.75", "invalid"],
    })

    df_clean = to_float(df, "amount")

    assert df_clean["amount"].tolist()[0] == 100.5
    assert df_clean["amount"].tolist()[1] == 200.75
    assert pd.isna(df_clean["amount"].tolist()[2])


def test_to_int_nullable():
    df = pd.DataFrame({
        "days": ["10", "20", "invalid"],
    })

    df_clean = to_int(df, "days")

    assert str(df_clean["days"].dtype) == "Int64"
    assert df_clean["days"].tolist()[0] == 10
    assert df_clean["days"].tolist()[1] == 20
    assert pd.isna(df_clean["days"].tolist()[2])


def test_to_date():
    df = pd.DataFrame({
        "date": ["2026-01-01", "2026-01-02", "invalid"],
    })

    df_clean = to_date(df, "date")

    assert str(df_clean["date"].dtype) == "datetime64[ns]"
    assert df_clean["date"].dt.hour.fillna(0).eq(0).all()
    assert pd.isna(df_clean["date"].iloc[2])


def test_to_date_with_year_range():
    df = pd.DataFrame({
        "date": ["2026-01-01", "1800-01-01"],
    })

    df_clean = to_date(
        df,
        "date",
        min_year=1900,
        max_year=2100,
    )

    assert pd.notna(df_clean["date"].iloc[0])
    assert pd.isna(df_clean["date"].iloc[1])


def test_to_datetime():
    df = pd.DataFrame({
        "created_at": ["2026-01-01 10:30:00", "invalid"],
    })

    df_clean = to_datetime(df, "created_at")

    assert str(df_clean["created_at"].dtype) == "datetime64[ns]"
    assert df_clean["created_at"].iloc[0].hour == 10
    assert pd.isna(df_clean["created_at"].iloc[1])


def test_clean_df_pipeline():
    df = pd.DataFrame({
        " Fecha Compra ": ["2026-01-01", "2026-01-02", None],
        "Monto": ["100,5", "200.0", "invalid"],
        " Dias Mora ": ["10", "20", None],
        " Estado ": [" paid ", " pending ", None],
    })

    df_clean = clean_df(
        df,
        cols_float=["monto"],
        cols_int=["dias_mora"],
        cols_date=["fecha_compra"],
    )

    assert list(df_clean.columns) == [
        "fecha_compra",
        "monto",
        "dias_mora",
        "estado",
    ]

    assert df_clean["monto"].tolist()[0] == 100.5
    assert str(df_clean["dias_mora"].dtype) == "Int64"
    assert str(df_clean["fecha_compra"].dtype) == "datetime64[ns]"
    assert df_clean["estado"].tolist()[0] == "paid"


def test_clean_df_missing_rename_column_raises_error():
    df = pd.DataFrame({
        "amount": [100],
    })

    with pytest.raises(ValueError):
        clean_df(
            df,
            rename_cols={
                "missing_column": "new_name",
            },
        )


def test_clean_df_with_rename():
    df = pd.DataFrame({
        "amount_raw": ["100,5"],
        "days_raw": ["10"],
    })

    df_clean = clean_df(
        df,
        rename_cols={
            "amount_raw": "amount",
            "days_raw": "days",
        },
        cols_float=["amount"],
        cols_int=["days"],
        normalize_columns=False,
    )

    assert list(df_clean.columns) == ["amount", "days"]
    assert df_clean["amount"].iloc[0] == 100.5
    assert df_clean["days"].iloc[0] == 10


def test_to_date_dayfirst():
    df = pd.DataFrame({
        "date": ["31-12-2026"],
    })

    df_clean = to_date(df, "date", dayfirst=True)

    assert df_clean["date"].iloc[0].year == 2026
    assert df_clean["date"].iloc[0].month == 12
    assert df_clean["date"].iloc[0].day == 31