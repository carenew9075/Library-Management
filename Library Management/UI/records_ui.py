import tkinter as tk
from tkinter import ttk, messagebox

from Modules.records import get_all_records, get_issued_records, get_returned_records
from UI.theme import *


# ---------------------------------------------------------
# CREATE RECORDS UI
# ---------------------------------------------------------

def create_records_ui(parent):
    clear_frame(parent)
    title_block(parent, "VIEW RECORDS", "Track issued and returned books")

    notebook = ttk.Notebook(parent)
    notebook.pack(fill="both", expand=True, padx=30, pady=(0, 30))

    tabs = {}
    for name in ["All", "Issued", "Returned"]:
        tab = tk.Frame(notebook, bg=BG)
        notebook.add(tab, text=name)
        tabs[name] = tab

    def build_table(tab, rows):
        for child in tab.winfo_children():
            child.destroy()

        tree = ttk.Treeview(
            tab,
            columns=("id", "book", "student", "issued", "due", "returned", "status"),
            show="headings"
        )

        headings = [
            ("id", "ID"),
            ("book", "Book"),
            ("student", "Student"),
            ("issued", "Issued On"),
            ("due", "Due Date"),
            ("returned", "Returned On"),
            ("status", "Status")
        ]

        for col, heading in headings:
            tree.heading(col, text=heading)
            tree.column(col, width=140, anchor="w")

        for row in rows:
            values = (
                row[0],
                str(row[1]) + " • " + str(row[2]),
                str(row[3]) + " • " + str(row[4]),
                row[5] or "-",
                row[6] or "-",
                row[7] or "-",
                row[8]
            )
            tree.insert("", "end", values=values)

        tree.pack(fill="both", expand=True, padx=12, pady=12)

    try:
        build_table(tabs["All"], get_all_records())
        build_table(tabs["Issued"], get_issued_records())
        build_table(tabs["Returned"], get_returned_records())
    except Exception as error:
        messagebox.showerror("Records", friendly_error(error))
