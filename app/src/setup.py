import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from db_config import pwd

#---------------------------------------paths----------------------------------------+
RUNS_FILE = 'app/data/runs.txt'                   #                                  |
logo="app/resources/logo.png"                     #                                  |
place_holder_gif="app/resources/loading.gif"      #                                  |
#------------------------------------------------------------------------------------+

# The default colors for terminal
prompt_colors={"prompt":"yellow","success":"lime","error":"red","info":"cyan","warning":"orange","normal":"white"}

import tkinter as tk
from tkinter import messagebox
import os

def update_setup_file(host, user, password, database):
    if os.path.exists("app/src/db_config.py"):
        with open("app/src/db_config.py", "r") as file:
            lines = file.readlines()
    else:
        lines = []

    # Ensure at least 8 lines exist
    while len(lines) < 8:
        lines.append("\n")

    # Max column where | should appear (choose a value wider than any line's left part)
    pipe_column = 70

    lines = [None] * 6
    lines[0] = "#-----------------------------------new variables-----------------------------------+\n"

    host_line = f"host='{host}'"
    user_line = f"user='{user}'"
    pwd_line = f"pwd = '{password}'"
    db_line = f"database = '{database}'"

    # Pad each line with spaces so that the '|' appears at the same column
    lines[1] = f"{host_line}{' ' * (pipe_column - len(host_line))}#{13*" "}|\n"
    lines[2] = f"{user_line}{' ' * (pipe_column - len(user_line))}#{13*" "}|\n"
    lines[3] = f"{pwd_line}{' ' * (pipe_column - len(pwd_line))}#{13*" "}|\n"
    lines[4] = f"{db_line}{' ' * (pipe_column - len(db_line))}#{13*" "}|\n"
    lines[5]="#-----------------------------------------------------------------------------------+"


    with open("app/src/db_config.py", "w") as file:
        file.writelines(lines)

def get_db_config():
    def submit():
        host = host_entry.get()
        user = user_entry.get()
        password = password_entry.get()
        database = db_entry.get()

        if not (host and user and password and database):
            messagebox.showerror("Error", "All fields are required!")
            return

        update_setup_file(host, user, password, database)
        messagebox.showinfo("Success", "Configuration updated in app/src/db_config.py")
        temp_root.destroy()

    temp_root = tk.Tk()
    temp_root.title("Banana-MySQL Setup")

    # Dark theme colors
    bg_color = "#000000"
    fg_color = "#ffffff"
    entry_bg = "#3c3f41"
    entry_fg = "#ffffff"
    btn_bg = "#444"
    btn_fg = "#fff"

    temp_root.configure(bg=bg_color)

    labels = ["Host", "User", "Password", "Database"]
    entries = []
    defaults = ["localhost", "root", "", ""]

    for i, label in enumerate(labels):
        tk.Label(temp_root, text=label, bg=bg_color, fg=fg_color).grid(row=i, column=0, padx=10, pady=5)
        entry = tk.Entry(temp_root, width=30, bg=entry_bg, fg=entry_fg, insertbackground=entry_fg,
                         show="*" if label == "Password" else "")
        entry.insert(0, defaults[i])
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries.append(entry)

    host_entry, user_entry, password_entry, db_entry = entries

    submit_btn = tk.Button(temp_root, text="Save", command=submit, bg=btn_bg, fg=btn_fg)
    submit_btn.grid(row=4, column=0, columnspan=2, pady=15)

    temp_root.mainloop()

if pwd=="":
    get_db_config()