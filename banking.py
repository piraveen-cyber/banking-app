import os
import random
from datetime import datetime

accounts = {}  # Dictionary to store accounts

# Ensure transaction directory exists
if not os.path.exists("transactions"):
    os.makedirs("transactions")

def verify_admin():
    print("🔐 Welcome Admin! Please login")
    correct_id = "admin123"
    for attempt in range(3):
        admin_id = input("🪪 Enter Admin ID: ")
        if admin_id == correct_id:
            print("✅ Access Granted\n")
            return True
        else:
            print(f"❌ Invalid ID. Attempts left: {2 - attempt}")
    print("🔒 Access Denied")
    return False

def generate_account_number():
    return "ACC" + str(random.randint(10000000, 99999999))

def generate_customer_id():
    return "cus" + str(random.randint(10000000, 99999999))

def create_account():
    try:
        name = input("👤 Enter Name: ")
        age = input("🎂 Enter Age: ")
        phone = input("📱 Enter 10-digit Phone Number: ")
        nic = input("🆔 Enter NIC: ")
        username = input("👥 Create Username: ")
        password = input("🔑 Create Password: ")

        if not (age.isdigit() and int(age) > 0):
            print("❗ Invalid Age")
            return
        if not (phone.isdigit() and len(phone) == 10):
            print("❗ Phone must be 10 digits")
            return

        cus_id = generate_customer_id()
        acc_num = generate_account_number()

        while acc_num in accounts:
            acc_num = generate_account_number()
        while any(acc.get("customer_id") == cus_id for acc in accounts.values()):
            cus_id = generate_customer_id()

        account_data = {
            "name": name,
            "age": int(age),
            "phone": int(phone),
            "nic": nic,
            "balance": 0,
            "transactions": [],
            "username": username,
            "password": password,
            "customer_id": cus_id
        }

        accounts[acc_num] = account_data

        # Save transaction log
        with open(f"transactions/{acc_num}.txt", "w") as f:
            f.write("Account created.\n")

        # Save user credentials 
        user_data = {
            "username": username,
            "password": password,
            "customer_id": cus_id
        }
        with open("user.txt", "a") as f_user:
            f_user.write(str(user_data) + "\n")

        # Save account details 
        account_data_to_save = {
            "account_number": acc_num,
            "customer_id": cus_id,
            "name": name,
            "age": int(age),
            "phone": int(phone),
            "nic": nic,
            "balance": 0
        }
        with open("account.txt", "a") as f_acc:
            f_acc.write(str(account_data_to_save) + "\n")

        print(f"🎉 Account Created Successfully!\nAccount Number: {acc_num}\nCustomer ID: {cus_id}")

    except Exception as e:
        print("⚠️ Error:", e)

def login_customer():
    username = input("👥 Enter Username: ")
    password = input("🔑 Enter Password: ")
    for acc_num, data in accounts.items():
        if data["username"] == username and data["password"] == password:
            print("✅ Login Successful!\n")
            return acc_num
    print("❌ Invalid credentials.")
    return None

def deposit(acc_num):
    try:
        amount = float(input("💰 Enter amount to deposit: "))
        if amount < 100:
            print("❗ Amount must be at least 100.")
            return
        accounts[acc_num]["balance"] += amount
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"{timestamp} - Deposited: {amount}"
        accounts[acc_num]["transactions"].append(message)
        with open(f"transactions/{acc_num}.txt", "a") as f:
            f.write(message + "\n")
        print("✅ Deposit Successful.")
    except Exception:
        print("⚠️ Invalid input.")

def withdraw(acc_num):
    try:
        amount = float(input("💸 Enter amount to withdraw: "))
        if amount <= 0:
            print("❗ Must be positive.")
            return
        if accounts[acc_num]["balance"] < amount:
            print("❌ Insufficient balance.")
            return
        accounts[acc_num]["balance"] -= amount
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"{timestamp} - Withdrew: {amount}"
        accounts[acc_num]["transactions"].append(message)
        with open(f"transactions/{acc_num}.txt", "a") as f:
            f.write(message + "\n")
        print("✅ Withdrawal Successful.")
    except Exception:
        print("⚠️ Invalid input.")

def check_balance(acc_num):
    print(f"💳 Current Balance: {accounts[acc_num]['balance']}")

def view_transactions(acc_num):
    path = f"transactions/{acc_num}.txt"
    print("\n📜 Transaction History:")
    if os.path.exists(path):
        with open(path, "r") as f:
            print(f.read())
    else:
        print("❗ No transaction file found.")

def customer_menu(acc_num):
    while True:
        print(f"\n🏦 Welcome {accounts[acc_num]['name']} ({acc_num})")
        print("""
 1️⃣  Deposit
 2️⃣  Withdraw
 3️⃣  Check Balance
 4️⃣  View Transactions
 5️⃣  Logout
        """)
        choice = input("👉 Choose: ")
        if choice == "1":
            deposit(acc_num)
        elif choice == "2":
            withdraw(acc_num)
        elif choice == "3":
            check_balance(acc_num)
        elif choice == "4":
            view_transactions(acc_num)
        elif choice == "5":
            print("🔓 Logged out.")
            break
        else:
            print("❌ Invalid choice.")

def main_menu():
    print("\n🧾 Mini Banking App")
    while True:
        print(""" 📋 Main Menu:
1️⃣  Create Account
2️⃣  Customer Login
3️⃣  Exit
        """)
        choice = input("👉 Enter your choice: ")
        if choice == "1":
            create_account()
        elif choice == "2":
            acc = login_customer()
            if acc:
                customer_menu(acc)
        elif choice == "3":
            print("👋 Exiting... Thank you!")
            break
        else:
            print("❌ Invalid option")

if __name__ == "__main__":
    if verify_admin():
        main_menu()
