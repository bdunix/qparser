# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'decoder.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_decoderDlg(object):
    def setupUi(self, decoderDlg):
        decoderDlg.setObjectName("decoderDlg")
        decoderDlg.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(decoderDlg)
        self.buttonBox.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.inputTextEdit = QtWidgets.QTextEdit(decoderDlg)
        self.inputTextEdit.setGeometry(QtCore.QRect(20, 10, 341, 71))
        self.inputTextEdit.setObjectName("inputTextEdit")
        self.panicregPushButton = QtWidgets.QPushButton(decoderDlg)
        self.panicregPushButton.setGeometry(QtCore.QRect(20, 90, 101, 25))
        self.panicregPushButton.setObjectName("panicregPushButton")
        self.outputTextEdit = QtWidgets.QTextEdit(decoderDlg)
        self.outputTextEdit.setGeometry(QtCore.QRect(20, 119, 341, 111))
        self.outputTextEdit.setObjectName("outputTextEdit")

        self.retranslateUi(decoderDlg)
        self.buttonBox.accepted.connect(decoderDlg.accept)
        self.buttonBox.rejected.connect(decoderDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(decoderDlg)

    def retranslateUi(self, decoderDlg):
        _translate = QtCore.QCoreApplication.translate
        decoderDlg.setWindowTitle(_translate("decoderDlg", "Decoder"))
        self.panicregPushButton.setText(_translate("decoderDlg", "Panic Register"))

