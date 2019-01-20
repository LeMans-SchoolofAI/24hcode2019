from PySide2.QtWidgets import (QHBoxLayout, QWidget, QGridLayout,
                               QScrollArea, QFrame, QSizePolicy)
from PySide2.QtCore import Slot, Qt, QEvent

class HorizontalScrollArea(QScrollArea):
    def __init__(self):
        QScrollArea.__init__(self)
        self.setWidgetResizable(True)
        self.setFrameStyle(QFrame.NoFrame)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollAreaWidgetContents = QWidget(self)
        self.scrollAreaWidgetContents.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        baseLayout = QHBoxLayout(self.scrollAreaWidgetContents)
        self.setWidget(self.scrollAreaWidgetContents)