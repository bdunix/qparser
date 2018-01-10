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
        self.load_paths()
        self.refresh_ui()

        settings = QSettings()
        self.restoreGeometry(settings.value("MainWindow/Geometry", QByteArray()))
        self.restoreState(settings.value("MainWindow/State", QByteArray()))

    def set_default_paths(self):
        self.paths = {}

        if platform.system() == 'Linux':
            self.paths['python'] = '/usr/bin/python2'
            self.paths['parserfolder'] = '/opt/tools/linux-ramdump-parser-v2'
            self.paths['toolsfolder'] = '/opt/LinaroToolchain/gcc-linaro-4.9.4-2017.01-x86_64_arm-eabi/bin'
            self.paths['toolsfolder64'] = '/opt/LinaroToolchain/gcc-linaro-4.9.4-2017.01-x86_64_aarch64-elf/bin'

        if platform.system() == 'Windows':
            self.paths['python'] = "C:\Python27\python.exe"
            self.paths['parserfolder'] = "C:\\work\\tools\\linux-ramdump-parser-v2"
            self.paths['toolsfolder'] = "C:\\tools\\arm-none-eabi"
            self.paths['toolsfolder64'] = "C:\\tools\\aarch64-linux-gnu-gcc"

        self.update_toolspath()

        self.paths['dumpfolder'] = os.path.join(os.environ["HOME"], "case")
        self.paths['vmlinux'] = os.path.join(self.paths['dumpfolder'], "vmlinux")
        self.paths['outputfolder'] = os.path.join(self.paths['dumpfolder'], "parser")

        # for k,v in self.paths.items(): print("{}:{}".format(k, v))

    def update_toolspath(self):
        self.paths['parser'] = os.path.join(self.paths['parserfolder'], 'ramparse.py')

        tools = ['gdb', 'nm', 'objdump']

        if platform.system() == 'Linux':
            prefix = 'arm-eabi-'
            prefix64 = 'aarch64-elf-'
            postfix = ''

        if platform.system() == 'Windows':
            prefix = 'arm-none-eabi'
            prefix64 = 'aarch64-linux-gnu-gcc-'
            postfix = '.exe'

        for key in tools:
            self.paths[key] = os.path.join(self.paths['toolsfolder'], prefix + key + postfix)
            self.paths[key + '64'] = os.path.join(self.paths['toolsfolder64'], prefix64 + key + postfix)

    def load_paths(self):
        self.set_default_paths()

        settings = QSettings()
        for k, v in self.paths.items():
            self.paths[k] = settings.value(k) or v

    def save_paths(self):
        settings = QSettings()
        for k, v in self.paths.items():
            settings.setValue(k, v)

    def closeEvent(self, *args, **kwargs):
        self.save_paths()

        settings = QSettings()
        settings.setValue("MainWindow/Geometry", self.saveGeometry())
        settings.setValue("MainWindow/State", self.saveState())

    def refresh_ui(self):
        self.parserfolderLineEdit.setText(self.paths['parserfolder'])
        self.toolsfolderLineEdit.setText(self.paths['toolsfolder'])
        self.toolsfolder64LineEdit.setText(self.paths['toolsfolder64'])
        self.dumpfolderLineEdit.setText(self.paths['dumpfolder'])
        self.vmlinuxLineEdit.setText(self.paths['vmlinux'])
        self.outputfolderLineEdit.setText(self.paths['outputfolder'])

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

        #self.process.readyRead.connect(self.on_process_readyRead)
        #self.process.setProcessChannelMode(QProcess.MergedChannels)

        self.process.readyReadStandardOutput.connect(self.on_process_readyReadStandardOutput)
        self.process.readyReadStandardError.connect(self.on_process_readyReadStandardError)
        self.process.finished.connect(self.on_process_finished)

        self.process.start(program, args)

    def on_process_readyRead(self):
        line = bytearray(self.process.readAll()).decode('utf-8')
        self.outputTextBrowser.setTextColor(Qt.blue)
        self.outputTextBrowser.append(line)

    def on_process_readyReadStandardOutput(self):
        line = bytearray(self.process.readAllStandardOutput()).decode('utf-8')
        self.outputTextBrowser.setTextColor(Qt.blue)
        self.outputTextBrowser.append(line)

    def on_process_readyReadStandardError(self):
        line = bytearray(self.process.readAllStandardError()).decode('utf-8')
        self.outputTextBrowser.setTextColor(Qt.red)
        self.outputTextBrowser.append(line)

    def on_process_finished(self):
        print("QProcess Finishied!")

    @pyqtSlot(str)
    def on_parserfolderLineEdit_textChanged(self, text):
        self.paths['parserfolder'] = text
        self.update_toolspath()

    @pyqtSlot()
    def on_parserfolderPushButton_clicked(self):
        path = self.get_folder_path(self.parserfolderLineEdit.text())
        if path:
            self.parserfolderLineEdit.setText(path)

    @pyqtSlot(str)
    def on_toolsfolderLineEdit_textChanged(self, text):
        self.paths['toolsfolder'] = text
        self.update_toolspath()

    @pyqtSlot()
    def on_toolsfolderPushButton_clicked(self):
        path = self.get_folder_path(self.toolsfolderLineEdit.text())
        if path:
            self.toolsfolderLineEdit.setText(path)

    @pyqtSlot(str)
    def on_toolsfolder64LineEdit_textChanged(self, text):
        self.paths['toolsfolder64'] = text
        self.update_toolspath()

    @pyqtSlot()
    def on_toolsfolder64PushButton_clicked(self):
        path = self.get_folder_path(self.toolsfolder64LineEdit.text())
        if path:
            self.toolsfolder64LineEdit.setText(path)

    @pyqtSlot(str)
    def on_dumpfolderLineEdit_textChanged(self, text):
        self.paths['dumpfolder'] = text
        self.vmlinuxLineEdit.setText(os.path.join(text, "vmlinux"))
        self.outputfolderLineEdit.setText(os.path.join(text, "parser"))

    @pyqtSlot()
    def on_dumpfolderPushButton_clicked(self):
        path = self.get_folder_path(self.dumpfolderLineEdit.text())
        if path:
            self.dumpfolderLineEdit.setText(path)

    @pyqtSlot(str)
    def on_vmlinuxLineEdit_textChanged(self, text):
        self.paths['vmlinux'] = text

    @pyqtSlot()
    def on_vmlinuxPushButton_clicked(self):
        path = self.get_file_path(self.vmlinuxLineEdit.text())
        if path:
            self.vmlinuxLineEdit.setText(path)

    @pyqtSlot(str)
    def on_outputfolderLineEdit_textChanged(self, text):
        self.paths['outputfolder'] = text

    @pyqtSlot()
    def on_outputfolderPushButton_clicked(self):
        path = self.get_folder_path(self.outputfolderLineEdit.text())
        if path:
            self.outputfolderLineEdit.setText(path)

    @pyqtSlot()
    def on_outputTextBrowser_cursorPositionChanged(self):
        cursor = self.outputTextBrowser.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.outputTextBrowser.setTextCursor(cursor)

    @pyqtSlot()
    def on_parsePushButton_clicked(self):
        python = self.paths['python']
        parser = self.paths['parser']
        dumpfolder = self.paths['dumpfolder']
        vmlinux = self.paths['vmlinux']
        outputfolder = self.paths['outputfolder']

        if self.aarch64CheckBox.isChecked():
            gdb = self.paths['gdb64']
            nm = self.paths['nm64']
            objdump = self.paths['objdump64']
        else:
            gdb = self.paths['gdb']
            nm = self.paths['nm']
            objdump = self.paths['objdump']

        args = [parser, '-v', vmlinux, '-g', gdb, '-n', nm, '-j', objdump, \
                '-o', outputfolder, '-a', dumpfolder]

        if self.everythingCheckBox.isChecked():
            args += ['-x']
        if self.forcehwCheckBox.isChecked():
            args += ['--force-hardware', self.hwidLineEdit.text()]

        self.outputTextBrowser.setTextColor(Qt.black)
        self.outputTextBrowser.setText(" ".join([python] + args))

        self.run_parser_qprocess(python, args)

    @pyqtSlot()
    def on_resultPushButton_clicked(self):
        if platform.system() == 'Linux':
            prog = '/usr/bin/gnome-text-editor'
        if platform.system() == 'Windows':
            prog = 'notepad.exe'

        target = os.path.join(self.paths['outputfolder'], 'dmesg_TZ.txt')

        if os.access(prog, os.F_OK) and os.access(target, os.F_OK):
            os.system(' '.join([prog, target]))

    @pyqtSlot()
    def on_explorePushButton_clicked(self):
        if platform.system() == 'Linux':
            prog = '/usr/bin/nautilus'
        if platform.system() == 'Windows':
            prog = 'explorer.exe'

        target = self.paths['outputfolder']

        if os.access(prog, os.F_OK) and os.access(target, os.F_OK):
            print(' '.join([prog, target]))
            os.system(' '.join([prog, target]))

    @pyqtSlot()
    def on_decoderPushButton_clicked(self):
        print(sys._getframe().f_code.co_name)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setOrganizationName("db ltd.")
    app.setOrganizationDomain("db.cn")
    app.setApplicationName("QParser")

    m = QParser()
    m.show()

    sys.exit(app.exec_())
