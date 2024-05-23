import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os
from PIL import Image, ImageTk
import random
import string

class BankingApplication:
    def __init__(self, master):
        self.master = master
        self.master.title("PocketGuard")
        self.master.geometry("500x500")
        
        self.current_user = None
        self.navigation_stack = []

        # Initialize balance
        self.balance = 0.0

        # Initialize login/register frame
        self.login_register_frame = tk.Frame(self.master, bg="white")
        self.login_register_frame.pack(fill=tk.BOTH, expand=True)
        
        # Load and place the logo
        self.logo_image = Image.open("Image/logo.png")
        self.logo_image = self.logo_image.resize((200, 200))
        self.logo_photo = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(self.login_register_frame, image=self.logo_photo, bg="white")
        self.logo_label.grid(row=0, column=6, columnspan=2, padx=10, pady=10, sticky='w')

        input_row = 1

        self.username_label = tk.Label(self.login_register_frame, text="Username:", font=("Helvetica", 12), bg="white", fg='black')
        self.username_label.grid(row=input_row, column=4, padx=10, pady=5, sticky='e')

        self.username_entry = tk.Entry(self.login_register_frame, font=("Helvetica", 12), highlightbackground="black", highlightthickness=2)
        self.username_entry.grid(row=input_row, column=6, padx=10, pady=5, sticky='w')

        input_row += 1

        self.password_label = tk.Label(self.login_register_frame, text="Password:", font=("Helvetica", 12), bg="white", fg='black')
        self.password_label.grid(row=input_row, column=4, padx=10, pady=5, sticky='e')

        self.password_entry = tk.Entry(self.login_register_frame, show="*", font=("Helvetica", 12), highlightbackground="black", highlightthickness=2)
        self.password_entry.grid(row=input_row, column=6, padx=10, pady=5, sticky='w')

        input_row += 1

        self.login_button = tk.Button(self.login_register_frame, text="Login", command=self.login, font=("Helvetica", 12))
        self.login_button.grid(row=input_row, column=6, columnspan=2, padx=10, pady=5)

        input_row += 1

        self.register_button = tk.Button(self.login_register_frame, text="Register", command=self.show_register_screen, font=("Helvetica", 12))
        self.register_button.grid(row=input_row, column=6, columnspan=2, padx=10, pady=5)
        
        # Initialize registration frame
        self.register_frame = tk.Frame(self.master, bg="white", highlightbackground="black", highlightthickness=2)

        self.name_label = tk.Label(self.register_frame, text="Name:", font=("Helvetica", 12), bg="white")
        self.name_label.grid(row=0, column=0, padx=10, pady=5)

        self.name_entry = tk.Entry(self.register_frame, font=("Helvetica", 12), bg="white", highlightbackground="black", highlightthickness=2)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        self.surname_label = tk.Label(self.register_frame, text="Surname:", font=("Helvetica", 12), bg="white")
        self.surname_label.grid(row=1, column=0, padx=10, pady=5)

        self.surname_entry = tk.Entry(self.register_frame, font=("Helvetica", 12), bg="white", highlightbackground="black", highlightthickness=2)
        self.surname_entry.grid(row=1, column=1, padx=10, pady=5)

        self.password_label_reg = tk.Label(self.register_frame, text="Password:", font=("Helvetica", 12), bg="white")
        self.password_label_reg.grid(row=2, column=0, padx=10, pady=5)

        self.password_entry_reg = tk.Entry(self.register_frame, show="*", font=("Helvetica", 12), highlightbackground="black", highlightthickness=2)
        self.password_entry_reg.grid(row=2, column=1, padx=10, pady=5)

        self.dob_label = tk.Label(self.register_frame, text="Date of Birth (YYYY-MM-DD):", font=("Helvetica", 12), bg="white")
        self.dob_label.grid(row=3, column=0, padx=10, pady=5)

        self.dob_entry = tk.Entry(self.register_frame, font=("Helvetica", 12), bg="white", highlightbackground="black", highlightthickness=2)
        self.dob_entry.grid(row=3, column=1, padx=10, pady=5)

        self.register_submit_button = tk.Button(self.register_frame, text="Register", command=self.register, font=("Helvetica", 12))
        self.register_submit_button.grid(row=4, column=0, columnspan=2, padx=10, pady=5)
        
        # Password generator button
        self.generate_password_button = tk.Button(self.register_frame, text="Generate Password", command=self.generate_password, font=("Helvetica", 12))
        self.generate_password_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        # Back button for registration frame
        self.register_back_button = tk.Button(self.register_frame, text="Back", command=self.go_back, font=("Helvetica", 12))
        self.register_back_button.grid(row=6, column=0, columnspan=2, padx=10, pady=5)
        
        # Hide registration frame initially
        self.register_frame.pack_forget()

        # Initialize transaction frame
        self.transaction_frame = tk.Frame(self.master, bg="white")

        self.balance_label = tk.Label(self.transaction_frame, text="Balance: R0.00", font=("Helvetica", 12), bg="white")
        self.balance_label.pack(padx=10, pady=5)

        self.view_transactions_button = tk.Button(self.transaction_frame, text="View Transactions", command=self.view_transactions, font=("Helvetica", 12))
        self.view_transactions_button.pack(padx=10, pady=5)

        self.transaction_prompt_button = tk.Button(self.transaction_frame, text="Make a Transaction", command=self.show_transaction_type_screen, font=("Helvetica", 12))
        self.transaction_prompt_button.pack(padx=10, pady=5)

        self.logout_button = tk.Button(self.transaction_frame, text="Logout", command=self.logout, font=("Helvetica", 12))
        self.logout_button.pack(padx=10, pady=5)
        
        # Hide transaction frame initially
        self.transaction_frame.pack_forget()

        # Initialize transaction type frame
        self.transaction_type_frame = tk.Frame(self.master, bg="white")

        self.transaction_type_label = tk.Label(self.transaction_type_frame, text="Would you like to make a deposit or withdrawal? (Deposit/Withdrawal)", font=("Helvetica", 12), bg="white")
        self.transaction_type_label.pack()

        self.transaction_type_entry = tk.Entry(self.transaction_type_frame, font=("Helvetica", 12), highlightbackground="black", highlightthickness=2)
        self.transaction_type_entry.pack()

        self.transaction_type_button = tk.Button(self.transaction_type_frame, text="Submit", command=self.choose_transaction_type, font=("Helvetica", 12))
        self.transaction_type_button.pack(padx=10, pady=5)

        # Back button for transaction type frame
        self.transaction_type_back_button = tk.Button(self.transaction_type_frame, text="Back", command=self.go_back, font=("Helvetica", 12))
        self.transaction_type_back_button.pack(padx=10, pady=5)
        
        # Hide transaction type frame initially
        self.transaction_type_frame.pack_forget()

        # Initialize amount frame
        self.amount_frame = tk.Frame(self.master, bg="white")

        self.amount_label = tk.Label(self.amount_frame, text="Enter amount:", font=("Helvetica", 12), bg="white")
        self.amount_label.pack()

        self.amount_entry = tk.Entry(self.amount_frame, font=("Helvetica", 12), highlightbackground="black", highlightthickness=2)
        self.amount_entry.pack()

        self.amount_button = tk.Button(self.amount_frame, text="Submit", command=self.perform_transaction, font=("Helvetica", 12))
        self.amount_button.pack(padx=10, pady=5)

        # Hide amount frame initially
        self.amount_frame.pack_forget()

    def load_balance(self):
        try:
            with open("BankData.txt", "r") as file:
                for line in file:
                    username, balance = line.strip().split(":")
                    if username == self.current_user:
                        self.balance = float(balance)
                        break
            self.update_balance_label()
        except FileNotFoundError:
            self.balance = 0.0
        except ValueError:
            self.balance = 0.0

    def save_balance(self):
        data = []
        if os.path.exists("BankData.txt"):
            with open("BankData.txt", "r") as file:
                data = file.readlines()
        
        with open("BankData.txt", "w") as file:
            user_found = False
            for line in data:
                username, balance = line.strip().split(":")
                if username == self.current_user:
                    file.write(f"{self.current_user}:{self.balance:.2f}\n")
                    user_found = True
                else:
                    file.write(line)
            if not user_found:
                file.write(f"{self.current_user}:{self.balance:.2f}\n")

    def log_transaction(self, username, transaction):
        with open("transactionLog.txt", "a") as file:
            file.write(f"{username}: {transaction}\n")

    def show_frame(self, frame):
        # Hide all frames before showing the new one
        for widget in self.master.winfo_children():
            widget.pack_forget()
        frame.pack()

    def show_transaction_screen(self):
        self.show_frame(self.transaction_frame)
        self.update_balance_label()

    def show_register_screen(self):
        self.navigation_stack.append(self.login_register_frame)
        self.show_frame(self.register_frame)

    def show_transaction_type_screen(self):
        self.navigation_stack.append(self.transaction_frame)
        self.show_frame(self.transaction_type_frame)

    def go_back(self):
        if self.navigation_stack:
            self.show_frame(self.navigation_stack.pop())

    def update_balance_label(self):
        self.balance_label.config(text="Balance: R{:.2f}".format(self.balance))

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.is_user_registered(username, password):
            messagebox.showinfo("Login", "Login successful!")
            self.current_user = username
            self.load_balance()
            self.navigation_stack.append(self.login_register_frame)
            self.show_transaction_screen()
        else:
            messagebox.showerror("Login Error", "Invalid username or password.")

    def is_user_registered(self, username, password):
        try:
            with open("user_data.txt", "r") as file:
                for line in file:
                    stored_username, stored_surname, stored_password, stored_dob = line.strip().split(",")
                    if username == stored_username and password == stored_password:
                        return True
        except FileNotFoundError:
            messagebox.showerror("File Error", "User data file not found")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        return False

    def register(self):
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        password = self.password_entry_reg.get()
        dob_str = self.dob_entry.get()

        if name and surname and password and dob_str:
            try:
                dob = datetime.strptime(dob_str, '%Y-%m-%d')
            except ValueError:
                messagebox.showerror("Register Error", "Invalid Date of Birth format. Please use YYYY-MM-DD.")
                return

            today = datetime.today()
            age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

            if age >= 16:
                with open("user_data.txt", "a") as file:
                    file.write(f"{name},{surname},{password},{dob_str}\n")
                messagebox.showinfo("Register", "Registration successful!")
                self.name_entry.delete(0, tk.END)
                self.surname_entry.delete(0, tk.END)
                self.password_entry_reg.delete(0, tk.END)
                self.dob_entry.delete(0, tk.END)
                self.go_back()
            else:
                messagebox.showerror("Register Error", "You must be at least 16 years old to register.")
        else:
            messagebox.showerror("Register Error", "Please fill in all fields.")

    def choose_transaction_type(self):
        self.transaction_type = self.transaction_type_entry.get().strip().lower()
        if self.transaction_type in ['deposit', 'withdrawal']:
            self.navigation_stack.append(self.transaction_type_frame)
            self.show_frame(self.amount_frame)
        else:
            messagebox.showerror("Input Error", "You provided an invalid input.")

    def perform_transaction(self):
        try:
            amount = float(self.amount_entry.get())
            if self.transaction_type == 'deposit':
                self.balance += amount
                transaction_details = f"Deposit: R{amount:.2f} on {datetime.now()}"
            elif self.transaction_type == 'withdrawal':
                if amount > self.balance:
                    messagebox.showerror("Transaction Error", "Insufficient funds for withdrawal.")
                    return
                self.balance -= amount
                transaction_details = f"Withdrawal: R{amount:.2f} on {datetime.now()}"
            self.log_transaction(self.current_user, transaction_details)
            self.update_balance_label()
            self.save_balance()
            messagebox.showinfo("Transaction Successful", f"Transaction successful! New balance: R{self.balance:.2f}")
        except ValueError:
            messagebox.showerror("Input Error", "You provided an invalid input.")
        self.amount_entry.delete(0, tk.END)
        self.go_back()

    def view_transactions(self):
        try:
            with open("transactionLog.txt", "r") as file:
                transactions = [line.strip() for line in file.readlines() if line.startswith(f"{self.current_user}:")]
                if transactions:
                    transaction_history = "\n".join(transactions)
                    messagebox.showinfo("Transaction Log", transaction_history)
                else:
                    messagebox.showinfo("Transaction Log", "No transactions found.")
        except FileNotFoundError:
            messagebox.showerror("Error", "Transaction log file not found.")

    def logout(self):
        self.current_user = None
        self.navigation_stack = []
        self.show_frame(self.login_register_frame)

    def generate_password(self):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.sample(characters, 12))
        self.password_entry_reg.delete(0, tk.END)
        self.password_entry_reg.insert(0, password)

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg='white')
    app = BankingApplication(root)
    root.mainloop()
