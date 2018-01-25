#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ui_decoder import Ui_decoderDlg


class DecoderDlg(QDialog, Ui_decoderDlg):
    def __init__(self, parent=None):
        super(DecoderDlg, self).__init__(parent)
        self.setupUi(self)

    @pyqtSlot()
    def on_panicregPushButton_clicked(self):
        input = self.inputTextEdit.toPlainText()

        xlate = {'pstate':'cpsr', 'lr':'x30'}
        input = re.sub("|".join(map(re.escape, xlate)), lambda m: xlate[m.group(0)], input)

        regnames = ['pc', 'cpsr', 'sp']
        result = []
        for i in range(31): # add register of "x0 - x30"
            regnames.append('x' + str(i))

        for name in regnames:
            m = re.search(r'' + name + '\s*:\s*\[?<?([0-9a-f]{8,16})>?\]?', input, re.IGNORECASE)
            value = '0x' + m.group(1) if m else '0x-1'
            t32cmd = ' '.join(['r.s', name, value])
            result.append(t32cmd)

        self.outputTextEdit.setText('\n'.join(result))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = DecoderDlg()
    form.show()
    app.exec_()
