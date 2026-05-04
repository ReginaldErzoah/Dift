# Dift Cheat Sheet (v0.3.0)

## Overview

Dift is a command-line tool used to compare two datasets and identify: -
structural changes - row-level changes - data quality issues - risk
level of changes

------------------------------------------------------------------------

## Core Command Structure

    dift <old_dataset> <new_dataset> [OPTIONS]

### Explanation

-   `<old_dataset>`: Path to the original dataset
-   `<new_dataset>`: Path to the updated dataset
-   `[OPTIONS]`: Optional flags to control behavior

------------------------------------------------------------------------

## Basic Usage

    dift old.csv new.csv

### What happens

-   Loads both datasets
-   Compares schema and data
-   Outputs results in terminal

------------------------------------------------------------------------

## Using a Key for Row Comparison

    dift old.csv new.csv --key id

### Why this matters

Without `--key`: - Only compares dataset as a whole

With `--key`: - Detects added rows - Detects removed rows - Detects
modified rows

### Common error

If the key column does not exist:

    Error: column not found

------------------------------------------------------------------------

## Output Formats

### JSON

    dift old.csv new.csv --report json --output report.json

#### What it does

-   Exports full structured report
-   Includes all diff details

#### Expected output structure

-   metadata
-   summary
-   schema
-   rows
-   quality
-   numeric
-   categorical

------------------------------------------------------------------------

### CSV

    dift old.csv new.csv --report csv --output report.csv

#### What it does

-   Exports summary only
-   Designed for pipelines

#### Expected output

metric,value\
old_rows,10\
new_rows,11

------------------------------------------------------------------------

### Excel

    dift old.csv new.csv --report excel --output report.xlsx

#### What it does

-   Creates multiple sheets
-   Includes quality details

#### Expected sheets

-   Summary
-   Quality Diff

------------------------------------------------------------------------

### HTML

    dift old.csv new.csv --report html --output report.html

#### What it does

-   Generates visual report
-   Supports templates

------------------------------------------------------------------------

## HTML Templates

    dift old.csv new.csv --report html --template clean

### Available options

-   default
-   clean
-   compact
-   enterprise
-   dark

------------------------------------------------------------------------

## Output Directory
Use --output-dir when you want Dift to create a folder and name the output file automatically.

dift old.csv new.csv --report json --output-dir summaries/

<Note: do not use --output and --output-dir together. Dift will reject the command to avoid ambiguity.

### Behavior

-   Creates folder if it does not exist
-   Auto-generates filename

### Expected result

reports/ dift_report.json

------------------------------------------------------------------------

## Null Spike Detection

### Example output

    Null spike: 'revenue' increased by 80.00% (high)

### Meaning

-   Significant increase in missing values

### Severity levels

-   low: less than 5 percent
-   medium: 5 to 15 percent
-   high: greater than or equal to 15 percent

------------------------------------------------------------------------

## What Dift Detects

### Schema

-   columns added
-   columns removed
-   type changes

### Rows

-   added rows
-   removed rows
-   changed rows

### Data Quality

-   null spikes
-   duplicates

------------------------------------------------------------------------

## Common Errors

### Missing file

    Error: File not found

### Invalid option combination

    --output and --output-dir cannot be used together

### Unsupported format

    Unsupported dataset type

------------------------------------------------------------------------

## Best Practices

-   Always use a key for accurate comparison
-   Use JSON for integrations
-   Use Excel or HTML for analysis
-   Use CSV for automation pipelines

------------------------------------------------------------------------

## Quick Commands

    dift old.csv new.csv
    dift old.csv new.csv --key id
    dift old.csv new.csv --report json --output report.json
    dift old.csv new.csv --report excel --output report.xlsx
    dift old.csv new.csv --report html --template dark
    dift old.csv new.csv --report csv --output-dir reports/
