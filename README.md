# dr-data-toolkit

Author: David Rodriguez

A lightweight Python toolkit for building reusable, reliable and notebook-friendly data processes.

`dr-data-toolkit` provides practical building blocks for common data tasks such as file ingestion, data cleaning, validation, standardized exports and Excel reporting from templates.

This project is designed to support flexible data work, especially in Jupyter notebooks, without forcing a rigid pipeline structure.

The Python package is imported as:

```python
import dr_datakit
```

or:

```python
from dr_datakit import load_file, clean_df, create_report
```

## Project Status

Early-stage MVP.

Current focus:

* Data ingestion
* Data cleaning
* Data validation
* Data export
* Excel reporting from templates
* Notebook-friendly usage
* Testing foundation
* Clear documentation

## Goal

The goal of this project is not to create a rigid workflow engine.

The goal is to provide a practical toolkit with reusable functions that make data processes easier to build, review, validate and maintain.

The project is especially useful when working with notebooks where each client, portfolio, report or process may have different requirements.

A typical process may look like this:

```text
raw data -> load -> clean -> validate -> export parquet -> create Excel report
```

But this is not enforced by the package. Each notebook or project can decide which tools to use and in what order.

## Philosophy

This project follows a toolkit-first approach:

```text
Jupyter Notebook = working space and review layer
dr_datakit       = reusable technical tools
Parquet          = official processed dataset
Excel/CSV        = review, delivery or reporting output
Templates        = formatted Excel reports with layout, formulas and logos
```

The package does not contain business-specific logic. It provides reusable tools that can be used across different projects.

## Project Structure

```text
dr-data-toolkit/
|-- src/
|   `-- dr_datakit/
|       |-- __init__.py
|       |-- ingestion.py
|       |-- cleaning.py
|       |-- validation.py
|       |-- export.py
|       `-- reporting.py
|-- examples/
|-- tests/
|-- docs/
|-- notebooks/
|-- data/
|   |-- raw/
|   `-- processed/
|-- output/
|   `-- reports/
|-- logs/
|-- README.md
|-- pyproject.toml
|-- requirements.txt
|-- LICENSE
`-- .gitignore
```

## Installation for Local Development

Install the package in editable mode:

```code
pip install -e .
```

For development dependencies:

```code
pip install -e ".[dev]"
```

Editable mode allows changes made inside `src/dr_datakit/` to be reflected immediately without reinstalling the package.

## Requirements

Core dependencies:

```text
pandas
openpyxl
pyarrow
Pillow
```

Development dependencies:

```text
pytest
jupyter
ipykernel
```

`Pillow` is included because Excel templates may contain images such as logos. When using `openpyxl` to open and save those templates, `Pillow` helps preserve embedded images correctly.

## Basic Toolkit Usage

```python
from dr_datakit import (
    load_file,
    clean_df,
    validate_not_empty,
    validate_required_columns,
    export_parquet,
)

df_raw = load_file("data/raw/example.csv")

df_clean = clean_df(
    df_raw,
    cols_float=["amount"],
    cols_date=["date"],
)

validate_not_empty(df_clean, "example data")
validate_required_columns(df_clean, ["id", "amount", "date"])

export_parquet(
    df_clean,
    "data/processed/example.parquet"
)
```

This example shows the general idea:

```text
load data
clean data
validate data
save processed output
```

The notebook or script decides what to run.

## Data Ingestion

The ingestion module provides utilities to load datasets from files and folders.

Current supported formats:

* CSV
* TXT
* Excel
* Parquet

By default:

* CSV and TXT files use `;` as separator.
* CSV, TXT and Excel files are loaded as strings.
* Parquet files preserve their original schema.

Loading CSV, TXT and Excel files as strings helps avoid losing information such as leading zeros, document numbers, identifiers or dates that should be transformed later in a controlled cleaning step.

Parquet files preserve their original schema because they are usually already processed or typed datasets.

If needed, Parquet files can also be converted to strings using `parquet_as_str=True`.

### Load a Single File

```python
from dr_datakit import load_file

df = load_file("data/raw/transactions_20260131.csv")
```

### Load a File With a Custom Separator

```python
from dr_datakit import load_file

df = load_file(
    "data/raw/transactions_20260131.csv",
    sep=","
)
```

### Load a File by Date

```python
from dr_datakit import load_date

df = load_date(
    path="data/raw",
    base_name="transactions",
    date_value="2026-01-31"
)
```

Supported filename patterns:

```text
transactions_20260131.csv
transactions_2026-01-31.csv
```

### Load Files by Prefix

```python
from dr_datakit import load_prefix

df = load_prefix(
    path="data/raw",
    prefix="transactions"
)
```

### Load Historical Files

```python
from dr_datakit import load_history

df = load_history(
    path="data/raw",
    name_filter="transactions",
    start_date="2026-01-01",
    end_date="2026-01-31"
)
```

The resulting DataFrame includes a `file_date` column by default when dates are extracted from filenames.

### Load Files From a Specific Month

```python
from dr_datakit import load_month

df = load_month(
    path="data/raw",
    name_filter="transactions",
    date_value="2026-01-15"
)
```

## Data Cleaning

The cleaning module provides utilities to standardize and transform datasets after ingestion.

The main idea is:

```text
load safely first
then clean and convert explicitly
```

Current cleaning utilities include:

* Column name normalization
* String trimming
* Empty row removal
* Float conversion
* Integer conversion
* Date conversion
* Datetime conversion
* Basic cleaning pipeline

### Clean Column Names

```python
from dr_datakit import clean_column_names

df = clean_column_names(df)
```

Example transformation:

```text
" Fecha Compra " -> "fecha_compra"
"Monto-Total"    -> "monto_total"
```

### Strip String Columns

```python
from dr_datakit import strip_strings

df = strip_strings(df)
```

This removes leading and trailing spaces from string columns.

Example:

```text
" paid " -> "paid"
```

### Drop Empty Rows

```python
from dr_datakit import drop_empty_rows

df = drop_empty_rows(df)
```

This removes rows where all values are missing.

### Convert Columns to Float

```python
from dr_datakit import to_float

df = to_float(df, "amount")
```

The function accepts comma or dot as decimal separator:

```text
"100,5"  -> 100.5
"200.75" -> 200.75
```

Invalid values are converted to `NaN`.

### Convert Columns to Integer

```python
from dr_datakit import to_int

df = to_int(df, "days_past_due")
```

The function uses pandas nullable integer type:

```text
Int64
```

Invalid values are converted to `<NA>`.

### Convert Columns to Date

```python
from dr_datakit import to_date

df = to_date(df, "purchase_date")
```

Dates are stored as normalized `datetime64[ns]` values.

Invalid dates are converted to `NaT`.

Optional year range validation:

```python
df = to_date(
    df,
    "purchase_date",
    min_year=1900,
    max_year=2100
)
```

For day-first formats:

```python
df = to_date(
    df,
    "purchase_date",
    dayfirst=True
)
```

### Convert Columns to Datetime

```python
from dr_datakit import to_datetime

df = to_datetime(df, "created_at")
```

Invalid datetime values are converted to `NaT`.

### Basic Cleaning Pipeline

```python
from dr_datakit import clean_df

df_clean = clean_df(
    df,
    cols_float=["amount"],
    cols_int=["days_past_due"],
    cols_date=["purchase_date"]
)
```

By default, `clean_df` applies:

```text
normalize column names
strip string columns
drop fully empty rows
convert selected columns
```

### Rename Columns During Cleaning

```python
from dr_datakit import clean_df

df_clean = clean_df(
    df,
    rename_cols={
        "amount_raw": "amount",
        "days_raw": "days_past_due"
    },
    cols_float=["amount"],
    cols_int=["days_past_due"],
    normalize_columns=False
)
```

If a column specified in `rename_cols` does not exist, the function raises a clear error.

## Data Validation

The validation module provides utilities to verify that datasets meet required rules before continuing with downstream processing.

The validation functions follow a simple rule:

```text
if the data is invalid -> raise an error
if the data is valid   -> continue
```

Current validation utilities include:

* Empty DataFrame validation
* Required column validation
* Null value validation
* Uniqueness validation
* Numeric tolerance validation
* Non-negative value validation
* Allowed values validation
* Numeric range validation

### Validate Non-Empty DataFrames

```python
from dr_datakit import validate_not_empty

validate_not_empty(df, name="transactions")
```

This raises an error if the DataFrame is empty.

### Validate Required Columns

```python
from dr_datakit import validate_required_columns

validate_required_columns(
    df,
    ["id", "amount", "status"]
)
```

This ensures that all required columns exist in the DataFrame.

### Validate Null Values

```python
from dr_datakit import validate_not_null

validate_not_null(
    df,
    ["id", "amount"]
)
```

This ensures that selected columns do not contain null values.

### Validate Unique Records

```python
from dr_datakit import validate_unique

validate_unique(df, "id")
```

For composite keys:

```python
validate_unique(
    df,
    ["client_id", "invoice_id"]
)
```

This ensures that selected columns define unique records.

### Validate Numeric Differences

```python
from dr_datakit import validate_zero_diff

validate_zero_diff(
    df,
    "balance_difference",
    tol=1
)
```

This is useful for reconciliation checks where small differences may be accepted due to rounding.

### Validate Non-Negative Values

```python
from dr_datakit import validate_non_negative

validate_non_negative(
    df,
    ["amount", "balance"]
)
```

This ensures that selected numeric columns do not contain negative values.

### Validate Allowed Values

```python
from dr_datakit import validate_allowed_values

validate_allowed_values(
    df,
    "status",
    ["paid", "pending", "cancelled"]
)
```

This is useful for categorical columns.

### Validate Numeric Ranges

```python
from dr_datakit import validate_between

validate_between(
    df,
    "rate",
    min_value=0,
    max_value=1
)
```

This ensures that numeric values are inside an expected range.

### Typical Validation Flow

```python
from dr_datakit import (
    validate_not_empty,
    validate_required_columns,
    validate_not_null,
    validate_unique,
    validate_non_negative,
)

validate_not_empty(df, "transactions")

validate_required_columns(
    df,
    ["id", "amount", "status"]
)

validate_not_null(
    df,
    ["id", "amount"]
)

validate_unique(df, "id")

validate_non_negative(df, "amount")
```

Validation functions do not return a DataFrame. They either pass silently or raise a clear error.

## Data Export

The export module provides utilities to save DataFrames using consistent and reusable defaults.

Current export utilities include:

* CSV export
* Excel export
* Parquet export
* Partitioned Parquet export

By default:

* CSV files use `;` as separator.
* Excel files are exported without index.
* Parquet files use `pyarrow`.
* Parquet files use `zstd` compression.
* Parent folders are created automatically when needed.

### Export to CSV

```python
from dr_datakit import export_csv

export_csv(
    df,
    "output/transactions.csv"
)
```

This is equivalent to a standardized CSV export with:

```text
sep=";"
index=False
encoding="utf-8"
```

For comma-separated CSV files:

```python
export_csv(
    df,
    "output/transactions.csv",
    sep=","
)
```

### Export to Excel

```python
from dr_datakit import export_excel

export_excel(
    df,
    "output/transactions.xlsx"
)
```

By default, the sheet name is:

```text
data
```

For a custom sheet name:

```python
export_excel(
    df,
    "output/transactions.xlsx",
    sheet_name="transactions"
)
```

### Export to Parquet

```python
from dr_datakit import export_parquet

export_parquet(
    df,
    "data/processed/transactions.parquet"
)
```

This uses the project default Parquet settings:

```text
engine="pyarrow"
compression="zstd"
index=False
```

### Export to Partitioned Parquet

```python
from dr_datakit import export_parquet_partitioned

export_parquet_partitioned(
    df,
    "data/processed/transactions_dataset",
    partition_cols=["year"]
)
```

This writes a directory-based Parquet dataset.

Example output:

```text
transactions_dataset/
|-- year=2026/
|   `-- part-00000.parquet
`-- year=2027/
    `-- part-00000.parquet
```

Partitioned datasets are useful for larger workflows, data lake style organization and efficient filtering by partition columns.

### Why Use Export Helpers Instead of Pandas Directly?

The export helpers are thin wrappers around pandas export methods.

For example, this:

```python
export_parquet(df, "data/processed/transactions.parquet")
```

standardizes this:

```python
df.to_parquet(
    "data/processed/transactions.parquet",
    engine="pyarrow",
    compression="zstd",
    index=False
)
```

The value is not replacing pandas. The value is centralizing export defaults, reducing repeated code and creating one place to improve export behavior later.

## Excel Reporting

The reporting module provides utilities to create formatted Excel reports from existing templates.

This module is designed for workflows where templates already contain:

* Logos or images
* Fixed text
* Predefined sheets
* Formulas
* Existing formatting
* Report layout
* Corporate or client-specific structure

The reporting layer does not replace processed datasets. It is used to present selected data in a formatted Excel output.

Current reporting utilities include:

* Template copying
* Writing blocks into worksheets
* Creating reports from templates and block definitions

### Reporting Philosophy

Everything written to Excel is treated as a block.

A block can be:

```text
1x1  -> single value
Nx1  -> vertical list of values
Nx2  -> parameter table
NxM  -> full table
```

This means fixed report values such as portfolio name, date and currency can be written the same way as any other block.

### Copy a Template

```python
from dr_datakit import copy_template

output_path = copy_template(
    "templates/report_template.xlsx",
    "output/reports/final_report.xlsx"
)
```

This creates a copy of the template and preserves the original file.

This is especially useful when the template contains images such as logos.

### Write a Single Value

A single value is treated as a 1x1 block.

```python
from openpyxl import load_workbook
from dr_datakit import copy_template, write_block

output_path = copy_template(
    "templates/report_template.xlsx",
    "output/reports/final_report.xlsx"
)

wb = load_workbook(output_path)
ws = wb["Report"]

write_block(
    ws,
    "Example Portfolio",
    "C5"
)

wb.save(output_path)
wb.close()
```

### Write Values as a Block

```python
import pandas as pd

report_values = [
    "Example Portfolio",
    pd.Timestamp("2026-01-31"),
    1500000.75,
]

write_block(
    ws,
    report_values,
    "C5",
    include_header=False
)
```

This writes:

```text
C5 = Example Portfolio
C6 = 2026-01-31
C7 = 1500000.75
```

When `include_header=False`, no Excel table is created.

### Write a DataFrame as a Table

```python
write_block(
    ws,
    df_summary,
    "B10",
    table_name="SummaryTable",
    number_cols=["count", "amount"],
    percent_cols=["rate"]
)
```

By default, a DataFrame with headers is written as an Excel table.

The default Excel table style is:

```text
TableStyleMedium2
```

You can override it when needed:

```python
write_block(
    ws,
    df_summary,
    "B10",
    table_name="SummaryTable",
    table_style="TableStyleMedium9"
)
```

### Write a DataFrame Without Headers

Use this when the template already contains headers or when writing raw values into fixed report cells.

```python
write_block(
    ws,
    df_values,
    "B20",
    include_header=False
)
```

When `include_header=False`, the block is not created as an Excel table.

### Write a Transposed Table

```python
write_block(
    ws,
    df_report,
    "B30",
    transpose=True,
    as_table=False,
    number_rows=["Average Balance"],
    percent_rows=["Payment Rate"]
)
```

This is useful when report metrics are stored by row rather than by column.

### Number, Percent and Date Formatting

Default visual formats:

```text
numbers      -> #,##0_);-#,##0;-
percentages  -> 0.00%
dates        -> yyyy-mm-dd
```

The number format only affects Excel visualization. It does not truncate or modify the underlying value.

For formatting by column:

```python
write_block(
    ws,
    df_summary,
    "B10",
    number_cols=["amount"],
    percent_cols=["rate"],
    date_cols=["date"]
)
```

For formatting by row:

```python
write_block(
    ws,
    df_transposed,
    "B20",
    number_rows=["Average Balance"],
    percent_rows=["Payment Rate"]
)
```

### Create a Report From a Template

```python
from dr_datakit import create_report

create_report(
    template_path="templates/report_template.xlsx",
    output_path="output/reports/final_report.xlsx",
    items=[
        {
            "sheet": "Report",
            "cell": "C5",
            "data": report_values,
            "include_header": False,
        },
        {
            "sheet": "Report",
            "cell": "B10",
            "data": df_summary,
            "table_name": "SummaryTable",
            "number_cols": ["amount"],
            "percent_cols": ["rate"],
        },
    ],
)
```

Each item defines:

```text
sheet -> Excel sheet name
cell  -> starting cell
data  -> value, DataFrame, Series, list or block
```

Optional item settings include:

```text
include_header
include_index
transpose
as_table
table_name
number_cols
percent_cols
date_cols
number_rows
percent_rows
row_label_col
value_type
table_style
```

## Recommended Notebook Structure

This toolkit is designed to work well in Jupyter notebooks.

A practical notebook can be organized like this:

```text
00. Imports and setup
01. Process dates
02. Paths and file names
03. Execution flags
04. Load input data
05. Clean data
06. Base validations
07. Report section 1
08. Report section 2
09. Monthly reports
10. Extra reports
11. Export processed outputs
12. Create final Excel reports
```

The notebook should control things such as:

```text
processing date
cutoff date
which sections to run
which reports are required
client-specific logic
portfolio-specific logic
manual checks
```

The package should provide reusable technical tools.

Example:

```python
from pathlib import Path
import pandas as pd

from dr_datakit import (
    load_date,
    clean_df,
    validate_not_empty,
    validate_required_columns,
    export_parquet,
    create_report,
)

# Process dates
process_date = pd.Timestamp("2026-01-31")
date_label = process_date.strftime("%Y%m%d")

# Paths
BASE_DIR = Path(".")
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR = BASE_DIR / "output"
REPORTS_DIR = OUTPUT_DIR / "reports"
TEMPLATES_DIR = BASE_DIR / "templates"

for folder in [RAW_DIR, PROCESSED_DIR, OUTPUT_DIR, REPORTS_DIR, TEMPLATES_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

# Execution flags
RUN_PART_1 = True
RUN_PART_2 = True
RUN_MONTHLY_REPORTS = process_date.is_month_end
RUN_EXTRA_REPORTS = False

# Load
df_raw = load_date(
    path=RAW_DIR,
    base_name="transactions",
    date_value=process_date
)

# Clean
df = clean_df(
    df_raw,
    cols_float=["amount"],
    cols_date=["transaction_date"]
)

# Validate
validate_not_empty(df, "transactions")
validate_required_columns(df, ["id", "amount", "transaction_date"])

# Export processed dataset
export_parquet(
    df,
    PROCESSED_DIR / f"transactions_{date_label}.parquet"
)

# Build report table
df_summary = df.groupby("status", as_index=False).agg(
    count=("id", "count"),
    amount=("amount", "sum")
)

# Create report
create_report(
    template_path=TEMPLATES_DIR / "report_template.xlsx",
    output_path=REPORTS_DIR / f"transactions_report_{date_label}.xlsx",
    items=[
        {
            "sheet": "Report",
            "cell": "B10",
            "data": df_summary,
            "table_name": "SummaryTable",
            "number_cols": ["count", "amount"],
        }
    ],
)
```

## Examples

The `examples/` folder contains simple executable scripts that show how to use the toolkit modules.

### Data Ingestion Example

```code
python examples/example_ingestion.py
```

### Data Cleaning Example

```code
python examples/example_cleaning.py
```

### Data Validation Example

```code
python examples/example_validation.py
```

### Data Export Example

```code
python examples/example_export.py
```

### Reporting Example

```code
python examples/example_reporting.py
```

### End-to-End Example

```code
python examples/example_end_to_end.py
```

The end-to-end example demonstrates:

```text
synthetic raw data -> load -> clean -> validate -> export parquet -> create Excel report
```

## Running Tests

Run all tests:

```code
python -m pytest
```

Run only ingestion tests:

```code
python -m pytest tests/test_ingestion.py
```

Run only cleaning tests:

```code
python -m pytest tests/test_cleaning.py
```

Run only validation tests:

```code
python -m pytest tests/test_validation.py
```

Run only export tests:

```code
python -m pytest tests/test_export.py
```

Run only reporting tests:

```code
python -m pytest tests/test_reporting.py
```

Current test coverage includes:

### Data Ingestion

* Loading CSV files with `;`
* Loading CSV files with `,` explicitly
* Loading Excel files as strings
* Loading Parquet files while preserving schema
* Loading Parquet files as strings when requested
* Detecting missing files
* Detecting unsupported file extensions
* Loading files by date
* Loading historical files
* Loading files from a specific month
* Adding `file_date` during historical loading

### Data Cleaning

* Normalizing column names
* Stripping string values
* Dropping fully empty rows
* Converting values to float
* Converting values to nullable integers
* Converting values to dates
* Converting values to datetimes
* Handling invalid numeric and date values
* Applying the basic `clean_df` pipeline
* Renaming columns during cleaning
* Supporting day-first date formats

### Data Validation

* Validating non-empty DataFrames
* Validating required columns
* Detecting missing columns
* Detecting null values
* Validating unique records
* Validating composite keys
* Validating numeric differences with tolerance
* Detecting negative values
* Validating allowed categorical values
* Validating numeric ranges

### Data Export

* Exporting CSV files
* Exporting CSV files with custom separators
* Exporting Excel files
* Exporting Excel files with custom sheet names
* Exporting Parquet files
* Exporting partitioned Parquet datasets
* Creating parent folders automatically

### Excel Reporting

* Copying Excel templates
* Writing scalar values as 1x1 blocks
* Writing DataFrames into specific cells
* Creating Excel tables by default when headers are included
* Avoiding Excel tables when headers are not included
* Raising errors when trying to create tables without headers
* Applying row-based number and percent formats
* Creating reports from templates
* Preserving images in templates

## Working With Notebooks

Notebooks are useful for reviewing intermediate DataFrames, checking errors and documenting process decisions step by step.

Before committing notebooks to GitHub, clear cell outputs to avoid uploading sensitive or unnecessary data.

Clear outputs from one notebook:

```code
jupyter nbconvert --clear-output --inplace notebooks/demo_end_to_end.ipynb
```

Clear outputs from all notebooks in the `notebooks/` folder:

```code
jupyter nbconvert --clear-output --inplace notebooks/*.ipynb
```

You can also clear outputs manually in VS Code:

```text
Notebook -> Clear All Outputs
```

This keeps the repository cleaner and safer for review.

## Environment Notes

A virtual environment is recommended but not required.

If you want to use a virtual environment locally:

```code
python -m venv .venv
python -m pip install -e ".[dev]"
```

The `.venv/` folder should not be uploaded to GitHub.

If you prefer to use your global Python installation during development, that also works as long as the required dependencies are installed.

## Design Principles

This project follows these principles:

* Toolkit before framework
* Notebook-friendly usage
* Simplicity before complexity
* Separation of concerns
* Parquet-first processing when possible
* Excel only for review, delivery or formatted reports
* Reliability through validation and testing
* Reusability across projects
* Clear module boundaries
* Business logic separated from toolkit logic
* Reporting from templates instead of hardcoded report layouts

## What Belongs in This Toolkit

This project should include general-purpose data tools such as:

* File ingestion
* Data cleaning helpers
* Data validation helpers
* Standardized data exports
* Parquet export helpers
* Excel reporting helpers for templates
* Notebook-friendly utilities that are broadly reusable

## What Does Not Belong in This Toolkit

This project should not include:

* Proprietary business logic
* Corporate paths
* Client-specific rules
* Confidential datasets
* Internal reporting templates
* Company-specific financial calculations
* Report-specific transformations tied to one client
* Automatic workflow engines
* Observability infrastructure
* PDF export tied to local Excel installation

Business-specific logic should live in separate private notebooks, scripts or projects that use this toolkit.

## Roadmap

### MVP

* Professional project structure
* Installable package
* Data ingestion module
* Data cleaning module
* Data validation module
* Data export module
* Excel reporting module
* Initial tests
* Initial examples
* Initial documentation

### v1

* Improved examples
* End-to-end example
* More documentation for notebook usage
* Expanded tests
* Optional generic transformation helpers if repeated across projects

### v2

* Optional config helpers if repeated path patterns become necessary
* Optional notebook templates
* Optional reusable reporting patterns

### v3

* Portfolio-ready documentation
* More complete examples using synthetic data
* Optional automation integrations

## Long-Term Vision

The long-term vision is to evolve `dr-data-toolkit` into a practical foundation for reusable data work.

The project should help transform repetitive notebook code into structured, reusable and testable tools.

It is intended to support future growth toward:

* Data reliability
* Analytics engineering
* Professional reporting workflows
* Workflow standardization without rigidity
* Portfolio-ready technical work

## License

MIT License.
