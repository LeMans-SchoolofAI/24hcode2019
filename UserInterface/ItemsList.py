from Osmose import get_node, get_images_around
from PySide2.QtWidgets import (QApplication, QLabel, QPushButton,
                               QWidget, QGridLayout)
from PySide2.QtCore import Slot, Qt
from UserInterface.Utils.VerticalScrollArea import *
from UserInterface.Utils.ClosableWidget import *

class ItemsList(QGridLayout):
    def __init__(self, mainWidget):
        QGridLayout.__init__(self)

        self.headerGrid = QGridLayout()
        self.dataGrid = QGridLayout()

        self.headerGridWidget = QWidget()
        self.headerGridWidget.setLayout(self.headerGrid)
        self.dataGridWidget = QWidget()
        self.dataGridWidget.setLayout(self.dataGrid)

        self.dataGridScrollArea = VerticalScrollArea()
        self.dataGridScrollArea.setWidget(self.dataGridWidget)

        self.addWidget(self.headerGridWidget, 0, 0)
        self.addWidget(self.dataGridScrollArea, 1, 0)
        self.setRowStretch(1, 1)

        self.mainWidget = mainWidget
        self.mainWidget.registerCloseEvent(self.onMainWidgetDestroyed)

        self.headerGrid.addWidget(QLabel("Id"), 0, 0)
        self.headerGrid.addWidget(QLabel("Latitude"), 0, 1)
        self.headerGrid.addWidget(QLabel("Longitude"), 0, 2)
        self.headerGrid.addWidget(QLabel("Highway"), 0, 3)
        self.headerGrid.addWidget(QLabel("Detail"), 0, 4)

        dummyWidget = QWidget()
        dummyWidget.setFixedWidth(10)		# dirty hard-coded number, ideally we should retrieve the width of the scroll bar

        self.headerGrid.addWidget(dummyWidget, 0, 5)

        for i, node in enumerate(get_node("lemans")):
            self.dataGrid.addWidget(QLabel(str(node["id"])), i, 0)
            self.dataGrid.addWidget(QLabel(str(node["lat"])), i, 1)
            self.dataGrid.addWidget(QLabel(str(node["lon"])), i, 2)
            self.dataGrid.addWidget(QLabel(str(node["highway"])), i, 3)
            button = QPushButton("Detail")
            button.clicked.connect(lambda: self.onButtonClicked(node, loggerWidget=self.mainWidget.logger))
            self.dataGrid.addWidget(button, i, 4)

        self.subWidget = None

    def onButtonClicked(self, node, loggerWidget=None):
        self.subWidget = ClosableWidget()
        self.subWidget.registerCloseEvent(self.onWidgetDestroyed)
        self.dataGridWidget.setDisabled(True)
        self.subWidget.setWindowTitle("Node " + str(node["id"]) + " Detail")
        self.subWidget.setFixedSize(640, 480)
        self.subWidget.show()
        get_images_around(node, radius=5, logger=loggerWidget)

    def onWidgetDestroyed(self):
        self.dataGridWidget.setDisabled(False)

    def onMainWidgetDestroyed(self):
    	if self.subWidget != None and self.subWidget.isVisible():
        	self.subWidget.close()

