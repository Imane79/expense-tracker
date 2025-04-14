import tkinter as tk
from db import init_db, insert_expense  # import from your db.py
import datetime
from tkinter import messagebox
from db import fetch_expenses


# Step 1: Initialize the database
init_db()

# Step 2: Create the main window
root = tk.Tk()

root.title("Expense Tracker")
root.geometry("400x400")

amount_label = tk.Label(root, text="Amount:")
amount_label.pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

category_label = tk.Label(root, text="Category:")
category_label.pack()

category_entry = tk.Entry(root)
category_entry.pack()

note_label = tk.Label(root, text="Note (optional):")
note_label.pack()
note_entry = tk.Entry(root)
note_entry.pack()


# --- Button Function ---
def add_expense():
    amount = amount_entry.get()
    category = category_entry.get()
    note = note_entry.get()
    date = datetime.date.today().isoformat()

    if not amount or not category:
        messagebox.showerror("Error", "Amount and Category are required.")
        return

    try:
        insert_expense(float(amount), category, note, date)
        messagebox.showinfo("Success", "Expense added successfully.")
        amount_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        note_entry.delete(0, tk.END)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number.")


# --- Add Button ---
add_button = tk.Button(root, text="Add Expense", command=add_expense)
add_button.pack(pady=10)


add_button.pack(pady=10)
# Expenses Display Area
expense_list = tk.Text(root, height=10, width=45)
expense_list.pack(pady=10)


def load_expenses():
    expense_list.delete(1.0, tk.END)  # Clear the box first
    expenses = fetch_expenses()
    for exp in expenses:
        expense_list.insert(
            tk.END, f"{exp[4]} - {exp[1]}₺ | {exp[2]} | {exp[3]}\n")


load_expenses()


root.mainloop()
