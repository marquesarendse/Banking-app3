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
        self.master.title("Banking Application")
        self.master.geometry("500x500")
        
        self.current_user = None

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
        self.transaction_type_frame = tk.Frame(self.master, bg="white",)

        self.transaction_type_label = tk.Label(self.transaction_type_frame, text="Would you like to make a deposit or withdrawal? (Deposit/Withdrawal)", font=("Helvetica", 12), bg="white")
        self.transaction_type_label.pack()

        self.transaction_type_entry = tk.Entry(self.transaction_type_frame, font=("Helvetica", 12), highlightbackground="black", highlightthickness=2)
        self.transaction_type_entry.pack()

        self.transaction_type_button = tk.Button(self.transaction_type_frame, text="Submit", command=self.choose_transaction_type, font=("Helvetica", 12))
        self.transaction_type_button.pack(padx=10, pady=5)

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

    def generate_new_password(self):
        characters = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
        new_password = ''.join(random.choice(characters) for i in range(12))
        return new_password

    def update_user_password(self, username, new_password):
        updated_data = []
        try:
            with open("user_data.txt", "r") as file:
                for line in file:
                    stored_username, stored_surname, stored_password, stored_dob = line.strip().split(",")
                    if stored_username == username:
                        updated_data.append(f"{stored_username},{stored_surname},{new_password},{stored_dob}\n")
                    else:
                        updated_data.append(line)
            with open("user_data.txt", "w") as file:
                file.writelines(updated_data)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while updating the password: {str(e)}")

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
        
