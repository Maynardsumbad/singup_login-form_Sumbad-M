import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageFilter # type: ignore
import sqlite3

# Initialize Database
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Signup Function
def signup():
    username = signup_username.get()
    password = signup_password.get()
    
    if not username or not password:
        messagebox.showerror("Error", "All fields are required")
        return
    
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Signup Successful!")
        signup_window.destroy()
    except sqlite3.IntegrityError:
        messagebox.showerror("Error", "Username already exists")

# Login Function
def login():
    username = login_username.get()
    password = login_password.get()
    
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        messagebox.showinfo("Success", "Login Successful!")
    else:
        messagebox.showerror("Error", "Invalid Credentials")

# GUI Setup
init_db()
root = tk.Tk()
root.title("Login Form")
root.geometry("400x350")

# Load and Blur Background Image
bg_image = Image.open("bg.jpg")  # Change to your image file
bg_image = bg_image.resize((400, 350), Image.Resampling.LANCZOS)  # Resize to match window
bg_image = bg_image.filter(ImageFilter.GaussianBlur(8))  # Apply Blur
bg_photo = ImageTk.PhotoImage(bg_image)

# Set Canvas for Background
canvas = tk.Canvas(root, width=400, height=350)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")  # Place background image

# Login Frame (Floating Effect)
login_frame = tk.Frame(root, bg="white", bd=5, relief="ridge")
login_frame.place(relx=0.5, rely=0.5, anchor="center", width=280, height=180)

tk.Label(login_frame, text="Username:", font=("Arial", 12), bg="white").pack(pady=5)
login_username = tk.Entry(login_frame, font=("Arial", 12))
login_username.pack(pady=2)

tk.Label(login_frame, text="Password:", font=("Arial", 12), bg="white").pack(pady=5)
login_password = tk.Entry(login_frame, show="*", font=("Arial", 12))
login_password.pack(pady=2)

tk.Button(login_frame, text="Login", command=login, font=("Arial", 12), bg="#3498DB", fg="white", padx=10, pady=5).pack(pady=10)

# Signup Window
def open_signup():
    global signup_window, signup_username, signup_password
    signup_window = tk.Toplevel(root)
    signup_window.title("Signup Form")
    signup_window.geometry("300x200")
    
    tk.Label(signup_window, text="Username:", font=("Arial", 12)).pack(pady=5)
    signup_username = tk.Entry(signup_window, font=("Arial", 12))
    signup_username.pack(pady=2)
    
    tk.Label(signup_window, text="Password:", font=("Arial", 12)).pack(pady=5)
    signup_password = tk.Entry(signup_window, show="*", font=("Arial", 12))
    signup_password.pack(pady=2)
    
    tk.Button(signup_window, text="Signup", command=signup, font=("Arial", 12), bg="#27AE60", fg="white", padx=10, pady=5).pack(pady=10)

tk.Button(root, text="Signup", command=open_signup, font=("Arial", 12), bg="#E74C3C", fg="white", padx=10, pady=5).place(relx=0.5, rely=0.85, anchor="center")

root.mainloop()
