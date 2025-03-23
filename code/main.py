import mysql.connector as my
from tkinter import messagebox

def init():
    host = input("Enter your MySQL localhost name: ")
    name = input("Enter your MySQL username: ")
    password = input("Enter your MySQL password: ")

    try:
        conn = my.connect(host=host, user=name, password=password, database="numis")
        cursor = conn.cursor()
        messagebox.showinfo("Success", "Connection Successful!")
        cursor.close()
        conn.close()
    
    except my.Error as e:
        messagebox.showerror("Error", f"Database Connection Failed!\n{e}")
        
init()
