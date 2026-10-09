import tkinter as tk
from tkinter import messagebox

from Database import queries
from UI.theme import BG, CARD, CARD_2, BORDER, BLUE, TEXT, MUTED, RED, GREEN, entry, button
from Utils.validation import email as valid_email, password as valid_password, required


# ---------------------------------------------------------
# CREATE LOGIN
# ---------------------------------------------------------

def create_login(root, on_login_success):

    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg=BG)

    outer = tk.Frame(root, bg=BG)
    outer.pack(fill="both", expand=True, padx=45, pady=40)

    left = tk.Frame(outer, bg="#0A1423")
    left.pack(side="left", fill="both", expand=True, padx=(0, 20))

    tk.Label(
        left,
        text="LIBRARY\nSYSTEM",
        bg="#0A1423",
        fg=TEXT,
        font=("Segoe UI", 34, "bold"),
        justify="left"
    ).pack(anchor="w", padx=50, pady=(70, 10))

    tk.Label(
        left,
        text="CONTROL TERMINAL",
        bg="#0A1423",
        fg=BLUE,
        font=("Consolas", 10, "bold")
    ).pack(anchor="w", padx=52)

    tk.Label(
        left,
        text="Read. Learn. Grow.",
        bg="#0A1423",
        fg=MUTED,
        font=("Segoe UI", 12)
    ).pack(anchor="w", padx=52, pady=(35, 0))

    right = tk.Frame(
        outer,
        bg=CARD,
        highlightthickness=1,
        highlightbackground=BORDER,
        width=500
    )
    right.pack(side="right", fill="both", expand=False)
    right.pack_propagate(False)

    content = tk.Frame(right, bg=CARD)
    content.pack(fill="both", expand=True, padx=45, pady=45)

    heading = tk.Label(
        content,
        text="ACCESS TERMINAL",
        bg=CARD,
        fg=TEXT,
        font=("Segoe UI", 22, "bold")
    )
    heading.pack(anchor="w")

    status = tk.Label(content, text="", bg=CARD, fg=MUTED, font=("Segoe UI", 9), wraplength=380, justify="left")
    status.pack(anchor="w", pady=(7, 20))

    fields = tk.Frame(content, bg=CARD)
    fields.pack(fill="x")

    tk.Label(fields, text="EMAIL", bg=CARD, fg=MUTED, font=("Consolas", 8, "bold")).pack(anchor="w")
    email_box = entry(fields)
    email_box.pack(fill="x", pady=(6, 15), ipady=7)

    tk.Label(fields, text="PASSWORD", bg=CARD, fg=MUTED, font=("Consolas", 8, "bold")).pack(anchor="w")
    password_box = entry(fields)
    password_box.config(show="•")
    password_box.pack(fill="x", pady=(6, 20), ipady=7)

    def setup_admin():

        name = email_box.get().strip()
        email = name
        password = password_box.get()

        if not required(name):
            status.config(text="Enter the administrator name in the email field temporarily.", fg=RED)
            return

        if not valid_email(email):
            status.config(text="Enter a valid email address.", fg=RED)
            return

        if not valid_password(password):
            status.config(text="Password must contain at least 4 characters.", fg=RED)
            return

        try:
            queries.create_user("Admin", email, password)
            status.config(text="Administrator created. You can now log in.", fg=GREEN)
            heading.config(text="ACCESS TERMINAL")
            setup_button.pack_forget()
            login_button.pack(fill="x")
            email_box.delete(0, "end")
            password_box.delete(0, "end")

        except Exception as error:
            status.config(text="Unable to create administrator.", fg=RED)

    def login():
        email = email_box.get().strip()
        password = password_box.get()

        if not valid_email(email) or not password:
            status.config(text="Enter your email and password.", fg=RED)
            return

        try:
            user = queries.check_user(email, password)

        except Exception as error:
            status.config(
                text="Database unavailable. Check MySQL and your local .env settings.",
                fg=RED
            )
            return

        if user:
            on_login_success(user)
        else:
            status.config(text="Invalid email or password.", fg=RED)

    def prepare_first_run():
        heading.config(text="CREATE ADMIN")
        status.config(
            text="No administrator account exists yet. Enter the administrator email and create the first account.",
            fg=MUTED
        )
        login_button.pack_forget()
        setup_button.pack(fill="x")

    login_button = button(content, "LOGIN", login)
    login_button.pack_forget()

    setup_button = button(content, "CREATE ADMINISTRATOR", setup_admin)
    setup_button.pack_forget()

    try:
        count = queries.user_count()
        if count == 0:
            prepare_first_run()
        else:
            login_button.pack(fill="x")
    except Exception:
        status.config(
            text="Database unavailable. Start MySQL and check your .env settings.",
            fg=RED
        )
        login_button.pack(fill="x")

    tk.Label(
        content,
        text="Local credentials are stored securely in the database.",
        bg=CARD,
        fg=MUTED,
        font=("Segoe UI", 8)
    ).pack(anchor="w", pady=(25, 0))
