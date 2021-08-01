from PyQt5.QtWidgets import QMainWindow, QApplication, QStackedWidget, QMessageBox, QLineEdit
from cryptography.fernet import Fernet
from PyQt5 import uic,QtWidgets, QtGui
import sys
import os.path

__version__ = "1"
__author__ = "Mahdi Yaghoubi"

def create_key():
    key = Fernet.generate_key()
    with open("key.key","wb") as key_file:
        key_file.write(key)

def load_key():
    key_file = open("key.key","rb")
    key = key_file.read()
    key_file.close()
    return key

key = load_key()
fer = Fernet(key)

class FirstTime(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("uis/FirstTime.ui", self)
        self.setFixedWidth(396)
        self.setFixedHeight(355)
        self.setWindowTitle("Password Manager")
        self.submit.clicked.connect(self.create_master)
        self.master1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.master2.setEchoMode(QtWidgets.QLineEdit.Password)
        link = "<a style='text-decoration: none; color:white;' href='https://github.com/ThisMahdi/'>By Mahdi Yaghoubi</a>"
        self.mahdi.setText(link)

    def create_master(self):
        global encrypt_master1
        encrypt_master1 = bytes(fer.encrypt(self.master1.text().encode()))
        if self.master1.text() == self.master2.text():
            if len(self.master1.text()) > 0 or len(self.master2.text()) > 0:
                with open('masterpassword.txt', 'w') as file:
                    encrypt = fer.encrypt(self.master1.text().encode()).decode()
                    decrypt = fer.decrypt(bytes(encrypt.encode()))
                    file.write(f"{encrypt}")
                msg = QMessageBox()
                msg.setWindowTitle(" ")
                msg.setText(f"Password Succsesfully Created. \nWrite It Down : \n\n{self.master1.text()}")
                msg.setWindowIcon(QtGui.QIcon("logo/PasswordManagerLogo.jpg"))
                msg.setIcon(QMessageBox.Information)
                msg.setStandardButtons(QMessageBox.Ok)
                msg.setDefaultButton(QMessageBox.Ok)
                # showing msg box
                x = msg.exec_()
                password_manager = PasswordManager()
                widget.addWidget(password_manager)
                widget.setCurrentIndex(widget.currentIndex() + 1)
        if self.master1.text() == "" or self.master2.text() == "":
            msg = QMessageBox()
            msg.setWindowTitle(" ")
            msg.setText("Please Fill All The Inputs.")
            msg.setWindowIcon(QtGui.QIcon("logo/PasswordManagerLogo.jpg"))
            msg.setIcon(QMessageBox.Critical)
            msg.setStandardButtons(QMessageBox.Retry)
            msg.setDefaultButton(QMessageBox.Retry)
            # showing msg box
            x = msg.exec_()
        elif self.master1.text() != self.master2.text():
            msg = QMessageBox()
            msg.setWindowTitle(" ")
            msg.setText("Master Passwords Are Not Equal! Try Again...")
            msg.setWindowIcon(QtGui.QIcon("logo/PasswordManagerLogo.jpg"))
            msg.setIcon(QMessageBox.Critical)
            msg.setStandardButtons(QMessageBox.Retry)
            msg.setDefaultButton(QMessageBox.Retry)
            # showing msg box
            x = msg.exec_()


class PasswordManager(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("uis/PasswordManager.ui", self)
        self.setFixedWidth(396)
        self.setFixedHeight(355)
        self.setWindowTitle("Password Manager")
        self.login.clicked.connect(self.login_function)
        self.master.setEchoMode(QtWidgets.QLineEdit.Password)
        link = "<a style='text-decoration: none; color:white;' href='https://github.com/ThisMahdi/'>By Mahdi Yaghoubi</a>"
        self.mahdi.setText(link)

    def login_function(self):
        with open("masterpassword.txt","r") as file:
            for line in file.readlines():
                dec = fer.decrypt(line.encode()).decode()
        if self.master.text() == dec:
            options = Options()
            widget.addWidget(options)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        else:
            msg = QMessageBox()
            msg.setWindowTitle(" ")
            msg.setText("Wrong Password! Try Again...")
            msg.setWindowIcon(QtGui.QIcon("logo/PasswordManagerLogo.jpg"))
            msg.setIcon(QMessageBox.Critical)
            msg.setStandardButtons(QMessageBox.Retry)
            msg.setDefaultButton(QMessageBox.Retry)
            # showing msg box
            x = msg.exec_()


class Options(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("uis/Options.ui", self)
        self.setFixedWidth(396)
        self.setFixedHeight(355)
        self.setWindowTitle("Password Manager")
        self.add.clicked.connect(self.add_page)
        self.view.clicked.connect(self.view_page)
        self.update.clicked.connect(self.update_page)
        self.deletepage.clicked.connect(self.delete_page)

    def delete_page(self):
        delete = Delete()
        widget.addWidget(delete)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def update_page(self):
        update = Update()
        widget.addWidget(update)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def view_page(self):
        view = View()
        widget.addWidget(view)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def add_page(self):
        add = Add()
        widget.addWidget(add)
        widget.setCurrentIndex(widget.currentIndex() + 1)

class Add(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("uis/Add.ui",self)
        self.setFixedWidth(396)
        self.setFixedHeight(355)
        self.setWindowTitle("Password Manager")
        self.add.clicked.connect(self.add_function)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.back.clicked.connect(self.back_function)

    def back_function(self):
        options = Options()
        widget.addWidget(options)
        widget.setCurrentWidget(options)
        # widget.setCurrentIndex(widget.currentIndex() - 1)

    def add_function(self):
        if self.name.text() == "" or self.password.text() == "":
            msg = QMessageBox()
            msg.setWindowTitle(" ")
            msg.setText("Please Fill All The Inputs.")
            msg.setWindowIcon(QtGui.QIcon("logo/PasswordManagerLogo.jpg"))
            msg.setIcon(QMessageBox.Critical)
            msg.setStandardButtons(QMessageBox.Retry)
            msg.setDefaultButton(QMessageBox.Retry)
            # showing msg box
            x = msg.exec_()
        else:
            with open("passwords.txt","a") as file:
                file.write(f"{self.name.text()}|{fer.encrypt(self.password.text().encode()).decode()}\n")
                msg = QMessageBox()
                msg.setWindowTitle(" ")
                msg.setText("Successfully Added.")
                msg.setWindowIcon(QtGui.QIcon("logo/PasswordManagerLogo.jpg"))
                msg.setIcon(QMessageBox.Information)
                msg.setStandardButtons(QMessageBox.Ok)
                msg.setDefaultButton(QMessageBox.Ok)
                # showing msg box
                x = msg.exec_()
                self.name.setText("")
                self.password.setText("")

class View(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("uis/View.ui",self)
        self.setFixedWidth(396)
        self.setFixedHeight(355)
        self.setWindowTitle("Password Manager")
        self.back.clicked.connect(self.back_function)
        self.views.setVerticalScrollBar(self.scroll)

        with open("passwords.txt","r") as file:
            fixed = []
            for line in file.readlines():
                name , password = line.split("|")
                views = f"[ Name : {name} | Password : {fer.decrypt(password.encode()).decode()} ]"
                fixed.append(views)

        final = '\n'.join(fixed)
        print(final)
        self.views.setText(final)


    def back_function(self):
        options = Options()
        widget.addWidget(options)
        widget.setCurrentWidget(options)
        # widget.setCurrentIndex(widget.currentIndex() - 1)


class Update(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("uis/Update.ui",self)
        self.setFixedWidth(396)
        self.setFixedHeight(355)
        self.setWindowTitle("Password Manager")
        self.back.clicked.connect(self.back_function)
        self.update.clicked.connect(self.update_function)
        self.newpassword.setEchoMode(QtWidgets.QLineEdit.Password)


    def back_function(self):
        options = Options()
        widget.addWidget(options)
        widget.setCurrentWidget(options)
        # widget.setCurrentIndex(widget.currentIndex() - 1)

    def update_function(self):
        with open('passwords.txt', 'r') as file:
            lines = file.readlines()
            name = f"{self.name.text()}"
            for idx, line in enumerate(lines):
                if line.startswith(name + '|'):
                    lines[idx] = f"{self.name.text()}|{fer.encrypt(self.newpassword.text().encode()).decode()}\n"
                    updatefile = open('passwords.txt', 'w')
                    updatefile.writelines(lines)
                    updatefile.close()
                    msg = QMessageBox()
                    msg.setWindowTitle(" ")
                    msg.setText(f"Password successfully changed!")
                    msg.setWindowIcon(QtGui.QIcon("logo/PasswordManagerLogo.jpg"))
                    msg.setIcon(QMessageBox.Information)
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.setDefaultButton(QMessageBox.Ok)
                    # showing msg box
                    x = msg.exec_()
                    break
            if not line.startswith(name):
                    msg = QMessageBox()
                    msg.setWindowTitle(" ")
                    msg.setText(f"There is no [{self.name.text()}] in database. Please enter a valid name")
                    msg.setWindowIcon(QtGui.QIcon("logo/PasswordManagerLogo.jpg"))
                    msg.setIcon(QMessageBox.Critical)
                    msg.setStandardButtons(QMessageBox.Retry)
                    msg.setDefaultButton(QMessageBox.Retry)
                    # showing msg box
                    x = msg.exec_()


class Delete(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("uis/Delete.ui",self)
        self.setFixedWidth(396)
        self.setFixedHeight(355)
        self.setWindowTitle("Password Manager")
        self.back.clicked.connect(self.back_function)
        self.deletefunction.clicked.connect(self.delete_function)

    def back_function(self):
        options = Options()
        widget.addWidget(options)
        widget.setCurrentWidget(options)

    def delete_function(self):
        if self.name.text() == "":
            msg = QMessageBox()
            msg.setWindowTitle(" ")
            msg.setText("Please fill the input.")
            msg.setWindowIcon(QtGui.QIcon("logo/PasswordManagerLogo.jpg"))
            msg.setIcon(QMessageBox.Critical)
            msg.setStandardButtons(QMessageBox.Retry)
            msg.setDefaultButton(QMessageBox.Retry)
            # showing msg box
            x = msg.exec_()
        else:
            with open("passwords.txt","r") as file:
                lines = file.readlines()
                flag = False
                for idx,line in enumerate(lines):
                    if line.startswith(self.name.text()+"|"):
                        flag = True
                        break
                if flag:
                    lines[idx] = ""
                    updatefile = open('passwords.txt', 'w')
                    updatefile.writelines(lines)
                    updatefile.close()
                    with open("passwords.txt", "r") as f:
                        a = "".join(line for line in f if not line.isspace())
                        print(a)
                    with open("passwords.txt", "w") as f:
                        f.write(a)
                    msg = QMessageBox()
                    msg.setWindowTitle(" ")
                    msg.setText(f"Chosen account have been successfully deleted.")
                    msg.setWindowIcon(QtGui.QIcon("logo/PasswordManagerLogo.jpg"))
                    msg.setIcon(QMessageBox.Information)
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.setDefaultButton(QMessageBox.Ok)
                    # showing msg box
                    x = msg.exec_()
                else:
                    msg = QMessageBox()
                    msg.setWindowTitle(" ")
                    msg.setText(f"There is no [{self.name.text()}] in database. Please enter a valid name")
                    msg.setWindowIcon(QtGui.QIcon("logo/PasswordManagerLogo.jpg"))
                    msg.setIcon(QMessageBox.Critical)
                    msg.setStandardButtons(QMessageBox.Retry)
                    msg.setDefaultButton(QMessageBox.Retry)
                    # showing msg box
                    x = msg.exec_()




if __name__ == "__main__":
    if not os.path.isfile("key.key"):
        create_key()
    else:
        pass
    app = QApplication(sys.argv)
    widget = QStackedWidget()
    widget.setWindowIcon(QtGui.QIcon("logo/PasswordManagerLogo.jpg"))
    widget.setWindowTitle("Password Manager")
    widget.setStyleSheet("background-color:white; padding: 0 0 0 0; border-spacing: 0px 0px; margin: 0px;")
    widget.setFixedWidth(396)
    widget.setFixedHeight(355)

    if os.path.isfile("masterpassword.txt"):
        login = PasswordManager()
        widget.addWidget(login)
        widget.show()
    else:
        first_time = FirstTime()
        widget.addWidget(first_time)
        widget.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print("Closing App...")
