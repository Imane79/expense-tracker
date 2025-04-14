import tkinter as tk
from tkinter import messagebox
import datetime
from db import init_db, insert_expense, fetch_expenses

# --- Initialize DB ---
init_db()

# --- Main Window ---
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("420x600")

# --- Input Fields ---
amount_label = tk.Label(root, text="Amount:")
amount_label.pack()
amount_entry = tk.Entry(root)
amount_entry.pack(pady=2)

# --- Category Input: Dropdown + Text ---
category_label = tk.Label(root, text="Category:")
category_label.pack()

category_frame = tk.Frame(root)
category_frame.pack()

# Dropdown
category_var = tk.StringVar()
category_var.set("Select category")

category_menu = tk.OptionMenu(category_frame, category_var, "Select category")
category_menu.pack(side=tk.LEFT, padx=2)

# Text entry for new category
new_category_entry = tk.Entry(category_frame)
new_category_entry.pack(side=tk.LEFT, padx=2)

note_label = tk.Label(root, text="Note (optional):")
note_label.pack()
note_entry = tk.Entry(root)
note_entry.pack(pady=2)

# --- Filter Section ---
filter_label = tk.Label(root, text="Filter by Category:")
filter_label.pack()

filter_var = tk.StringVar()
filter_var.set("All")

filter_menu = tk.OptionMenu(root, filter_var, "All")
filter_menu.pack(pady=2)

# --- Expense Display ---
expense_list = tk.Text(root, height=12, width=45)
expense_list.pack(pady=10)

# --- Functions ---


def add_expense():
    amount = amount_entry.get()
    note = note_entry.get()
    date = datetime.date.today().isoformat()

    # Use new category if typed, otherwise use dropdown
    category = new_category_entry.get().strip() or category_var.get()

    if not amount or not category or category == "Select category":
        messagebox.showerror("Error", "Amount and Category are required.")
        return

    try:
        insert_expense(float(amount), category, note, date)
        messagebox.showinfo("Success", "Expense added successfully.")
        amount_entry.delete(0, tk.END)
        note_entry.delete(0, tk.END)
        new_category_entry.delete(0, tk.END)
        category_var.set("Select category")
        load_expenses()
        update_category_options()
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number.")


def load_expenses():
    expense_list.delete(1.0, tk.END)
    expenses = fetch_expenses()
    for exp in expenses:
        expense_list.insert(
            tk.END, f"{exp[4]} - {exp[1]}₺ | {exp[2]} | {exp[3]}\n")


def filter_expenses():
    keyword = filter_var.get()
    expense_list.delete(1.0, tk.END)
    expenses = fetch_expenses()
    for exp in expenses:
        if keyword == "All" or keyword.lower() == exp[2].lower():
            expense_list.insert(
                tk.END, f"{exp[4]} - {exp[1]}₺ | {exp[2]} | {exp[3]}\n")


def update_category_options():
    categories = list(set([exp[2] for exp in fetch_expenses()]))
    categories.sort()

    # Update dropdowns
    menu1 = category_menu["menu"]
    menu1.delete(0, "end")
    menu1.add_command(label="Select category",
                      command=lambda: category_var.set("Select category"))
    for cat in categories:
        menu1.add_command(label=cat, command=lambda c=cat: category_var.set(c))

    menu2 = filter_menu["menu"]
    menu2.delete(0, "end")
    menu2.add_command(label="All", command=lambda: filter_var.set("All"))
    for cat in categories:
        menu2.add_command(label=cat, command=lambda c=cat: filter_var.set(c))


# --- Buttons ---
add_button = tk.Button(root, text="Add Expense", command=add_expense)
add_button.pack(pady=10)

filter_button = tk.Button(root, text="Apply Filter", command=filter_expenses)
filter_button.pack(pady=5)

reset_button = tk.Button(root, text="Reset Filter", command=load_expenses)
reset_button.pack(pady=5)

# --- Load and Start ---
load_expenses()
update_category_options()
root.mainloop()
