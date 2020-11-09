import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from InstagramAPI import InstagramAPI


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(454, 286)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: rgb(46, 52, 54);")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 181, 221))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        pixmap = QtGui.QPixmap("images/icon.png")
        self.label.setPixmap(pixmap)
        self.label.setStyleSheet("margin-left: 55;")

        self.verticalLayout.addWidget(self.label)
        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet(
            "background-color: rgb(186, 189, 182);\n"
            "color: black;\n"
            "text-align: center;"
        )
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        # self.setEchoMode(QLineEdit.Password) для маскировки пароля
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setStyleSheet(
            "background-color: rgb(186, 189, 182);\n"
            "color: rgb(0, 0, 0);\n"
            "text-align: center;"
        )
        self.lineEdit_2.setInputMask("")
        self.lineEdit_2.setText("")
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout.addWidget(self.lineEdit_2)
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton.setStyleSheet(
            "background-color: rgba(126, 52, 161, 0.9);\n"
            "color: rgb(46, 52, 54);\n"
            "font-weight: bold;"
        )
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.plainTextEdit.setGeometry(QtCore.QRect(220, 20, 211, 221))
        self.plainTextEdit.setReadOnly(True)
        self.plainTextEdit.setStyleSheet("background-color: rgb(186, 189, 182);\n")

        self.messageBox = QtWidgets.QMessageBox()
        pixmap = QtGui.QPixmap("images/okay.jpg")
        self.messageBox.setIconPixmap(pixmap)
        self.messageBox.setWindowTitle("Информация")
        self.messageBox.setStyleSheet(
            "background-color: rgb(255,255,255);\n"
            "color: rgb(46, 52, 54);\n"
            "font-weight: bold;\n"
            "text-align: center;"
        )
        self.messageBox.setText("Вы вошли в аккаунт")
        self.okButton = self.messageBox.addButton(
            "Окей", QtWidgets.QMessageBox.AcceptRole
        )

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Insta Unfollower"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "логин"))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "пароль"))
        self.pushButton.setText(_translate("MainWindow", "Войти"))
        self.plainTextEdit.setPlaceholderText(
            _translate("MainWindow", "                  Результат")
        )


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.buttonClicked)

    def send_info(self):
        """ Вывод результатов в textEdit через setPlainText"""
        followers = self.get_total_followers(self.api, self.user_id)
        followings = self.get_total_followings(self.api, self.user_id)
        self.non_follow = self.non_followers(followers, followings)
        self.total_non_followed = len(self.non_follow)
        results = [
            "=======================",
            f"Кол-во подписчиков: {len(followers)}",
            f"Кол-во подписок: {len(followings)}",
            f"Кол-во неподписаных: {self.total_non_followed}",
            "=======================\n",
        ]
        return "\n".join(results)

    def unfollow(self):
        text = "Вы отписались от всех"
        if self.total_non_followed == 0:
            return text
        else:
            for i in range(self.total_non_followed):
                if i >= self.total_non_followed:
                    break
                user = list(self.non_follow.keys())[len(self.non_follow) - 1]
                self.api.unfollow(self.non_follow[user])
                self.non_follow.pop(user)
            return text

    def buttonClicked(self):
        self.login = self.ui.lineEdit.text()
        self.password = self.ui.lineEdit_2.text()
        self.api = InstagramAPI(self.login, self.password)
        self.sing_in = self.api.login()
        try:
            self.user_id = self.api.username_id
        except AttributeError:
            self.ui.plainTextEdit.insertPlainText(
                "\u274E" + "Вход не выполнен, повторите попытку"
            )

        info = str(self.send_info())
        unfollow = str(self.unfollow())
        if self.sing_in is True:
            self.ui.messageBox.exec()
            if self.ui.messageBox.clickedButton() == self.ui.okButton:
                self.ui.plainTextEdit.clear()
                self.ui.plainTextEdit.insertPlainText(info)
                self.ui.plainTextEdit.insertPlainText("\u2611" + unfollow)
        else:
            self.ui.plainTextEdit.insertPlainText(
                "\u274E" + "Вход не выполнен, повторите попытку"
            )
            exit()

    def get_total_followers(self, api, user_id):
        followers = list()
        next_max_id = True

        while next_max_id:
            if next_max_id is True:
                next_max_id = ""
            _ = self.api.getUserFollowers(self.user_id, next_max_id)
            followers.extend(self.api.LastJson.get("users", []))
            next_max_id = self.api.LastJson.get("next_max_id", "")

        return followers

    def get_total_followings(self, api, user_id):
        followings = list()
        next_max_id = True

        while next_max_id:
            if next_max_id is True:
                next_max_id = ""
            _ = self.api.getUserFollowings(self.user_id, next_max_id)
            followings.extend(self.api.LastJson.get("users", []))
            next_max_id = self.api.LastJson.get("next_max_id", "")

        return followings

    def non_followers(self, followers, followings):
        non_followers = dict()
        dict_followers = dict()

        for follower in followers:
            dict_followers[follower["username"]] = follower["pk"]

        for followed_user in followings:
            if followed_user["username"] not in dict_followers:
                non_followers[followed_user["username"]] = followed_user["pk"]

        return non_followers


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec())
