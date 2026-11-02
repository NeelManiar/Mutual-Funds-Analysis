# Mutual Funds Analysis

A small Streamlit application that compares two mutual fund portfolio statements and shows what has changed between them.

The idea is simple: upload two portfolio files, choose which one is the earlier statement and which one is the later statement, and see which instruments have been added, removed or retained.

## What it does

- Accepts two portfolio files in CSV or Excel (`.xlsx`) format.
- Reads the `NAME_OF_THE_INSTRUMENT` column from each file.
- Compares the instrument names across both portfolios.
- Identifies newly added instruments.
- Identifies instruments that have been removed.
- Lists instruments that appear in both portfolios.
- Displays the results in separate tabs.
- Provides a downloadable CSV containing the comparison results.

Instrument names are cleaned before comparison. Extra spaces and differences in capitalisation are ignored, so minor formatting differences do not create false additions or removals.

## Built with

- Python
- Streamlit
- Pandas
- Openpyxl

## Running the project

Clone the repository:

```bash
git clone https://github.com/NeelManiar/Mutual-Funds-Analysis.git
cd Mutual-Funds-Analysis
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Start the application:

```bash
streamlit run app.py
```

Streamlit will open the application in your browser.

## Input file requirements

Both uploaded files must contain a column named:

```text
NAME_OF_THE_INSTRUMENT
```

The application accepts `.csv` and `.xlsx` files.

You can upload two statements from different reporting dates and select which one should be treated as the earlier portfolio.

## How the comparison works

The application converts the instrument names into sets and uses set operations to identify the differences.

- **Added:** Instruments present in the later portfolio but absent from the earlier one.
- **Removed:** Instruments present in the earlier portfolio but absent from the later one.
- **Unchanged:** Instruments present in both portfolios.

The results can be downloaded as `portfolio_comparison.csv`.

## Current limitations

This version compares instrument names only. It does not yet compare units held, NAV, market value, allocation percentages or changes in investment amounts.

It is intended as a simple way to identify changes between two portfolio statements, with scope for more detailed portfolio analysis in future versions.

---

**Author:** [Neel Maniar](https://github.com/NeelManiar)
