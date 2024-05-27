#########################################
#TshewangNima
#Electronics and communications engineering
#02230114
##########################################
#REFERENCES
#https://www.freecodecamp.org/news/how-to-build-an-online-banking-system-python-oop-tutorial/
#https://www.geeksforgeeks.org/python-program-to-create-bankaccount-class-with-deposit-withdraw-function/
############################################


import os
import random

# Created a basic account class with shared features and functions
class Account:
    def __init__(self, acc_num, password, acc_type, balance=0):
        self.account_number = acc_num
        self.password = password
        self.account_type = acc_type
        self.balance = balance  # Initial balance, default is 0

    # method to deposit money after an account is created
    def Deposit(self, amount):
        self.balance += amount  # Increasing the balance by the deposited amount
        print(f"Nu.{amount} is deposited successfully. Your new balance is Nu.{self.balance}")

    # method to withdraw money from the account
    def Withdraw(self, amount):
        if self.balance >= amount:  # Checking the balance before withdrawing
            self.balance -= amount
            print(f"Nu.{amount} is withdrawn successfully. Your new balance is Nu.{self.balance}")
        else:
            print("Sorry, your account has insufficient balance.")

    # method to check current existing balance
    def Checkbalance(self):
        print(f"Your current balance: Nu.{self.balance}")

    # method to save account details into the file
    def Save_to_file(self):
        with open("accounts.txt", "a") as f:
            f.write(f"{self.account_number},{self.password},{self.account_type},{self.balance}\n")

# Created a subclass for Personal Accounts
class PersonalAcc(Account):
    def __init__(self, acc_num, password, balance=0):
        # initialized the base class with 'Personal' account type
        super().__init__(acc_num, password, 'Personal', balance)

# Created a subclass for Business Accounts
class BusinessAcc(Account):
    def __init__(self, acc_num, password, balance=0):
        # Similar to the earlier one, initialized the base class with 'Business' account type
        super().__init__(acc_num, password, 'Business', balance)

# Create a function that reads accounts from a file and gives back a dictionary containing account objects.
def Read_acc_from_file():
    # Initialize an empty dictionary to store accounts
    accounts = {}
    if os.path.exists("accounts.txt"):  # checking if the file exists or not
        with open("accounts.txt", "r") as f:
            for line in f:  # iterating through each line in the file
                account_number, password, account_type, balance = line.strip().split(',')
                balance = float(balance)
                if account_type == 'Personal':
                    account = PersonalAcc(account_number, password, balance)  # Creating a PersonalAcc object
                elif account_type == 'Business':
                    account = BusinessAcc(account_number, password, balance)  # Creating a BusinessAcc object
                accounts[account_number] = account
    return accounts

# created a function to log in an existing user
def Login(accounts):
    acc_number = input("Enter your account number: ")
    password = input("Enter your password: ")
    account = accounts.get(acc_number)
    # checking if the account exists and the given password is correct
    if account and account.password == password:
        print("Login successful!")
        return account
    else:
        print("Invalid account number or password. Try again.")
        return None  # returns None if login failed

# created a function to create a new account
def create_account(accounts):
    # generates a random 6-digit account number
    acc_number = str(random.randint(100000, 999999))
    password = str(random.randint(1000, 9999))
    print(f"Your new account number is: {acc_number}")
    print(f"Your default password is: {password}")
    acc_type = input("Enter account type (Personal/Business): ").lower()
    if acc_type in ['personal', 'p']:
        # creates a PersonalAccount object
        account = PersonalAcc(acc_number, password)
    elif acc_type in ['business', 'b']:
        # creates a BusinessAccount object
        account = BusinessAcc(acc_number, password)
    else:
        print("Invalid account type.")
        return
    # adding the account object to the created dictionary
    accounts[acc_number] = account
    # saves the account details to the file
    account.Save_to_file()
    print("Your account has created successfully!")

# created a function to delete an account
def del_account(accounts, account):
    del accounts[account.account_number]
    with open("accounts.txt", "w") as f:
        for acc in accounts.values():
            # updates each account's details to the file
            f.write(f"{acc.account_number},{acc.password},{acc.account_type},{acc.balance}\n")
    print("Your account has deleted successfully!")

# created a function to transfer money between accounts
def transfer_money(accounts, sender):
    receiver_acc_number = input("Please enter the receiver's account number: ")
    amount = float(input("Enter the amount to transfer: "))
    # Retrieve receiver's account object from the dictionary
    receiver = accounts.get(receiver_acc_number)
    # checking if the receiver's account exists
    if receiver:
        if sender.balance >= amount:
            sender.Withdraw(amount)
            receiver.Deposit(amount)
            with open("accounts.txt", "w") as f:
                for acc in accounts.values():
                    # updates each account's details to the file
                    f.write(f"{acc.account_number},{acc.password},{acc.account_type},{acc.balance}\n")
            print(f"Nu.{amount} transferred successfully to account {receiver_acc_number}")
        else:
            print("You have insufficient balance.")
    else:
        print("The account number you provided does not exist")

# created a main function to drive the application
def main():
    accounts = Read_acc_from_file()  # Load accounts from the file
    while True:
        print("\n1. Create Account")
        print("2. Login")
        print("3. Exit")
        choice = input("please enter your choice: ")
        if choice == '1':
            # it calls the function to create a new account
            create_account(accounts)
        elif choice == '2':
            account = Login(accounts) 
            if account:
                while True:
                    # providing options
                    print("\n1. Check Balance")  
                    print("2. Deposit Money")  
                    print("3. Withdraw Money")  
                    print("4. Transfer Money")  
                    print("5. Delete Account") 
                    print("6. Logout")  
                    action = input("Enter your choice: ")  
                    if action == '1':
                        # respective functions are called 
                        account.Checkbalance() 
                    elif action == '2':
                        amount = float(input("Enter amount to deposit: "))
                        account.Deposit(amount) 
                    elif action == '3':
                        amount = float(input("Enter amount to withdraw: ")) 
                        account.Withdraw(amount)  
                    elif action == '4':
                        transfer_money(accounts, account)  
                    elif action == '5':
                        del_account(accounts, account) 
                         # it exits the inner loop after deleting account
                        break 
                    elif action == '6':
                        # it exits the inner loop to log out
                        break  
        elif choice == '3':
            break 

if __name__ == "__main__":
    main()  # Finally it calls the main function to start the application
