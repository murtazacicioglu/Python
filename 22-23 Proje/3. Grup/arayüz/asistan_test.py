import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer,QTime,QDate
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from asistanUi import Ui_MainWindow

class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

execution = MainThread()

class Mywindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startgif)
        
    def startgif(self):
        self.ui.movie = QtGui.QMovie("22-23 Proje/3. Grup/arayüz/circle.gif")
        self.ui.circle.setMovie(self.ui.movie)
        self.ui.movie.start()
        execution.start()


app = QApplication(sys.argv)
asistan = Mywindow()
asistan.show()
exit(app.exec_())