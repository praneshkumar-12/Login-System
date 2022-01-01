# Python 3.10.0
import sys
from datetime import datetime
import random
import smtplib
import os

try:
    import mysql.connector
except ModuleNotFoundError:
    os.system('pip install mysql.connector')
    time.sleep(10)
    import mysql.connector
try:
    from PyQt5 import QtGui
    from PyQt5 import QtWidgets, QtCore
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QMessageBox
except ModuleNotFoundError:
    os.system('pip install PyQt5')
    time.sleep(10)
    from PyQt5 import QtGui
    from PyQt5 import QtWidgets, QtCore
    from PyQt5.QtCore import Qt
    from PyQt5.QtWidgets import QMessageBox

from email.message import EmailMessage

now, time, chk = 0, 0, 0

try:
    user = os.environ["EMAIL_USER"]
    key = os.environ["EMAIL_PASS"]
except KeyError:
    print("You haven't set the credentials for OTP Authentication")
    email_address = input("To continue please enter your email id:")
    email_password = input("Enter your mail password(if 2FA is off) or app password(if 2FA is on):")
    os.environ["EMAIL_USER"] = email_address
    os.environ["EMAIL_PASS"] = email_password
    
message = 0
addr = 0

def settime():
    global now
    global time
    global chk
    now = datetime.now()
    time = now.strftime("%I:%M %p")
    chk = now.strftime("%H")


mydb = mysql.connector.connect(
    host="localhost", user="root", password="root", database="test"
)
cur = mydb.cursor()

def sql_connect(u, k):
    query = "SELECT passphrase FROM login_details WHERE username = '" + u + "'"
    cur.execute(query)
    try:
        result_pass = cur.fetchone()[0]
        if result_pass == k:
            return True
    except:
        return False


def sql_insert(user, key, fname, lname, email):
    query = (
        "INSERT INTO login_details VALUES('"
        + user
        + "','"
        + key
        + "','"
        + fname
        + "','"
        + lname
        + "','"
        + email
        + "')"
    )
    try:
        cur.execute(query)
        mydb.commit()
        return True
    except:
        return False


def sql_usr_mail_chk(usr, mail):
    query = "SELECT email, f_name FROM login_details WHERE username = '" + usr + "'"
    cur.execute(query)
    try:
        ex = cur.fetchone()
        result = ex[0]
        f_name = ex[1]
        if result == mail:
            return True, f_name
    except:
        return False


def send_otp(mail, name):
    random_integer = random.randint(100000, 999999)
    msg = EmailMessage()
    msg["Subject"] = "OTP Verification for Reseting your Password"
    msg["From"] = user
    msg["To"] = mail
    msg.set_content(
        """Hello """
        + str(name)
        + """,
    This mail is in response to your request of resetting your xyz password.

Please enter or provide the following OTP: """
        + str(random_integer)
        + """

Note that this OTP is valid only for this instance. Requesting another OTP will make this OTP invalid. Incase you haven't requested to reset your password, contact your xyz. Thank You"""
    )
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(user, key)
    server.send_message(msg)
    server.quit()
    return True, random_integer


def change_password(usr, keyphrase):
    query = (
        "UPDATE login_details SET passphrase = '"
        + keyphrase
        + "' WHERE username = '"
        + usr
        + "'"
    )
    cur.execute(query)
    mydb.commit()


# ------------------------------------------- Class Login -------------------------------------
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(780, 600)
        Form.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        Form.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        Form.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(30, 30, 771, 590))
        self.widget.setStyleSheet("")
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(50, 30, 371, 530))
        self.label.setStyleSheet("")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(50, 30, 371, 530))
        self.label_2.setStyleSheet(
            "background-color: rgba(0, 0, 0, 80);\n" "border-top-left-radius: 50px;"
        )
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(360, 29, 370, 531))
        self.label_3.setStyleSheet(
            "background-color: rgba(255, 255, 255, 255);\n"
            "border-bottom-right-radius: 50px;"
        )
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setGeometry(QtCore.QRect(493, 90, 110, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color:rgba(0,0,0,200)\n" "")
        self.label_4.setObjectName("label_4")
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setGeometry(QtCore.QRect(400, 190, 290, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet(
            "background-color: rgba(0,0,0,0);\n"
            "border: none;\n"
            "border-bottom: 2px solid rgba(0, 142, 242, 1);\n"
            "color: rgba(0,0,0,240);\n"
            "padding-bottom: 7px;"
        )
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setGeometry(QtCore.QRect(400, 290, 290, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet(
            "background-color: rgba(0,0,0,0);\n"
            "border: none;\n"
            "border-bottom: 2px solid rgba(0, 142, 242, 1);\n"
            "color: rgba(0,0,0,240);\n"
            "padding-bottom: 7px;"
        )
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(439, 380, 201, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("")
        self.pushButton.setObjectName("pushButton")
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setGeometry(QtCore.QRect(50, 200, 310, 60))
        font = QtGui.QFont()
        self.label.setStyleSheet(
            """border-image: url(Nature9.jpg);
            border-top-left-radius: 50px;"""
        )
        font.setFamily("Losing Grip")
        font.setPointSize(35)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: rgb(255, 255, 255)")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.widget)
        self.label_7.setGeometry(QtCore.QRect(100, 274, 201, 61))
        font = QtGui.QFont()
        font.setFamily("Losing Grip")
        font.setPointSize(35)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color: rgb(255, 255, 255)")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.label_9 = QtWidgets.QLabel(self.widget)
        self.label_9.setGeometry(QtCore.QRect(393, 449, 310, 22))
        font = QtGui.QFont()
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.label_9.setStyleSheet("color: rgb(96, 16, 255);")
        self.pushButton.setGraphicsEffect(
            QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=3, yOffset=3)
        )
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.checkBox = QtWidgets.QCheckBox(self.widget)
        self.checkBox.setGeometry(QtCore.QRect(700, 310, 20, 20))
        self.checkBox.setText("")
        self.checkBox.setObjectName("checkBox")
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setGeometry(QtCore.QRect(465, 479, 151, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet(
            "border: none;\n"
            "background-color: transparent;\n"
            "height: 50px;\n"
            "width: 200px;\n"
        )
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        self.pushButton_3.setGeometry(QtCore.QRect(416, 509, 270, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet(
            "border: none;\n"
            "background-color: transparent;\n"
            "height: 50px;\n"
            "width: 200px;\n"
        )
        self.pushButton_3.setObjectName("pushButton_3")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_4.setText(_translate("Form", "Log In"))
        self.lineEdit.setPlaceholderText(_translate("Form", "User Name"))
        self.lineEdit_2.setPlaceholderText(_translate("Form", "Password"))
        self.pushButton.setText(_translate("Form", "Log In"))
        if 6 <= int(chk) <= 11:
            self.label_6.setText(_translate("Form", "Good Morning!"))
        elif 12 <= int(chk) <= 14:
            self.label_6.setText(_translate("Form", "Good Afternoon!"))
        elif 14 <= int(chk) <= 23:
            self.label_6.setText(_translate("Form", "Good Evening!"))
        self.label_7.setText(_translate("Form", time))
        self.label_9.setText(_translate("Form", ""))
        self.pushButton.clicked.connect(lambda: self.login_process())
        self.checkBox.stateChanged.connect(self.clickBox)
        self.pushButton_2.setText(_translate("Form", "Forgot Password?"))
        self.pushButton_3.setText(
            _translate("Form", "Don't have an account? Click here")
        )
        self.pushButton_3.clicked.connect(lambda: self.open_Register(Form))
        self.pushButton_2.clicked.connect(lambda: self.open_Forgot(Form))

    def login_process(self):
        user = self.lineEdit.text()
        key = self.lineEdit_2.text()
        if user == "" or key == "":
            print("Please fill all the fields!")
        else:
            res = sql_connect(user, key)
            if res:
                self.label_9.setText("Authorization Success!")
                print("Login Successful!")
                # sleep(2)
                # Form.hide()
            else:
                self.label_9.setText("Invalid credentials!")
                print("Invalid username or password!")

    def clickBox(self, state):
        if state == QtCore.Qt.Checked:
            self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)

    def open_Register(self, login_object):
        login_object.hide()
        settime()
        self.reg_app = QtWidgets.QApplication(sys.argv)
        self.reg_Form = QtWidgets.QWidget()
        self.reg_ui = Ui_Register()
        self.reg_ui.setupUi(self.reg_Form)
        self.reg_Form.show()

    def open_Forgot(self, login_object):
        login_object.hide()
        settime()
        self.for_app = QtWidgets.QApplication(sys.argv)
        self.for_Form = QtWidgets.QWidget()
        self.for_ui = Ui_Forgot()
        self.for_ui.setupUi(self.for_Form)
        self.for_Form.show()


# ---------------------------- End of Class Login --------------------------------------

# ------------------------------ Class Register ---------------------------------------


class Ui_Register(object):
    def setupUi(self, Register):
        Register.setObjectName("Register")
        Register.resize(780, 600)
        Register.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        Register.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        Register.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        Register.setStyleSheet("")
        self.widget = QtWidgets.QWidget(Register)
        self.widget.setGeometry(QtCore.QRect(30, 30, 771, 590))
        self.widget.setStyleSheet("")
        self.widget.setObjectName("widget")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(50, 30, 371, 530))
        self.label.setStyleSheet(
            """border-image: url(City3.png);
            border-top-left-radius: 50px;"""
        )
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(50, 30, 371, 530))
        self.label_2.setStyleSheet(
            "background-color: rgba(0, 0, 0, 80);\n" "border-top-left-radius: 50px;"
        )
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(360, 29, 370, 531))
        self.label_3.setStyleSheet(
            "background-color: rgba(255, 255, 255, 255);\n"
            "border-bottom-right-radius: 50px;"
        )
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setGeometry(QtCore.QRect(50, 200, 310, 60))
        font = QtGui.QFont()
        font.setFamily("Losing Grip")
        font.setPointSize(35)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: rgb(255, 255, 255)")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.widget)
        self.label_7.setGeometry(QtCore.QRect(100, 274, 201, 61))
        font = QtGui.QFont()
        font.setFamily("Losing Grip")
        font.setPointSize(35)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color: rgb(255, 255, 255)")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.stat_lbl = QtWidgets.QLabel(self.widget)
        self.stat_lbl.setGeometry(QtCore.QRect(388, 460, 310, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.stat_lbl.setFont(font)
        self.stat_lbl.setStyleSheet("\n" "color: rgb(96, 16, 255);")
        self.stat_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.stat_lbl.setObjectName("stat_lbl")
        self.widget_2 = QtWidgets.QWidget(self.widget)
        self.widget_2.setGeometry(QtCore.QRect(383, 65, 341, 391))
        self.widget_2.setObjectName("widget_2")
        self.f_name = QtWidgets.QLineEdit(self.widget_2)
        self.f_name.setGeometry(QtCore.QRect(10, 95, 147, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.f_name.setFont(font)
        self.f_name.setStyleSheet(
            "background-color: rgba(0,0,0,0);\n"
            "border: none;\n"
            "border-bottom: 2px solid rgb(0, 48, 239);\n"
            "color: rgba(0,0,0,240);\n"
            "padding-bottom: 7px;"
        )
        self.f_name.setText("")
        self.f_name.setObjectName("f_name")
        self.reg_btn = QtWidgets.QPushButton(self.widget_2)
        self.reg_btn.setGeometry(QtCore.QRect(60, 319, 201, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.reg_btn.setFont(font)
        self.reg_btn.setStyleSheet("")
        self.reg_btn.setObjectName("reg_btn")
        self.pwd = QtWidgets.QLineEdit(self.widget_2)
        self.pwd.setGeometry(QtCore.QRect(10, 206, 290, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pwd.setFont(font)
        self.pwd.setStyleSheet(
            "background-color: rgba(0,0,0,0);\n"
            "border: none;\n"
            "border-bottom: 2px solid rgb(0, 48, 239);\n"
            "color: rgba(0,0,0,240);\n"
            "padding-bottom: 7px;"
        )
        self.pwd.setObjectName("pwd")
        self.checkBox_2 = QtWidgets.QCheckBox(self.widget_2)
        self.checkBox_2.setGeometry(QtCore.QRect(316, 224, 20, 20))
        self.checkBox_2.setText("")
        self.checkBox_2.setObjectName("checkBox_2")
        self.label_10 = QtWidgets.QLabel(self.widget_2)
        self.label_10.setGeometry(QtCore.QRect(104, 20, 151, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("color:rgba(0,0,0,200)\n" "")
        self.label_10.setObjectName("label_10")
        self.l_name = QtWidgets.QLineEdit(self.widget_2)
        self.l_name.setGeometry(QtCore.QRect(171, 95, 160, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.l_name.setFont(font)
        self.l_name.setStyleSheet(
            "background-color: rgba(0,0,0,0);\n"
            "border: none;\n"
            "border-bottom: 2px solid rgb(0, 48, 239);\n"
            "color: rgba(0,0,0,240);\n"
            "padding-bottom: 7px;"
        )
        self.l_name.setObjectName("l_name")
        self.email_fld = QtWidgets.QLineEdit(self.widget_2)
        self.email_fld.setGeometry(QtCore.QRect(10, 154, 290, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.email_fld.setFont(font)
        self.email_fld.setStyleSheet(
            "background-color: rgba(0,0,0,0);\n"
            "border: none;\n"
            "border-bottom: 2px solid rgb(0, 48, 239);\n"
            "color: rgba(0,0,0,240);\n"
            "padding-bottom: 7px;"
        )
        self.email_fld.setObjectName("email_fld")
        self.con_fld = QtWidgets.QLineEdit(self.widget_2)
        self.con_fld.setGeometry(QtCore.QRect(10, 260, 290, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.con_fld.setFont(font)
        self.con_fld.setStyleSheet(
            "background-color: rgba(0,0,0,0);\n"
            "border: none;\n"
            "border-bottom: 2px solid rgb(0, 48, 239);\n"
            "color: rgba(0,0,0,240);\n"
            "padding-bottom: 7px;"
        )
        self.con_fld.setObjectName("con_fld")
        self.pwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.con_fld.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        self.pushButton_3.setGeometry(QtCore.QRect(402, 500, 290, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setStyleSheet(
            "border: none;\n"
            "background-color: transparent;\n"
            "height: 50px;\n"
            "width: 200px;"
        )
        self.pushButton_3.setObjectName("pushButton_3")
        global addr
        addr = Register

        self.retranslateUi(Register)
        QtCore.QMetaObject.connectSlotsByName(Register)
        Register.setTabOrder(self.f_name, self.l_name)
        Register.setTabOrder(self.l_name, self.email_fld)
        Register.setTabOrder(self.email_fld, self.pwd)
        Register.setTabOrder(self.pwd, self.con_fld)
        Register.setTabOrder(self.con_fld, self.reg_btn)
        Register.setTabOrder(self.reg_btn, self.checkBox_2)

    def retranslateUi(self, Register):
        _translate = QtCore.QCoreApplication.translate
        Register.setWindowTitle(_translate("Register", "Form"))
        self.label_6.setText(_translate("Register", "Good Morning!"))
        self.label_7.setText(_translate("Register", "11:00 AM"))
        self.stat_lbl.setText(_translate("Register", "          "))
        self.f_name.setPlaceholderText(_translate("Register", "First Name"))
        self.reg_btn.setText(_translate("Register", "Register"))
        self.pwd.setPlaceholderText(_translate("Register", "Password"))
        self.label_10.setText(_translate("Register", "Register"))
        self.l_name.setPlaceholderText(_translate("Register", "Last Name"))
        self.email_fld.setPlaceholderText(_translate("Register", "Email Address"))
        self.con_fld.setPlaceholderText(_translate("Register", "Confirm Password"))
        if 6 <= int(chk) <= 11:
            self.label_6.setText(_translate("Form", "Good Morning!"))
        elif 12 <= int(chk) <= 14:
            self.label_6.setText(_translate("Form", "Good Afternoon!"))
        elif 14 <= int(chk) <= 23:
            self.label_6.setText(_translate("Form", "Good Evening!"))
        self.label_7.setText(_translate("Form", time))
        self.pushButton_3.setText(
            _translate("Register", "Already have an account? Click Here")
        )
        self.checkBox_2.stateChanged.connect(self.clickBox)
        self.reg_btn.clicked.connect(lambda: self.register_process())
        self.pushButton_3.clicked.connect(lambda: self.open_Login(Register))

    def register_process(self):
        msg = QMessageBox()
        msg.setWindowTitle("Registration")
        __fname = self.f_name.text()
        __lname = self.l_name.text()
        __mail = self.email_fld.text()
        __key = self.pwd.text()
        __rekey = self.con_fld.text()
        if (
            __fname == ""
            or __lname == ""
            or __mail == ""
            or __key == ""
            or __rekey == ""
        ):
            self.stat_lbl.setText("Please fill out all the fields!")
        elif __key == __rekey:
            ip_user = __fname.lower() + "_" + __lname.lower()
            chk = sql_insert(ip_user, __key, __fname, __lname, __mail)
            if chk:
                self.stat_lbl.setText("Registration Success!")
                __msg_txt = "Registration Successful!, Your username is " + ip_user
                msg.setText(__msg_txt)
                msg.setIcon(QMessageBox.Information)
                x = msg.exec_()
                self.open_Login(addr)
            else:
                self.stat_lbl.setText("Registration Failed!")
                msg.setIcon(QMessageBox.Information)
                msg.setText("Registration unsuccessful!")
                x = msg.exec_()
        elif __key != __rekey:
            print("Please check your passwords!")

    def clickBox(self, state):
        if state == QtCore.Qt.Checked:
            self.pwd.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.con_fld.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.pwd.setEchoMode(QtWidgets.QLineEdit.Password)
            self.con_fld.setEchoMode(QtWidgets.QLineEdit.Password)

    def open_Login(self, register_object):
        register_object.hide()
        settime()
        self.log_app = QtWidgets.QApplication(sys.argv)
        self.log_Form = QtWidgets.QWidget()
        self.log_ui = Ui_Form()
        self.log_ui.setupUi(self.log_Form)
        self.log_Form.show()


# ------------------------------- End of Class Register --------------------------------

# ---------------------------------- Class Forgot Password ------------------------------


class Ui_Forgot(object):
    def setupUi(self, Forgot):
        Forgot.setObjectName("Forgot")
        Forgot.resize(780, 600)
        Forgot.setStyleSheet("")
        self.widget = QtWidgets.QWidget(Forgot)
        self.widget.setGeometry(QtCore.QRect(30, 30, 771, 590))
        self.widget.setStyleSheet("")
        self.widget.setObjectName("widget")
        Forgot.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        Forgot.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground, True)
        Forgot.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(50, 30, 371, 530))
        self.label.setStyleSheet(
            """border-image: url(LandWater4.jpg);
            border-top-left-radius: 50px;"""
        )
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(50, 30, 371, 530))
        self.label_2.setStyleSheet(
            "background-color: rgba(0, 0, 0, 80);\n" "border-top-left-radius: 50px;"
        )
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(360, 29, 370, 531))
        self.label_3.setStyleSheet(
            "background-color: rgba(255, 255, 255, 255);\n"
            "border-bottom-right-radius: 50px;"
        )
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setGeometry(QtCore.QRect(50, 200, 310, 60))
        font = QtGui.QFont()
        font.setFamily("Losing Grip")
        font.setPointSize(35)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: rgb(255, 255, 255)")
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.widget)
        self.label_7.setGeometry(QtCore.QRect(100, 274, 201, 61))
        font = QtGui.QFont()
        font.setFamily("Losing Grip")
        font.setPointSize(35)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color: rgb(255, 255, 255)")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.stat_lbl = QtWidgets.QLabel(self.widget)
        self.stat_lbl.setGeometry(QtCore.QRect(388, 473, 310, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.stat_lbl.setFont(font)
        self.stat_lbl.setStyleSheet("\n" "color: rgb(96, 16, 255);")
        self.stat_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.stat_lbl.setObjectName("stat_lbl")
        self.widget_2 = QtWidgets.QWidget(self.widget)
        self.widget_2.setGeometry(QtCore.QRect(383, 65, 341, 410))
        self.widget_2.setObjectName("widget_2")
        self.usr_fld = QtWidgets.QLineEdit(self.widget_2)
        self.usr_fld.setGeometry(QtCore.QRect(10, 86, 291, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.usr_fld.setFont(font)
        self.usr_fld.setStyleSheet(
            "background-color: rgba(0,0,0,0);\n"
            "border: none;\n"
            "border-bottom: 2px solid rgba(38, 204, 0, 1);\n"
            "color: rgba(0,0,0,240);\n"
            "padding-bottom: 7px;"
        )
        self.usr_fld.setText("")
        self.usr_fld.setObjectName("usr_fld")
        self.res_btn = QtWidgets.QPushButton(self.widget_2)
        self.res_btn.setGeometry(QtCore.QRect(13, 350, 150, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.res_btn.setFont(font)
        self.res_btn.setStyleSheet("")
        self.res_btn.setObjectName("res_btn")
        self.checkBox_2 = QtWidgets.QCheckBox(self.widget_2)
        self.checkBox_2.setGeometry(QtCore.QRect(310, 224, 20, 20))
        self.checkBox_2.setText("")
        self.checkBox_2.setObjectName("checkBox_2")
        self.label_10 = QtWidgets.QLabel(self.widget_2)
        self.label_10.setGeometry(QtCore.QRect(35, 20, 300, 51))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("color:rgba(0,0,0,200)\n" "")
        self.label_10.setObjectName("label_10")
        self.email_fld = QtWidgets.QLineEdit(self.widget_2)
        self.email_fld.setGeometry(QtCore.QRect(10, 143, 290, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.email_fld.setFont(font)
        self.email_fld.setStyleSheet(
            "background-color: rgba(0,0,0,0);\n"
            "border: none;\n"
            "border-bottom: 2px solid rgba(38, 204, 0, 1);\n"
            "color: rgba(0,0,0,240);\n"
            "padding-bottom: 7px;"
        )
        self.email_fld.setObjectName("email_fld")
        self.otp_fld = QtWidgets.QLineEdit(self.widget_2)
        self.otp_fld.setGeometry(QtCore.QRect(10, 196, 290, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.otp_fld.setFont(font)
        self.otp_fld.setStyleSheet(
            "background-color: rgba(0,0,0,0);\n"
            "border: none;\n"
            "border-bottom: 2px solid rgba(38, 204, 0, 1);\n"
            "color: rgba(0,0,0,240);\n"
            "padding-bottom: 7px;"
        )
        self.otp_fld.setObjectName("otp_fld")
        self.pwd_fld = QtWidgets.QLineEdit(self.widget_2)
        self.pwd_fld.setGeometry(QtCore.QRect(10, 247, 290, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pwd_fld.setFont(font)
        self.pwd_fld.setStyleSheet(
            "background-color: rgba(0,0,0,0);\n"
            "border: none;\n"
            "border-bottom: 2px solid rgba(38, 204, 0, 1);\n"
            "color: rgba(0,0,0,240);\n"
            "padding-bottom: 7px;"
        )
        self.pwd_fld.setObjectName("pwd_fld")
        self.repass_fld = QtWidgets.QLineEdit(self.widget_2)
        self.repass_fld.setGeometry(QtCore.QRect(10, 297, 290, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.repass_fld.setFont(font)
        self.repass_fld.setStyleSheet(
            "background-color: rgba(0,0,0,0);\n"
            "border: none;\n"
            "border-bottom: 2px solid rgba(38, 204, 0, 1);\n"
            "color: rgba(0,0,0,240);\n"
            "padding-bottom: 7px;"
        )
        self.repass_fld.setObjectName("repass_fld")
        self.res_btn_2 = QtWidgets.QPushButton(self.widget_2)
        self.res_btn_2.setGeometry(QtCore.QRect(160, 350, 150, 51))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.res_btn_2.setFont(font)
        self.res_btn_2.setStyleSheet("")
        self.res_btn_2.setObjectName("res_btn_2")
        self.redir_log = QtWidgets.QPushButton(self.widget)
        self.redir_log.setGeometry(QtCore.QRect(405, 513, 290, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.redir_log.setFont(font)
        self.redir_log.setStyleSheet(
            "border: none;\n"
            "background-color: transparent;\n"
            "height: 50px;\n"
            "width: 200px;"
        )
        self.redir_log.setObjectName("redir_log")

        self.retranslateUi(Forgot)
        QtCore.QMetaObject.connectSlotsByName(Forgot)
        Forgot.setTabOrder(self.usr_fld, self.email_fld)
        Forgot.setTabOrder(self.email_fld, self.otp_fld)
        Forgot.setTabOrder(self.otp_fld, self.pwd_fld)
        Forgot.setTabOrder(self.pwd_fld, self.repass_fld)
        Forgot.setTabOrder(self.repass_fld, self.res_btn)
        Forgot.setTabOrder(self.res_btn, self.res_btn_2)
        Forgot.setTabOrder(self.res_btn_2, self.checkBox_2)
        Forgot.setTabOrder(self.checkBox_2, self.redir_log)
        self.otp_fld.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pwd_fld.setEchoMode(QtWidgets.QLineEdit.Password)
        self.repass_fld.setEchoMode(QtWidgets.QLineEdit.Password)
        self.otp_fld.setEnabled(False)
        self.pwd_fld.setEnabled(False)
        self.repass_fld.setEnabled(False)

    def retranslateUi(self, Forgot):
        _translate = QtCore.QCoreApplication.translate
        Forgot.setWindowTitle(_translate("Forgot", "Form"))
        self.label_6.setText(_translate("Forgot", "Good Morning!"))
        self.label_7.setText(_translate("Forgot", "11:00 AM"))
        self.stat_lbl.setText(_translate("Forgot", ""))
        self.usr_fld.setPlaceholderText(_translate("Forgot", "Username"))
        self.res_btn.setText(_translate("Forgot", "Reset"))
        self.label_10.setText(_translate("Forgot", "Forgot Password"))
        self.email_fld.setPlaceholderText(_translate("Forgot", "Email Address"))
        self.otp_fld.setPlaceholderText(_translate("Forgot", "OTP"))
        self.pwd_fld.setPlaceholderText(_translate("Forgot", "Password"))
        self.repass_fld.setPlaceholderText(_translate("Forgot", "Confirm Password"))
        self.res_btn_2.setText(_translate("Forgot", "Send OTP"))
        self.redir_log.setText(
            _translate("Forgot", "Already have an account? Click Here")
        )
        if 6 <= int(chk) <= 11:
            self.label_6.setText(_translate("Forgot", "Good Morning!"))
        elif 12 <= int(chk) <= 14:
            self.label_6.setText(_translate("Forgot", "Good Afternoon!"))
        elif 14 <= int(chk) <= 23:
            self.label_6.setText(_translate("Forgot", "Good Evening!"))
        self.label_7.setText(_translate("Forgot", time))
        self.checkBox_2.stateChanged.connect(self.clickBox)
        self.res_btn_2.clicked.connect(lambda: self.otp_process())
        self.res_btn.clicked.connect(lambda: self.reset_process())
        global addr
        addr = Forgot
        self.redir_log.clicked.connect(lambda: self.open_Login(Forgot))

    def clickBox(self, state):
        if state == QtCore.Qt.Checked:
            self.otp_fld.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.pwd_fld.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.repass_fld.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.otp_fld.setEchoMode(QtWidgets.QLineEdit.Password)
            self.pwd_fld.setEchoMode(QtWidgets.QLineEdit.Password)
            self.repass_fld.setEchoMode(QtWidgets.QLineEdit.Password)

    def otp_process(self):
        result = sql_usr_mail_chk(self.usr_fld.text(), self.email_fld.text())
        try:
            bool_chk = result[0]
        except:
            bool_chk = result
        if bool_chk:
            global message
            message = send_otp(self.email_fld.text(), result[1])
            if message[0]:
                self.stat_lbl.setText("OTP Sent!")
                self.otp_fld.setEnabled(True)
                self.pwd_fld.setEnabled(True)
                self.repass_fld.setEnabled(True)
            else:
                self.stat_lbl.setText("Please try again!")
        else:
            self.stat_lbl.setText("Please check your credentials!")

    def reset_process(self):
        if (
            self.otp_fld.text() == str(message[1])
            and self.pwd_fld.text() == self.repass_fld.text()
        ):
            change_password(self.usr_fld.text(), self.pwd_fld.text())
            self.stat_lbl.setText("Reset Successful!")
            msg = QMessageBox()
            msg.setWindowTitle("Reset Password")
            msg.setText("Password reset successful!")
            msg.setIcon(QMessageBox.Information)
            x = msg.exec_()
            self.open_Login(addr)
        elif self.otp_fld != str(message[1]):
            self.stat_lbl.setText("Please check your OTP!")
        else:
            self.stat_lbl.setText("Please check your passwords!")

    def open_Login(self, reset_object):
        reset_object.hide()
        settime()
        self.log_app = QtWidgets.QApplication(sys.argv)
        self.log_Form = QtWidgets.QWidget()
        self.log_ui = Ui_Form()
        self.log_ui.setupUi(self.log_Form)
        self.log_Form.show()


# ------------------------------ End of Class Forgot Password -------------------------

if __name__ == "__main__":
    settime()
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
    cur.close()
