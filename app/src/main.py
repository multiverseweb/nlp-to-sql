import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import Canvas
import mysql.connector as my
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from tabulate import tabulate
from matplotlib import cm
from matplotlib.colors import Normalize
from PIL import Image, ImageTk

RUNS_FILE = 'app/data/runs.txt'

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
        self.root.title("NLP to SQL")
        self.root.geometry("1000x700")
        self.root.configure(bg="black")
        self.version = "v1.0"
        self.run = f"Run {update_runs()}"
        self.status_color = "yellow"
        self.status_text = "Running"

        self.setup_ui()

    def setup_ui(self):

        # Top bar
        topbar = tk.Frame(self.root, bg="black", height=30)
        topbar.pack(fill=tk.X, side=tk.TOP)
        # Load and display logo
        logo_img = Image.open("app/resources/logo.png")
        logo_img = logo_img.resize((int(logo_img.width * (30 / logo_img.height)), 30), Image.Resampling.LANCZOS)
        self.logo_photo = ImageTk.PhotoImage(logo_img)

        logo_label = tk.Label(topbar, image=self.logo_photo, bg="#111")
        logo_label.pack(side=tk.LEFT, padx=10, pady=5)

        info = tk.Label(topbar, text=f"{self.version}  {self.run}", fg="white", bg="black", font=("Consolas", 10))
        info.pack(side=tk.RIGHT, padx=10)

        self.status_label = tk.Label(topbar, text=self.status_text, fg="black", bg=self.status_color, font=("Consolas", 10, "bold"))
        self.status_label.pack(side=tk.RIGHT, padx=10)

        # Input Frame
        input_frame = tk.Frame(self.root, bg="black")
        input_frame.pack(padx=20, pady=10, fill=tk.X)

        # Input Entries
        tk.Label(input_frame, text="Host", bg="black", fg="white", font=("Consolas", 10)).grid(row=0, column=0, padx=5, sticky="w")
        self.host_entry = tk.Entry(input_frame, fg="white", bg="#111", insertbackground='white')
        self.host_entry.insert(0, "localhost")
        self.host_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="User", bg="black", fg="white", font=("Consolas", 10)).grid(row=0, column=2, padx=5, sticky="w")
        self.user_entry = tk.Entry(input_frame, fg="white", bg="#111", insertbackground='white')
        self.user_entry.insert(0, "root")
        self.user_entry.grid(row=0, column=3, padx=5)

        tk.Label(input_frame, text="Password", bg="black", fg="white", font=("Consolas", 10)).grid(row=1, column=0, padx=5, sticky="w")
        self.pass_entry = tk.Entry(input_frame, fg="white", bg="#111", insertbackground='white', show="*")
        self.pass_entry.insert(0, "tejas123")
        self.pass_entry.grid(row=1, column=1, padx=5)

        tk.Label(input_frame, text="Database", bg="black", fg="white", font=("Consolas", 10)).grid(row=1, column=2, padx=5, sticky="w")
        self.db_entry = tk.Entry(input_frame, fg="white", bg="#111", insertbackground='white')
        self.db_entry.grid(row=1, column=3, padx=5)

        self.train_btn = tk.Button(input_frame, text="Train", command=self.connect_and_parse, bg="#222", fg="white", font=("Consolas", 10), bd=0)
        self.train_btn.grid(row=0, column=4, rowspan=2, padx=10)

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
        self.schema_area = tk.Text(left_frame, bg="#111", fg="white", font=("Consolas", 10),
                                bd=0, highlightbackground="gray", highlightcolor="gray", highlightthickness=1)
        self.schema_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.schema_gif = GIFPlayer(left_frame, "app/resources/loading.gif")
        self.schema_gif.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        # Terminal Frame in top-right
        self.terminal = tk.Text(right_frame, bg="#111", fg="white", font=("Consolas", 10), height=1,
                                bd=0, highlightbackground="gray", highlightcolor="gray", highlightthickness=1)
        self.terminal.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 5))

        self.terminal_gif = GIFPlayer(right_frame, "app/resources/loading.gif")
        self.terminal_gif.place(relx=0.5, rely=0.25, anchor=tk.CENTER)  # Adjust vertically if needed

        # Bar Graph Frame in bottom-right
        self.graph_frame = tk.Frame(right_frame, bg="#111", highlightbackground="gray", highlightthickness=1, height=300)
        self.graph_frame.pack(fill=tk.X, expand=False, padx=10, pady=(5, 10))

        self.graph_gif = GIFPlayer(self.graph_frame, "app/resources/loading.gif")
        self.graph_gif.place(relx=0.5, rely=0.5, anchor=tk.CENTER)



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
        host = self.host_entry.get()
        user = self.user_entry.get()
        password = self.pass_entry.get()
        database = self.db_entry.get()
        self.terminal.tag_config("prompt", foreground="yellow")
# Insert the prompt with the tag applied₹
        self.terminal.insert(tk.END, " 🍌_", "prompt")

        try:
            conn = my.connect(host=host, user=user, password=password, database=database)
            cursor = conn.cursor()
            self.status_color = "green"
            self.status_text = "Connected"
            self.status_label.config(bg=self.status_color, text=self.status_text)
            if cursor:
                self.schema_gif.destroy()
                self.terminal_gif.destroy()
                self.graph_gif.destroy()
                self.terminal.insert(tk.END, "Connection Successful!\n")
            self.show_schema(cursor)
            cursor.close()
            conn.close()
        except my.Error as e:
            self.status_color = "red"
            self.status_text = "Failed"
            self.status_label.config(bg=self.status_color, text=self.status_text)
            self.terminal.insert(tk.END, f"Database Connection Failed!\n{e}\n")

    def show_schema(self, cursor):
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        self.schema_area.delete(1.0, tk.END)

        bar_data_columns = {}
        bar_data_rows = {}

        for table in tables:
            cursor.execute("DESCRIBE " + table[0])
            columns = cursor.fetchall()
            self.schema_area.insert(tk.END, f"\nSchema of {table[0]}\n{tabulate(columns, headers=['Field', 'Type', 'Null', 'Key', 'Default', 'Extra'], tablefmt='pretty')}\n\n")
            
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

        fig, ax = plt.subplots(figsize=(5.5, 5), dpi=100)
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

        
if __name__ == '__main__':
    root = tk.Tk()
    app = SQLApp(root)
    root.mainloop()
