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


class PathSettings():
    def __init__(self):
        self.__paths = {}

        if platform.system() == 'Linux':
            self.__paths['python'] = '/usr/bin/python2'
            self.__paths['parserfolder'] = '/opt/tools/linux-ramdump-parser-v2'
            self.__paths['toolsfolder'] = '/opt/LinaroToolchain/gcc-linaro-4.9.4-2017.01-x86_64_arm-eabi/bin'
            self.__paths['toolsfolder64'] = '/opt/LinaroToolchain/gcc-linaro-4.9.4-2017.01-x86_64_aarch64-elf/bin'
            prefix = 'arm-eabi-'
            prefix64 = 'aarch64-elf-'
            postfix = ''

        if platform.system() == 'Windows':
            self.__paths['python'] = "C:\Python27\python.exe"
            self.__paths['parserfolder'] = "C:\\work\\tools\\linux-ramdump-parser-v2"
            self.__paths['toolsfolder'] = "C:\\tools\\arm-none-eabi"
            self.__paths['toolsfolder64'] = "C:\\tools\\aarch64-linux-gnu-gcc"
            prefix = 'arm-none-eabi'
            prefix64 = 'aarch64-linux-gnu-gcc-'
            postfix = '.exe'

        self.__paths['parser'] = os.path.join(self.__paths['parserfolder'], 'ramparse.py')

        tools = ['gdb', 'nm', 'objdump']
        for key in tools:
            self.__paths[key] = os.path.join(self.__paths['toolsfolder'], prefix + key + postfix)
            self.__paths[key + '64'] = os.path.join(self.__paths['toolsfolder64'], prefix64 + key + postfix)

        self.__paths['dumpfolder'] = os.path.join(os.environ["HOME"], "case")
        self.__paths['vmlinux'] = os.path.join(self.__paths['dumpfolder'], "vmlinux")
        self.__paths['outputfolder'] = os.path.join(self.__paths['dumpfolder'], "parser")

        # for k,v in self.__paths.items(): print("{}:{}".format(k, v))

        self.load()

    def load(self, org=None, ):
        '''Load all stored value from system'''
        settings = QSettings()
        for k, v in self.__paths.items():
            self.__paths[k] = settings.value(k) or v

    def save(self):
        '''Store all value in system'''
        settings = QSettings()
        for k, v in self.__paths.items():
            settings.setValue(k, v)

    def get(self, key=None):
        return self.__paths[key]

    def set(self, key=None, value=None):
        self.__paths[key] = value


class QParser(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.paths = PathSettings()

        self.refresh_ui()

    def closeEvent(self, *args, **kwargs):
        self.paths.save()

    def refresh_ui(self):
        self.parserfolderLineEdit.setText(self.paths.get('parserfolder'))
        self.toolsfolderLineEdit.setText(self.paths.get('toolsfolder'))
        self.toolsfolder64LineEdit.setText(self.paths.get('toolsfolder64'))
        self.dumpfolderLineEdit.setText(self.paths.get('dumpfolder'))
        self.vmlinuxLineEdit.setText(self.paths.get('vmlinux'))
        self.outputfolderLineEdit.setText(self.paths.get('outputfolder'))

    def get_folder_path(self, folder_path):
        dir = os.path.dirname(folder_path if folder_path is not None else ".")
        path = QFileDialog.getExistingDirectory(self, "Open folder", dir)
        return QDir.toNativeSeparators(path)

    def get_file_path(self, file_path):
        dir = os.path.dirname(file_path if file_path is not None else ".")
        path = QFileDialog.getOpenFileName(self, "Open file", dir)
        path = path[0]
        return QDir.toNativeSeparators(path)

    def run_parser_subprocess(self, program, args):
        p = subprocess.Popen([program] + args, stdout=subprocess.PIPE)
        while p.poll() is None:
            line = p.stdout.readline()
            line = line.strip()
            if line:
                print('Subprocess output: [{}]'.format(line))
        if p.returncode == 0:
            print('Subprocess success')
        else:
            print('Subprocess failed')

    def run_parser_qprocess(self, program, args):
        self.process = QProcess()

        self.process.readyReadStandardOutput.connect(self.on_process_readyReadStandardOutput)
        self.process.readyReadStandardError.connect(self.on_process_readyReadStandardError)
        self.process.finished.connect(self.on_process_finished)

        self.process.start(program, args)

    def on_process_readyReadStandardOutput(self):
        #while self.process.canReadLine(): print(self.process.readLine())
        line = str(self.process.readAllStandardOutput())
        self.outputTextBrowser.setTextColor(Qt.blue)
        self.outputTextBrowser.append(line)


    def on_process_readyReadStandardError(self):
        line = str(self.process.readAllStandardError())
        # if line.endswith('\n'):
        #    print(line)
        # else:
        #   print(line, end=' ')
        self.outputTextBrowser.setTextColor(Qt.red)
        self.outputTextBrowser.append(line)

    def on_process_finished(self):
        print("QProcess Finishied!")

    @pyqtSlot(str)
    def on_parserfolderLineEdit_textChanged(self, text):
        self.paths.set('parserfolder', text)

    @pyqtSlot()
    def on_parserfolderPushButton_clicked(self):
        path = self.get_folder_path(self.parserfolderLineEdit.text())
        if path:
            self.parserfolderLineEdit.setText(path)

    @pyqtSlot(str)
    def on_toolsfolderLineEdit_textChanged(self, text):
        self.paths.set('toolsfolder', text)

    @pyqtSlot()
    def on_toolsfolderPushButton_clicked(self):
        path = self.get_folder_path(self.toolsfolderLineEdit.text())
        if path:
            self.toolsfolderLineEdit.setText(path)

    @pyqtSlot(str)
    def on_toolsfolder64LineEdit_textChanged(self, text):
        self.paths.set('toolsfolder64', text)

    @pyqtSlot()
    def on_toolsfolder64PushButton_clicked(self):
        path = self.get_folder_path(self.toolsfolder64LineEdit.text())
        if path:
            self.toolsfolder64LineEdit.setText(path)

    @pyqtSlot(str)
    def on_dumpfolderLineEdit_textChanged(self, text):
        self.paths.set('dumpfolder', text)
        self.vmlinuxLineEdit.setText(os.path.join(text, "vmlinux"))
        self.outputfolderLineEdit.setText(os.path.join(text, "parser"))

    @pyqtSlot()
    def on_dumpfolderPushButton_clicked(self):
        path = self.get_folder_path(self.dumpfolderLineEdit.text())
        if path:
            self.dumpfolderLineEdit.setText(path)

    @pyqtSlot(str)
    def on_vmlinuxLineEdit_textChanged(self, text):
        self.paths.set('vmlinux', text)

    @pyqtSlot()
    def on_vmlinuxPushButton_clicked(self):
        path = self.get_file_path(self.vmlinuxLineEdit.text())
        if path:
            self.vmlinuxLineEdit.setText(path)

    @pyqtSlot(str)
    def on_outputfolderLineEdit_textChanged(self, text):
        self.paths.set('outputfolder', text)

    @pyqtSlot()
    def on_outputfolderPushButton_clicked(self):
        path = self.get_folder_path(self.outputfolderLineEdit.text())
        if path:
            self.outputfolderLineEdit.setText(path)

    @pyqtSlot()
    def on_parsePushButton_clicked(self):
        python = self.paths.get('python')
        parser = self.paths.get('parser')
        dumpfolder = self.paths.get('dumpfolder')
        vmlinux = self.paths.get('vmlinux')
        outputfolder = self.paths.get('outputfolder')

        if self.aarch64CheckBox.isChecked():
            gdb = self.paths.get('gdb64')
            nm = self.paths.get('nm64')
            objdump = self.paths.get('objdump64')
        else:
            gdb = self.paths.get('gdb')
            nm = self.paths.get('nm')
            objdump = self.paths.get('objdump')

        args = [parser, "-v", vmlinux, "-g", gdb, "-n", nm, "-j", objdump, \
                "-o", outputfolder, "-a", dumpfolder, "-x"]

        if self.forcehwCheckBox.isChecked():
            args += ["--force-hardware", self.hwidLineEdit.text()]

        self.outputTextBrowser.setText(" ".join([python] + args))
        
        self.run_parser_qprocess(python, args)

    @pyqtSlot()
    def on_outputTextBrowser_cursorPositionChanged(self):
        cursor = self.outputTextBrowser.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.outputTextBrowser.setTextCursor(cursor)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setOrganizationName("db ltd.")
    app.setOrganizationDomain("db.cn")
    app.setApplicationName("QParser")

    m = QParser()
    m.show()

    sys.exit(app.exec_())
