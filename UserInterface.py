import sys
from UserInterface.MainWidget import *
from PySide2.QtWidgets import (QApplication)
from PySide2.QtCore import Slot, Qt


if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = MainWidget()
    widget.setWindowTitle("ScooterStop")
    widget.resize(800, 600)
    widget.showMaximized()

    sys.exit(app.exec_())