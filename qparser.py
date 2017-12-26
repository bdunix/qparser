#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ui_qparser import Ui_MainWindow


class QParser(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        settings = QSettings()
        self.parserfolder_path = settings.value("parserfolder_path") or "C:\\work\\tools\\linux-ramdump-parser-v2\\"
        self.toolsfolder_path = settings.value("toolsfolder_path") or "C:\\work\\tools\\"

        self.dumpfolder_path = settings.value("dumpfolder_path") or "E:\\"
        self.vmlinux_path = os.path.join(self.dumpfolder_path, "vmlinux")
        self.outputfolder_path = os.path.join(self.dumpfolder_path, "parser\\")

        self.update_ui()

    def update_ui(self):
        self.parserfolderLineEdit.setText(self.parserfolder_path)
        self.toolsfolderLineEdit.setText(self.toolsfolder_path)
        self.dumpfolderLineEdit.setText(self.dumpfolder_path)
        self.vmlinuxLineEdit.setText(self.vmlinux_path)
        self.outputfolderLineEdit.setText(self.outputfolder_path)

    @pyqtSlot()
    def dumpfolderLineEdit_textChanged(self):
        self.vmlinux_path = os.path.join(self.dumpfolder_path, "vmlinux")
        self.outputfolder_path = os.path.join(self.dumpfolder_path, "parser\\")


    @pyqtSlot()
    def on_parserfolderPushButton_clicked(self):
        dir = os.path.dirname(self.parserfolder_path if self.parserfolder_path is not None else ".")
        path = QFileDialog.getExistingDirectory(self, "Open parser folder", dir)
        if path:
            self.parserfolder_path = path
            self.update_ui()
            #self.parserfolderLineEdit.setText(self.parserfolder_path)

    @pyqtSlot()
    def on_toolsfolderPushButton_clicked(self):
        dir = os.path.dirname(self.toolsfolder_path if self.toolsfolder_path is not None else ".")
        path = QFileDialog.getExistingDirectory(self, "Open tools((gdb/nm/objdump)) folder", dir)
        if path:
            self.toolsfolder_path = path
            self.toolsfolderLineEdit.setText(self.toolsfolder_path)

    @pyqtSlot()
    def on_dumpfolderPushButton_clicked(self):
        dir = os.path.dirname(self.dumpfolder_path if self.dumpfolder_path is not None else ".")
        path = QFileDialog.getExistingDirectory(self, "Open dump folder", dir)
        if path:
            self.dumpfolder_path = path
            self.dumpfolderLineEdit.setText(self.dumpfolder_path)

    @pyqtSlot()
    def on_vmlinuxPushButton_clicked(self):
        dir = os.path.dirname(self.vmlinux_path if self.vmlinux_path is not None else ".")
        path = QFileDialog.getOpenFileName(self, "Open vmlinux", dir)[0]
        if path:
            self.vmlinux_path = path
            self.vmlinuxLineEdit.setText(self.vmlinux_path)

    @pyqtSlot()
    def on_outputfolderPushButton_clicked(self):
        dir = os.path.dirname(self.outputfolder_path if self.outputfolder_path is not None else ".")
        path = QFileDialog.getExistingDirectory(self, "Open output folder", dir)
        if path:
            self.outputfolder_path = path
            self.outputfolderLineEdit.setText(self.outputfolder_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainwin = QParser()
    mainwin.show()

    sys.exit(app.exec_())
