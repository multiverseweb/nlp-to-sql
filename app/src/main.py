import tkinter as tk
from tkinter import ttk
from tkinter import messagebox                                          #   +-------------------+
from tkinter import Canvas                                              #   |  Tejas Codes :D   |
import mysql.connector as my                                            #   |   30-04-2025      |
import os                                                               #   +-------------------+
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tabulate import tabulate
from matplotlib import cm
from matplotlib.colors import Normalize
from PIL import Image, ImageTk
from setup import *                                                  # user defined module

#==========================================================================================================#

banner='''====================================================================================
=====  ====================================================  ============  ==  =====
=====  ====================================================  ============  ==  =====
=====  ====================================================  ============  ==  =====
=====  ======   ===  = ====   ===  = ====   =========   ===  ======   ===  ==  =====
=====    ===  =  ==     ==  =  ==     ==  =  =======  =  ==    ===  =  ==  ==  =====
=====  =  =====  ==  =  =====  ==  =  =====  ========  ====  =  ==     ==  ==  =====
=====  =  ===    ==  =  ===    ==  =  ===    =========  ===  =  ==  =====  ==  =====
=====  =  ==  =  ==  =  ==  =  ==  =  ==  =  =======  =  ==  =  ==  =  ==  ==  =====
=====    ====    ==  =  ===    ==  =  ===    ========   ===  =  ===   ===  ==  =====
====================================================================================
'''

def update_runs():
    try:
        if not os.path.exists(RUNS_FILE):
            with open(RUNS_FILE, 'w') as f:
                f.write('0')
        with open(RUNS_FILE, 'r+') as f:
            runs = int(f.read().strip()) + 1
            f.seek(0)
            f.write(str(runs))
            f.truncate()
        return runs
    except:
        return 'N/A'
from PIL import Image, ImageTk, ImageSequence

class GIFPlayer(tk.Label):
    def __init__(self, parent, gif_path, height=60):
        super().__init__(parent, bg='#111')
        self.gif = Image.open(gif_path)
        self.frames = []

        for frame in ImageSequence.Iterator(self.gif):
            frame = frame.copy().convert("RGBA")
            aspect_ratio = frame.width / frame.height
            resized = frame.resize((int(height * aspect_ratio), height))
            self.frames.append(ImageTk.PhotoImage(resized))

        self.frame_index = 0
        self.animate()

    def animate(self):
        self.configure(image=self.frames[self.frame_index])
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.after(100, self.animate)

class SQLApp:
    def __init__(self, root):
        self.root = root
        self.version = f"v1.{str(update_runs())[:1]}.{str(update_runs())[1:]}"
        self.status_color = "yellow"
        self.status_text = "Banana"

        self.setup_ui()

    def add_table(self, text):
        label = tk.Label(self.schema_area, text=text, bg="#111", bd=0, relief="raised", font=("Courier", 8), justify="left",fg="white")
        label_window = self.schema_area.create_window(50, 50, window=label, anchor="nw")

        def on_drag_start(event, lbl=label, win=label_window):
            lbl._drag_data = {"x": event.x, "y": event.y}

        def on_drag_motion(event, lbl=label, win=label_window):
            dx = event.x - lbl._drag_data["x"]
            dy = event.y - lbl._drag_data["y"]
            self.schema_area.move(win, dx, dy)

        label.bind("<Button-1>", on_drag_start)
        label.bind("<B1-Motion>", on_drag_motion)

    def setup_ui(self):
        def destroy_guide(event):
            if guide.winfo_exists():
                guide.destroy()

        # Top bar
        topbar = tk.Frame(self.root, bg="black", height=50)
        topbar.pack(fill=tk.X, side=tk.TOP)
        # Load and display logo
        logo_img = Image.open(logo)
        logo_img = logo_img.resize((int(logo_img.width * (50 / logo_img.height)), 50), Image.Resampling.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(logo_img)

        logo_label = tk.Label(topbar, image=self.logo_photo, bg="black")
        logo_label.pack(side=tk.LEFT, padx=10, pady=5)

        info = tk.Label(topbar, text=f"{self.version}", fg="white", bg="black", font=("Consolas", 10))
        info.pack(side=tk.RIGHT, padx=10)

        self.status_label = tk.Label(topbar, text=self.status_text, fg="black", bg=self.status_color, font=("Consolas", 10, "bold"))
        self.status_label.pack(side=tk.RIGHT, padx=10)

        # Input Frame
        input_frame = tk.Frame(self.root, bg="black")
        input_frame.pack(padx=20, pady=10, fill=tk.X)

        # Input Entries
        tk.Label(input_frame, text="Host", bg="black", fg="white", font=("Consolas", 10)).grid(row=0, column=0, padx=5, sticky="w")
        self.host_entry = tk.Entry(input_frame, fg="white", bg="#111", insertbackground='white')
        self.host_entry.insert(0, host)
        self.host_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="User", bg="black", fg="white", font=("Consolas", 10)).grid(row=0, column=2, padx=5, sticky="w")
        self.user_entry = tk.Entry(input_frame, fg="white", bg="#111", insertbackground='white')
        self.user_entry.insert(0, user)
        self.user_entry.grid(row=0, column=3, padx=5)

        tk.Label(input_frame, text="Password", bg="black", fg="white", font=("Consolas", 10)).grid(row=1, column=0, padx=5, sticky="w")
        self.pass_entry = tk.Entry(input_frame, fg="white", bg="#111", insertbackground='white', show="*")
        self.pass_entry.insert(0, pwd)
        self.pass_entry.grid(row=1, column=1, padx=5)

        tk.Label(input_frame, text="Database", bg="black", fg="white", font=("Consolas", 10)).grid(row=1, column=2, padx=5, sticky="w")
        self.db_entry = tk.Entry(input_frame, fg="white", bg="#111", insertbackground='white')
        self.db_entry.insert(0, database)
        self.db_entry.grid(row=1, column=3, padx=5)
        self.db_entry.bind("<FocusIn>", destroy_guide)

        guide=tk.Label(input_frame, text="<----------------------- Start here :D", bg="black", fg="white", font=("Consolas", 10))
        guide.grid(row=1, column=4, padx=5, sticky="w")

        self.train_btn = tk.Button(input_frame, text="Train Infinity", command=self.connect_and_parse, bg="#222", fg="white", font=("Consolas", 10), bd=0, cursor="hand2")
        self.train_btn.grid(row=0, column=4, rowspan=1, padx=10, sticky="w")

        # Main container frame
        main_frame = tk.Frame(self.root, bg="black")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Left frame for schema (50% width, full height)
        left_frame = tk.Frame(main_frame, bg="black", width=self.root.winfo_screenwidth()//2)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Right frame for terminal + bar graph (50% width, stacked)
        right_frame = tk.Frame(main_frame, bg="black", width=self.root.winfo_screenwidth()//2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Schema Frame in left
        self.schema_area = tk.Canvas(left_frame, bg="#111",
                                bd=0, highlightbackground="gray", highlightcolor="gray", highlightthickness=1)
        self.schema_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.schema_gif = GIFPlayer(left_frame, place_holder_gif)
        self.schema_gif.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Terminal Frame in top-right
        self.terminal = tk.Text(right_frame, bg="#111", fg="white", font=("Consolas", 10), height=1,
                                bd=0, highlightbackground="gray", highlightcolor="gray", highlightthickness=1,insertbackground="yellow")
        self.terminal.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))
        
        self.user_terminal = tk.Text(right_frame, bg="#111", fg="white", font=("Consolas", 10), height=1,
                                bd=0, highlightbackground="gray", highlightcolor="gray", highlightthickness=1,insertbackground="yellow")
        self.user_terminal.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))

        self.terminal_gif = GIFPlayer(right_frame, place_holder_gif)
        self.terminal_gif.place(relx=0.5, rely=0.50, anchor=tk.CENTER)  # Adjust vertically if needed

        # Bar Graph Frame in bottom-right
        self.graph_frame = tk.Frame(right_frame, bg="#111", highlightbackground="gray", highlightthickness=1, height=150)
        self.graph_frame.pack(fill=tk.X, expand=False, padx=10, pady=(5, 10))

        self.graph_gif = GIFPlayer(self.graph_frame, place_holder_gif)
        self.graph_gif.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        unlock_terminal(self)
        self.terminal.insert(tk.END, "🍌_", "prompt")
        self.terminal.insert(tk.END, "Banana logs appear here... (Read-only)\n", "info")
        self.terminal.insert(tk.END, f"{banner}\n", "normal")
        self.terminal.insert(tk.END, "Prompt\t", "prompt")
        self.terminal.insert(tk.END, "Success\t", "success")
        self.terminal.insert(tk.END, "Error\t", "error")
        self.terminal.insert(tk.END, "Info\t", "info")
        self.terminal.insert(tk.END, "Warning\n", "warning")
        lock_terminal(self)
        self.user_terminal.insert(tk.END, "🍌_", "prompt")
        self.user_terminal.insert(tk.END, "Write SQL or Banana prompts here...\n", "info")
        self.user_terminal.bind("<Return>", self.on_enter_pressed)


    def create_entry(self, parent, label_text, default_text="", show=None):
        frame = tk.Frame(parent, bg="#111")
        frame.grid(row=0, column=len(parent.grid_slaves())//2, padx=10)

        label = tk.Label(frame, text=label_text, fg="white", bg="#111", font=("Consolas", 10))
        label.pack(anchor="w")

        entry = tk.Entry(frame, font=("Consolas", 10), show=show, fg="white", bg="#222", insertbackground="white", bd=0)
        entry.insert(0, default_text)
        entry.pack()
        return entry

    def connect_and_parse(self):
        unlock_terminal(self)
        self.terminal.insert(tk.END, "🍌_", "prompt")
        lock_terminal(self)
        host = self.host_entry.get()
        user = self.user_entry.get()
        password = self.pass_entry.get()
        global database
        database = self.db_entry.get()
        self.terminal_gif.destroy()

        try:
            conn = my.connect(host=host, user=user, password=password, database=database)
            cursor = conn.cursor()
            self.status_color = "green"
            self.status_text = "Connected"
            self.status_label.config(bg=self.status_color, text=self.status_text)
            if conn.is_connected():
                cursor.execute("SELECT DATABASE();")  # This will fail if DB doesn't exist
                db = cursor.fetchone()
                if db and db[0] == database:
                    self.schema_gif.destroy()
                    self.graph_gif.destroy()
                    unlock_terminal(self)
                    self.terminal.insert(tk.END, "Connection Successful!\n", "success")
                    lock_terminal(self)
                else:
                    pass
                
            self.show_schema(cursor)
            cursor.close()
            conn.close()
        except my.Error as e:
            self.status_color = "red"
            self.status_text = "Failed"
            self.status_label.config(bg=self.status_color, text=self.status_text)
            unlock_terminal(self)
            self.terminal.insert(tk.END, f"Database Connection Failed!\n\t> {e}\n", "error")
            lock_terminal(self)
        self.terminal.see(tk.END)  

    def show_schema(self, cursor):
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        self.schema_area.delete("all")  # Clear previous schema

        bar_data_columns = {}
        bar_data_rows = {}

        for table in tables:
            cursor.execute("DESCRIBE " + table[0])
            columns = cursor.fetchall()
            dashes="-" * (len(table[0]) + 2)
            self.add_table(f"+---------{dashes}-+\n| Schema of {table[0]} |\n{tabulate(columns, headers=['Field', 'Type', 'Null', 'Key', 'Default', 'Extra'], tablefmt='pretty')}")
            
            # Fetch the number of rows in the table
            cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
            row_count = cursor.fetchone()[0]

            # Store the number of rows and columns
            bar_data_columns[table[0]] = len(columns)
            bar_data_rows[table[0]] = row_count

        self.display_bargraph(bar_data_columns, bar_data_rows)

    def display_bargraph(self, data_columns, data_rows):
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(5.5, 2), dpi=100)
        fig.patch.set_facecolor('#111')  # Set figure background
        ax.set_facecolor('#111')         # Set axes background

        # Normalize data values for colormap
        norm_columns = Normalize(vmin=min(data_columns.values()), vmax=max(data_columns.values()))
        norm_rows = Normalize(vmin=min(data_rows.values()), vmax=max(data_rows.values()))
        
        # Define color maps
        colors_columns = cm.plasma_r(norm_columns(list(data_columns.values())))
        colors_rows = cm.viridis(norm_rows(list(data_rows.values())))


        # Bar width: wider for rows, thinner for columns
        bar_width_columns = 0.3  # Thinner bars for columns
        bar_width_rows = 0.5     # Wider bars for rows

        # Positioning for bars so they overlap
        table_names = list(data_columns.keys())
        x_positions = range(len(table_names))  # Same x-positions for both columns and rows

        # Plot columns and rows bars on the same positions (overlapping)
        ax.bar(x_positions, data_rows.values(), color=colors_rows, width=bar_width_rows, label="Rows", align='center')
        ax.bar(x_positions, data_columns.values(), color=colors_columns, width=bar_width_columns, label="Columns", align='center')

        ax.set_title('Rows (wider) and Columns (thinner) per Table', color='white')
        ax.set_ylabel('Count', color='white')
        ax.set_xlabel('Tables', color='white')
        ax.set_xticks(x_positions)
        ax.set_xticklabels(table_names, color='white')

        # Dark theme styling
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        ax.grid(True, linestyle='--', alpha=0.3, color='white')
        for spine in ax.spines.values():
            spine.set_edgecolor('#333')

        # Create the canvas and display it
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

#===================================================================================user terminal
    def on_enter_pressed(self, event):
        # Prevent default newline behavior
        self.user_terminal.mark_set("insert", "end")
        self.user_terminal.see(tk.END)
        self.execute_last_query()
        self.user_terminal.insert(tk.END, "\n🍌_", "prompt")
        return "break"  # prevents a new line from being inserted

    def execute_last_query(self):
        content = self.user_terminal.get("1.0", tk.END).strip().split("\n")
        if not content:
            return
        last_line = content[-1].strip()
        if not last_line.startswith("🍌_"):
            unlock_terminal(self)
            self.terminal.insert(tk.END, "❌ No SQL command found on last line.\n", "error")
            lock_terminal(self)
            return
        query = last_line[len("🍌_"):].strip()

        try:
            if not database:
                unlock_terminal(self)
                self.terminal.insert(tk.END, "❌ Database name is required.\n", "error")
                lock_terminal(self)
                return
            conn = my.connect(host=host, user=user, password=pwd, database=database)
            cursor = conn.cursor()
            cursor.execute(query)

            # If it's a SELECT query
            if query.lower().strip().startswith("select"):
                rows = cursor.fetchall()
                for row in rows:
                    unlock_terminal(self)
                    self.terminal.insert(tk.END, f"{row}\n", "info")
                    lock_terminal(self)
            else:
                conn.commit()
                unlock_terminal(self)
                self.terminal.insert(tk.END, "✅ Query executed successfully.\n", "success")
                lock_terminal(self)

            cursor.close()
            conn.close()

        except my.Error as e:
            unlock_terminal(self)
            self.terminal.insert(tk.END, f"❌ Error: {e}\n", "error")
            lock_terminal(self)
        self.terminal.see(tk.END)
        self.user_terminal.see(tk.END)

def unlock_terminal(self):
    self.terminal.config(state=tk.NORMAL)
def lock_terminal(self):
    self.terminal.config(state=tk.DISABLED)
def start_move(event):
    root.x = event.x
    root.y = event.y

def do_move(event):
    x = root.winfo_pointerx() - root.x
    y = root.winfo_pointery() - root.y
    root.geometry(f'+{x}+{y}')

def close_window():
    root.destroy()

if __name__ == '__main__':
    from db_config import host, user, pwd, database
    root = tk.Tk()
    root.title("Banana SQL")
    root.geometry("1200x700+100+100")
    root.configure(bg="black")
    root.attributes('-alpha', 0.85)  # Set transparency
    root.overrideredirect(True)

    title_bar = tk.Frame(root, bg="#101010", relief="raised", bd=0, height=10, cursor="fleur")
    title_bar.pack(fill='both', side='top')

    # Title
    title_label = tk.Label(title_bar, text="Banana SQL", bg="#101010", fg="white", font=("Segoe UI", 10, "bold"))
    title_label.pack(side="left", padx=10)

    # Move window
    title_bar.bind("<ButtonPress-1>", start_move)
    title_bar.bind("<B1-Motion>", do_move)

    # Minimize and close buttons
    btn_close = tk.Button(title_bar, text="X", bg="red", fg="white", borderwidth=0, command=close_window,width=5, cursor="hand2")
    btn_close.pack(side="right")
    app = SQLApp(root)
# =================================================================================================== Set the terminal colors
    for _ in prompt_colors:
            app.terminal.tag_config(_, foreground=prompt_colors[_])
            app.user_terminal.tag_config(_, foreground=prompt_colors[_])
    root.mainloop()