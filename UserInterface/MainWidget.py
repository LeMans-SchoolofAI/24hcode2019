from PySide2.QtWidgets import (QLabel, QWidget, QGridLayout,
                               QScrollArea, QFrame, QSizePolicy)
from PySide2.QtCore import Slot, Qt

from UserInterface.ItemsList import *
from UserInterface.Utils.VerticalScrollArea import *

class MainWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.itemsList = ItemsList()
        self.itemsList.setAlignment(Qt.AlignTop)
        self.map = QLabel("TODO: map")
        self.map.setAlignment(Qt.AlignCenter)
        self.logs = QLabel("TODO: logs")
        self.logs.setAlignment(Qt.AlignCenter)

        scrollItemsList = VerticalScrollArea()

        itemsListWidget = QWidget(self)
        itemsListWidget.setLayout(self.itemsList)
        itemsListWidget.setMinimumWidth(scrollItemsList.width())

        scrollItemsList.setWidget(itemsListWidget)

        self.grid = QGridLayout()
        self.grid.addWidget(self.map, 0, 0)
        self.grid.addWidget(scrollItemsList, 1, 0)
        self.grid.addWidget(self.logs, 0, 1, 2, 1)
        self.grid.setColumnStretch(0, 3)
        self.grid.setColumnStretch(1, 1)
        self.grid.setRowStretch(0, 1)
        self.grid.setRowStretch(1, 1)
        self.grid.setVerticalSpacing(2)
        self.grid.setHorizontalSpacing(2)
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

        self.setLayout(self.grid)