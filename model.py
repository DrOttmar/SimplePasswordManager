import os
import pickle
import collections

from cryptography.fernet import Fernet


SEPARATOR = "__%%__"


class PasswordContainer:
    fernet_object = None

    # Form von password_database: {"Account": {"Username": "abc", "Password": "def"}}
    password_database = {}

    def __init__(self):

        self._init_dirs()

        if "fernet.pickle" not in os.listdir("env"):
            key = Fernet.generate_key()
            with open(r"env\fernet.pickle", "wb") as pic:
                pickle.dump(key, pic)

        with open(r"env\fernet.pickle", "rb") as pic:
            tmp = pickle.load(pic)
        self.fernet_object = Fernet(tmp)

        if "secret.env" not in os.listdir("env"):
            print("Initialisation process. Set a global password:")
            pw = input()
            with open(r"env\secret.env", "wb") as sec:
                encoded = self.fernet_object.encrypt(pw.encode())
                sec.write(encoded)

        if "database.txt" not in os.listdir("db"):
            with open(r"db\database.txt", "w") as db:
                pass

        self.import_passwords()

    # Authentication
    def authenticate(self):
        user_input = input("Enter password: ")
        return user_input == self._get_secret_env()

    # Init
    def import_passwords(self):
        with open(r"db\database.txt", "rb") as pws:
            tmp = pws.readlines()
            for i in tmp:
                _creds = self._decrypt_password(i)
                self._update_passwords(_creds)
            self._reorder_passwords()

    # Option 1
    def list_passwords(self):
        last_ct = 0
        for ct, acc in enumerate(self.password_database):
            print(f"({ct + 1}) {acc}")
            last_ct = ct + 1
        print(f"({last_ct + 1}) Exit.")
        return last_ct + 1

    def show_account_credentials(self, index):
        try:
            _acc = list(self.password_database.keys())[index - 1]
        except:
            print("User Input invalid. Exit by default.")
            return
        print(f"\nUsername: {self.password_database[_acc]['Username']}")
        print(f"Password: {self.password_database[_acc]['Password']}")

    # Option 2
    def add_new_account(self, credentials: list):

        self._update_passwords(credentials)
        self._reorder_passwords()

        encrypted_string = self._encrypt_credentials(credentials)

        with open(r"db\database.txt", "ab") as db:
            db.write(encrypted_string + b"\n")

    # Option 3
    def delete_account(self, index):
        try:
            _acc = list(self.password_database.keys())[index - 1]
        except:
            print("User Input invalid. Exit by default.")
            return
        self.password_database.pop(_acc)
        self._update_database()

    def _decrypt_password(self, crypted_string):
        return self.fernet_object.decrypt(crypted_string).decode().split(SEPARATOR)

    def _encrypt_credentials(self, credentials: list):
        encrypted_string = ""
        for ct, cred in enumerate(credentials):
            encrypted_string += cred
            if ct < 2:
                encrypted_string += SEPARATOR

        return self.fernet_object.encrypt(encrypted_string.encode())

    def _get_secret_env(self):
        with open("env\secret.env", "r") as env:
            content = env.read()
            return self.fernet_object.decrypt(content.encode()).decode()


    def _reorder_passwords(self):
        if len(self.password_database) <= 1:
            return
        self.password_database = collections.OrderedDict(sorted(self.password_database.items(),
                                                                key=lambda i: i[0].lower()))

    def _update_passwords(self, credentials):
        self.password_database.update({credentials[0]: {"Username": credentials[1], "Password": credentials[-1]}})

    def _update_database(self):
        with open(r"db\database.txt", "wb") as db:
            for acc in self.password_database:
                user = self.password_database[acc]["Username"]
                pawo = self.password_database[acc]["Password"]

                encrypted_string = self._encrypt_credentials([acc, user, pawo])

                db.write(encrypted_string + b"\n")

    def _init_dirs(self):
        if "db" not in os.listdir():
            os.mkdir("db")
        if "env" not in os.listdir():
            os.mkdir("env")
