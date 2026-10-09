# ---------------------------------------------------------
# START HERE
# ---------------------------------------------------------

import tkinter as tk
from tkinter import messagebox

import customtkinter as ctk

from Database.database import test_connection
from Database.model import create_all_tables
from Database.queries import check_user, create_user
from UI.window import LibraryApp
from UI.look import BG, CARD, BORDER, TEXT, MUTED, PRIMARY, BLUE, font, entry, button


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():
    saved_name = read_session()
    if saved_name != "":
        ok, message = test_connection()
        if ok:
            try:
                create_all_tables()
                LibraryApp(saved_name).mainloop()
                return
            except Exception:
                pass
    show_login()


# ---------------------------------------------------------
# SHOW LOGIN
# ---------------------------------------------------------

def show_login():
    ctk.set_appearance_mode("dark")
    window = ctk.CTk(fg_color=BG)
    window.title("Library Management System")
    window.geometry("900x560")
    left = ctk.CTkFrame(window, fg_color=CARD, corner_radius=0)
    left.pack(side="left", fill="both", expand=True)
    ctk.CTkLabel(left, text="LIBRARY\nSYSTEM", font=font(34, "bold"), text_color=TEXT, justify="left").pack(anchor="w", padx=40, pady=(80, 10))
    ctk.CTkLabel(left, text="Read  •  Learn  •  Grow", font=font(12), text_color=BLUE).pack(anchor="w", padx=42)
    right = ctk.CTkFrame(window, fg_color=BG, corner_radius=0)
    right.pack(side="right", fill="both", expand=True)
    box = ctk.CTkFrame(right, fg_color=CARD, border_color=BORDER, border_width=1, corner_radius=16)
    box.pack(padx=40, pady=50, fill="both", expand=True)
    ctk.CTkLabel(box, text="Sign in", font=font(22, "bold"), text_color=TEXT).pack(anchor="w", padx=24, pady=(24, 8))
    name_box = entry(box, "Name, only for a new account", 280)
    email_box = entry(box, "Email", 280)
    password_box = entry(box, "Password", 280)
    password_box.configure(show="*")
    name_box.pack(padx=24, pady=6)
    email_box.pack(padx=24, pady=6)
    password_box.pack(padx=24, pady=6)
    status = ctk.CTkLabel(box, text="", text_color=MUTED)
    status.pack(anchor="w", padx=24, pady=6)
    stay = ctk.CTkCheckBox(box, text="Stay signed in on this computer", text_color=TEXT)
    stay.pack(anchor="w", padx=24, pady=4)
    stay.select()

    def prepare_database():
        ok, message = test_connection()
        if not ok:
            status.configure(text=message)
            return False
        try:
            create_all_tables()
        except Exception:
            status.configure(text="Connected, but the tables could not be prepared.")
            return False
        return True

    def login():
        if prepare_database() == False:
            return
        user = check_user(email_box.get().strip(), password_box.get())
        if user is None:
            status.configure(text="Email or password is not correct.")
            return
        window.destroy()
        if stay.get() == 1:
            write_session(user[1])
        else:
            clear_session()
        ask_api_key(user[1])

    def register():
        if name_box.get().strip() == "" or "@" not in email_box.get() or len(password_box.get()) < 4:
            status.configure(text="Enter a name, email, and a password of at least 4 characters.")
            return
        if prepare_database() == False:
            return
        try:
            create_user(name_box.get().strip(), email_box.get().strip(), password_box.get())
            status.configure(text="Account saved. Click Login.")
        except Exception:
            status.configure(text="The account could not be saved.")

    button(box, "Login", login, width=280).pack(padx=24, pady=(8, 6))
    button(box, "Create account", register, color=CARD, width=280).pack(padx=24, pady=6)
    window.mainloop()


# ---------------------------------------------------------
# SESSION
# ---------------------------------------------------------

def session_file():
    from Config import config
    return config.PROJECT_ROOT / "session.txt"


def read_session():
    path = session_file()
    if path.exists() == False:
        return ""
    return path.read_text(encoding="utf-8").strip()


def write_session(user_name):
    session_file().write_text(user_name, encoding="utf-8")


def clear_session():
    path = session_file()
    if path.exists():
        path.unlink()

def ask_api_key(user_name):
    from Config import config

    window = ctk.CTk(fg_color=BG)
    window.title("Gemini API key")
    window.geometry("520x340")
    box = ctk.CTkFrame(window, fg_color=CARD, border_color=BORDER, border_width=1, corner_radius=16)
    box.pack(fill="both", expand=True, padx=24, pady=24)
    ctk.CTkLabel(box, text="Gemini API key", font=font(22, "bold"), text_color=TEXT).pack(anchor="w", padx=24, pady=(24, 6))
    ctk.CTkLabel(box, text="Add a key for the AI panel, or continue without it.", font=font(12), text_color=MUTED).pack(anchor="w", padx=24)
    key_box = entry(box, "Paste Gemini API key", 360)
    key_box.pack(padx=24, pady=18)
    if config.GEMINI_API_KEY:
        key_box.insert(0, config.GEMINI_API_KEY)

    def open_app():
        window.destroy()
        LibraryApp(user_name).mainloop()

    def save_and_continue():
        key = key_box.get().strip()
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
        open_app()

    button(box, "Save key and continue", save_and_continue, width=360).pack(padx=24, pady=6)
    button(box, "Continue anyway", open_app, color=CARD, width=360).pack(padx=24, pady=6)
    window.mainloop()


if __name__ == "__main__":
    main()
