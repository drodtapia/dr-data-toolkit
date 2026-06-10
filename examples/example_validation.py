import pandas as pd

from dr_datakit import (
    validate_not_empty,
    validate_required_columns,
    validate_not_null,
    validate_unique,
    validate_non_negative,
    validate_allowed_values,
    validate_between,
)


df = pd.DataFrame({
    "id": [1, 2, 3],
    "amount": [100.5, 200.0, 350.75],
    "status": ["paid", "pending", "paid"],
})


validate_not_empty(df, "transactions")
validate_required_columns(df, ["id", "amount", "status"])
validate_not_null(df, ["id", "amount"])
validate_unique(df, "id")
validate_non_negative(df, "amount")
validate_allowed_values(df, "status", ["paid", "pending", "cancelled"])
validate_between(df, "amount", min_value=0)

print("All validations passed successfully.")