"""Expense Tracker: a console app using only the Python standard library."""

import csv
import json
import math
from collections import defaultdict
from datetime import date, datetime
from pathlib import Path

DATA_FILE = Path("expenses.json")
CSV_FILE = Path("expenses.csv")
FIELDS = ["id", "date", "category", "amount", "note"]



def load_expenses():
    """Return the saved expenses as a list of dictionaries."""
    if not DATA_FILE.exists():
        return []
    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        if not isinstance(data, list) or not all(
            isinstance(item, dict) and set(FIELDS) <= item.keys() for item in data
        ):
            raise ValueError("unexpected file layout")
        return data
    except ValueError:
        backup = DATA_FILE.with_name(f"expenses_{datetime.now():%Y%m%d_%H%M%S}.bak")
        DATA_FILE.replace(backup)
        print(f"Data file was damaged. It was moved to {backup}.")
        return []


def save_expenses(expenses):
    """Write to a temporary file first so a crash cannot corrupt the data."""
    temp = DATA_FILE.with_suffix(".tmp")
    temp.write_text(json.dumps(expenses, indent=2), encoding="utf-8")
    temp.replace(DATA_FILE)


def export_csv(expenses):
    with CSV_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(expenses)



def add_expense(expenses, day, category, amount, note=""):
    next_id = max((e["id"] for e in expenses), default=0) + 1
    expense = {"id": next_id, "date": day, "category": category,
               "amount": amount, "note": note}
    expenses.append(expense)
    return expense


def delete_expense(expenses, expense_id):
    for index, expense in enumerate(expenses):
        if expense["id"] == expense_id:
            del expenses[index]
            return True
    return False


def search_expenses(expenses, keyword):
    keyword = keyword.lower()
    return [e for e in expenses
            if keyword in e["category"].lower() or keyword in e["note"].lower()]


def category_totals(expenses):
    totals = defaultdict(float)
    for e in expenses:
        totals[e["category"]] += e["amount"]
    return dict(totals)


def ask_date():
    while True:
        text = input("Date (YYYY-MM-DD, Enter for today): ").strip()
        if not text:
            return date.today().isoformat()
        try:
            return datetime.strptime(text, "%Y-%m-%d").date().isoformat()
        except ValueError:
            print("Invalid date.")


def ask_amount():
    while True:
        try:
            amount = float(input("Amount: ").strip())
            if math.isfinite(amount) and round(amount, 2) > 0:
                return round(amount, 2)
        except ValueError:
            pass
        print("Enter a number greater than 0.")


def ask_category():
    while True:
        text = input("Category: ").strip().title()
        if text:
            return text
        print("Category cannot be empty.")


def show_table(expenses):
    if not expenses:
        print("No expenses found.")
        return
    print(f"{'ID':<5}{'Date':<12}{'Category':<15}{'Amount':>10}  Note")
    print("-" * 60)
    for e in sorted(expenses, key=lambda item: (item["date"], item["id"])):
        print(f"{e['id']:<5}{e['date']:<12}{e['category']:<15}"
              f"{e['amount']:>10.2f}  {e['note']}")
    print("-" * 60)
    print(f"{'Total':<32}{sum(e['amount'] for e in expenses):>10.2f}")


def show_summary(expenses):
    totals = category_totals(expenses)
    if not totals:
        print("No expenses found.")
        return
    grand_total = sum(totals.values())
    for category, total in sorted(totals.items(), key=lambda kv: kv[1], reverse=True):
        print(f"{category:<15}{total:>10.2f}  {total / grand_total:>6.1%}")
    print(f"{'Total':<15}{grand_total:>10.2f}")


MENU = """
=== Expense Tracker ===
1. Add expense
2. View all
3. Search
4. Delete
5. Category summary
6. Export to CSV
0. Exit"""


def main():
    expenses = load_expenses()
    while True:
        print(MENU)
        choice = input("Choose: ").strip()
        if choice == "1":
            expense = add_expense(expenses, ask_date(), ask_category(),
                                  ask_amount(), input("Note (optional): ").strip())
            save_expenses(expenses)
            print(f"Added expense #{expense['id']}.")
        elif choice == "2":
            show_table(expenses)
        elif choice == "3":
            show_table(search_expenses(expenses, input("Keyword: ").strip()))
        elif choice == "4":
            text = input("ID to delete: ").strip()
            if text.isdecimal() and delete_expense(expenses, int(text)):
                save_expenses(expenses)
                print("Deleted.")
            else:
                print("No expense with that ID.")
        elif choice == "5":
            show_summary(expenses)
        elif choice == "6":
            export_csv(expenses)
            print(f"Exported to {CSV_FILE}.")
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nGoodbye!")
