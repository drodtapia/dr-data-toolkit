# Roadmap

This roadmap describes the planned evolution of `dr-data-toolkit`.

The project is currently focused on being a practical, notebook-friendly data toolkit rather than a rigid workflow framework.

## Current Status

Current package name:

```text
dr-data-toolkit
```

Current import name:

```python
import dr_datakit
```

Current MVP modules:

```text
ingestion.py
cleaning.py
validation.py
export.py
reporting.py
```

Current focus:

* Reusable data tools.
* Clean notebook usage.
* Standardized loading, cleaning, validation and export.
* Excel reporting from templates.
* Simple examples.
* Reliable tests.

## MVP Scope

The MVP is focused on the core tools needed for practical data work.

### Included

* Professional Python package structure.
* Editable local installation.
* Data ingestion utilities.
* Data cleaning utilities.
* Data validation utilities.
* Data export utilities.
* Excel reporting utilities.
* End-to-end example using synthetic data.
* Initial documentation.
* Test suite.

### Not Included

The following items are intentionally excluded from the MVP:

* Workflow engine.
* Config framework.
* Custom exception hierarchy.
* Client-specific logic.
* Portfolio-specific calculations.
* Internal templates.
* PDF export through local Excel.
* Observability or monitoring infrastructure.
* Automated scheduling.
* Cloud deployment.

## Version 0.1

Version 0.1 represents the first stable local toolkit.

Main goals:

* Keep the package simple.
* Keep the API easy to understand.
* Make the toolkit useful from Jupyter notebooks.
* Ensure all main functions have tests.
* Provide examples that can be executed without private data.

Expected modules:

```text
dr_datakit.ingestion
dr_datakit.cleaning
dr_datakit.validation
dr_datakit.export
dr_datakit.reporting
```

Expected examples:

```text
examples/example_ingestion.py
examples/example_cleaning.py
examples/example_validation.py
examples/example_export.py
examples/example_reporting.py
examples/example_end_to_end.py
```

## Version 0.2

Version 0.2 should improve usability and documentation.

Possible improvements:

* Improve README examples.
* Add a notebook demo using synthetic data.
* Add a clear notebook structure example.
* Improve `example_end_to_end.py`.
* Add more edge case tests.
* Improve docstrings.
* Review naming consistency.
* Add contribution notes for clearing notebook outputs.

Potential notebook:

```text
notebooks/demo_end_to_end.ipynb
```

The notebook should explain the process step by step:

```text
1. Create synthetic data
2. Load data
3. Clean data
4. Validate data
5. Export processed Parquet
6. Create an Excel report
```

## Version 0.3

Version 0.3 may add generic transformation helpers if repeated patterns appear across projects.

Potential module:

```text
transforms.py
```

This should only be added if there are repeated generic needs.

Possible helpers:

* Add total rows.
* Build monthly matrices.
* Format month labels.
* Build simple summary tables.
* Prepare report-friendly tables.

Important rule:

Generic transformations are allowed.

Client-specific transformations should not be included.

## Version 0.4

Version 0.4 may add optional notebook-friendly helpers.

Possible ideas:

* Clear outputs instruction in documentation.
* Simple folder creation helper.
* Simple file naming helper.
* Simple date label helper.

These should only be added if they clearly reduce repeated notebook code.

The project should avoid adding abstractions too early.

## Version 1.0

Version 1.0 should represent a stable public toolkit.

Possible requirements for v1.0:

* Clear README.
* Clean docs.
* Stable API.
* Tests passing.
* No private data.
* No proprietary paths.
* No broken examples.
* End-to-end example available.
* Optional notebook demo available.
* Installation instructions validated.
* Clean project structure.

## Long-Term Possibilities

Future directions may include:

* More robust reporting helpers.
* Optional template-based notebook examples.
* More validation helpers.
* More export helpers.
* Improved documentation for portfolio presentation.
* Synthetic examples based on realistic business processes.
* Optional integration examples with cloud storage or SharePoint.

## Things to Avoid

The project should avoid becoming too broad or too abstract.

Avoid:

* Adding functions before they are needed.
* Turning the toolkit into a rigid framework.
* Hiding important notebook decisions.
* Mixing business logic with toolkit logic.
* Adding client-specific calculations.
* Adding complex configuration too early.
* Adding a workflow engine without a clear need.
* Adding dependencies that are not necessary.

## Guiding Principle

The project should grow from repeated real needs.

If a pattern appears in several notebooks or projects, it may belong in the toolkit.

If a pattern is specific to one client, portfolio or report, it should stay outside the toolkit.
