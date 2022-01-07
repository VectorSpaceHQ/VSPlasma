#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import sys
import gui.vsplasma_ui as vsplasma_ui
import core.file_handler as file_handler

from PyQt5.QtWidgets import QMainWindow, QGraphicsView, QFileDialog, QApplication, QMessageBox
from PyQt5.QtGui import QSurfaceFormat
from PyQt5 import QtCore

logger = logging.getLogger()
# QResource.registerResource("./gui/resources.qrc")


class MainWindow(QMainWindow):

    """
    Main Class
    """

    # Define a QT signal that is emitted when the configuration changes.
    # Connect to this signal if you need to know when the configuration has
    # changed.
    configuration_changed = QtCore.pyqtSignal()

    def __init__(self, app):
        """
        Initialization of the Main window. This is directly called after the
        Logger has been initialized. The Function loads the GUI, creates the
        used Classes and connects the actions to the GUI.
        """
        QMainWindow.__init__(self)
        self.app = app
        self.settings = QtCore.QSettings("vsplasma", "vsplasma")

        self.ui = vsplasma_ui.Ui_MainWindow()
        self.ui.setupUi(self)
        self.showMaximized()

        self.canvas = self.ui.canvasView

        self.connect_signals()

    def connect_signals(self):
        # File
        self.ui.actionOpen.triggered.connect(lambda: file_handler.open(self))
        self.ui.actionImport.triggered.connect(lambda: file_handler.import_drawing(self))
        self.ui.actionSave.triggered.connect(lambda: file_handler.saveProject(self))



if __name__ == "__main__":
    """
    The main function which is executed after program start.
    """
    app = QApplication(sys.argv)

    window = MainWindow(app)

    window.show()
    sys.exit(app.exec_())
