import tkinter as tk
from tkinter import ttk, messagebox

from Modules.students import register_student, view_all_students
from Utils.validation import phone, required
from UI.theme import *


# ---------------------------------------------------------
# CREATE STUDENTS UI
# ---------------------------------------------------------

def create_students_ui(parent):
    clear_frame(parent)
    title_block(parent, "STUDENTS", "Register and manage library students")

    main = tk.Frame(parent, bg=BG)
    main.pack(fill="both", expand=True, padx=30, pady=(0, 30))

    form = card(main, "REGISTER STUDENT")
    form.pack(fill="x")

    row = tk.Frame(form, bg=CARD)
    row.pack(fill="x", padx=18, pady=15)

    fields = []
    for label in ["FULL NAME", "CLASS / SECTION", "PHONE NUMBER"]:
        block = tk.Frame(row, bg=CARD)
        block.pack(side="left", fill="x", expand=True, padx=(0, 10))
        tk.Label(block, text=label, bg=CARD, fg=MUTED, font=("Consolas", 8, "bold")).pack(anchor="w")
        e = entry(block)
        e.pack(fill="x", pady=(5, 0), ipady=6)
        fields.append(e)

    def save():
        name, class_section, phone_number = [x.get().strip() for x in fields]

        if not required(name) or not required(class_section):
            messagebox.showerror("Student", "Name and class/section are required.")
            return

        if not phone(phone_number):
            messagebox.showerror("Student", "Phone number must contain exactly 10 digits.")
            return

        try:
            register_student(name, class_section, phone_number)
            messagebox.showinfo("Student", "Student registered successfully.")
            for e in fields:
                e.delete(0, "end")
            refresh()
        except Exception as error:
            messagebox.showerror("Student", friendly_error(error))

    button(row, "REGISTER STUDENT", save).pack(side="left", pady=(18, 0))

    table = card(main, "STUDENTS")
    table.pack(fill="both", expand=True, pady=15)

    tree = ttk.Treeview(table, columns=("id", "name", "class", "phone"), show="headings")
    for col, heading, width in [
        ("id", "Student ID", 90),
        ("name", "Name", 250),
        ("class", "Class", 160),
        ("phone", "Phone", 160)
    ]:
        tree.heading(col, text=heading)
        tree.column(col, width=width, anchor="w")
    tree.pack(fill="both", expand=True, padx=15, pady=15)

    def refresh():
        for item in tree.get_children():
            tree.delete(item)
        for row in view_all_students():
            tree.insert("", "end", values=row)

    try:
        refresh()
    except Exception as error:
        messagebox.showerror("Students", friendly_error(error))
