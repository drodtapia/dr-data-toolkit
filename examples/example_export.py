import pandas as pd

from dr_datakit import (
    export_csv,
    export_excel,
    export_parquet,
)


df = pd.DataFrame({
    "id": [1, 2, 3],
    "amount": [100.5, 200.0, 350.75],
    "status": ["paid", "pending", "paid"],
})

export_csv(df, "output/example.csv")
export_excel(df, "output/example.xlsx")
export_parquet(df, "output/example.parquet")

print("Export examples created successfully.")