from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

# ------------------- DATABASE -------------------
def connect_db():
    with sqlite3.connect("student.db", timeout=10) as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS student(
                roll INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT,
                gender TEXT,
                contact TEXT,
                dob TEXT,
                address TEXT
            )
        """)

# ------------------- FUNCTIONS -------------------
def add_student():
    if roll.get() == "" or name.get() == "":
        messagebox.showerror("Error", "All fields required")
        return

    try:
        with sqlite3.connect("student.db", timeout=10) as conn:
            cur = conn.cursor()

            cur.execute("SELECT * FROM student WHERE roll=?", (roll.get(),))
            if cur.fetchone():
                messagebox.showerror("Error", "Roll No already exists")
                return

            cur.execute("INSERT INTO student VALUES (?,?,?,?,?,?,?)", (
                roll.get(),
                name.get(),
                email.get(),
                gender.get(),
                contact.get(),
                dob.get(),
                address.get()
            ))

        messagebox.showinfo("Success", "Student Added Successfully")

    except Exception as e:
        messagebox.showerror("Error", str(e))

    show_data()
    clear_data()

def show_data():
    with sqlite3.connect("student.db", timeout=10) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM student")
        rows = cur.fetchall()

        table.delete(*table.get_children())
        for row in rows:
            table.insert('', END, values=row)

def clear_data():
    roll.set("")
    name.set("")
    email.set("")
    gender.set("")
    contact.set("")
    dob.set("")
    address.set("")

def get_data(ev):
    cursor_row = table.focus()
    content = table.item(cursor_row)
    row = content['values']
    if row:
        roll.set(row[0])
        name.set(row[1])
        email.set(row[2])
        gender.set(row[3])
        contact.set(row[4])
        dob.set(row[5])
        address.set(row[6])

def update_student():
    try:
        with sqlite3.connect("student.db", timeout=10) as conn:
            cur = conn.cursor()
            cur.execute("""UPDATE student SET name=?,email=?,gender=?,contact=?,dob=?,address=? WHERE roll=?""",
                        (name.get(), email.get(), gender.get(), contact.get(), dob.get(), address.get(), roll.get()))
        messagebox.showinfo("Success", "Student Updated")

    except Exception as e:
        messagebox.showerror("Error", str(e))

    show_data()
    clear_data()

def delete_student():
    try:
        with sqlite3.connect("student.db", timeout=10) as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM student WHERE roll=?", (roll.get(),))
        messagebox.showinfo("Success", "Student Deleted")

    except Exception as e:
        messagebox.showerror("Error", str(e))

    show_data()
    clear_data()

def search_student():
    with sqlite3.connect("student.db", timeout=10) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM student WHERE name LIKE ?", ('%'+search_txt.get()+'%',))
        rows = cur.fetchall()

        table.delete(*table.get_children())
        for row in rows:
            table.insert('', END, values=row)

# ------------------- UI -------------------
root = Tk()
root.title("Student Management System")
root.geometry("1100x600")
root.config(bg="#e6f2ff")

connect_db()

# Variables
roll = StringVar()
name = StringVar()
email = StringVar()
gender = StringVar()
contact = StringVar()
dob = StringVar()
address = StringVar()
search_txt = StringVar()

# Title
Label(root, text="Student Management System", font=("Arial", 25, "bold"),
      bg="#007acc", fg="white").pack(fill=X)

# Left Frame
frame1 = Frame(root, bd=4, relief=RIDGE, bg="white")
frame1.place(x=10, y=70, width=400, height=520)

Label(frame1, text="Manage Students", font=("Arial", 18, "bold"),
      bg="white").grid(row=0, columnspan=2, pady=10)

# Fields
labels = ["Roll No", "Name", "Email", "Gender", "Contact", "D.O.B", "Address"]
variables = [roll, name, email, gender, contact, dob, address]

for i, label in enumerate(labels):
    Label(frame1, text=label, font=("Arial", 12),
          bg="white").grid(row=i+1, column=0, pady=6, padx=10, sticky="w")

    if label == "Gender":
        combo = ttk.Combobox(frame1, textvariable=gender,
                             state="readonly", font=("Arial", 12))
        combo['values'] = ("Male", "Female", "Other")
        combo.grid(row=i+1, column=1, pady=6, padx=10)
    else:
        Entry(frame1, textvariable=variables[i],
              font=("Arial", 12)).grid(row=i+1, column=1, pady=6, padx=10)

# Buttons
btn_frame = Frame(frame1, bg="white")
btn_frame.grid(row=9, columnspan=2, pady=15)

Button(btn_frame, text="Add", width=10, bg="#28a745", fg="white",
       command=add_student).grid(row=0, column=0, padx=5)
Button(btn_frame, text="Update", width=10, bg="#007bff", fg="white",
       command=update_student).grid(row=0, column=1, padx=5)
Button(btn_frame, text="Delete", width=10, bg="#dc3545", fg="white",
       command=delete_student).grid(row=0, column=2, padx=5)
Button(btn_frame, text="Clear", width=10, bg="#6c757d", fg="white",
       command=clear_data).grid(row=0, column=3, padx=5)

# Right Frame
frame2 = Frame(root, bd=4, relief=RIDGE, bg="white")
frame2.place(x=420, y=70, width=660, height=520)

Label(frame2, text="Search Name:", bg="white",
      font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)

Entry(frame2, textvariable=search_txt,
      font=("Arial", 12)).grid(row=0, column=1, padx=10)

Button(frame2, text="Search", bg="#17a2b8", fg="white",
       command=search_student).grid(row=0, column=2, padx=5)

Button(frame2, text="Show All", bg="#343a40", fg="white",
       command=show_data).grid(row=0, column=3, padx=5)

# Table
table = ttk.Treeview(frame2,
                     columns=("roll", "name", "email", "gender", "contact", "dob", "address"),
                     show='headings')

for col in ("roll", "name", "email", "gender", "contact", "dob", "address"):
    table.heading(col, text=col)
    table.column(col, width=90)

table.grid(row=1, columnspan=4, padx=10, pady=10)

table.bind("<ButtonRelease-1>", get_data)

show_data()

root.mainloop()