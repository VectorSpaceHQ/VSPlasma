# -*- coding: utf-8 -*-

import os
import logging
import core.globals as g
from preprocess.dxfimport.importer import ReadDXF

from PyQt5.QtWidgets import QMainWindow, QGraphicsView, QFileDialog, QApplication, QMessageBox
from PyQt5.QtGui import QSurfaceFormat
from PyQt5 import QtCore

getOpenFileName = QFileDialog.getOpenFileName
getSaveFileName = QFileDialog.getSaveFileName
logger = logging.getLogger()


def open(ui):
    """
    Loads .vsp project files
    """
    ui.filename, _ = getOpenFileName(ui,
                                     "Open Project File",
                                     g.open_path,
                                     "Project Files (*.vsp)")
    if not ui.filename:
        return False  # cancelled
    ui.setCursor(QtCore.Qt.WaitCursor)
    ui.setWindowTitle("VSPlasma - [%s]" % ui.filename)
    ui.canvas.resetAll()
    ui.app.processEvents()
    ui.unsetCursor()

def import_drawing(ui, plot=True):
    """
    Loads dxf and other drawings.  Also calls the command to
    make the plot.
    @param plot: if it should plot
    """
    # debuggging
    ui.filename = '../tests/1in-box.dxf'
    # ui.filename, _ = getOpenFileName(ui,
    #                                  "Import Drawing File",
    #                                  g.open_path,
    #                                  "Drawing Files (*.dxf)")
    # if not QtCore.QFile.exists(ui.filename):
    #     logger.info("Cannot locate file: %s" % ui.filename)
    #     if not ui.filename:
    #         return False

    ui.setCursor(QtCore.Qt.WaitCursor)
    ui.setWindowTitle("VSPlasma - [%s]" % ui.filename)
    ui.canvas.resetAll()
    ui.app.processEvents()

    (name, ext) = os.path.splitext(ui.filename)

    ui.DXF_file = ReadDXF(ui.filename)

    # Output the information in the text window
    logger.info(ui.tr('Loaded layers: %s') % len(ui.DXF_file.layers))
    logger.info(ui.tr('Loaded blocks: %s') % len(ui.DXF_file.blocks.Entities))
    for i in range(len(ui.DXF_file.blocks.Entities)):
        layers = ui.DXF_file.blocks.Entities[i].get_used_layers()
        logger.info(ui.tr('Block %i includes %i Geometries, reduced to %i Contours, used layers: %s')
                    % (i, len(ui.DXF_file.blocks.Entities[i].geo), len(ui.DXF_file.blocks.Entities[i].cont), layers))
    layers = ui.DXF_file.entities.get_used_layers()
    insert_nr = ui.DXF_file.entities.get_insert_nr()
    logger.info(ui.tr('Loaded %i entity geometries; reduced to %i contours; used layers: %s; number of inserts %i')
                % (len(ui.DXF_file.entities.geo), len(ui.DXF_file.entities.cont), layers, insert_nr))

    ui.units = ui.DXF_file.units
    ui.unsetCursor()

def OpenFileDialog(ui, title):
    ui.filename, _ = getOpenFileName(ui,
                                     title,
                                     g.config.vars.Paths['import_dir'],
                                     ui.tr("All supported files (*.dxf *.DXF *.ps *.PS *.pdf *.PDF *%s);;"
                                           "DXF files (*.dxf *.DXF);;"
                                           "PS files (*.ps *.PS);;"
                                           "PDF files (*.pdf *.PDF);;"
                                           "Project files (*%s);;"
                                           "All types (*.*)") % (PROJECT_EXTENSION, PROJECT_EXTENSION))

    # If there is something to load then call the load function callback
    if ui.filename:
        ui.filename = qstr_encode(ui.filename)
        logger.info(ui.tr("File: %s selected") % ui.filename)

def reload(ui):
    pass

def load_project(ui, filename):
    pass

def save_project(ui, filename):
    pass

def showSaveDialog(ui, title, MyFormats):
    """
    This function is called by the menu "Export/Export Shapes" of the main toolbar.
    It creates the selection dialog for the exporter
    @return: Returns the filename of the selected file.
    """

    (beg, ende) = os.path.split(ui.filename)
    (fileBaseName, fileExtension) = os.path.splitext(ende)

    selected_filter = ui.MyPostProcessor.output_format[0]
    default_name = os.path.join(g.config.vars.Paths['output_dir'], fileBaseName + selected_filter)
    filename = getSaveFileName(ui,
                               title, default_name,
                               MyFormats, selected_filter)

    logger.info(ui.tr("File: %s selected") % filename[0])
    logger.info("<a href='%s'>%s</a>" % (filename[0], filename[0]))
    return filename

def reload(ui):
    """
    This function is called by the menu "File/Reload File" of the main toolbar.
    It reloads the previously loaded file (if any)
    """
    if ui.filename:
        logger.info(ui.tr("Reloading file: %s") % ui.filename)
        ui.load()

def loadProject(ui, filename):
    """
    Load all variables from file
    """
    # since Py3 has no longer execfile -  we need to open it manually
    file_ = open(filename, 'r')
    str_ = file_.read()
    file_.close()
    ui.d2g.load(str_)

def saveProject(ui):
    """
    Save all variables to file
    """
    prj_filename = ui.showSaveDialog(ui.tr('Save project to file'), "Project files (*%s)" % PROJECT_EXTENSION)
    save_prj_filename = qstr_encode(prj_filename[0])

    # If Cancel was pressed
    if not save_prj_filename:
        return

    (beg, ende) = os.path.split(save_prj_filename)
    (fileBaseName, fileExtension) = os.path.splitext(ende)

    if fileExtension != PROJECT_EXTENSION:
        if not QtCore.QFile.exists(save_prj_filename):
            save_prj_filename += PROJECT_EXTENSION

    pyCode = ui.d2g.export()
    try:
        # File open and write
        f = open(save_prj_filename, "w")
        f.write(str_encode(pyCode))
        f.close()
        logger.info(ui.tr("Save project to FILE was successful"))
    except IOError:
        QMessageBox.warning(g.window,
                            ui.tr("Warning during Save Project As"),
                            ui.tr("Cannot Save the File"))
