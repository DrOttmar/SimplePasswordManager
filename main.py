import time
import sys

from model import PasswordContainer


def main():
    instance = PasswordContainer()
    while True:
        print("\nChoose an option:")
        print("1: Show all accounts.")
        print("2: Add new account.")
        print("3: Delete account.")
        print("4: Exit application.\n")

        decision = input("User Input: ")

        if decision == "1":
            exit_option = instance.list_passwords()
            no_account = input("\nUser Input: ")
            if no_account == str(exit_option):
                continue
            try:
                instance.show_account_credentials(int(no_account))
            except ValueError:
                print("User input invalid.")

        elif decision == "2":
            account = input("Account: ")
            if account in instance.password_database:
                print("Account already exists.")
                continue
            username = input("Username: ")
            password = input("Password: ")

            instance.add_new_account([account, username, password])

        elif decision == "3":
            exit_option = instance.list_passwords()
            no_account = input("\nUser Input: ")
            if no_account == str(exit_option):
                continue
            try:
                instance.delete_account(int(no_account))
            except ValueError:
                print("User input invalid.")

        elif decision == "4":
            print("Bye!")
            time.sleep(1)
            sys.exit()


if __name__ == "__main__":
    main()
