import mysql.connector as my                           #  +-------------------+
import tkinter as tk                                   #  |  Tejas' Codes :)  |
from tkinter import messagebox                         #  +-------------------+
from tabulate import tabulate

def init():
    #root = tk.Tk()

    #host = input("Enter your MySQL localhost name: ")
    #name = input("Enter your MySQL username: ")
    #password = input("Enter your MySQL password: ")
    database = input("Enter database name: ")

    try:
        conn = my.connect(host="localhost", user="root", password="tejas123", database=database)
        cursor = conn.cursor()
        print("Connection Successful!")
        parse(conn, cursor)
    
    except my.Error as e:
        print("Error", f"Database Connection Failed!\n{e}")
    cursor.close()
    conn.close()

def parse(con, cursor):
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    for table in tables:
        cursor.execute("DESCRIBE " + table[0])
        columns = cursor.fetchall()
        print(f"\n=========================Schema of {table[0]}========================")
        print(tabulate(columns, headers=['Field', 'Type', 'Null', 'Key', 'Default', 'Extra'],tablefmt="pretty"))

init()
