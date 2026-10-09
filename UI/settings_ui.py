import tkinter as tk
from tkinter import messagebox
from dotenv import set_key

from Config import config
from Database.database import test_connection
from Modules.library_ai import test_gemini
from UI.theme import *


# ---------------------------------------------------------
# CREATE SETTINGS UI
# ---------------------------------------------------------

def create_settings_ui(parent, logout_callback=None):
    clear_frame(parent)
    title_block(parent, "SETTINGS", "Connection and application configuration")

    main = tk.Frame(parent, bg=BG)
    main.pack(fill="both", expand=True, padx=30, pady=(0, 30))

    database_card = card(main, "DATABASE")
    database_card.pack(fill="x", pady=(0, 15))

    labels = [
        ("Host", config.DB_HOST),
        ("User", config.DB_USER),
        ("Database", config.DB_NAME)
    ]

    for name, value in labels:
        row = tk.Frame(database_card, bg=CARD)
        row.pack(fill="x", padx=18, pady=5)
        tk.Label(row, text=name, bg=CARD, fg=MUTED, width=12, anchor="w", font=("Consolas", 8, "bold")).pack(side="left")
        tk.Label(row, text=value, bg=CARD, fg=TEXT, anchor="w", font=("Segoe UI", 9)).pack(side="left")

    def check_db():
        ok, message = test_connection()
        messagebox.showinfo("Database", message)

    button(database_card, "TEST DATABASE CONNECTION", check_db).pack(anchor="w", padx=18, pady=15)

    gemini_card = card(main, "GEMINI AI")
    gemini_card.pack(fill="x")

    model_row = tk.Frame(gemini_card, bg=CARD)
    model_row.pack(fill="x", padx=18, pady=(12, 6))
    tk.Label(model_row, text="MODEL", bg=CARD, fg=MUTED, width=12, anchor="w", font=("Consolas", 8, "bold")).pack(side="left")
    model_box = entry(model_row)
    model_box.insert(0, config.GEMINI_MODEL)
    model_box.pack(side="left", fill="x", expand=True, ipady=6)

    key_row = tk.Frame(gemini_card, bg=CARD)
    key_row.pack(fill="x", padx=18, pady=6)
    tk.Label(key_row, text="API KEY", bg=CARD, fg=MUTED, width=12, anchor="w", font=("Consolas", 8, "bold")).pack(side="left")
    key_box = entry(key_row)
    key_box.insert(0, config.GEMINI_API_KEY)
    key_box.config(show="•")
    key_box.pack(side="left", fill="x", expand=True, ipady=6)

    def save_gemini():
        try:
            set_key(str(config.ENV_FILE), "GEMINI_MODEL", model_box.get().strip())
            set_key(str(config.ENV_FILE), "GEMINI_API_KEY", key_box.get().strip())
            config.reload_environment()
            messagebox.showinfo("Gemini", "Gemini settings saved locally.")
        except Exception:
            messagebox.showerror("Gemini", "Unable to save Gemini settings.")

    def check_gemini():
        if test_gemini():
            messagebox.showinfo("Gemini", "Gemini connection successful.")
        else:
            messagebox.showerror("Gemini", "Gemini could not be reached. Check the API key and model.")

    actions = tk.Frame(gemini_card, bg=CARD)
    actions.pack(fill="x", padx=18, pady=15)
    button(actions, "SAVE GEMINI SETTINGS", save_gemini).pack(side="left")
    button(actions, "TEST GEMINI", check_gemini).pack(side="left", padx=8)

    logout_card = card(main, "SESSION")
    logout_card.pack(fill="x", pady=15)

    def logout():
        if logout_callback:
            logout_callback()

    button(logout_card, "LOGOUT", logout, danger=True).pack(anchor="w", padx=18, pady=15)
