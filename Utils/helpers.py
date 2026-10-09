from tkinter import messagebox


# ---------------------------------------------------------
# CLEAN
# ---------------------------------------------------------

def clean(value):
    return str(value).strip()


# ---------------------------------------------------------
# SHOW ERROR
# ---------------------------------------------------------

def show_error(title, message):
    messagebox.showerror(title, message)


# ---------------------------------------------------------
# SHOW INFO
# ---------------------------------------------------------

def show_info(title, message):
    messagebox.showinfo(title, message)


# ---------------------------------------------------------
# SHOW SUCCESS
# ---------------------------------------------------------

def show_success(title, message):
    messagebox.showinfo(title, message)
