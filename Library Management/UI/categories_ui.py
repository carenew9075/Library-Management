import tkinter as tk
from tkinter import ttk, messagebox

from Modules.categories import add_category, delete_category, view_all_categories
from UI.theme import *


# ---------------------------------------------------------
# CREATE CATEGORIES UI
# ---------------------------------------------------------

def create_categories_ui(parent):
    clear_frame(parent)
    title_block(parent, "CATEGORIES", "Manage optional book categories")

    form = card(parent, "ADD CATEGORY")
    form.pack(fill="x", padx=30)

    row = tk.Frame(form, bg=CARD)
    row.pack(fill="x", padx=18, pady=15)
    box = entry(row)
    box.pack(side="left", fill="x", expand=True, ipady=7)

    table = card(parent, "CATEGORIES")
    table.pack(fill="both", expand=True, padx=30, pady=15)

    tree = ttk.Treeview(table, columns=("id", "name"), show="headings")
    tree.heading("id", text="ID")
    tree.heading("name", text="Category")
    tree.column("id", width=90)
    tree.column("name", width=300)
    tree.pack(fill="both", expand=True, padx=15, pady=15)

    def refresh():
        for item in tree.get_children():
            tree.delete(item)
        for row in view_all_categories():
            tree.insert("", "end", values=row)

    def save():
        value = box.get().strip()
        if not value:
            return
        try:
            add_category(value)
            box.delete(0, "end")
            refresh()
        except Exception as error:
            messagebox.showerror("Category", friendly_error(error))

    def remove():
        selected = tree.selection()
        if not selected:
            return
        category_id = tree.item(selected[0])["values"][0]
        try:
            delete_category(category_id)
            refresh()
        except Exception as error:
            messagebox.showerror("Category", friendly_error(error))

    button(row, "ADD", save).pack(side="left", padx=10)
    button(row, "DELETE SELECTED", remove, danger=True).pack(side="left")

    try:
        refresh()
    except Exception as error:
        messagebox.showerror("Categories", friendly_error(error))
