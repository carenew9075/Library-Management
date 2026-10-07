import random
import tkinter as tk
from tkinter import messagebox

from Database import queries
from Modules.library_ai import ask_gemini
from UI.theme import *
from Utils.constant import QUOTES


# ---------------------------------------------------------
# CREATE DASHBOARD
# ---------------------------------------------------------

def create_dashboard(parent, user_name="Admin", navigation_callback=None):

    clear_frame(parent)

    root = tk.Frame(parent, bg=BG)
    root.pack(fill="both", expand=True)

    title_block(root, "LIBRARY MANAGEMENT SYSTEM", "READ  •  LEARN  •  GROW")

    welcome = tk.Frame(root, bg=BG)
    welcome.pack(fill="x", padx=30)

    tk.Label(
        welcome,
        text="Welcome to Library Management System",
        bg=BG,
        fg=TEXT,
        font=("Segoe UI", 17, "bold")
    ).pack(anchor="w")

    tk.Label(
        welcome,
        text=random.choice(QUOTES),
        bg=BG,
        fg=MUTED,
        font=("Segoe UI", 9),
        wraplength=900,
        justify="left"
    ).pack(anchor="w", pady=(5, 15))

    body = tk.Frame(root, bg=BG)
    body.pack(fill="both", expand=True, padx=30, pady=(0, 30))

    left = tk.Frame(body, bg=BG)
    left.pack(side="left", fill="both", expand=True, padx=(0, 15))

    right = tk.Frame(body, bg=BG, width=330)
    right.pack(side="right", fill="y")
    right.pack_propagate(False)

    stats_frame = tk.Frame(left, bg=BG)
    stats_frame.pack(fill="x")

    try:
        total_books, total_students, issued_books, available_copies = queries.get_all_records(), 0, 0, 0
        stats = (
            queries.count_book_titles(),
            queries.count_students(),
            queries.count_issued_books(),
            queries.count_available_copies()
        )
    except Exception:
        stats = (0, 0, 0, 0)

    labels = ["TOTAL BOOKS", "TOTAL STUDENTS", "ISSUED BOOKS", "AVAILABLE COPIES"]
    for index, value in enumerate(stats):
        c = card(stats_frame)
        c.grid(row=0, column=index, sticky="nsew", padx=(0 if index == 0 else 6, 0))
        stats_frame.columnconfigure(index, weight=1)
        tk.Label(c, text=labels[index], bg=CARD, fg=MUTED, font=("Consolas", 8, "bold")).pack(anchor="w", padx=15, pady=(12, 4))
        tk.Label(c, text=str(value), bg=CARD, fg=TEXT, font=("Segoe UI", 20, "bold")).pack(anchor="w", padx=15, pady=(0, 12))

    quick = card(left, "QUICK ACCESS")
    quick.pack(fill="x", pady=15)

    quick_buttons = [
        ("Add Books", "Books"),
        ("Search Books", "Books"),
        ("Register Student", "Students"),
        ("Issue Book", "Issue Books"),
        ("Return Book", "Return Books")
    ]

    row = tk.Frame(quick, bg=CARD)
    row.pack(fill="x", padx=15, pady=(3, 15))

    for text, page in quick_buttons:
        tk.Button(
            row,
            text=text,
            command=(lambda p=page: navigation_callback(p)) if navigation_callback else None,
            bg=CARD_2,
            fg=TEXT,
            activebackground="#17314F",
            activeforeground=BLUE,
            relief="flat",
            cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            padx=13,
            pady=10
        ).pack(side="left", padx=(0, 7))

    recent = card(left, "RECENT ACTIVITIES")
    recent.pack(fill="both", expand=True)

    tree = ttk.Treeview(recent, columns=("book", "title", "student", "date"), show="headings")
    for col, heading, width in [
        ("book", "Book ID", 80),
        ("title", "Book", 230),
        ("student", "Student", 180),
        ("date", "Issued On", 110)
    ]:
        tree.heading(col, text=heading)
        tree.column(col, width=width, anchor="w")
    tree.pack(fill="both", expand=True, padx=15, pady=15)

    try:
        rows = queries.get_recent_activities()
        for row in rows:
            tree.insert("", "end", values=row)
    except Exception:
        pass

    ai_card = card(right, "AI ASSISTANT")
    ai_card.pack(fill="both", expand=True)

    tk.Label(
        ai_card,
        text="Powered by Gemini",
        bg=CARD,
        fg=BLUE,
        font=("Consolas", 8, "bold")
    ).pack(anchor="w", padx=18)

    answer = tk.Label(
        ai_card,
        text="Ask about books, students, or library operations.",
        bg=CARD,
        fg=MUTED,
        font=("Segoe UI", 9),
        wraplength=280,
        justify="left"
    )
    answer.pack(fill="both", expand=True, padx=18, pady=18, anchor="nw")

    question = tk.Entry(
        ai_card,
        bg=CARD_2,
        fg=TEXT,
        insertbackground=BLUE,
        relief="flat"
    )
    question.pack(fill="x", padx=18, ipady=8)

    def ask():
        q = question.get().strip()
        if not q:
            return
        answer.config(text="Thinking...", fg=BLUE)
        root.update_idletasks()
        answer.config(text=ask_gemini(q), fg=TEXT)

    button(ai_card, "ASK GEMINI", ask).pack(fill="x", padx=18, pady=18)
