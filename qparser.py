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

        self.dumpfolder_path = None
        self.vmlinux_path = None
        self.outputfolder_path = None

    @pyqtSlot()
    def on_dumpfolderPushButton_clicked(self):
        dir = QFileDialog.getExistingDirectory(self, "Open dump folder",
                                               self.dumpfolder_path if self.dumpfolder_path is not None else ".")
        if dir:
            self.dumpfolder_path = dir
            self.dumpfolderLineEdit.setText(self.dumpfolder_path)

    @pyqtSlot()
    def on_vmlinuxPushButton_clicked(self):
        dir = QFileDialog.getOpenFileName(self, "Open vmlinux",
                                          self.vmlinux_path if self.vmlinux_path is not None else ".")
        dir = dir[0]
        if dir:
            self.vmlinux_path = dir
            self.vmlinuxLineEdit.setText(self.vmlinux_path)

    @pyqtSlot()
    def on_outputfolderPushButon_clicked(self):
        dir = QFileDialog.getExistingDirectory(self, "Open output folder",
                                               self.outputfolder_path if self.outputfolder_path is not None else ".")
        if dir:
            self.outputfolder_path = dir
            self.outputfolderLineEdit.setText(self.outputfolder_path)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    mainwin = QParser()
    mainwin.show()

    sys.exit(app.exec_())
