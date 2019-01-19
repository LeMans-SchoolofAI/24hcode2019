from PySide2.QtWidgets import (QVBoxLayout, QWidget, QGridLayout,
                               QScrollArea, QFrame, QSizePolicy)
from PySide2.QtCore import Slot, Qt, QEvent

class VerticalScrollArea(QScrollArea):
    def __init__(self):
        QScrollArea.__init__(self)
        self.setWidgetResizable(True)
        self.setFrameStyle(QFrame.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scrollAreaWidgetContents = QWidget(self)
        self.scrollAreaWidgetContents.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        baseLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.setWidget(self.scrollAreaWidgetContents)
        self.scrollAreaWidgetContents.installEventFilter(self)

    def eventFilter(self, o, e):
        if o == self.scrollAreaWidgetContents and e.type() == QEvent.Resize:
            self.setMinimumWidth(self.scrollAreaWidgetContents.minimumSizeHint().width() + verticalScrollBar().width());
        return False