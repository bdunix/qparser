#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import os
import sys
import platform
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ui_qparser import *
from decoder import *


class QParser(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.load_paths()
        self.refresh_ui()

        settings = QSettings()
        self.restoreGeometry(settings.value("MainWindow/Geometry", QByteArray()))
        self.restoreState(settings.value("MainWindow/State", QByteArray()))

        self.casenoLineEdit.setValidator(QIntValidator(0, 99999999, self))
        self.decoderDlg = None

    def set_default_paths(self):
        self.paths = {}
        for path in ['python', 'parserfolder', 'toolsfolder', 'gdb', 'nm', 'objdump', 'casefolder', 'caseno', 'dumpfolder', 'vmlinux',
                     'outputfolder']:
            self.paths[path] = ''

        if platform.system() == 'Linux':
            self.paths['python'] = '/usr/bin/python2'
            self.paths['parserfolder'] = '/opt/tools/linux-ramdump-parser-v2'
            self.paths['toolsfolder'] = '/usr/bin'
            self.paths['casefolder'] = os.path.join(os.environ['HOME'], 'case')

        if platform.system() == 'Windows':
            self.paths['python'] = 'C:\Python27\python.exe'
            self.paths['parserfolder'] = 'C:\\work\\tools\\linux-ramdump-parser-v2'
            self.paths['toolsfolder'] = 'C:\\work\\aarch64-elf'
            self.paths['casefolder'] = os.path.join(os.environ['USERPROFILE'], 'case')

        self.update_toolspath()
        
        self.paths['dumpfolder'] = self.paths['casefolder']
        self.paths['vmlinux'] = os.path.join(self.paths['dumpfolder'], "vmlinux")
        self.paths['outputfolder'] = os.path.join(self.paths['dumpfolder'], "parser")

        # for k,v in self.paths.items(): print("{}:{}".format(k, v))

    def update_toolspath(self):
        self.paths['parser'] = os.path.join(self.paths['parserfolder'], 'ramparse.py')

        folder = self.paths['toolsfolder']
        if not os.path.exists(folder): return

        files = []
        for entry in os.scandir(folder):  # get all files name in folder
            if not entry.name.startswith('.') and entry.is_file():
                files.append(entry.name)

        for tool in ['gdb', 'nm', 'objdump']:
            for f in files:
                root, ext = os.path.splitext(f)
                if root.startswith('aarch64') and root.endswith(tool):
                    self.paths[tool] = os.path.join(folder, f)
                    # print('found {} for {}'.format(f, tool))
                    break

    def load_paths(self):
        self.set_default_paths()

        settings = QSettings()
        for k, v in self.paths.items():
            #print("loading {}:{}".format(k,v))
            self.paths[k] = settings.value(k) or v

    def save_paths(self):
        settings = QSettings()
        for k, v in self.paths.items():
            #print("saving {}:{}".format(k,v))
            settings.setValue(k, v)

    def closeEvent(self, *args, **kwargs):
        self.save_paths()

        settings = QSettings()
        settings.setValue("MainWindow/Geometry", self.saveGeometry())
        settings.setValue("MainWindow/State", self.saveState())

    def refresh_ui(self):
        self.pythonLineEdit.setText(self.paths['python'])
        self.parserfolderLineEdit.setText(self.paths['parserfolder'])
        self.toolsfolderLineEdit.setText(self.paths['toolsfolder'])
        self.casefolderLineEdit.setText(self.paths['casefolder'])
        self.casenoLineEdit.setText(self.paths['caseno'])
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

        # self.process.readyRead.connect(self.on_process_readyRead)
        # self.process.setProcessChannelMode(QProcess.MergedChannels)

        self.process.readyReadStandardOutput.connect(self.on_process_readyReadStandardOutput)
        self.process.readyReadStandardError.connect(self.on_process_readyReadStandardError)
        self.process.finished.connect(self.on_process_finished)
        self.process.errorOccurred.connect(self.on_process_errorOccurred)

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
        #print("QProcess Finishied!")
        self.outputTextBrowser.setTextColor(Qt.black)
        self.outputTextBrowser.append('Finished!')
        self.tune_output()

    def on_process_errorOccurred(self, err):
        errors = ['FailedToStart', 'Crashed', 'Timedout', 'WriteError', 'ReadError', 'UnknownError']
        QMessageBox.warning(self, "Parser process error", errors[err])

    def tune_output(self):
        t32_config_file = os.path.join(self.paths['outputfolder'], 't32_config.t32')
        if platform.system() == 'Linux':
            try:
                with open(t32_config_file, 'r') as f:
                    all_lines = f.readlines()
                with open(t32_config_file, 'w') as f:
                    for line in all_lines:
                        if 'PRINTER=' in line: continue
                        f.write(line)
            except Exception as e:
                #print(str(e))
                QMessageBox.warning(self, "Open file error", str(e))

        if platform.system() == 'Windows':
            try:
                with open(t32_config_file, 'r') as f:
                    all_lines = f.readlines()
                with open(t32_config_file, 'w') as f:
                    for line in all_lines:
                        if line.startswith('TMP='):
                            line = 'TMP=' + os.environ['TEMP'] + '\n'
                        f.write(line)
            except Exception as e:
                #print(str(e))
                QMessageBox.warning(self, "Open file error", str(e))

    def find_folder(self, root='', target=''):
        if not os.path.exists(root): return None

        subfolders = []
        for entry in os.scandir(root): # get all subfolders of current root folder
            if entry.is_dir():
                subfolders.append(entry.name)

        if not subfolders: # no any subfolders under current root
            return None

        for folder in subfolders: # find in current root
            if folder == target:
                return os.path.join(root, folder) # return full path of target

            path = self.find_folder(os.path.join(root, folder), target)
            if path: # found in this subfolder
                return path
            else:
                continue

        # not found in under any of subfolders
        return None



    @pyqtSlot(str)
    def on_pythonLineEdit_textChanged(self, text):
        self.paths['python'] = text

    @pyqtSlot()
    def on_pythonPushButton_clicked(self):
        path = self.get_file_path(self.vmlinuxLineEdit.text())
        if path:
            self.pythonLineEdit.setText(path)

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
    def on_casefolderLineEdit_textChanged(self, text):
        self.paths['casefolder'] = text

    @pyqtSlot()
    def on_casefolderPushButton_clicked(self):
        path = self.get_folder_path(self.parserfolderLineEdit.text())
        if path:
            self.casefolderLineEdit.setText(path)

    @pyqtSlot(str)
    def on_casenoLineEdit_textChanged(self, text):
        self.paths['caseno'] = text

    @pyqtSlot()
    def on_casenoLineEdit_returnPressed(self):
        self.findcasePushButton.clicked.emit()

    @pyqtSlot()
    def on_findcasePushButton_clicked(self):
        casefolder = self.paths['casefolder']
        caseno = self.casenoLineEdit.text()
        path = self.find_folder(casefolder, caseno)
        if path:
            #print("find case {} in {}".format(caseno, path))
            self.dumpfolderLineEdit.setText(path)
        else:
            QMessageBox.warning(self, "Find case folder", "Not found case folder of " + caseno)


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
        gdb = self.paths['gdb']
        nm = self.paths['nm']
        objdump = self.paths['objdump']

        args = [parser, '-v', vmlinux, '-g', gdb, '-n', nm, '-j', objdump, \
                '-o', outputfolder, '-a', dumpfolder, '-x']

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
            prog = os.path.join(os.environ['WINDIR'], 'write.exe')

        target = os.path.join(self.paths['outputfolder'], 'dmesg_TZ.txt')
        if os.access(prog, os.F_OK) and os.access(target, os.F_OK):
            os.system(' '.join([prog, target]))

    @pyqtSlot()
    def on_t32PushButton_clicked(self):
        launcher = os.path.join(self.paths['outputfolder'], 'launch_t32')
        if platform.system() == 'Linux':
            launcher += '.sh'
        if platform.system() == 'Windows':
            launcher += '.bat'

        if os.access(launcher, os.F_OK):
            os.system(launcher)
        else:
            QMessageBox.warning(self, "T32 launcher error", "No such file: " + launcher)

    @pyqtSlot()
    def on_explorePushButton_clicked(self):
        if platform.system() == 'Linux':
            prog = '/usr/bin/nautilus'
        if platform.system() == 'Windows':
            prog = os.path.join(os.environ['WINDIR'], 'explorer.exe')

        target = self.paths['outputfolder']
        if os.access(prog, os.F_OK) and os.access(target, os.F_OK):
            #print(' '.join([prog, target]))
            os.system(' '.join([prog, target]))

    @pyqtSlot()
    def on_decoderPushButton_clicked(self):
        # print(sys._getframe().f_code.co_name)
        if self.decoderDlg is None:
            self.decoderDlg = DecoderDlg()
        self.decoderDlg.show()
        self.decoderDlg.raise_()
        self.decoderDlg.activateWindow()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setOrganizationName("db ltd.")
    app.setOrganizationDomain("db.cn")
    app.setApplicationName("QParser")

    m = QParser()
    m.show()

    sys.exit(app.exec_())
