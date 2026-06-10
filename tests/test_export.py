import pandas as pd
import pytest

from dr_datakit.export import (
    export_csv,
    export_excel,
    export_parquet,
    export_parquet_partitioned,
)


def test_export_csv_creates_file(tmp_path):
    output_path = tmp_path / "nested" / "example.csv"

    df = pd.DataFrame({
        "id": [1, 2],
        "amount": [100.5, 200.0],
    })

    result_path = export_csv(df, output_path)

    assert result_path == output_path
    assert output_path.exists()

    df_loaded = pd.read_csv(output_path, sep=";")

    assert df_loaded.shape == (2, 2)
    assert list(df_loaded.columns) == ["id", "amount"]


def test_export_csv_with_comma_separator(tmp_path):
    output_path = tmp_path / "example.csv"

    df = pd.DataFrame({
        "id": [1, 2],
        "amount": [100.5, 200.0],
    })

    export_csv(df, output_path, sep=",")

    df_loaded = pd.read_csv(output_path, sep=",")

    assert df_loaded.shape == (2, 2)
    assert list(df_loaded.columns) == ["id", "amount"]


def test_export_excel_creates_file(tmp_path):
    pytest.importorskip("openpyxl")

    output_path = tmp_path / "nested" / "example.xlsx"

    df = pd.DataFrame({
        "id": [1, 2],
        "amount": [100.5, 200.0],
    })

    result_path = export_excel(df, output_path)

    assert result_path == output_path
    assert output_path.exists()

    df_loaded = pd.read_excel(output_path)

    assert df_loaded.shape == (2, 2)
    assert list(df_loaded.columns) == ["id", "amount"]


def test_export_excel_custom_sheet_name(tmp_path):
    pytest.importorskip("openpyxl")

    output_path = tmp_path / "example.xlsx"

    df = pd.DataFrame({
        "id": [1, 2],
        "amount": [100.5, 200.0],
    })

    export_excel(df, output_path, sheet_name="transactions")

    df_loaded = pd.read_excel(output_path, sheet_name="transactions")

    assert df_loaded.shape == (2, 2)
    assert list(df_loaded.columns) == ["id", "amount"]


def test_export_parquet_creates_file(tmp_path):
    pytest.importorskip("pyarrow")

    output_path = tmp_path / "nested" / "example.parquet"

    df = pd.DataFrame({
        "id": [1, 2],
        "amount": [100.5, 200.0],
    })

    result_path = export_parquet(df, output_path)

    assert result_path == output_path
    assert output_path.exists()

    df_loaded = pd.read_parquet(output_path)

    assert df_loaded.shape == (2, 2)
    assert list(df_loaded.columns) == ["id", "amount"]


def test_export_parquet_partitioned_creates_dataset(tmp_path):
    pytest.importorskip("pyarrow")

    dataset_dir = tmp_path / "dataset"

    df = pd.DataFrame({
        "id": [1, 2, 3],
        "year": [2026, 2026, 2027],
        "amount": [100.5, 200.0, 350.75],
    })

    result_path = export_parquet_partitioned(
        df,
        dataset_dir,
        partition_cols=["year"],
    )

    assert result_path == dataset_dir
    assert dataset_dir.exists()
    assert dataset_dir.is_dir()

    files = list(dataset_dir.rglob("*.parquet"))

    assert len(files) > 0

    df_loaded = pd.read_parquet(dataset_dir)

    assert df_loaded.shape[0] == 3
    assert "amount" in df_loaded.columns