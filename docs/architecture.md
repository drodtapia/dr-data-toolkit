# Architecture

`dr-data-toolkit` is a lightweight Python toolkit for reusable, reliable and notebook-friendly data work.

The package is imported as:

```python
import dr_datakit
```

or:

```python
from dr_datakit import load_file, clean_df, create_report
```

## Architecture Goal

The goal of this project is not to enforce a rigid workflow or pipeline structure.

The goal is to provide reusable tools that help with common data tasks while keeping the user in control of the process.

This is especially useful when working in Jupyter notebooks, where each client, portfolio, report or process may require different steps, validations and outputs.

## Current Package Structure

```text
src/
`-- dr_datakit/
    |-- __init__.py
    |-- ingestion.py
    |-- cleaning.py
    |-- validation.py
    |-- export.py
    `-- reporting.py
```

## Module Responsibilities

### `ingestion.py`

Handles loading files and historical datasets.

Main responsibilities:

* Load single files.
* Load files by prefix.
* Load files by date.
* Load historical files.
* Load files from a specific month.
* Support CSV, TXT, Excel and Parquet.
* Preserve raw data safely when needed.

Typical use:

```python
from dr_datakit import load_file, load_date, load_history
```

### `cleaning.py`

Handles basic and reusable DataFrame cleaning operations.

Main responsibilities:

* Normalize column names.
* Strip string values.
* Drop empty rows.
* Convert selected columns to float.
* Convert selected columns to nullable integer.
* Convert selected columns to date.
* Convert selected columns to datetime.
* Apply a basic cleaning pipeline with `clean_df`.

Typical use:

```python
from dr_datakit import clean_df, to_float, to_date
```

### `validation.py`

Handles reusable validation checks.

Main responsibilities:

* Validate non-empty DataFrames.
* Validate required columns.
* Validate non-null fields.
* Validate unique records.
* Validate values within tolerance.
* Validate non-negative numbers.
* Validate allowed categorical values.
* Validate numeric ranges.

Typical use:

```python
from dr_datakit import validate_not_empty, validate_required_columns, validate_unique
```

Validation functions do not return a DataFrame. They either pass silently or raise a clear error.

### `export.py`

Handles standardized exports.

Main responsibilities:

* Export CSV files.
* Export Excel files.
* Export Parquet files.
* Export partitioned Parquet datasets.
* Create parent folders automatically.
* Centralize export defaults.

Typical use:

```python
from dr_datakit import export_csv, export_excel, export_parquet
```

### `reporting.py`

Handles Excel reporting from templates.

Main responsibilities:

* Copy Excel templates.
* Preserve template structure, formatting and images.
* Write scalar values, lists, Series or DataFrames into worksheets.
* Create Excel tables when appropriate.
* Apply number, percent and date formats.
* Create final reports from a list of block definitions.

Typical use:

```python
from dr_datakit import copy_template, write_block, create_report
```

## Design Philosophy

The package follows a toolkit-first architecture.

```text
Jupyter Notebook = working space and review layer
dr_datakit       = reusable technical tools
Parquet          = official processed dataset
Excel/CSV        = review, delivery or reporting output
Templates        = formatted Excel reports
```

The notebook or script controls the process.

The package provides reusable building blocks.

## Typical Flow

A common process may look like this:

```text
raw data -> load -> clean -> validate -> export parquet -> create Excel report
```

However, this flow is not enforced.

A notebook may use only some modules, depending on the process.

Examples:

```text
load -> clean -> validate
load -> export parquet
load processed parquet -> create report
clean -> validate -> export Excel
```

## Why There Is No Workflow Engine

This project intentionally does not include a workflow engine.

The reason is that the target use case is flexible notebook-based work, where each process may have different sections, rules and outputs.

A rigid workflow engine would hide important decisions and make the project harder to adapt.

Instead, the user can organize a notebook into clear sections such as:

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

## What Belongs in the Toolkit

This package should include generic reusable tools such as:

* File loading helpers.
* Data cleaning helpers.
* Data validation helpers.
* Standardized export helpers.
* Excel reporting helpers.
* Notebook-friendly utilities that are broadly useful.

## What Does Not Belong in the Toolkit

This package should not include:

* Client-specific business logic.
* Portfolio-specific calculations.
* Corporate paths.
* Confidential data.
* Internal templates.
* Report-specific transformations tied to a single use case.
* Automatic workflow engines.
* Observability infrastructure.
* PDF export tied to local Excel installation.

Business-specific logic should live in private notebooks, scripts or client-specific projects that use this toolkit.

## Data and Output Philosophy

The project is designed around a practical separation:

```text
raw data      -> original inputs
processed data -> cleaned and validated datasets, preferably Parquet
reports       -> formatted Excel outputs for review or delivery
```

Parquet is preferred for processed datasets because it preserves schema and is efficient for reuse.

Excel and CSV are used for review, delivery or reporting.

## Current MVP

The current MVP includes:

* Data ingestion.
* Data cleaning.
* Data validation.
* Data export.
* Excel reporting from templates.
* Tests.
* Examples.
* Documentation.

The MVP intentionally avoids unnecessary abstractions.
