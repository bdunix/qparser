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

        self.load_settings()

        self.update_ui()

    def load_settings(self):
        self.paths = PathSettings()

        self.python_path = self.paths.get('python')

        self.parserfolder_path = self.paths.get('parserfolder')
        self.parser_path = self.paths.get('parser')

        if self.aarch64CheckBox.isChecked():
            self.set_tools_aarch64(True)
        else:
            self.set_tools_aarch64(False)

        self.dumpfolder_path = self.paths.get('dumpfolder')
        self.vmlinux_path = self.paths.get('vmlinux')
        self.outputfolder_path = self.paths.get('outputfolder')

        self.hardwareid = self.forcehwLineEdit.text()

    def set_tools_aarch64(self, is_aarch64=True):
        if is_aarch64:
            self.toolsfolder_path = self.paths.get('toolsfolder64')
            self.gdb_path = self.paths.get('gdb64')
            self.nm_path = self.paths.get('nm64')
            self.objdump_path = self.paths.get('objdump64')
        else:
            self.toolsfolder_path = self.paths.get('toolsfolder')
            self.gdb_path = self.paths.get('gdb')
            self.nm_path = self.paths.get('nm')
            self.objdump_path = self.paths.get('objdump')

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

        self.process.readyReadStandardOutput.connect(self.on_readyReadStandardOutput)
        self.process.readyReadStandardError.connect(self.on_readyReadStandardError)
        self.process.finished.connect(self.on_finished)

        self.process.start(program, args)

    def on_readyReadStandardOutput(self):
        while self.process.canReadLine():
            print(self.process.readLine())

    def on_readyReadStandardError(self):
        line = str(self.process.readAllStandardError())
        # if line.endswith('\n'):
        #    print(line)
        # else:
        #   print(line, end=' ')
        self.outputTextBrowser.append(line)

    def on_finished(self):
        print("QProcess Finishied!")

    @pyqtSlot()
    def on_parserfolderLineEdit_textChanged(self):
        self.paths.set('parserfolder', self.parserfolderLineEdit.text())

    @pyqtSlot()
    def on_parserfolderPushButton_clicked(self):
        path = self.get_folder_path(self.parserfolderLineEdit.text())
        if path:
            self.parserfolder_path = path
            self.parserfolderLineEdit.setText(path)

    @pyqtSlot()
    def on_toolsfolderLineEdit_textChanged(self):
        self.paths.set('toolsfolder64', self.toolsfolderLineEdit.text())

    @pyqtSlot()
    def on_toolsfolderPushButton_clicked(self):
        path = self.get_folder_path(self.toolsfolderLineEdit.text())
        if path:
            self.toolsfolder_path = path
            self.toolsfolderLineEdit.setText(path)
            self.update_toolspath()

    @pyqtSlot(str)
    def on_dumpfolderLineEdit_textChanged(self, arg):
        self.paths.set('dumpfolder', arg)
        self.vmlinux_path = os.path.join(arg, "vmlinux")
        self.vmlinuxLineEdit.setText(self.vmlinux_path)
        self.outputfolder_path = os.path.join(arg, "parser")
        self.outputfolderLineEdit.setText(self.outputfolder_path)

    @pyqtSlot()
    def on_dumpfolderPushButton_clicked(self):
        path = self.get_folder_path(self.dumpfolderLineEdit.text())
        if path:
            self.dumpfolder_path = path
            self.dumpfolderLineEdit.setText(path)

    @pyqtSlot()
    def on_vmlinuxLineEdit_textChanged(self):
        self.paths.set('vmlinux', self.vmlinuxLineEdit.text())

    @pyqtSlot()
    def on_vmlinuxPushButton_clicked(self):
        path = self.get_file_path(self.vmlinuxLineEdit.text())
        if path:
            self.vmlinux_path = path
            self.vmlinuxLineEdit.setText(path)

    @pyqtSlot()
    def on_outputfolderLineEdit_textChanged(self):
        self.paths.set('outputfolder', self.outputfolderLineEdit.text())

    @pyqtSlot()
    def on_outputfolderPushButton_clicked(self):
        path = self.get_folder_path(self.outputfolderLineEdit.text())
        if path:
            self.outputfolder_path = path
            self.outputfolderLineEdit.setText(path)

    @pyqtSlot()
    def on_parsePushButton_clicked(self):
        args = [self.parser_path, "-v", self.vmlinux_path, "-g", self.gdb_path, \
                "-n", self.nm_path, "-j", self.objdump_path, "-o", self.outputfolder_path, \
                "-a", self.dumpfolder_path, "-x"]

        if self.forcehwCheckBox.isChecked():
            args += ["--force-hardware", self.hardwareid]

        self.outputTextBrowser.setText(" ".join(args))
        self.outputTextBrowser.append("\n")

        self.run_parser_qprocess(self.python_path, args)

    @pyqtSlot()
    def on_forcehwLineEdit_textChanged(self, arg):
        self.hardwareid = self.forcehwLineEdit.text()

    @pyqtSlot(int)
    def on_aarch64CheckBox_stateChanged(self, state):
        if state == Qt.Checked:
            self.set_tools_aarch64(True)
        else:
            self.set_tools_aarch64(False)

        self.toolsfolderLineEdit.setText(self.toolsfolder_path)

    @pyqtSlot()
    def on_outputTextBrowser_cursorPositionChanged(self):
        cursor = self.outputTextBrowser.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.outputTextBrowser.setTextCursor(cursor)

    def closeEvent(self, *args, **kwargs):
        self.paths.save()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setOrganizationName("db ltd.")
    app.setOrganizationDomain("db.cn")
    app.setApplicationName("QParser")

    m = QParser()
    m.show()

    sys.exit(app.exec_())
