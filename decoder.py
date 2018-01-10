#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ui_decoder import Ui_decoderDlg


class DecoderDlg(QDialog, Ui_decoderDlg):
    def __init__(self, parent=None):
        super(DecoderDlg, self).__init__(parent)
        self.setupUi(self)
