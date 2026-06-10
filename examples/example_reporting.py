from pathlib import Path

import pandas as pd
from openpyxl import Workbook

from dr_datakit import create_report


template_dir = Path("output/templates")
template_dir.mkdir(parents=True, exist_ok=True)

template_path = template_dir / "report_template.xlsx"
output_path = Path("output/reports/example_report.xlsx")

wb = Workbook()
ws = wb.active
ws.title = "Report"
ws["B2"] = "Example Report Template"
wb.save(template_path)
wb.close()

df_params = pd.DataFrame({
    "value": [
        "Example Portfolio",
        pd.Timestamp("2026-01-31"),
        "USD",
    ]
})

df_summary = pd.DataFrame({
    "status": ["paid", "pending"],
    "count": [10, 5],
    "amount": [1500.75, 800.25],
    "rate": [0.85, 0.15],
})

df_transposed = pd.DataFrame({
    "-": ["Payment Rate", "Average Balance"],
    "jan-2026": [0.85, 1500.75],
    "feb-2026": [0.82, 1800.25],
})

report_path = create_report(
    template_path=template_path,
    output_path=output_path,
    items=[
        {
            "sheet": "Report",
            "cell": "C5",
            "data": df_params,
            "include_header": False,
        },
        {
            "sheet": "Report",
            "cell": "B10",
            "data": df_summary,
            "table_name": "SummaryTable",
            "number_cols": ["count", "amount"],
            "percent_cols": ["rate"],
        },
        {
            "sheet": "Report",
            "cell": "B18",
            "data": df_transposed,
            "include_header": True,
            "as_table": False,
            "number_rows": ["Average Balance"],
            "percent_rows": ["Payment Rate"],
        },
    ],
)

print(f"Report created successfully: {report_path}")