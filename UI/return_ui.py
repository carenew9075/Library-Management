import tkinter as tk
from tkinter import ttk, messagebox

from Modules.book_returned import return_book
from Database.queries import get_issued_books
from UI.theme import *


# ---------------------------------------------------------
# CREATE RETURN UI
# ---------------------------------------------------------

def create_return_ui(parent):
    clear_frame(parent)
    title_block(parent, "RETURN BOOKS", "Return an active library issue")

    main = tk.Frame(parent, bg=BG)
    main.pack(fill="both", expand=True, padx=30, pady=(0, 30))

    form = card(main, "RETURN BOOK")
    form.pack(fill="x")

    row = tk.Frame(form, bg=CARD)
    row.pack(fill="x", padx=18, pady=15)

    boxes = []
    for label in ["BOOK ID", "STUDENT ID"]:
        block = tk.Frame(row, bg=CARD)
        block.pack(side="left", fill="x", expand=True, padx=(0, 10))
        tk.Label(block, text=label, bg=CARD, fg=MUTED, font=("Consolas", 8, "bold")).pack(anchor="w")
        e = entry(block)
        e.pack(fill="x", pady=(5, 0), ipady=6)
        boxes.append(e)

    def return_book_action():
        book_id, student_id = [x.get().strip() for x in boxes]

        if not book_id.isdigit() or not student_id.isdigit():
            messagebox.showerror("Return Book", "Book ID and Student ID must be numbers.")
            return

        try:
            ok, text = return_book(int(book_id), int(student_id))
            messagebox.showinfo("Return Book", text)
            if ok:
                for box in boxes:
                    box.delete(0, "end")
                refresh()
        except Exception as error:
            messagebox.showerror("Return Book", friendly_error(error))

    button(row, "RETURN BOOK", return_book_action).pack(side="left", pady=(18, 0))

    table = card(main, "ACTIVE ISSUES")
    table.pack(fill="both", expand=True, pady=15)

    tree = ttk.Treeview(table, columns=("bookid", "title", "studentid", "student", "issued", "due"), show="headings")
    for col, heading, width in [
        ("bookid", "Book ID", 80),
        ("title", "Title", 220),
        ("studentid", "Student ID", 90),
        ("student", "Student", 180),
        ("issued", "Issued On", 110),
        ("due", "Due Date", 110)
    ]:
        tree.heading(col, text=heading)
        tree.column(col, width=width, anchor="w")
    tree.pack(fill="both", expand=True, padx=15, pady=15)

    def refresh():
        for item in tree.get_children():
            tree.delete(item)
        for row in get_issued_books():
            tree.insert("", "end", values=row[1:])

    try:
        refresh()
    except Exception as error:
        messagebox.showerror("Return Books", friendly_error(error))
