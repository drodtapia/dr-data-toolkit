import pandas as pd

from dr_datakit import clean_df


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

print(df_clean)
print(df_clean.dtypes)