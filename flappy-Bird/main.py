import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QMessageBox
import subprocess
import mysql.connector

class LoginForm(QtWidgets.QWidget):
    def __init__(self):
        super(LoginForm, self).__init__()
        uic.loadUi('login1.ui', self)  # Load the login UI
        self.pushButton.clicked.connect(self.login)
        self.createAccountButton.clicked.connect(self.open_register_form)
        self.AI.clicked.connect(self.open_AI_model)

    def open_register_form(self):
        self.register_form = RegisterForm()
        self.register_form.show()
        self.close()

    def open_AI_model(self):
        self.close()
        subprocess.run([sys.executable, 'NEAT-Model/flappy_bird.py'])


    def authentificate(self, username, password):
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="game")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM login WHERE username = %s AND password = %s", (username, password))
            result = cursor.fetchone()
            conn.close()
            return result is not None
        except mysql.connector.Error as er:
            QMessageBox.critical(self, 'Database Error', f"Error: {er}")
            return False

    def login(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if self.authentificate(username, password):
            self.start_game()
        else:
            QMessageBox.warning(self, 'Error', 'Incorrect Username or Password')

    def start_game(self):
        self.close()
        subprocess.run([sys.executable, 'Game.py'])

class RegisterForm(QtWidgets.QWidget):
    def __init__(self):
        super(RegisterForm, self).__init__()
        uic.loadUi('register.ui', self)  # Load the register UI
        self.registerButton.clicked.connect(self.register)

    def register(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()
        if self.create_account(username, password) and (username !='' and password != ''):
            QMessageBox.information(self, 'Success', 'Account created successfully')
            self.open_login_form()
        else:
            QMessageBox.warning(self, 'Error', 'Failed to create account')

    def create_account(self, username, password):
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="game")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO login (username, password) VALUES (%s, %s)", (username, password))
            conn.commit()
            conn.close()
            return True
        except mysql.connector.Error as er:
            QMessageBox.critical(self, 'Database Error', f"Error: {er}")
            return False

    def open_login_form(self):
        self.login_form = LoginForm()
        self.login_form.show()
        self.close()

def update_top_score(username, score):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="mysql"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT topscore FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        if result:
            highest_score = result[0]
            if score > highest_score:
                cursor.execute("UPDATE users SET topscore = %s WHERE username = %s", (score, username))
                conn.commit()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Error: {err}")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    login_form = LoginForm()
    login_form.show()
    sys.exit(app.exec())
