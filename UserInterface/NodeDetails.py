from PySide2.QtWidgets import (QGridLayout, QLabel, QWidget, QPushButton)
from PySide2.QtCore import Slot, Qt
from PySide2.QtGui import QPixmap
from Osmose import get_images_around, save_workspace, add_info_to_images
from UserInterface.Utils.HorizontalScrollArea import *

class NodeDetails(QGridLayout):
	def __init__(self, node, loggerWidget):
		QGridLayout.__init__(self)
		self.node = node
		self.loggerWidget = loggerWidget

		self.saveImagesWidget = QPushButton("Get images")
		self.saveImagesWidget.clicked.connect(self.saveImages)
		self.getInfoDataWidget = QPushButton("Check stop sign")
		self.getInfoDataWidget.clicked.connect(self.getInfoData)
		self.getInfoDataWidget.setDisabled(True)

		self.images = get_images_around(node, radius=5, logger=self.loggerWidget)

		self.addWidget(QLabel("Id:"), 0, 0)
		self.addWidget(QLabel("Latitude:"), 1, 0)
		self.addWidget(QLabel("Longitude:"), 2, 0)
		self.addWidget(QLabel("Direction:"), 3, 0)

		self.addWidget(QLabel(str(node["id"])), 0, 1)
		self.addWidget(QLabel(str(node["lat"]) + "°"), 1, 1)
		self.addWidget(QLabel(str(node["lon"]) + "°"), 2, 1)

		self.addWidget(self.saveImagesWidget, 0, 2, 2, 1)
		self.addWidget(self.getInfoDataWidget, 2, 2, 2, 1)

		self.setVerticalSpacing(20)

		if "direction" in node:
			self.addWidget(QLabel(str(node["direction"])), 3, 1)
		else:
			self.addWidget(QLabel("Unknown direction"), 3, 1)

		self.imagesLayout = QGridLayout()

		self.imagesWidget = QWidget()
		self.imagesWidget.setLayout(self.imagesLayout)

		self.imagesScrollArea = HorizontalScrollArea()
		self.imagesScrollArea.setWidget(self.imagesWidget)

		self.addWidget(self.imagesScrollArea, 4, 0, 1, 3)
		self.setRowStretch(4, 1)

	def saveImages(self):
		self.images = save_workspace(self.images, self.node, logger=self.loggerWidget)

		for i, image in enumerate(self.images):
			imageWidget = QLabel()
			imagePixmap = QPixmap(image["path"])
			imagePixmap = imagePixmap.scaledToHeight(240)
			imageWidget.setPixmap(imagePixmap)

			self.imagesLayout.addWidget(imageWidget, 0, i)
		self.saveImagesWidget.setDisabled(True)
		self.getInfoDataWidget.setDisabled(False)

	def getInfoData(self):
		self.images = add_info_to_images(self.images, self.node)

		for i, image in enumerate(self.images):
			if image["classifier_prediction"] == 1:
				labelWidget = QLabel("There is a stop sign. Hurray!!!")
			else:
				labelWidget = QLabel("There is no stop sign")

			labelWidget.setAlignment(Qt.AlignCenter)
			self.imagesLayout.addWidget(labelWidget, 1, i)
		self.getInfoDataWidget.setDisabled(True)


