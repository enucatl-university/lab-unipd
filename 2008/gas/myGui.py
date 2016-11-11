# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'myGui.ui'
#
# Created: Mon May 26 13:06:43 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,800,600).size()).expandedTo(MainWindow.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20,40,161,31))
        self.lineEdit.setObjectName("lineEdit")

        self.textBrowser = QtGui.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(30,80,401,441))
        self.textBrowser.setObjectName("textBrowser")

        self.Binterpolazione = QtGui.QPushButton(self.centralwidget)
        self.Binterpolazione.setGeometry(QtCore.QRect(470,80,121,30))
        self.Binterpolazione.setObjectName("Binterpolazione")

        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30,20,81,20))
        self.label.setObjectName("label")

        self.spinValori = QtGui.QSpinBox(self.centralwidget)
        self.spinValori.setGeometry(QtCore.QRect(190,40,62,30))
        self.spinValori.setObjectName("spinValori")

        self.spinErrori = QtGui.QSpinBox(self.centralwidget)
        self.spinErrori.setGeometry(QtCore.QRect(260,40,62,30))
        self.spinErrori.setObjectName("spinErrori")

        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(200,20,41,20))
        self.label_2.setObjectName("label_2")

        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(270,20,41,20))
        self.label_3.setObjectName("label_3")

        self.Bmedia = QtGui.QPushButton(self.centralwidget)
        self.Bmedia.setGeometry(QtCore.QRect(470,140,149,30))
        self.Bmedia.setObjectName("Bmedia")

        self.Bmediap = QtGui.QPushButton(self.centralwidget)
        self.Bmediap.setGeometry(QtCore.QRect(470,170,128,30))
        self.Bmediap.setObjectName("Bmediap")

        self.Bscarta = QtGui.QPushButton(self.centralwidget)
        self.Bscarta.setGeometry(QtCore.QRect(470,200,116,30))
        self.Bscarta.setObjectName("Bscarta")

        self.Salva = QtGui.QPushButton(self.centralwidget)
        self.Salva.setGeometry(QtCore.QRect(470,110,121,30))
        self.Salva.setObjectName("Salva")
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,800,27))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.lineEdit.setText(QtGui.QApplication.translate("MainWindow", "0c 0e", None, QtGui.QApplication.UnicodeUTF8))
        self.Binterpolazione.setText(QtGui.QApplication.translate("MainWindow", "Inter. lineare", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "File di dati:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Valori", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Errori", None, QtGui.QApplication.UnicodeUTF8))
        self.Bmedia.setText(QtGui.QApplication.translate("MainWindow", "Media aritmetica", None, QtGui.QApplication.UnicodeUTF8))
        self.Bmediap.setText(QtGui.QApplication.translate("MainWindow", "Media pesata", None, QtGui.QApplication.UnicodeUTF8))
        self.Bscarta.setText(QtGui.QApplication.translate("MainWindow", "Scarta dati", None, QtGui.QApplication.UnicodeUTF8))
        self.Salva.setText(QtGui.QApplication.translate("MainWindow", "Salva I.L.", None, QtGui.QApplication.UnicodeUTF8))

