#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
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
        self.parserfolder_path = settings.value("parserfolder_path") \
                                 or "C:\\work\\tools\\linux-ramdump-parser-v2"
        self.toolsfolder_path = settings.value("toolsfolder_path") \
                                or "C:\\work\\tools"
        self.dumpfolder_path = settings.value("dumpfolder_path") \
                               or "E:\\"
        self.vmlinux_path = settings.value("vmlinux_path") \
                            or os.path.join(self.dumpfolder_path, "vmlinux")
        self.outputfolder_path = settings.value("outputfolder_path") \
                                 or os.path.join(self.dumpfolder_path, "parser")

        self.python_path = "C:\Python27\python.exe"
        parser = "ramparse.py"
        self.parser_path = os.path.join(self.parserfolder_path, parser)

        self.update_tools_path()

        self.hardware = "660"


        self.update_ui()

    def update_tools_path(self):
        gdb64 = "aarch64-linux-gnu-gdb.exe"
        nm64 = "aarch64-linux-gnu-gcc-nm.exe"
        objdump64 = "aarch64-linux-gnu-objdump.exe"
        self.gdb64_path = os.path.join(self.toolsfolder_path, gdb64)
        self.nm64_path = os.path.join(self.toolsfolder_path, nm64)
        self.objdump64_path = os.path.join(self.toolsfolder_path, objdump64)

    def update_ui(self):
        self.parserfolderLineEdit.setText(self.parserfolder_path)
        self.toolsfolderLineEdit.setText(self.toolsfolder_path)
        self.dumpfolderLineEdit.setText(self.dumpfolder_path)
        self.vmlinuxLineEdit.setText(self.vmlinux_path)
        self.outputfolderLineEdit.setText(self.outputfolder_path)

    def get_folder_path(self, folder_path):
        dir = os.path.dirname(folder_path if folder_path is not None else ".")
        path = QFileDialog.getExistingDirectory(self, "Open folder", dir)
        return QDir.toNativeSeparators(path)

    def get_file_path(self, file_path):
        dir = os.path.dirname(file_path if file_path is not None else ".")
        path = QFileDialog.getOpenFileName(self, "Open file", dir)
        path = path[0]
        return QDir.toNativeSeparators(path)

    @pyqtSlot()
    def on_parserfolderPushButton_clicked(self):
        path = self.get_folder_path(self.parserfolder_path)
        if path:
            self.parserfolder_path = path
            self.parserfolderLineEdit.setText(path)

    @pyqtSlot()
    def on_toolsfolderPushButton_clicked(self):
        path = self.get_folder_path(self.toolsfolder_path)
        if path:
            self.toolsfolder_path = path
            self.toolsfolderLineEdit.setText(path)
            self.update_toolspath()

    @pyqtSlot()
    def on_dumpfolderPushButton_clicked(self):
        path = self.get_folder_path(self.dumpfolder_path)
        if path:
            self.dumpfolder_path = path
            self.dumpfolderLineEdit.setText(path)

    @pyqtSlot()
    def on_vmlinuxPushButton_clicked(self):
        path = self.get_file_path(self.vmlinux_path)
        if path:
            self.vmlinux_path = path
            self.vmlinuxLineEdit.setText(path)

    @pyqtSlot()
    def on_outputfolderPushButton_clicked(self):
        path = self.get_folder_path(self.outputfolder_path)
        if path:
            self.outputfolder_path = path
            self.outputfolderLineEdit.setText(path)

    @pyqtSlot(str)
    def on_dumpfolderLineEdit_textChanged(self, arg):
        self.vmlinux_path = os.path.join(arg, "vmlinux")
        self.outputfolder_path = os.path.join(arg, "parser")
        self.update_ui()

    def run_parser_subprocess(self):
        p = subprocess.run(self.cmdline)
        while p.poll() is None:
            line = p.stdout.readline()
            line = line.strip()
            if line:
                print('Subprogram output: [{}]'.format(line))
        if p.returncode == 0:
            print('Subprogram success')
        else:
            print('Subprogram failed')

    @pyqtSlot()
    def on_parsePushButton_clicked(self):
        options = [self.python_path, self.parser_path, "-v", self.vmlinux_path, "-g", self.gdb64_path, \
                       "-n", self.nm64_path, "-j", self.objdump64_path, "-o", self.outputfolder_path, \
                       "-a", self.dumpfolder_path, "--force-hardware", self.hardware, "-x"]
        self.cmdline = " ".join(options)
        self.outputTextEdit.setText(self.cmdline)

        self.run_parser_subprocess()


def closeEvent(self, *args, **kwargs):
        settings = QSettings()
        self.parserfolder_path = settings.setValue("parserfolder_path", self.parserfolder_path)
        self.toolsfolder_path = settings.setValue("toolsfolder_path", self.toolsfolder_path)
        self.dumpfolder_path = settings.setValue("dumpfolder_path", self.dumpfolder_path)
        self.vmlinux_path = settings.setValue("vmlinux_path", self.vmlinux_path)
        self.outputfolder_path = settings.setValue("outputfolder_path", self.outputfolder_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setOrganizationName("bdu ltd.")
    app.setOrganizationDomain("bdu.org")
    app.setApplicationName("QParser")

    m = QParser()
    m.show()

    sys.exit(app.exec_())
