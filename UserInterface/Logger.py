from PySide2.QtWidgets import (QGridLayout, QTextEdit, QLabel)
from PySide2.QtCore import Slot, Qt, QEvent

from datetime import *

class Logger(QGridLayout):
    def __init__(self):
        QGridLayout.__init__(self)

        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)

        self.addWidget(QLabel("Logs"), 0, 0)
        self.addWidget(self.textEdit, 1, 0)
        self.setRowStretch(1, 1)

    def log(self, message):
        self.textEdit.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ": " + message)

