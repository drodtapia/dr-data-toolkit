# Vision

`dr-data-toolkit` is a practical Python toolkit for reusable, reliable and notebook-friendly data work.

The package is imported as:

```python
import dr_datakit
```

## Why This Project Exists

Many real data processes start as notebooks.

Notebooks are useful because they allow the user to:

* Review intermediate DataFrames.
* Validate results step by step.
* Debug issues quickly.
* Document process decisions.
* Adapt the logic to each client, portfolio or report.
* Keep manual control over execution.

However, notebooks can become difficult to maintain when the same technical code is repeated many times.

This project exists to move reusable technical logic out of notebooks and into a clean Python package.

The notebook remains the working space.

The package provides the reusable tools.

## Core Idea

The core idea is:

```text
Do not force the workflow.
Make the tools reliable.
```

The package should not decide what process to run.

The user decides the process in a notebook or script.

The package helps with common technical tasks:

* Loading files.
* Cleaning data.
* Validating data.
* Exporting processed outputs.
* Creating Excel reports from templates.

## Target Use Case

The toolkit is designed for data work where each process may have different requirements.

Examples:

* Monthly reports.
* Portfolio reports.
* Client-specific data checks.
* Operational reconciliations.
* Data validation processes.
* Excel reporting from templates.
* Notebook-based review workflows.

The toolkit should be flexible enough to support different processes without forcing them into a single structure.

## Project Philosophy

The project follows a toolkit-first philosophy:

```text
Jupyter Notebook = control and review
dr_datakit       = reusable technical tools
Parquet          = processed data
Excel/CSV        = review or delivery
Templates        = formatted reporting layer
```

This separation helps keep notebooks cleaner and makes repeated tasks easier to maintain.

## What the Toolkit Should Do

The toolkit should make common tasks easier and more consistent.

It should help users:

* Load files with consistent defaults.
* Preserve raw data safely.
* Clean columns and values consistently.
* Convert numeric and date fields explicitly.
* Validate important assumptions.
* Export processed data with standard settings.
* Create Excel reports from existing templates.
* Reduce repeated code in notebooks.
* Keep business logic separate from technical helpers.

## What the Toolkit Should Not Do

The toolkit should not become a rigid workflow engine.

It should not:

* Decide which reports to run.
* Decide which process date to use.
* Hide important validations.
* Contain client-specific business logic.
* Contain proprietary paths.
* Contain confidential datasets.
* Contain internal report templates.
* Force a fixed folder structure.
* Replace Jupyter notebooks.
* Replace pandas.

The toolkit should support the user's process, not control it.

## Notebook-Friendly Design

A good notebook using this toolkit should be easy to read.

It may follow a structure like:

```text
00. Imports and setup
01. Process dates
02. Paths and file names
03. Execution flags
04. Load input data
05. Clean data
06. Base validations
07. Specific report logic
08. Export processed data
09. Create Excel reports
```

The notebook can still contain process-specific logic.

The toolkit removes repeated technical details.

## Long-Term Vision

The long-term vision is to evolve `dr-data-toolkit` into a reliable foundation for professional data work.

It should help transform repeated notebook code into reusable, tested and documented tools.

The project should support growth toward:

* Cleaner notebooks.
* Better data reliability.
* More consistent reporting.
* Reusable technical patterns.
* Professional portfolio work.
* Analytics engineering practices.
* Practical automation when needed.

## Portfolio Vision

This project can also serve as a portfolio project.

It demonstrates:

* Python package structure.
* Editable package installation.
* Modular design.
* Testing with `pytest`.
* Data ingestion design.
* Data cleaning design.
* Data validation design.
* Export standardization.
* Excel reporting from templates.
* Documentation.
* Separation between reusable tools and business logic.

The portfolio version should use only synthetic data and public examples.

It should not include confidential information, client names, corporate paths or proprietary templates.

## Growth Principle

The project should grow only when a repeated need appears.

A function should be added when it solves a general problem that appears across multiple notebooks or projects.

A function should not be added only because it was useful once in one specific report.

## Final Vision

`dr-data-toolkit` should remain simple, practical and useful.

It should be a toolkit that helps people work better with data, especially in notebook-based environments where clarity, validation and flexibility matter.
