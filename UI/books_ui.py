import tkinter as tk
from tkinter import ttk, messagebox

from Modules.books import add_book, delete_book, search_book, view_all_books
from Utils.validation import non_negative_integer, required
from Utils.constant import EDUCATION_OPTIONS
from UI.theme import *


# ---------------------------------------------------------
# CREATE BOOKS UI
# ---------------------------------------------------------

def create_books_ui(parent):
    clear_frame(parent)
    title_block(parent, "BOOKS", "Manage library books and available copies")

    main = tk.Frame(parent, bg=BG)
    main.pack(fill="both", expand=True, padx=30, pady=(0, 30))

    form = card(main, "BOOK ENTRY")
    form.pack(fill="x")

    fields = tk.Frame(form, bg=CARD)
    fields.pack(fill="x", padx=18, pady=15)

    widgets = {}
    specs = [
        ("TITLE", 0),
        ("AUTHOR", 1),
        ("EDUCATION", 2),
        ("COPIES", 3)
    ]

    for label, index in specs:
        box = tk.Frame(fields, bg=CARD)
        box.grid(row=0, column=index, sticky="ew", padx=(0, 10))
        fields.columnconfigure(index, weight=1)
        tk.Label(box, text=label, bg=CARD, fg=MUTED, font=("Consolas", 8, "bold")).pack(anchor="w")

        if label == "EDUCATION":
            value = ttk.Combobox(box, values=EDUCATION_OPTIONS, state="readonly")
            value.set(EDUCATION_OPTIONS[0])
        else:
            value = entry(box)

        value.pack(fill="x", pady=(5, 0), ipady=6)
        widgets[label] = value

    def refresh():
        for item in tree.get_children():
            tree.delete(item)
        for row in view_all_books():
            tree.insert("", "end", values=row)

    def save():
        title = widgets["TITLE"].get()
        author = widgets["AUTHOR"].get()
        education = widgets["EDUCATION"].get()
        copies = widgets["COPIES"].get()

        if not required(title) or not required(author):
            messagebox.showerror("Book", "Title and author are required.")
            return

        if not non_negative_integer(copies):
            messagebox.showerror("Book", "Copies must be a whole number 0 or greater.")
            return

        try:
            add_book(title, author, education, int(copies))
            messagebox.showinfo("Book", "Book added successfully.")
            widgets["TITLE"].delete(0, "end")
            widgets["AUTHOR"].delete(0, "end")
            widgets["COPIES"].delete(0, "end")
            refresh()
        except Exception as error:
            messagebox.showerror("Book", friendly_error(error))

    button(fields, "ADD BOOK", save).grid(row=1, column=0, sticky="w", pady=(12, 0))

    search_card = card(main, "SEARCH / DELETE")
    search_card.pack(fill="x", pady=15)

    row = tk.Frame(search_card, bg=CARD)
    row.pack(fill="x", padx=18, pady=15)

    tk.Label(row, text="SEARCH BY ID", bg=CARD, fg=MUTED, font=("Consolas", 8, "bold")).pack(side="left")
    search_box = entry(row)
    search_box.pack(side="left", padx=10, ipady=6)

    result_label = tk.Label(row, text="", bg=CARD, fg=TEXT, font=("Segoe UI", 9))
    result_label.pack(side="left", padx=15)

    def search():
        value = search_box.get().strip()
        if not value.isdigit():
            result_label.config(text="Enter a valid Book ID.", fg=RED)
            return
        try:
            row = search_book(int(value))
            if row:
                result_label.config(text=str(row), fg=TEXT)
            else:
                result_label.config(text="Book not found.", fg=RED)
        except Exception as error:
            result_label.config(text=friendly_error(error), fg=RED)

    def remove():
        value = search_box.get().strip()
        if not value.isdigit():
            return
        if not messagebox.askyesno("Delete Book", "Delete this book? This cannot be undone."):
            return
        try:
            ok, text = delete_book(int(value))
            messagebox.showinfo("Book", text)
            if ok:
                refresh()
        except Exception as error:
            messagebox.showerror("Book", friendly_error(error))

    button(row, "SEARCH", search).pack(side="left")
    button(row, "DELETE", remove, danger=True).pack(side="left", padx=8)

    table = card(main, "BOOKS")
    table.pack(fill="both", expand=True)

    tree = ttk.Treeview(table, columns=("id", "title", "author", "education", "copies"), show="headings")
    for col, heading, width in [
        ("id", "Book ID", 80),
        ("title", "Title", 250),
        ("author", "Author", 210),
        ("education", "Education", 160),
        ("copies", "Copies Available", 130)
    ]:
        tree.heading(col, text=heading)
        tree.column(col, width=width, anchor="w")
    tree.pack(fill="both", expand=True, padx=15, pady=15)

    try:
        refresh()
    except Exception as error:
        messagebox.showerror("Books", friendly_error(error))
