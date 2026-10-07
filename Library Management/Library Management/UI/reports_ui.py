import tkinter as tk
from tkinter import ttk, messagebox

from Modules.reports import get_report_summary, get_most_issued_books
from UI.theme import *


# ---------------------------------------------------------
# CREATE REPORTS UI
# ---------------------------------------------------------

def create_reports_ui(parent):
    clear_frame(parent)
    title_block(parent, "LIBRARY REPORTS", "Summary of library activity")

    main = tk.Frame(parent, bg=BG)
    main.pack(fill="both", expand=True, padx=30, pady=(0, 30))

    try:
        summary = get_report_summary()
    except Exception as error:
        messagebox.showerror("Reports", friendly_error(error))
        summary = (0, 0, 0, 0, 0, 0)

    names = ["BOOK TITLES", "TOTAL COPIES", "STUDENTS", "ISSUED", "RETURNED", "AVAILABLE"]
    stats = tk.Frame(main, bg=BG)
    stats.pack(fill="x")

    for index, value in enumerate(summary):
        stats.columnconfigure(index, weight=1)
        c = card(stats)
        c.grid(row=0, column=index, sticky="nsew", padx=(0 if index == 0 else 6, 0))
        tk.Label(c, text=names[index], bg=CARD, fg=MUTED, font=("Consolas", 8, "bold")).pack(anchor="w", padx=15, pady=(12, 4))
        tk.Label(c, text=str(value), bg=CARD, fg=TEXT, font=("Segoe UI", 18, "bold")).pack(anchor="w", padx=15, pady=(0, 12))

    table = card(main, "MOST ISSUED BOOKS")
    table.pack(fill="both", expand=True, pady=15)

    tree = ttk.Treeview(table, columns=("id", "title", "count"), show="headings")
    for col, heading in [("id", "Book ID"), ("title", "Title"), ("count", "Issue Count")]:
        tree.heading(col, text=heading)
        tree.column(col, width=220, anchor="w")
    tree.pack(fill="both", expand=True, padx=15, pady=15)

    try:
        for row in get_most_issued_books():
            tree.insert("", "end", values=row)
    except Exception:
        pass
