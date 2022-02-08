#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import sys
import gui.vsplasma_ui as vsplasma_ui
import core.file_handler as file_handler
import gui
import preprocess.dxfimport.importer as importer
import core.tooltable as tooltable
import core.globals as globals
import gui.parts_tab as parts_tab
import gui.tools_tab as tools_tab
import gui.operations_tab as operations_tab
import core.workpiece as workpiece
import core.machine as machine
import core.geometry as geometry
import core.config as config
import core.operation as operation
import gui.setup_tab as setup_tab

from PyQt5.QtWidgets import QMainWindow, QGraphicsView, QFileDialog, QApplication, QMessageBox
from PyQt5.QtGui import QSurfaceFormat
from PyQt5.QtGui import QIcon, QPainterPath, QBrush, QPen
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

        self.config = config.Config()
        self.tools = tooltable.ToolTable()
        self.machine = machine.Machine()
        self.operations = operation.Operations()
        self.workpiece = workpiece.Workpiece(machine=self.machine)
        self.geometry = geometry.initialize()
        self.setup_graphics()

        self.connect_signals()

    def setup_graphics(self):
        # Canvas
        self.canvas_scene = gui.canvas.MyGraphicsScene(self.workpiece, self.machine)
        self.canvas_view = self.ui.canvasView
        self.canvas_view.setScene(self.canvas_scene)

        # Setup Tab
        self.SetupTab = setup_tab.SetupTab(self, self.operations)

        # Parts Tab
        self.PartsTab = parts_tab.PartsTab(self.ui, self.geometry, self.refresh)

        # Tool table tab
        self.ToolsTab = tools_tab.ToolsTab(self.ui, self.tools)

        # Operations tab
        self.OperationTab = operations_tab.OperationsTab(self.ui, self.tools, self.geometry)

    def connect_signals(self):
        # File
        self.ui.actionOpen.triggered.connect(lambda: file_handler.open(self))
        # self.ui.actionImport.triggered.connect(lambda: file_handler.import_drawing(self))

        self.ui.actionImport.triggered.connect(self.open_file)
        # self.ui.actionSave.triggered.connect(lambda: file_handler.saveProject(self))
        self.ui.generate_paths_action.pressed.connect(self.generate_operations)
        self.ui.save_gcode_action.pressed.connect(self.save_gcode)

    def import_dxf(self):
        file_handler.import_drawing(self)

    def save_gcode(self):
        pass

    def generate_operations(self):
        selected_shapes = self.geometry.shapes.get_selected()
        active_tool = self.tools.get_active_tool()
        op = operation.Operation(selected_shapes, active_tool, parent=self.operations)
        # self.operations.add(op)
        # print(self.operations)

    def open_file(self, filename=None):
        # filename="../tests/1in-box.dxf"
        # Read drawing file into self.DXF_file
        file_handler.import_drawing(self, filename=filename)

        # create ui.graphics objects
        importer.make_geometry_from_dxf(self)

        # signal an update to the parts_tab
        self.PartsTab.load_parts(self.geometry)

        # plot graphics objects
        self.canvas_scene.draw_all(self)

        logger.info("\n\n*********** TESTING GEOMETRY IMPORT")
        logger.info(self.geometry.parts)
        logger.info(self.geometry.groups)
        logger.info(self.geometry.shapes)
        for part in self.geometry.parts:
            logger.info(part.name)
            for group in part.groups:
                logger.info([group, group.name, group.nr, group.num_shapes])
                for shape in group.shapes:
                    logger.info(shape)


    def refresh(self):
        # plot graphics objects
        self.canvas_view.items().clear()
        self.canvas_scene.clear()
        self.canvas_scene.draw_all(self)



if __name__ == "__main__":
    """
    The main function which is executed after program start.
    """
    app = QApplication(sys.argv)

    window = MainWindow(app)
    window.setWindowTitle('VSPlasma')
    window.setWindowIcon(QIcon('./images/vsp_icon.png'))

    window.show()
    sys.exit(app.exec_())
