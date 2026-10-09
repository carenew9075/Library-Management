# ---------------------------------------------------------
# MAIN WINDOW
# CustomTkinter screens. Database calls stay in Modules.
# ---------------------------------------------------------

import os
from datetime import datetime
from tkinter import messagebox, ttk
import tkinter as tk

import customtkinter as ctk
from PIL import Image

from Database import queries
from Modules.books import add_book, delete_book, view_all_books, add_many_books, update_book
from Modules.bookselection import search_book_by_title
from Modules.students import register_student, view_all_students, update_student, delete_student
from Modules.book_issued import issue_book, view_issued_books
from Modules.book_returned import return_book
from Modules.dashboard import get_dashboard_data, get_recent_activities
from Modules.library_ai import ask_gemini
from UI.look import *


class LibraryApp(ctk.CTk):

    def __init__(self, user_name):
        super().__init__(fg_color=BG)
        ctk.set_appearance_mode("dark")
        self.user_name = user_name
        self.title("Library Management System")
        self.geometry("1280x780")
        self.minsize(1100, 700)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.build_topbar()
        self.build_sidebar()
        self.build_pages()
        self.build_ai()
        self.build_statusbar()
        self.show_page("home")

    # -----------------------------------------------------
    # TOP BAR
    # -----------------------------------------------------

    def build_topbar(self):
        bar = ctk.CTkFrame(self, fg_color=SIDEBAR, height=64, corner_radius=0)
        bar.grid(row=0, column=0, columnspan=3, sticky="ew")
        bar.grid_propagate(False)
        ctk.CTkLabel(bar, text="Library Management System", font=font(17, "bold"), text_color=TEXT).pack(side="left", padx=(18, 8))
        ctk.CTkLabel(bar, text="Read  •  Learn  •  Grow", font=font(10), text_color=BLUE).pack(side="left")
        ctk.CTkLabel(bar, text=self.user_name[:1].upper(), width=36, height=36, corner_radius=18, fg_color=PRIMARY, font=font(14, "bold")).pack(side="right", padx=(8, 18))
        who = ctk.CTkFrame(bar, fg_color="transparent")
        who.pack(side="right")
        ctk.CTkLabel(who, text="Welcome, " + self.user_name, font=font(12, "bold"), text_color=TEXT).pack(anchor="e")
        ctk.CTkLabel(who, text="Admin", font=font(9), text_color=MUTED).pack(anchor="e")

    # -----------------------------------------------------
    # SIDEBAR
    # -----------------------------------------------------

    def build_sidebar(self):
        side = ctk.CTkFrame(self, fg_color=SIDEBAR, width=210, corner_radius=0)
        side.grid(row=1, column=0, sticky="ns")
        side.grid_propagate(False)
        ctk.CTkButton(side, text="Logout", height=42, fg_color="transparent", text_color=TEXT, command=self.logout).pack(side="bottom", fill="x", padx=12, pady=16)
        self.nav_buttons = {}
        pages = [
            ("home", "Home"),
            ("books", "Books"),
            ("students", "Students"),
            ("issue", "Issue Book"),
            ("return", "Return Book"),
            ("records", "View Records"),
            ("settings", "Settings")
        ]
        icons = {
            "home": "H",
            "books": "B",
            "students": "S",
            "issue": "I",
            "return": "R",
            "records": "V",
            "settings": "G"
        }
        for key, label in pages:
            button = ctk.CTkButton(
                side,
                text="  " + icons[key] + "    " + label,
                anchor="w",
                height=42,
                corner_radius=10,
                fg_color="transparent",
                hover_color=CARD_HOVER,
                text_color=TEXT,
                command=lambda page=key: self.show_page(page)
            )
            button.pack(fill="x", padx=12, pady=3)
            self.nav_buttons[key] = button

    # -----------------------------------------------------
    # PAGES
    # -----------------------------------------------------

    def build_pages(self):
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.grid(row=1, column=1, sticky="nsew", padx=14, pady=12)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.pages = {
            "home": HomePage(self.container, self),
            "books": BooksPage(self.container),
            "students": StudentsPage(self.container),
            "issue": IssuePage(self.container),
            "return": ReturnPage(self.container),
            "records": RecordsPage(self.container),
            "settings": SettingsPage(self.container)
        }
        for page in self.pages.values():
            page.grid(row=0, column=0, sticky="nsew")

    def show_page(self, name):
        page = self.pages[name]
        page.refresh()
        page.tkraise()
        for key, button in self.nav_buttons.items():
            if key == name:
                button.configure(fg_color=PRIMARY, text_color="white")
            else:
                button.configure(fg_color="transparent", text_color=TEXT)

    # -----------------------------------------------------
    # AI PANEL
    # -----------------------------------------------------

    def build_ai(self):
        panel = ctk.CTkFrame(self, width=300, fg_color=SIDEBAR, border_color=BORDER, border_width=1, corner_radius=12)
        panel.grid(row=1, column=2, sticky="ns", padx=(0, 12), pady=12)
        panel.grid_propagate(False)
        ctk.CTkLabel(panel, text="AI Assistant", font=font(14, "bold"), text_color=TEXT).pack(anchor="w", padx=14, pady=(14, 0))
        ctk.CTkLabel(panel, text="Powered by Gemini", font=font(9), text_color=BLUE).pack(anchor="w", padx=14)
        self.chat = ctk.CTkTextbox(panel, fg_color=CARD, text_color=TEXT)
        self.chat.pack(fill="both", expand=True, padx=12, pady=10)
        self.chat.insert(
            "end",
            "Hi " + self.user_name + ".\n"
            "Ask about books or students.\n\n"
            "Try:\n"
            "Which books are available?\n"
            "How many students are there?\n"
        )
        self.chat.configure(state="disabled")
        row = ctk.CTkFrame(panel, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=(0, 12))
        self.question = entry(row, "Ask me anything...", 190)
        self.question.pack(side="left")
        button(row, "Ask", self.ask, width=60).pack(side="left", padx=6)

    def logout(self):
        from Config import config
        path = config.PROJECT_ROOT / "session.txt"
        if path.exists():
            path.unlink()
        self.destroy()

    def ask(self):
        text = self.question.get().strip()
        if text == "":
            return
        self.question.delete(0, "end")
        answer = ask_gemini(text)
        self.chat.configure(state="normal")
        self.chat.insert("end", "\nYou: " + text + "\n" + answer + "\n")
        self.chat.configure(state="disabled")

    # -----------------------------------------------------
    # STATUS BAR
    # -----------------------------------------------------

    def build_statusbar(self):
        bar = ctk.CTkFrame(self, fg_color=SIDEBAR, height=30, corner_radius=0)
        bar.grid(row=2, column=0, columnspan=3, sticky="ew")
        ctk.CTkLabel(bar, text="Connected to database", font=font(10), text_color=GREEN).pack(side="left", padx=16)
        self.clock = ctk.CTkLabel(bar, text="", font=font(10), text_color=MUTED)
        self.clock.pack(side="right", padx=16)
        self.tick()

    def tick(self):
        self.clock.configure(text=datetime.now().strftime("%d %b %Y   |   %H:%M"))
        self.after(10000, self.tick)


# ---------------------------------------------------------
# HOME
# ---------------------------------------------------------

class HomePage(ctk.CTkFrame):

    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.build_banner()
        ctk.CTkLabel(self, text="Quick Access", font=font(15, "bold"), text_color=TEXT).grid(row=1, column=0, sticky="w", pady=(12, 4))
        items = [
            ("+", "Add Book", "Add a new book to the library.", "books", PURPLE),
            ("S", "Search Book", "Find books by title or category.", "books", TEAL),
            ("B", "View All Books", "See all available books.", "books", PRIMARY),
            ("U", "Register Student", "Add a new student.", "students", ORANGE),
            ("I", "Issue Book", "Issue a book to a student.", "issue", RED),
            ("R", "Return Book", "Mark a book as returned.", "return", GREEN)
        ]
        for index, item in enumerate(items):
            self.make_card(index, item)
        self.build_stats()
        self.build_activity()

    # ---------------------------------------------------------
    # BANNER
    # ---------------------------------------------------------

    def build_banner(self):
        banner = card(self)
        banner.grid(row=0, column=0, columnspan=3, sticky="ew")
        banner.configure(height=140)
        banner.grid_propagate(False)
        image_path = os.path.join("assets", "banner.png")
        if os.path.exists(image_path):
            self.photo = ctk.CTkImage(Image.open(image_path), size=(980, 140))
            picture = ctk.CTkLabel(banner, text="", image=self.photo)
            picture.place(relx=0, rely=0, relwidth=1, relheight=1)
        ctk.CTkLabel(banner, text="Welcome to", font=font(16), text_color=TEXT, fg_color="#070d1a").place(x=24, y=24)
        ctk.CTkLabel(banner, text="Library Management System", font=font(26, "bold"), text_color=BLUE, fg_color="#070d1a").place(x=24, y=52)
        ctk.CTkLabel(banner, text='"A library is a hospital for the mind."  — Anonymous', font=font(11), text_color=MUTED, fg_color="#070d1a").place(x=24, y=96)

    # ---------------------------------------------------------
    # QUICK CARD
    # ---------------------------------------------------------

    def make_card(self, index, item):
        icon, name, detail, page, color = item
        box = ctk.CTkFrame(self, fg_color=CARD, border_color=BORDER, border_width=1, corner_radius=12, cursor="hand2", height=110)
        box.grid(row=2 + index // 3, column=index % 3, padx=5, pady=5, sticky="ew")
        box.grid_propagate(False)
        ctk.CTkLabel(box, text=icon, width=36, height=36, corner_radius=8, fg_color=color, font=font(16, "bold")).place(x=14, y=14)
        ctk.CTkLabel(box, text=">", width=26, height=26, corner_radius=13, fg_color=CARD_HOVER, text_color=TEXT).place(relx=1, x=-36, y=14)
        ctk.CTkLabel(box, text=name, font=font(13, "bold"), text_color=TEXT).place(x=14, y=58)
        ctk.CTkLabel(box, text=detail, font=font(10), text_color=MUTED).place(x=14, y=80)
        box.bind("<Button-1>", lambda event, target=page: self.app.show_page(target))

    # ---------------------------------------------------------
    # STATS
    # ---------------------------------------------------------

    def build_stats(self):
        stats = card(self)
        stats.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(10, 0), padx=(0, 6))
        ctk.CTkLabel(stats, text="Library Stats", font=font(13, "bold"), text_color=TEXT).grid(row=0, column=0, columnspan=2, sticky="w", padx=14, pady=(12, 6))
        self.stat_labels = {}
        names = ["Total Books", "Total Students", "Issued Books", "Available Books"]
        for index, name in enumerate(names):
            tile = ctk.CTkFrame(stats, fg_color=BG, corner_radius=10)
            tile.grid(row=1 + index // 2, column=index % 2, padx=10, pady=6, sticky="ew")
            ctk.CTkLabel(tile, text=name, font=font(10), text_color=MUTED).pack(anchor="w", padx=10, pady=(8, 0))
            label = ctk.CTkLabel(tile, text="0", font=font(18, "bold"), text_color=TEXT)
            label.pack(anchor="w", padx=10, pady=(0, 8))
            self.stat_labels[name] = label
        stats.grid_columnconfigure((0, 1), weight=1)

    # ---------------------------------------------------------
    # ACTIVITY
    # ---------------------------------------------------------

    def build_activity(self):
        self.activity = card(self)
        self.activity.grid(row=4, column=2, sticky="nsew", pady=(10, 0))
        ctk.CTkLabel(self.activity, text="Recent Activity", font=font(13, "bold"), text_color=TEXT).pack(anchor="w", padx=14, pady=(12, 6))
        self.activity_text = ctk.CTkLabel(self.activity, text="No activity yet", font=font(11), text_color=MUTED, justify="left")
        self.activity_text.pack(anchor="w", padx=14, pady=6)

    # ---------------------------------------------------------
    # REFRESH
    # ---------------------------------------------------------

    def refresh(self):
        try:
            books, students, issued, available = get_dashboard_data()
            self.stat_labels["Total Books"].configure(text=str(books))
            self.stat_labels["Total Students"].configure(text=str(students))
            self.stat_labels["Issued Books"].configure(text=str(issued))
            self.stat_labels["Available Books"].configure(text=str(available))
            rows = get_recent_activities()
            if len(rows) == 0:
                self.activity_text.configure(text="No activity yet")
            else:
                lines = []
                for book_id, title, student, issued_on in rows:
                    lines.append("Issued " + str(title) + " to " + str(student))
                self.activity_text.configure(text="\n".join(lines))
        except Exception:
            self.activity_text.configure(text="Stats could not be loaded.")


# ---------------------------------------------------------
# BOOKS
# ---------------------------------------------------------

class BooksPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        ctk.CTkLabel(self, text="Books", font=font(22, "bold"), text_color=TEXT).pack(anchor="w")
        form = card(self)
        form.pack(fill="x", pady=10)
        self.code_box = entry(form, "Book code, like B001", 160)
        self.title_box = entry(form, "Book title", 180)
        self.author_box = entry(form, "Author", 160)
        self.category_box = entry(form, "Category", 140)
        self.copies_box = entry(form, "Copies", 80)
        self.code_box.grid(row=0, column=0, padx=10, pady=12)
        self.title_box.grid(row=0, column=1, padx=6, pady=12)
        self.author_box.grid(row=0, column=2, padx=6, pady=12)
        self.category_box.grid(row=1, column=0, padx=10, pady=12)
        self.copies_box.grid(row=1, column=1, padx=6, pady=12, sticky="w")
        button(form, "Add Book", self.add).grid(row=0, column=3, rowspan=2, padx=10)
        button(form, "Update", self.update).grid(row=0, column=4, rowspan=2, padx=6)
        bar = ctk.CTkFrame(self, fg_color="transparent")
        bar.pack(fill="x")
        self.search_box = entry(bar, "Search by title", 260)
        self.search_box.pack(side="left")
        button(bar, "Search", self.refresh).pack(side="left", padx=8)
        button(bar, "Import CSV", self.import_csv).pack(side="left", padx=8)
        button(bar, "Delete", self.delete, RED, 80).pack(side="right")
        self.tree = make_table(self, ["Book ID", "Title", "Author", "Category", "Copies"], [80, 220, 180, 140, 80])
        self.tree.bind("<<TreeviewSelect>>", self.fill_form)

    def add(self):
        code = self.code_box.get().strip()
        title = self.title_box.get().strip()
        author = self.author_box.get().strip()
        category = self.category_box.get().strip()
        copies = self.copies_box.get().strip()
        if code == "" or title == "" or author == "" or category == "" or copies.isdigit() == False:
            messagebox.showwarning("Books", "Enter a book code, title, author, category, and copies.")
            return
        try:
            add_book(code, title, author, category, int(copies))
            self.refresh()
        except Exception:
            messagebox.showerror("Books", "The book could not be saved. That book code may already exist.")

    def fill_form(self, event):
        selected = self.tree.selection()
        if len(selected) == 0:
            return
        code, title, author, category, copies = self.tree.item(selected[0])["values"]
        self.set_box(self.code_box, code)
        self.set_box(self.title_box, title)
        self.set_box(self.author_box, author)
        self.set_box(self.category_box, category)
        self.set_box(self.copies_box, copies)

    def set_box(self, box, value):
        box.delete(0, "end")
        box.insert(0, str(value))

    def update(self):
        code = self.code_box.get().strip()
        title = self.title_box.get().strip()
        author = self.author_box.get().strip()
        category = self.category_box.get().strip()
        copies = self.copies_box.get().strip()
        if code == "" or title == "" or author == "" or category == "" or copies.isdigit() == False:
            messagebox.showwarning("Books", "Click a row, then fill code, title, author, category, and copies.")
            return
        if update_book(code, title, author, category, int(copies)) == False:
            messagebox.showerror("Books", "That book code was not found.")
            return
        self.refresh()

    def import_csv(self):
        from tkinter import filedialog
        import csv
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if path == "":
            return
        rows = []
        file = open(path, encoding="utf-8-sig")
        reader = csv.reader(file)
        next(reader, None)
        for line in reader:
            if len(line) < 5 or line[4].strip().isdigit() == False:
                continue
            rows.append((line[0].strip(), line[1].strip(), line[2].strip(), line[3].strip(), int(line[4])))
        file.close()
        saved, skipped = add_many_books(rows)
        messagebox.showinfo("Books", "Saved " + str(saved) + ". Skipped " + str(skipped) + ".")
        self.refresh()

    def delete(self):
        selected = self.tree.selection()
        if len(selected) == 0:
            return
        book_id = self.tree.item(selected[0])["values"][0]
        ok, text = delete_book(book_id)
        messagebox.showinfo("Books", text)
        self.refresh()

    def refresh(self):
        word = self.search_box.get().strip()
        if word == "":
            rows = view_all_books()
        else:
            rows = search_book_by_title(word)
        fill_table(self.tree, rows)


# ---------------------------------------------------------
# STUDENTS
# ---------------------------------------------------------

class StudentsPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        ctk.CTkLabel(self, text="Students", font=font(22, "bold"), text_color=TEXT).pack(anchor="w")
        form = card(self)
        form.pack(fill="x", pady=10)
        self.selected_id = None
        self.id_box = entry(form, "Student code, like ST004", 180)
        self.name_box = entry(form, "Full name", 180)
        self.class_box = entry(form, "Class", 100)
        self.phone_box = entry(form, "Phone", 130)
        self.id_box.pack(side="left", padx=10, pady=12)
        self.name_box.pack(side="left", padx=6, pady=12)
        self.class_box.pack(side="left", padx=6, pady=12)
        self.phone_box.pack(side="left", padx=6, pady=12)
        button(form, "Register", self.save).pack(side="left", padx=6)
        button(form, "Update", self.update).pack(side="left", padx=6)
        button(form, "Delete", self.delete, RED, 90).pack(side="left", padx=6)
        self.picked = ctk.CTkLabel(self, text="Click a row to edit it.", text_color=MUTED)
        self.picked.pack(anchor="w")
        self.tree = make_table(self, ["Student ID", "Name", "Class", "Phone"], [90, 220, 120, 140])
        self.tree.bind("<<TreeviewSelect>>", self.fill_form)

    def fill_form(self, event):
        selected = self.tree.selection()
        if len(selected) == 0:
            return
        student_id, name, class_name, phone = self.tree.item(selected[0])["values"]
        self.selected_id = student_id
        self.set_box(self.name_box, name)
        self.set_box(self.class_box, class_name)
        self.set_box(self.phone_box, phone)
        self.picked.configure(text="Editing student " + str(student_id))

    def set_box(self, box, value):
        box.delete(0, "end")
        box.insert(0, str(value))

    def save(self):
        code = self.id_box.get().strip()
        name = self.name_box.get().strip()
        class_name = self.class_box.get().strip()
        phone = self.phone_box.get().strip()
        if code == "" or name == "" or class_name == "" or len(phone) != 10:
            messagebox.showwarning("Students", "Enter a student code, name, class, and a 10 digit phone number.")
            return
        try:
            register_student(code, name, class_name, phone)
            self.refresh()
        except Exception:
            messagebox.showerror("Students", "The student could not be saved. That student code may already exist, or the old table still expects a number ID. Use a new database name in .env if this keeps failing.")

    def update(self):
        if self.selected_id is None:
            messagebox.showwarning("Students", "Click a student row first.")
            return
        name = self.name_box.get().strip()
        class_name = self.class_box.get().strip()
        phone = self.phone_box.get().strip()
        if name == "" or class_name == "" or len(phone) != 10:
            messagebox.showwarning("Students", "Name, class, and a 10 digit phone number are required.")
            return
        update_student(self.selected_id, name, class_name, phone)
        self.refresh()

    def delete(self):
        if self.selected_id is None:
            messagebox.showwarning("Students", "Click a student row first.")
            return
        ok = messagebox.askyesno("Delete student", "Do you want to delete this student?")
        if ok == False:
            return
        delete_student(self.selected_id)
        self.selected_id = None
        self.picked.configure(text="Click a row to edit it.")
        self.refresh()

    def refresh(self):
        fill_table(self.tree, view_all_students())


# ---------------------------------------------------------
# ISSUE AND RETURN
# ---------------------------------------------------------

class IssuePage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        ctk.CTkLabel(self, text="Issue Book", font=font(22, "bold"), text_color=TEXT).pack(anchor="w")
        form = card(self)
        form.pack(fill="x", pady=10)
        self.book_box = entry(form, "Book code", 120)
        self.student_box = entry(form, "Student code", 120)
        self.book_box.pack(side="left", padx=10, pady=12)
        self.student_box.pack(side="left", padx=6, pady=12)
        self.day_box, self.month_box, self.year_box = date_blocks(form)
        button(form, "Issue", self.save).pack(side="left", padx=10)
        self.note = ctk.CTkLabel(self, text="", text_color=MUTED)
        self.note.pack(anchor="w")

    def save(self):
        book_id = self.book_box.get().strip()
        student_id = self.student_box.get().strip()
        day = self.day_box.get().strip()
        month = self.month_box.get().strip()
        year = self.year_box.get().strip()
        if book_id == "" or student_id == "" or day == "" or month == "" or year == "":
            messagebox.showwarning("Issue", "Enter the book code, student code, day, month, and year.")
            return
        try:
            ok, text = issue_book(book_id, student_id, make_due(day, month, year))
            if ok:
                messagebox.showinfo("Issue", text)
            else:
                messagebox.showerror("Issue", text)
        except Exception as error:
            messagebox.showerror("Issue", "Use day, month, and year as 18, 10, and 2026. " + str(error))

    def refresh(self):
        self.note.configure(text="Use the book ID and student ID from the tables.")


class ReturnPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        ctk.CTkLabel(self, text="Return Book", font=font(22, "bold"), text_color=TEXT).pack(anchor="w")
        form = card(self)
        form.pack(fill="x", pady=10)
        self.book_box = entry(form, "Book ID", 120)
        self.student_box = entry(form, "Student ID", 120)
        self.book_box.pack(side="left", padx=10, pady=12)
        self.student_box.pack(side="left", padx=6, pady=12)
        button(form, "Return", self.save).pack(side="left", padx=10)
        self.tree = make_table(self, ["Issue", "Book", "Title", "Student ID", "Student", "Issued", "Due"], [60, 60, 180, 80, 140, 100, 100])

    def save(self):
        book_id = self.book_box.get().strip()
        student_id = self.student_box.get().strip()
        if book_id == "" or student_id == "":
            return
        ok, text = return_book(book_id, student_id)
        messagebox.showinfo("Return", text)
        self.refresh()

    def refresh(self):
        try:
            fill_table(self.tree, view_issued_books())
        except Exception:
            fill_table(self.tree, [])


# ---------------------------------------------------------
# RECORDS AND SETTINGS
# ---------------------------------------------------------

class RecordsPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        ctk.CTkLabel(self, text="View Records", font=font(22, "bold"), text_color=TEXT).pack(anchor="w")
        self.tree = make_table(self, ["ID", "Book", "Title", "Student ID", "Student", "Issued", "Due", "Returned", "Status"], [70, 60, 160, 80, 140, 90, 90, 90, 80])

    def refresh(self):
        try:
            fill_table(self.tree, queries.get_all_records())
        except Exception:
            messagebox.showerror("Records", "Records could not be loaded. Check the Students table columns.")


class SettingsPage(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        ctk.CTkLabel(self, text="Settings", font=font(22, "bold"), text_color=TEXT).pack(anchor="w")
        sql = card(self)
        sql.pack(fill="x", pady=10)
        ctk.CTkLabel(sql, text="MySQL", text_color=MUTED).pack(anchor="w", padx=14, pady=(12, 4))
        self.sql_status = ctk.CTkLabel(sql, text="Leave blank to use this computer's own database.", text_color=TEXT)
        self.sql_status.pack(anchor="w", padx=14, pady=6)
        from Config import config
        self.host_box = entry(sql, "Host", 220)
        self.user_box = entry(sql, "User", 160)
        self.password_box = entry(sql, "Password", 160)
        self.database_box = entry(sql, "Database name", 180)
        self.host_box.insert(0, config.DB_HOST)
        self.user_box.insert(0, config.DB_USER)
        self.password_box.insert(0, config.DB_PASSWORD)
        self.database_box.insert(0, config.DB_NAME)
        self.password_box.configure(show="*")
        self.host_box.pack(anchor="w", padx=14, pady=4)
        self.user_box.pack(anchor="w", padx=14, pady=4)
        self.password_box.pack(anchor="w", padx=14, pady=4)
        self.database_box.pack(anchor="w", padx=14, pady=4)
        button(sql, "Save server", self.save_server).pack(anchor="w", padx=14, pady=(8, 4))
        button(sql, "Test connection", self.test_sql).pack(anchor="w", padx=14, pady=(0, 8))
        ctk.CTkLabel(sql, text="Paste SQL", text_color=MUTED).pack(anchor="w", padx=14)
        self.sql_box = ctk.CTkTextbox(sql, height=90)
        self.sql_box.pack(fill="x", padx=14, pady=6)
        button(sql, "Run SQL", self.run_pasted_sql).pack(anchor="w", padx=14, pady=(0, 14))
        box = card(self)
        box.pack(fill="x", pady=10)
        ctk.CTkLabel(box, text="Gemini API key", text_color=MUTED).pack(anchor="w", padx=14, pady=(12, 4))
        self.key_box = entry(box, "API key", 320)
        self.key_box.pack(anchor="w", padx=14, pady=(0, 12))
        button(box, "Save key", self.save).pack(anchor="w", padx=14, pady=(0, 14))

    def save_server(self):
        from Config import config
        host = self.host_box.get().strip() or "localhost"
        user = self.user_box.get().strip() or "root"
        password = self.password_box.get()
        database = self.database_box.get().strip() or "library_management"
        lines = [
            "DB_HOST=" + host,
            "DB_USER=" + user,
            "DB_PASSWORD=" + password,
            "DB_NAME=" + database,
            "GEMINI_API_KEY=" + config.GEMINI_API_KEY,
            "GEMINI_MODEL=" + config.GEMINI_MODEL
        ]
        file = open(config.ENV_FILE, "w", encoding="utf-8")
        file.write("\n".join(lines) + "\n")
        file.close()
        config.reload_environment()
        self.sql_status.configure(text="Saved. The program creates " + database + " if it is missing.")

    def test_sql(self):
        from Database.database import test_connection
        ok, message = test_connection()
        self.sql_status.configure(text=message)

    def run_pasted_sql(self):
        from Modules.run_sql import run_sql
        statement = self.sql_box.get("1.0", "end").strip()
        if statement == "":
            self.sql_status.configure(text="Paste a statement first.")
            return
        try:
            self.sql_status.configure(text=run_sql(statement))
        except Exception as error:
            self.sql_status.configure(text=str(error))

    def save(self):
        from Config import config
        key = self.key_box.get().strip()
        lines = [
            "DB_HOST=" + config.DB_HOST,
            "DB_USER=" + config.DB_USER,
            "DB_PASSWORD=" + config.DB_PASSWORD,
            "DB_NAME=" + config.DB_NAME,
            "GEMINI_API_KEY=" + key,
            "GEMINI_MODEL=" + config.GEMINI_MODEL
        ]
        file = open(config.ENV_FILE, "w", encoding="utf-8")
        file.write("\n".join(lines) + "\n")
        file.close()
        config.reload_environment()
        messagebox.showinfo("Settings", "Key saved on this computer only.")

    def refresh(self):
        pass


# ---------------------------------------------------------
# TABLE HELPER
# ---------------------------------------------------------

def make_table(parent, headings, widths):
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background=CARD, fieldbackground=CARD, foreground=TEXT, rowheight=30, borderwidth=0)
    style.configure("Treeview.Heading", background=SIDEBAR, foreground=BLUE, relief="flat")
    frame = tk.Frame(parent, bg=CARD)
    frame.pack(fill="both", expand=True, pady=10)
    tree = ttk.Treeview(frame, columns=headings, show="headings")
    for heading, width in zip(headings, widths):
        tree.heading(heading, text=heading)
        tree.column(heading, width=width, anchor="w")
    tree.pack(fill="both", expand=True)
    return tree


# ---------------------------------------------------------
# FILL TABLE
# ---------------------------------------------------------

def date_blocks(parent):
    group = ctk.CTkFrame(parent, fg_color=CARD, border_color=BORDER, border_width=1, corner_radius=10)
    group.pack(side="left", padx=8, pady=12)
    day_box = entry(group, "DD", 52)
    month_box = entry(group, "MM", 52)
    year_box = entry(group, "YYYY", 70)
    day_box.pack(side="left", padx=(6, 2), pady=6)
    ctk.CTkLabel(group, text="/", text_color=MUTED).pack(side="left")
    month_box.pack(side="left", padx=2, pady=6)
    ctk.CTkLabel(group, text="/", text_color=MUTED).pack(side="left")
    year_box.pack(side="left", padx=(2, 6), pady=6)
    jump(day_box, month_box, 2)
    jump(month_box, year_box, 2, day_box)
    jump(year_box, None, 4, month_box)
    return day_box, month_box, year_box


def jump(box, next_box, limit, previous_box=None):
    def on_key(event):
        if event.keysym == "BackSpace" and box.get() == "" and previous_box is not None:
            previous_box.focus()
            return
        digits = ""
        for char in box.get():
            if char.isdigit():
                digits = digits + char
        digits = digits[:limit]
        if box.get() != digits:
            box.delete(0, "end")
            box.insert(0, digits)
        if len(digits) == limit and next_box is not None:
            next_box.focus()
    box.bind("<KeyRelease>", on_key)


def make_due(day_text, month_text, year_text):
    from datetime import date
    return date(int(year_text), int(month_text), int(day_text))


def fill_table(tree, rows):
    for item in tree.get_children():
        tree.delete(item)
    for row in rows:
        tree.insert("", "end", values=row)
