#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import sys
import gui.vsplasma_ui as vsplasma_ui
import core.file_handler as file_handler
import gui
import preprocess.dxfimport.importer as importer


from PyQt5.QtWidgets import QMainWindow, QGraphicsView, QFileDialog, QApplication, QMessageBox
from PyQt5.QtGui import QSurfaceFormat
from PyQt5.QtGui import QPainterPath, QBrush, QPen
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

        self.setup_graphics()


        self.connect_signals()

    def setup_graphics(self):
        self.canvas_scene = gui.canvas.MyGraphicsScene()

        self.canvas_view = self.ui.canvasView
        self.canvas_view.setScene(self.canvas_scene)

        # path = QPainterPath()
        # pen = QPen()
        # path.addRect(20,20,50,50)
        # path.lineTo(0,0)
        # path.lineTo(100,200)
        # path.moveTo(200,400)
        # path.lineTo(40,22)
        # self.canvas_scene.addPath(path)

    def connect_signals(self):
        # File
        self.ui.actionOpen.triggered.connect(lambda: file_handler.open(self))
        # self.ui.actionImport.triggered.connect(lambda: file_handler.import_drawing(self))
        self.ui.actionImport.triggered.connect(self.open_file)
        self.ui.actionSave.triggered.connect(lambda: file_handler.saveProject(self))

    def open_file(self):
        # Read drawing file into self.DXF_file
        file_handler.import_drawing(self)

        # create ui.graphics objects
        importer.make_geometry_from_dxf(self)

        # plot graphics objects
        self.canvas_scene.draw_shapes(self.geometry)



if __name__ == "__main__":
    """
    The main function which is executed after program start.
    """
    app = QApplication(sys.argv)

    window = MainWindow(app)

    window.show()
    sys.exit(app.exec_())
