from pathlib import Path
import pandas as pd

from dr_datakit import load_file, load_date, load_history, load_month


data_dir = Path("data/raw")
data_dir.mkdir(parents=True, exist_ok=True)

df_sample = pd.DataFrame({
    "id": [1, 2, 3],
    "amount": [100.5, 200.0, 350.75],
    "status": ["paid", "pending", "paid"],
})

df_sample.to_csv(data_dir / "transactions_20260107.csv", sep=";", index=False)
df_sample.to_csv(data_dir / "transactions_20260108.csv", sep=";", index=False)
df_sample.to_csv(data_dir / "transactions_20260201.csv", sep=";", index=False)

df_file = load_file(data_dir / "transactions_20260107.csv")
print("load_file result:")
print(df_file)
print(df_file.dtypes)

df_date = load_date(
    path=data_dir,
    base_name="transactions",
    date_value="2026-01-07",
)
print("\nload_date result:")
print(df_date)

df_history = load_history(
    path=data_dir,
    name_filter="transactions",
    start_date="2026-01-07",
    end_date="2026-01-08",
)
print("\nload_history result:")
print(df_history)

df_month = load_month(
    path=data_dir,
    name_filter="transactions",
    date_value="2026-01-15",
)
print("\nload_month result:")
print(df_month)