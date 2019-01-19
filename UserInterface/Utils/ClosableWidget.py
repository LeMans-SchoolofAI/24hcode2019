from PySide2.QtWidgets import (QWidget)
from PySide2.QtCore import Slot, Qt, QEvent

class ClosableWidget(QWidget):
	def __init__(self):
		QWidget.__init__(self)

		self.customCloseEvent = None

	def registerCloseEvent(self, event):
		self.customCloseEvent = event

	def closeEvent(self, event):
		if self.customCloseEvent != None:
			self.customCloseEvent()