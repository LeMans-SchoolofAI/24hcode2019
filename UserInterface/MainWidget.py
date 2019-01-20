from PySide2.QtWidgets import (QLabel, QWidget, QGridLayout,
                               QScrollArea, QFrame, QSizePolicy)
from PySide2.QtCore import Slot, Qt

from UserInterface.ItemsList import *
from UserInterface.Logger import *
from UserInterface.Utils.ClosableWidget import *

class MainWidget(ClosableWidget):
    def __init__(self):
        ClosableWidget.__init__(self)

        self.itemsList = ItemsList(self)
        self.logger = Logger()

        self.grid = QGridLayout()
        self.grid.addItem(self.itemsList, 0, 0)
        self.grid.addItem(self.logger, 0, 1, 2, 1)
        self.grid.setColumnStretch(0, 3)
        self.grid.setColumnStretch(1, 1)
        self.grid.setVerticalSpacing(2)
        self.grid.setHorizontalSpacing(2)
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

        self.setLayout(self.grid)