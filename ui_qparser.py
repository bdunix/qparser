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
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.parserfolderLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.parserfolderLineEdit.setObjectName("parserfolderLineEdit")
        self.gridLayout.addWidget(self.parserfolderLineEdit, 0, 1, 1, 1)
        self.parserfolderPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.parserfolderPushButton.setObjectName("parserfolderPushButton")
        self.gridLayout.addWidget(self.parserfolderPushButton, 0, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.toolsfolderLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.toolsfolderLineEdit.setObjectName("toolsfolderLineEdit")
        self.gridLayout.addWidget(self.toolsfolderLineEdit, 1, 1, 1, 1)
        self.toolsfolderPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.toolsfolderPushButton.setObjectName("toolsfolderPushButton")
        self.gridLayout.addWidget(self.toolsfolderPushButton, 1, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 2, 0, 1, 1)
        self.toolsfolder64LineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.toolsfolder64LineEdit.setObjectName("toolsfolder64LineEdit")
        self.gridLayout.addWidget(self.toolsfolder64LineEdit, 2, 1, 1, 1)
        self.toolsfolder64PushButton = QtWidgets.QPushButton(self.centralwidget)
        self.toolsfolder64PushButton.setObjectName("toolsfolder64PushButton")
        self.gridLayout.addWidget(self.toolsfolder64PushButton, 2, 2, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.dumpfolderLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.dumpfolderLineEdit.setObjectName("dumpfolderLineEdit")
        self.gridLayout_2.addWidget(self.dumpfolderLineEdit, 0, 1, 1, 1)
        self.dumpfolderPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.dumpfolderPushButton.setObjectName("dumpfolderPushButton")
        self.gridLayout_2.addWidget(self.dumpfolderPushButton, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.vmlinuxLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.vmlinuxLineEdit.setObjectName("vmlinuxLineEdit")
        self.gridLayout_2.addWidget(self.vmlinuxLineEdit, 1, 1, 1, 1)
        self.vmlinuxPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.vmlinuxPushButton.setObjectName("vmlinuxPushButton")
        self.gridLayout_2.addWidget(self.vmlinuxPushButton, 1, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.outputfolderLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.outputfolderLineEdit.setObjectName("outputfolderLineEdit")
        self.gridLayout_2.addWidget(self.outputfolderLineEdit, 2, 1, 1, 1)
        self.outputfolderPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.outputfolderPushButton.setObjectName("outputfolderPushButton")
        self.gridLayout_2.addWidget(self.outputfolderPushButton, 2, 2, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_2)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.forcehwCheckBox = QtWidgets.QCheckBox(self.groupBox_2)
        self.forcehwCheckBox.setObjectName("forcehwCheckBox")
        self.gridLayout_3.addWidget(self.forcehwCheckBox, 0, 2, 1, 1)
        self.hwidLineEdit = QtWidgets.QLineEdit(self.groupBox_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hwidLineEdit.sizePolicy().hasHeightForWidth())
        self.hwidLineEdit.setSizePolicy(sizePolicy)
        self.hwidLineEdit.setObjectName("hwidLineEdit")
        self.gridLayout_3.addWidget(self.hwidLineEdit, 0, 4, 1, 1)
        self.aarch64CheckBox = QtWidgets.QCheckBox(self.groupBox_2)
        self.aarch64CheckBox.setChecked(True)
        self.aarch64CheckBox.setObjectName("aarch64CheckBox")
        self.gridLayout_3.addWidget(self.aarch64CheckBox, 0, 0, 1, 1)
        self.everythingCheckBox = QtWidgets.QCheckBox(self.groupBox_2)
        self.everythingCheckBox.setChecked(True)
        self.everythingCheckBox.setObjectName("everythingCheckBox")
        self.gridLayout_3.addWidget(self.everythingCheckBox, 0, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem, 0, 5, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setObjectName("label_6")
        self.verticalLayout.addWidget(self.label_6)
        self.outputTextBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.outputTextBrowser.setObjectName("outputTextBrowser")
        self.verticalLayout.addWidget(self.outputTextBrowser)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.parsePushButton = QtWidgets.QPushButton(self.centralwidget)
        self.parsePushButton.setObjectName("parsePushButton")
        self.horizontalLayout.addWidget(self.parsePushButton)
        self.exitPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.exitPushButton.setObjectName("exitPushButton")
        self.horizontalLayout.addWidget(self.exitPushButton)
        self.resultPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.resultPushButton.setObjectName("resultPushButton")
        self.horizontalLayout.addWidget(self.resultPushButton)
        self.t32PushButton = QtWidgets.QPushButton(self.centralwidget)
        self.t32PushButton.setObjectName("t32PushButton")
        self.horizontalLayout.addWidget(self.t32PushButton)
        self.explorePushButton = QtWidgets.QPushButton(self.centralwidget)
        self.explorePushButton.setObjectName("explorePushButton")
        self.horizontalLayout.addWidget(self.explorePushButton)
        self.decoderPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.decoderPushButton.setObjectName("decoderPushButton")
        self.horizontalLayout.addWidget(self.decoderPushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.fileMenu = QtWidgets.QMenu(self.menubar)
        self.fileMenu.setObjectName("fileMenu")
        self.helpMenu = QtWidgets.QMenu(self.menubar)
        self.helpMenu.setObjectName("helpMenu")
        MainWindow.setMenuBar(self.menubar)
        self.exitAction = QtWidgets.QAction(MainWindow)
        self.exitAction.setObjectName("exitAction")
        self.settingAction = QtWidgets.QAction(MainWindow)
        self.settingAction.setObjectName("settingAction")
        self.aboutAction = QtWidgets.QAction(MainWindow)
        self.aboutAction.setObjectName("aboutAction")
        self.fileMenu.addAction(self.settingAction)
        self.fileMenu.addAction(self.exitAction)
        self.helpMenu.addAction(self.aboutAction)
        self.menubar.addAction(self.fileMenu.menuAction())
        self.menubar.addAction(self.helpMenu.menuAction())

        self.retranslateUi(MainWindow)
        self.exitAction.triggered.connect(MainWindow.close)
        self.exitPushButton.clicked.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "QParser"))
        self.label_4.setText(_translate("MainWindow", "Parser Folder:"))
        self.parserfolderPushButton.setText(_translate("MainWindow", "..."))
        self.label_5.setText(_translate("MainWindow", "Tools(gdb/nm/objdump) Folder:"))
        self.toolsfolderPushButton.setText(_translate("MainWindow", "..."))
        self.label_7.setText(_translate("MainWindow", "Tools(gdb/nm/objdump) Folder (64bit ):"))
        self.toolsfolder64PushButton.setText(_translate("MainWindow", "..."))
        self.label.setText(_translate("MainWindow", "Dump Folder:"))
        self.dumpfolderPushButton.setText(_translate("MainWindow", "..."))
        self.label_2.setText(_translate("MainWindow", "Vmlinux:"))
        self.vmlinuxPushButton.setText(_translate("MainWindow", "..."))
        self.label_3.setText(_translate("MainWindow", "Output Folder:"))
        self.outputfolderPushButton.setText(_translate("MainWindow", "..."))
        self.groupBox_2.setTitle(_translate("MainWindow", "Parser Options"))
        self.forcehwCheckBox.setText(_translate("MainWindow", "force hardware"))
        self.hwidLineEdit.setText(_translate("MainWindow", "8953"))
        self.aarch64CheckBox.setText(_translate("MainWindow", "64bit"))
        self.everythingCheckBox.setText(_translate("MainWindow", "everything"))
        self.label_6.setText(_translate("MainWindow", "Output:"))
        self.parsePushButton.setText(_translate("MainWindow", "Parse"))
        self.exitPushButton.setText(_translate("MainWindow", "Exit"))
        self.resultPushButton.setText(_translate("MainWindow", "Result"))
        self.t32PushButton.setText(_translate("MainWindow", "Launch T32"))
        self.explorePushButton.setText(_translate("MainWindow", "Explore Output"))
        self.decoderPushButton.setText(_translate("MainWindow", "Decoder"))
        self.fileMenu.setTitle(_translate("MainWindow", "File"))
        self.helpMenu.setTitle(_translate("MainWindow", "Help"))
        self.exitAction.setText(_translate("MainWindow", "Exit"))
        self.settingAction.setText(_translate("MainWindow", "Setting"))
        self.aboutAction.setText(_translate("MainWindow", "About"))

