# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qparser.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(40, 140, 541, 83))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.dumpfolderLineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.dumpfolderLineEdit.setObjectName("dumpfolderLineEdit")
        self.gridLayout.addWidget(self.dumpfolderLineEdit, 0, 1, 1, 1)
        self.dumpfolderPushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.dumpfolderPushButton.setObjectName("dumpfolderPushButton")
        self.gridLayout.addWidget(self.dumpfolderPushButton, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.vmlinuxPushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.vmlinuxPushButton.setObjectName("vmlinuxPushButton")
        self.gridLayout.addWidget(self.vmlinuxPushButton, 1, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.outputfolderLineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.outputfolderLineEdit.setObjectName("outputfolderLineEdit")
        self.gridLayout.addWidget(self.outputfolderLineEdit, 2, 1, 1, 1)
        self.outputfolderPushButton = QtWidgets.QPushButton(self.layoutWidget)
        self.outputfolderPushButton.setObjectName("outputfolderPushButton")
        self.gridLayout.addWidget(self.outputfolderPushButton, 2, 2, 1, 1)
        self.vmlinuxLineEdit = QtWidgets.QLineEdit(self.layoutWidget)
        self.vmlinuxLineEdit.setObjectName("vmlinuxLineEdit")
        self.gridLayout.addWidget(self.vmlinuxLineEdit, 1, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(40, 20, 511, 91))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        self.parserfolderLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.parserfolderLineEdit.setObjectName("parserfolderLineEdit")
        self.gridLayout_2.addWidget(self.parserfolderLineEdit, 0, 1, 1, 1)
        self.parserfolderPushButton = QtWidgets.QPushButton(self.groupBox)
        self.parserfolderPushButton.setObjectName("parserfolderPushButton")
        self.gridLayout_2.addWidget(self.parserfolderPushButton, 0, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 0, 1, 1)
        self.toolsfolderLineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.toolsfolderLineEdit.setObjectName("toolsfolderLineEdit")
        self.gridLayout_2.addWidget(self.toolsfolderLineEdit, 1, 1, 1, 1)
        self.toolsfolderPushButton = QtWidgets.QPushButton(self.groupBox)
        self.toolsfolderPushButton.setObjectName("toolsfolderPushButton")
        self.gridLayout_2.addWidget(self.toolsfolderPushButton, 1, 2, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.fileMenu = QtWidgets.QMenu(self.menubar)
        self.fileMenu.setObjectName("fileMenu")
        MainWindow.setMenuBar(self.menubar)
        self.exitAction = QtWidgets.QAction(MainWindow)
        self.exitAction.setObjectName("exitAction")
        self.settingAction = QtWidgets.QAction(MainWindow)
        self.settingAction.setObjectName("settingAction")
        self.fileMenu.addAction(self.settingAction)
        self.fileMenu.addAction(self.exitAction)
        self.menubar.addAction(self.fileMenu.menuAction())

        self.retranslateUi(MainWindow)
        self.exitAction.triggered.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "QParser"))
        self.label.setText(_translate("MainWindow", "Dump Folder:"))
        self.dumpfolderPushButton.setText(_translate("MainWindow", "Open"))
        self.label_2.setText(_translate("MainWindow", "Vmlinux:"))
        self.vmlinuxPushButton.setText(_translate("MainWindow", "Open"))
        self.label_3.setText(_translate("MainWindow", "Output Folder:"))
        self.outputfolderPushButton.setText(_translate("MainWindow", "Open"))
        self.groupBox.setTitle(_translate("MainWindow", "Parser Info"))
        self.label_4.setText(_translate("MainWindow", "Parser Folder:"))
        self.parserfolderPushButton.setText(_translate("MainWindow", "Open"))
        self.label_5.setText(_translate("MainWindow", "Tools(gdb/nm/objdump) Folder:"))
        self.toolsfolderPushButton.setText(_translate("MainWindow", "Open"))
        self.fileMenu.setTitle(_translate("MainWindow", "File"))
        self.exitAction.setText(_translate("MainWindow", "Exit"))
        self.settingAction.setText(_translate("MainWindow", "Setting"))

