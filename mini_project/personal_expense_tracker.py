# -*- coding: utf-8 -*-
"""personal_expense_tracker.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MpwAG3mej8Nccs0960P0QffsC3QPwxrc
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

"""##Data Structure and File Handling"""

expenses = []

"""##Add Expense Function"""

from datetime import datetime

def isvalid_date(date):
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def Date():
    date = input("Enter date (YYYY-MM-DD) or press Enter for today: ")

    # if it is void or null entry then take it as today
    if not date :
        date = datetime.today().strftime('%Y-%m-%d')

    #check if it is valid or not
    elif not isvalid_date(date):
        print("Invalid date format. Please use format YYYY-MM-DD.")
        return Date()   # if not valid ask user again to put

    # again check if the date is not in future
    elif datetime.strptime(date, '%Y-%m-%d') > datetime.now():
        print("Date cannot be in the future.")
        return Date()

    # check if it is more than 100 years old (which is seems invalid)
    elif datetime.today().year - datetime.strptime(date, '%Y-%m-%d').year >= 10:
        print("Date seems unrealistic (it cannot be more than 10 years old)!")
        return Date()

    return date

def add_amount():
    amount = input("Enter amount: ₹")
    try:
        amount = float(amount)
        return amount
    except ValueError:
        print("Invalid amount. Please enter a valid number.")
        return add_amount()

def add_expense():

    category = str()
    while True:
        cat_choice = input("""
              ---Enter category----
                    1. Food
                    2. Travel
                    3. Transport
                    4. Entertainment
                    5. study
                    Enter you category: """)

        if cat_choice == '1':
            category = 'Food'
            break
        elif cat_choice == '2':
            category = 'Travel'
            break
        elif cat_choice == '3':
            category = 'Transport'
            break
        elif cat_choice == '4':
            category = 'Entertainment'
            break
        elif cat_choice == '5':
            category = 'Study'
            break
        else:
            print("Invalid choice! Try again.")

    amount = add_amount()
    date = Date()

    expense = {'amount': amount, 'category': category, 'date': date}
    expenses.append(expense)
    print("Expense added successfully!")

"""## Delete some data"""

def delete_expense():
    # """Remove one or more expenses that match a given date + category."""
    if not expenses:
        print("No expenses recorded yet.")
        return

    # Date() helper for validation
    date_to_del = Date()
    cat_to_del = input("Enter category to delete from: ").strip()

    # Find indices of matching rows
    matches = [
        idx for idx, exp in enumerate(expenses)
        if exp["date"] == date_to_del and exp["category"].lower() == cat_to_del.lower()
    ]

    if not matches:
        print("No expense found for that date and category.")
        return

    # If more than one match, let the user choose
    if len(matches) > 1:
        print("\nMatching expenses:")
        for i, idx in enumerate(matches, start=1):
            e = expenses[idx]
            print(f"{i}. ₹{e['amount']:.2f}  |  {e['category']}  |  {e['date']}")
        sel = input("Enter number to delete (or 'a' to delete *all*): ").strip()

        if sel.lower() == "a":
            for idx in sorted(matches, reverse=True):
                expenses.pop(idx)
            print("All matching expenses deleted.")
        else:
            try:
                choice = int(sel)
                expenses.pop(matches[choice - 1])
                print("Expense deleted.")
            except (ValueError, IndexError):
                print("Invalid selection — nothing deleted.")
    else:
        expenses.pop(matches[0])
        print("Expense deleted.")

"""## Save & Load from File"""

import json
from datetime import date, datetime


def save_expenses(filename="expenses.json"):
    with open(filename, "w") as f:
        # Convert datetime objects to strings before saving
        serializable_expenses = []
        for exp in expenses:
            exp_copy = exp.copy()
            if isinstance(exp_copy.get('date'), datetime):
                exp_copy['date'] = exp_copy['date'].strftime('%Y-%m-%d')
            serializable_expenses.append(exp_copy)
        json.dump(serializable_expenses, f)

def load_expenses(filename="expenses.json"):
    global expenses
    try:
        with open(filename, "r") as f:
            expenses = json.load(f)
    except FileNotFoundError:
        expenses = []

"""## Visual summary"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

## visual summary

def visual_summary():
  exp_data = pd.DataFrame(expenses)
  exp_data['date'] = pd.to_datetime(exp_data['date'], errors='coerce')
  exp_data = exp_data.sort_values('date')

  plt.style.use('seaborn-v0_8-darkgrid') # Use a dark grid style for a more aesthetic look

  plt.figure(figsize=(10,6))
  # bar plot categpry wise expense and annotate
  category_wise = exp_data.groupby('category')['amount'].sum().reset_index()
  sns.barplot(data=category_wise, x='category',y='amount', palette='coolwarm')

  # annotate
  for i in range(len(category_wise)):

      plt.text(i, category_wise['amount'][i]+1.5, '$' + str(category_wise['amount'][i]), ha='center')
  plt.title("Category wise Expense",fontsize=20, fontweight="bold")
  plt.xlabel("Category",fontsize=18)
  plt.ylabel("Amount",fontsize=18)
  plt.ylim(0,category_wise['amount'].max()+100)
  plt.show()

  ### daiy wise expenses

  # Aggregate data by date and category
  daily_expenses = exp_data.groupby(['date', 'category'])['amount'].sum().reset_index()

  plt.figure(figsize=(13, 7)) # Increase figure size

  # Plot with Seaborn for enhanced aesthetics
  ax = sns.lineplot(data=daily_expenses, x='date', y='amount', hue='category', marker='o', palette='Paired', linewidth=2)

  # Annotate points
  for line in ax.lines:
    for x_val, y_val in zip(line.get_xdata(), line.get_ydata()):
      ax.annotate(f'{y_val:.0f}', (x_val, y_val), textcoords="offset points", xytext=(0,10), ha='center', fontsize=9)

  plt.title('Day-wise Expenses by Category', fontsize=20, fontweight='bold') # Make title bold
  plt.xlabel('Date', fontsize=18)
  plt.ylabel('Amount', fontsize=18)
  plt.xticks(rotation=45, ha='right') # Rotate x-axis labels for better readability
  plt.grid(True) # Add a more subtle grid
  plt.tight_layout()

  plt.show()

  print("\nWant to see as table?? press 'Y' for yes else press any other key: ")
  ch = input()
  if ch == 'Y' or ch == 'y':
    exp_data= exp_data.reset_index(drop=True)
    print(exp_data)
  return 

"""##View Summary"""

from collections import defaultdict

def view_summary():

    summary = defaultdict(float)
    total = 0.0

    # to track all kind of spending
    max_spending = 0.0
    max_spending_date = None
    max_spending_category = None

    min_spending = float('inf')
    min_spending_date = None
    min_spending_category = None

    for exp in expenses:
        summary[exp['category']] += exp['amount']
        total += exp['amount']

        # record of max spending
        if exp['amount'] > max_spending:
            max_spending = exp['amount']
            max_spending_date = exp['date']
            max_spending_category = exp['category']

        # recored of minimum spending
        if exp['amount'] < min_spending:
            min_spending = exp['amount']
            min_spending_date = exp['date']
            min_spending_category = exp['category']

    print("\nSummary by Category:")
    for cat, amt in summary.items():
        print(f"{cat}: ₹{amt:.2f}")

    print(f"Total spending: ₹{total:.2f}")
    if total ==0:
      return

    print(f"\nAverage spending per day: ₹{total/len(expenses):.2f}")
    print(f"Maximum spending: amount: ₹{max_spending:.2f} , category: {max_spending_category} , date: {max_spending_date}")
    print(f"Minimum spending: amount: ₹{min_spending:.2f} , category: {min_spending_category} , date: {min_spending_date}")
    print(f"Number of expenses: {len(expenses)}")


    print("\nwant more visual summary!!\nPress 'Y' for that")
    choice = input()
    if choice == 'Y' or choice=='y':
        visual_summary()
    return

"""## Menu System"""

def main():
    load_expenses()
    while True:
        print("\n----- Expense Tracker -----")
        print("1. Add Expense")
        print("2. View Summary")
        print("3. Delete Expense")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_expense()
            save_expenses()
        elif choice == '2':
            view_summary()
        elif choice == '3':
            delete_expense()
            save_expenses()
        elif choice == '4':
            save_expenses()
            print("Goodbye!")
            break
        else:
            print("Invalid choice! Try again.")

main()


