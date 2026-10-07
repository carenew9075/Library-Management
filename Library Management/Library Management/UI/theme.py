import tkinter as tk
from tkinter import ttk

from Utils.constant import BG, CARD, CARD_2, BORDER, BLUE, TEXT, MUTED, RED, GREEN


# ---------------------------------------------------------
# SETUP STYLE
# ---------------------------------------------------------

def setup_style():
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "Treeview",
        background=CARD_2,
        foreground=TEXT,
        fieldbackground=CARD_2,
        borderwidth=0,
        rowheight=34,
        font=("Segoe UI", 9)
    )
    style.configure(
        "Treeview.Heading",
        background=CARD,
        foreground=BLUE,
        borderwidth=0,
        font=("Segoe UI", 9, "bold")
    )
    style.map("Treeview", background=[("selected", "#17314F")])
    style.configure(
        "TCombobox",
        fieldbackground=CARD_2,
        background=CARD_2,
        foreground=TEXT,
        arrowcolor=BLUE
    )
    style.configure("TNotebook", background=BG, borderwidth=0)
    style.configure("TNotebook.Tab", background=CARD_2, foreground=MUTED, padding=(18, 9))
    style.map("TNotebook.Tab", background=[("selected", CARD)], foreground=[("selected", BLUE)])


# ---------------------------------------------------------
# CLEAR FRAME
# ---------------------------------------------------------

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()


# ---------------------------------------------------------
# TITLE BLOCK
# ---------------------------------------------------------

def title_block(parent, title, subtitle):
    wrapper = tk.Frame(parent, bg=BG)
    wrapper.pack(fill="x", padx=30, pady=(25, 15))

    tk.Label(
        wrapper,
        text=title,
        bg=BG,
        fg=TEXT,
        font=("Segoe UI", 24, "bold")
    ).pack(anchor="w")

    tk.Label(
        wrapper,
        text=subtitle,
        bg=BG,
        fg=MUTED,
        font=("Segoe UI", 10)
    ).pack(anchor="w", pady=(3, 0))

    return wrapper


# ---------------------------------------------------------
# CARD
# ---------------------------------------------------------

def card(parent, title=None):
    frame = tk.Frame(parent, bg=CARD, highlightthickness=1, highlightbackground=BORDER)

    if title:
        tk.Label(
            frame,
            text=title,
            bg=CARD,
            fg=MUTED,
            font=("Consolas", 9, "bold")
        ).pack(anchor="w", padx=18, pady=(15, 5))

    return frame


# ---------------------------------------------------------
# ENTRY
# ---------------------------------------------------------

def entry(parent):
    return tk.Entry(
        parent,
        bg=CARD_2,
        fg=TEXT,
        insertbackground=BLUE,
        relief="flat",
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=BLUE,
        font=("Segoe UI", 10)
    )


# ---------------------------------------------------------
# BUTTON
# ---------------------------------------------------------

def button(parent, text, command, danger=False):
    return tk.Button(
        parent,
        text=text,
        command=command,
        bg=RED if danger else BLUE,
        fg="white" if danger else "#06111B",
        activebackground="#FFFFFF",
        activeforeground="#06111B",
        relief="flat",
        cursor="hand2",
        font=("Segoe UI", 9, "bold"),
        padx=16,
        pady=9
    )


# ---------------------------------------------------------
# FRIENDLY ERROR
# ---------------------------------------------------------

def friendly_error(error):
    text = str(error).lower()

    if "1045" in text or "access denied" in text:
        return "MySQL rejected the database login. Check DB_USER and DB_PASSWORD in your local .env file."

    if "unknown database" in text:
        return "The library database could not be opened. Please check your MySQL settings."

    if "duplicate" in text or "1062" in text:
        return "That value already exists. Please use a different value."

    if "foreign key" in text or "1451" in text:
        return "This record is still being used elsewhere and cannot be deleted."

    if "connection" in text or "2003" in text:
        return "MySQL Server could not be reached. Make sure the server is running."

    return "The operation could not be completed. Please check your settings and try again."
