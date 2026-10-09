# ---------------------------------------------------------
# COLORS AND SMALL WIDGETS
# Same look as the CustomTkinter design.
# ---------------------------------------------------------

import customtkinter as ctk

BG = "#070d1a"
SIDEBAR = "#0a1224"
CARD = "#0d1830"
CARD_HOVER = "#122244"
BORDER = "#1c2d52"
PRIMARY = "#2563eb"
TEXT = "#e8eeff"
MUTED = "#8697bd"
BLUE = "#4f8cff"
GREEN = "#22c55e"
RED = "#ef4444"
PURPLE = "#8b5cf6"
ORANGE = "#f59e0b"
TEAL = "#14b8a6"


# ---------------------------------------------------------
# FONT
# ---------------------------------------------------------

def font(size=13, weight="normal"):
    return ("Segoe UI", size, weight)


# ---------------------------------------------------------
# CARD
# ---------------------------------------------------------

def card(parent):
    return ctk.CTkFrame(
        parent,
        fg_color=CARD,
        border_color=BORDER,
        border_width=1,
        corner_radius=12
    )


# ---------------------------------------------------------
# ENTRY
# ---------------------------------------------------------

def entry(parent, placeholder, width=180):
    return ctk.CTkEntry(
        parent,
        placeholder_text=placeholder,
        width=width,
        height=36,
        fg_color=BG,
        border_color=BORDER,
        text_color=TEXT
    )


# ---------------------------------------------------------
# BUTTON
# ---------------------------------------------------------

def button(parent, text, command, color=PRIMARY, width=120):
    return ctk.CTkButton(
        parent,
        text=text,
        command=command,
        width=width,
        height=36,
        fg_color=color,
        font=font(12, "bold")
    )
