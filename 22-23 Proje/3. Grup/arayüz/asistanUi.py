from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(890, 657)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.circle = QtWidgets.QLabel(self.centralwidget)
        self.circle.setGeometry(QtCore.QRect(0, 0, 891, 651))
        font = QtGui.QFont()
        font.setFamily("Roman")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.circle.setFont(font)
        self.circle.setStyleSheet("font: 8pt \"Roman\";")
        self.circle.setText("")
        self.circle.setPixmap(QtGui.QPixmap("22-23 Proje/3. Grup/arayüz/circle.gif"))
        self.circle.setScaledContents(True)
        self.circle.setIndent(-1)
        self.circle.setObjectName("circle")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(390, 297, 141, 61))
        font = QtGui.QFont()
        font.setFamily("OCR A Extended")
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("background: transparent;\n"
            "color: rgb(255, 255, 255);\n"
            "selection-background-color: rgb(18, 4, 33);\n"
            "\n"
            "background-color: rgb(18, 4, 33);\n"
            "border-color: rgb(205, 169, 244);")
        self.pushButton.setCheckable(False)
        self.pushButton.setObjectName("pushButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setEnabled(False)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ASİSTAN"))
        self.pushButton.setText(_translate("MainWindow", "A.S.İ.S.T.A.N"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
