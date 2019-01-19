from Osmose import get_node
from PySide2.QtWidgets import (QApplication, QLabel, QPushButton,
                               QWidget, QGridLayout)
from PySide2.QtCore import Slot, Qt

class ItemsList(QGridLayout):
    def __init__(self):
        QGridLayout.__init__(self)

        for i, node in enumerate(get_node("lemans")):
            self.addWidget(QLabel(str(node["id"])), i, 0)
            self.addWidget(QLabel(str(node["lat"])), i, 1)
            self.addWidget(QLabel(str(node["lon"])), i, 2)
            self.addWidget(QLabel(str(node["highway"])), i, 3)
            button = QPushButton("Detail")
            self.addWidget(button, i, 4)
            button.clicked.connect(lambda: self.onButtonClicked(str(node)))

    def onButtonClicked(self, node):
        print("TODO: open window with node details")
        return
