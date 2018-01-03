#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os
import sys
import platform
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ui_qparser import Ui_MainWindow


class QParser(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.load_settings()

        self.update_ui()

    def load_settings(self):
        if platform.system() == 'Linux':
            self.python_path = "/usr/bin/python2"
            parserfolder = "/opt/tools/linux-ramdump-parser-v2"
            toolsfolder = "/opt/LinaroToolchain/gcc-linaro-4.9.4-2017.01-x86_64_aarch64-elf/bin"
            dumpfolder = "~/case"
            gdb64 = "aarch64-elf-gdb"
            nm64 = "aarch64-elf-nm"
            objdump64 = "aarch64-elf-objdump"
            gdb = "arm-eabi-gdb"
            nm = "arm-eabi-nm"
            objdump = "arm-eabi-objdump"

        if platform.system() == 'Windows':
            self.python_path = "C:\Python27\python.exe"
            parserfolder = "C:\\work\\tools\\linux-ramdump-parser-v2"
            toolsfolder = "C:\\work\\tools"
            dumpfolder = "E:\\"
            gdb64 = "aarch64-linux-gnu-gdb.exe"
            nm64 = "aarch64-linux-gnu-gcc-nm.exe"
            objdump64 = "aarch64-linux-gnu-objdump.exe"
            gdb = "arm-none-eabi-gdb.exe"
            nm = "arm-none-eabi-nm.exe"
            objdump = "arm-none-eabi-objdump.exe"

        settings = QSettings()
        self.parserfolder_path = settings.value("parserfolder_path") or parserfolder
        self.parser_path = os.path.join(self.parserfolder_path, "ramparse.py")
        self.toolsfolder_path = settings.value("toolsfolder_path") or toolsfolder
        self.gdb64_path = os.path.join(self.toolsfolder_path, gdb64)
        self.nm64_path = os.path.join(self.toolsfolder_path, nm64)
        self.objdump64_path = os.path.join(self.toolsfolder_path, objdump64)
        self.gdb_path = os.path.join(self.toolsfolder_path, gdb)
        self.nm_path = os.path.join(self.toolsfolder_path, nm)
        self.objdump_path = os.path.join(self.toolsfolder_path, objdump)
        self.dumpfolder_path = settings.value("dumpfolder_path") or dumpfolder
        self.vmlinux_path = settings.value("vmlinux_path") \
                            or os.path.join(self.dumpfolder_path, "vmlinux")
        self.outputfolder_path = settings.value("outputfolder_path") \
                                 or os.path.join(self.dumpfolder_path, "parser")
        self.hardware = self.forcehwLineEdit.text()

    def save_settings(self):
        settings = QSettings()
        self.parserfolder_path = settings.setValue("parserfolder_path", self.parserfolder_path)
        self.toolsfolder_path = settings.setValue("toolsfolder_path", self.toolsfolder_path)
        self.dumpfolder_path = settings.setValue("dumpfolder_path", self.dumpfolder_path)
        self.vmlinux_path = settings.setValue("vmlinux_path", self.vmlinux_path)
        self.outputfolder_path = settings.setValue("outputfolder_path", self.outputfolder_path)

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

    def run_parser_subprocess(self, args):
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        while p.poll() is None:
            line = p.stdout.readline()
            line = line.strip()
            if line:
                print('Subprocess output: [{}]'.format(line))
        if p.returncode == 0:
            print('Subprocess success')
        else:
            print('Subprocess failed')

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

    @pyqtSlot()
    def on_parsePushButton_clicked(self):
        args = [self.python_path, self.parser_path, "-v", self.vmlinux_path, "-g", self.gdb64_path, \
                "-n", self.nm64_path, "-j", self.objdump64_path, "-o", self.outputfolder_path, \
                "-a", self.dumpfolder_path, "-x"]
        if self.forcehwCheckBox.isChecked():
            args += ["--force-hardware", self.hardware]
        self.outputTextEdit.setText(" ".join(args))
        self.run_parser_subprocess(args)

    @pyqtSlot()
    def on_forcehwLineEdit_textChanged(self, arg):
        self.hardware = self.forcehwLineEdit.text()

    def closeEvent(self, *args, **kwargs):
        self.save_settings()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setOrganizationName("bdu ltd.")
    app.setOrganizationDomain("bdu.org")
    app.setApplicationName("QParser")

    m = QParser()
    m.show()

    sys.exit(app.exec_())
