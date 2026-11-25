# Python CLI Utility: Expense Tracker

## Objective
A console application that applies core logic, data structures and file handling.

## Run
Requires Python 3.8 or later. No extra packages.

    python expense_tracker.py

## Features
- Add, view, search and delete expenses
- Category-wise summary with percentages
- Input validation
- Data saved between runs, plus CSV export

## Concepts used
| Concept | Where |
|---|---|
| List of dictionaries | Storing expenses |
| `defaultdict` | Category totals |
| Set comparison | Validating loaded records |
| Sorting with `lambda` | Table and summary |
| List comprehension | Search |
| JSON and CSV file handling | Load, save, export |
| Exception handling | Bad input, damaged data file |

## Files created while running
- `expenses.json`: saved data
- `expenses.csv`: created by the export option

## Possible improvements
Edit an expense, monthly reports, budget limits, unit tests.
