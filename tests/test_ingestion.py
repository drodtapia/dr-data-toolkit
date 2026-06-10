import pandas as pd
import pytest

from dr_datakit.ingestion import (
    load_file,
    load_date,
    load_history,
    load_month,
)


def test_load_file_csv_semicolon(tmp_path):
    file_path = tmp_path / "transactions_20260107.csv"

    df_original = pd.DataFrame({
        "id": [1, 2],
        "amount": [100.5, 200.0],
        "status": ["paid", "pending"],
    })

    df_original.to_csv(file_path, sep=";", index=False)

    df_loaded = load_file(file_path)

    assert df_loaded.shape == (2, 3)
    assert list(df_loaded.columns) == ["id", "amount", "status"]

    # CSV files are loaded as strings by default
    assert df_loaded["id"].tolist() == ["1", "2"]
    assert df_loaded["status"].tolist() == ["paid", "pending"]


def test_load_file_with_comma_separator(tmp_path):
    file_path = tmp_path / "transactions_20260107.csv"

    df_original = pd.DataFrame({
        "id": [1, 2],
        "amount": [100.5, 200.0],
    })

    df_original.to_csv(file_path, sep=",", index=False)

    df_loaded = load_file(file_path, sep=",")

    assert df_loaded.shape == (2, 2)
    assert list(df_loaded.columns) == ["id", "amount"]


def test_load_file_not_found(tmp_path):
    file_path = tmp_path / "missing_file.csv"

    with pytest.raises(FileNotFoundError):
        load_file(file_path)


def test_load_file_unsupported_extension(tmp_path):
    file_path = tmp_path / "data.json"
    file_path.write_text('{"id": 1}', encoding="utf-8")

    with pytest.raises(ValueError):
        load_file(file_path)


def test_load_date_yyyymmdd(tmp_path):
    file_path = tmp_path / "transactions_20260107.csv"

    df_original = pd.DataFrame({
        "id": [1, 2],
        "amount": [100.5, 200.0],
    })

    df_original.to_csv(file_path, sep=";", index=False)

    df_loaded = load_date(
        path=tmp_path,
        base_name="transactions",
        date_value="2026-01-07",
    )

    assert df_loaded.shape == (2, 2)
    assert list(df_loaded.columns) == ["id", "amount"]


def test_load_date_iso_filename(tmp_path):
    file_path = tmp_path / "transactions_2026-01-07.csv"

    df_original = pd.DataFrame({
        "id": [1],
        "amount": [100.5],
    })

    df_original.to_csv(file_path, sep=";", index=False)

    df_loaded = load_date(
        path=tmp_path,
        base_name="transactions",
        date_value="2026-01-07",
    )

    assert df_loaded.shape == (1, 2)
    assert df_loaded["id"].iloc[0] == "1"


def test_load_history(tmp_path):
    df_original = pd.DataFrame({
        "id": [1, 2],
        "amount": [100.5, 200.0],
    })

    df_original.to_csv(tmp_path / "transactions_20260107.csv", sep=";", index=False)
    df_original.to_csv(tmp_path / "transactions_20260108.csv", sep=";", index=False)

    df_loaded = load_history(
        path=tmp_path,
        name_filter="transactions",
        start_date="2026-01-07",
        end_date="2026-01-08",
    )

    assert df_loaded.shape == (4, 3)
    assert "file_date" in df_loaded.columns
    assert df_loaded["file_date"].nunique() == 2


def test_load_history_returns_empty_dataframe_when_no_files(tmp_path):
    df_loaded = load_history(
        path=tmp_path,
        name_filter="transactions",
        start_date="2026-01-07",
        end_date="2026-01-08",
    )

    assert isinstance(df_loaded, pd.DataFrame)
    assert df_loaded.empty


def test_load_month(tmp_path):
    df_original = pd.DataFrame({
        "id": [1],
        "amount": [100.5],
    })

    df_original.to_csv(tmp_path / "transactions_20260107.csv", sep=";", index=False)
    df_original.to_csv(tmp_path / "transactions_20260120.csv", sep=";", index=False)
    df_original.to_csv(tmp_path / "transactions_20260201.csv", sep=";", index=False)

    df_loaded = load_month(
        path=tmp_path,
        name_filter="transactions",
        date_value="2026-01-15",
    )

    assert df_loaded.shape == (2, 3)
    assert "file_date" in df_loaded.columns

def test_load_file_parquet_preserves_schema(tmp_path):
    pytest.importorskip("pyarrow")

    file_path = tmp_path / "transactions_20260107.parquet"

    df_original = pd.DataFrame({
        "id": [1, 2],
        "amount": [100.5, 200.0],
    })

    df_original.to_parquet(file_path, index=False)

    df_loaded = load_file(file_path)

    assert df_loaded.shape == (2, 2)
    assert list(df_loaded.columns) == ["id", "amount"]

    # Parquet preserves schema by default
    assert str(df_loaded["id"].dtype) in ["int64", "Int64"]
    assert str(df_loaded["amount"].dtype) == "float64"


def test_load_file_parquet_as_str(tmp_path):
    pytest.importorskip("pyarrow")

    file_path = tmp_path / "transactions_20260107.parquet"

    df_original = pd.DataFrame({
        "id": [1, 2],
        "amount": [100.5, 200.0],
    })

    df_original.to_parquet(file_path, index=False)

    df_loaded = load_file(file_path, parquet_as_str=True)

    assert df_loaded.shape == (2, 2)
    assert list(df_loaded.columns) == ["id", "amount"]

    # Parquet can be forced to string when needed
    assert df_loaded["id"].tolist() == ["1", "2"]
    assert df_loaded["amount"].tolist() == ["100.5", "200.0"]

def test_load_file_excel_as_str(tmp_path):
    pytest.importorskip("openpyxl")

    file_path = tmp_path / "transactions_20260107.xlsx"

    df_original = pd.DataFrame({
        "id": [1, 2],
        "document_number": ["001", "002"],
        "amount": [100.5, 200.0],
    })

    df_original.to_excel(file_path, index=False)

    df_loaded = load_file(file_path)

    assert df_loaded.shape == (2, 3)
    assert df_loaded["id"].tolist() == ["1", "2"]
    assert df_loaded["document_number"].tolist() == ["001", "002"]