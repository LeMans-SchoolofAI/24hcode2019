from PySide2.QtWidgets import (QGridLayout, QLabel, QWidget)
from PySide2.QtCore import Slot, Qt

class NodeDetails(QGridLayout):
	def __init__(self, node):
		QGridLayout.__init__(self)
		self.node = node

		#self.paths = [image["path"] for image in self.node["images"]]

		self.addWidget(QLabel("Id:"), 0, 0)
		self.addWidget(QLabel("Latitude:"), 1, 0)
		self.addWidget(QLabel("Longitude:"), 2, 0)
		self.addWidget(QLabel("Direction:"), 3, 0)

		self.addWidget(QLabel(str(node["id"])), 0, 1)
		self.addWidget(QLabel(str(node["lat"]) + "°"), 1, 1)
		self.addWidget(QLabel(str(node["lon"]) + "°"), 2, 1)

		self.setVerticalSpacing(20)

		if "direction" in node:
			self.addWidget(QLabel(str(node["direction"])), 3, 1)
		else:
			self.addWidget(QLabel("Unknown direction"), 3, 1)

		self.addWidget(QWidget(), 4, 0, 1, 2)
		self.setRowStretch(4, 1)

