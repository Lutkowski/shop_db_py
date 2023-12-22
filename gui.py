import tkinter as tk
from tkinter import messagebox


class GUI:
    def __init__(self, database):
        self.db = database
        self.root = tk.Tk()
        self.root.title("Login")
        self.current_frame = None
        self.user_role = None
        self.user_id = None

    def create_login_view(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack()

        btn_login = tk.Button(self.current_frame, text="Login", command=self.show_login_fields)
        btn_login.pack()

        btn_register = tk.Button(self.current_frame, text="Register", command=self.show_register_fields)
        btn_register.pack()

    def show_login_fields(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack()

        label_email = tk.Label(self.current_frame, text="Email:")
        label_email.pack()

        entry_email = tk.Entry(self.current_frame)
        entry_email.pack()

        label_password = tk.Label(self.current_frame, text="Password:")
        label_password.pack()

        entry_password = tk.Entry(self.current_frame, show="*")
        entry_password.pack()

        btn_login = tk.Button(self.current_frame, text="Login",
                              command=lambda: self.authenticate_user(entry_email.get(), entry_password.get()))
        btn_login.pack()

        btn_back = tk.Button(self.current_frame, text="Back", command=self.create_login_view)
        btn_back.pack()

    def show_register_fields(self):
        if self.current_frame:
            self.current_frame.destroy()

        self.current_frame = tk.Frame(self.root)
        self.current_frame.pack()

        label_email = tk.Label(self.current_frame, text="Email:")
        label_email.pack()

        entry_email = tk.Entry(self.current_frame)
        entry_email.pack()

        label_username = tk.Label(self.current_frame, text="Username:")
        label_username.pack()

        entry_username = tk.Entry(self.current_frame)
        entry_username.pack()

        label_password = tk.Label(self.current_frame, text="Password:")
        label_password.pack()

        entry_password = tk.Entry(self.current_frame, show="*")
        entry_password.pack()

        btn_register = tk.Button(self.current_frame, text="Register",
                                 command=lambda: self.register_user(entry_email.get(), entry_username.get(),
                                                                    entry_password.get()))
        btn_register.pack()

        btn_back = tk.Button(self.current_frame, text="Back", command=self.create_login_view)
        btn_back.pack()

    def authenticate_user(self, email, password):
        if not email or not password:
            messagebox.showerror("Login Failed", "Please enter both email and password")
            return

        authenticated = self.db.authenticate_user(email, password)
        if authenticated:
            messagebox.showinfo("Login Successful", "Welcome, {}".format(email))
            self.user_id = self.db.get_user_id_by_email(email)
            print(self.user_id)
            if email == "adm@ya.ru" and password == "admpass":
                print("hello admin")
                self.user_role = "admin"
            else:
                self.user_role = "customer"
        else:
            messagebox.showerror("Login Failed", "Invalid email or password")

    def register_user(self, email, username, password):
        if not email or not username or not password:
            messagebox.showerror("Registration Failed", "Please enter email, username, and password")
            return

        try:
            self.db.register_user(username, email, password, 'customer')
            messagebox.showinfo("Registration Successful", "User {} registered successfully".format(username))
            self.create_login_view()
        except Exception as e:
            messagebox.showerror("Registration Failed", str(e))

    def run(self):
        self.create_login_view()
        self.root.mainloop()
