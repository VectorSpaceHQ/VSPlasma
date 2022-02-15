# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QTreeView
from gui import treeview
from PyQt5.QtGui import QStandardItem
import PyQt5.QtCore
from core.geometry import Shape, Geometry


class PartsTab(QWidget):
    """
    Creates GUI behavior of Parts Tab.
    ui: the GUI
    """
    checkbox_changed = PyQt5.QtCore.pyqtSignal(Geometry)

    def __init__(self, ui, geometry, refresh):
        QWidget.__init__(self)
        self.refresh = refresh
        self.ui = ui
        self.geometry = geometry

        self.ui.model = treeview.QStandardItemModel()
        self.ui.entitiesTreeView.setModel(self.ui.model)
        self.ui.model.itemChanged.connect(self.on_item_changed)

    def on_item_changed(self, item):
        """
        Executes whenever something is changed in the Parts Tab (e.g., checkboxes)
        """
        self.ui.model.blockSignals(True) # Prevents infinite recursion when changing items
        self.set_visible_state(item, item.checkState())
        self.ui.model.blockSignals(False)
        self.checkbox_changed.emit(self.geometry)
        self.refresh() # makes the canvas redraw

    def set_visible_state(self, item, parent_state):
        """
        Alters whether a shape is rendered or not in the cavas based on user selection
        """
        if item.checkState() != parent_state:
            item.setCheckState(parent_state)

        if item.hasChildren():
            for row_index in range(item.rowCount()):
                self.set_visible_state(item.child(row_index), item.checkState())

        state = ['UNCHECKED', 'TRISTATE',  'CHECKED'][item.checkState()]
        if state == "UNCHECKED":
            # if isinstance(item.data(), Shape):
            item.data().setDisable(True)
        elif state == "CHECKED":
            # if isinstance(item.data(), Shape):
            item.data().setDisable(False)

    def load_parts(self, geometry):
        """
        Creates a treeview object based on imported drawing geometry
        """
        self.geometry = geometry
        
        if self.geometry.parts:
            for part in self.geometry.parts:
                part_item = QStandardItem(part.name)
                part_item.setData(part)
                part_item.setCheckable(True)
                part_item.setCheckState(PyQt5.QtCore.Qt.Checked)
                for group in part.groups:
                    group_item = QStandardItem("_".join([part_item.text(), group.name]))
                    group_item.setData(group)
                    group_item.setCheckable(True)
                    group_item.setCheckState(PyQt5.QtCore.Qt.Checked)
                    for shape_index, shape in enumerate(group.shapes):
                        shape_name = "_".join([group_item.text(), str(shape_index)])
                        shape.name = shape_name
                        shape_item = QStandardItem(shape_name)
                        shape_item.setData(shape)
                        shape_item.setCheckable(True)
                        shape_item.setCheckState(PyQt5.QtCore.Qt.Checked)
                        group_item.appendRow(shape_item)
                    part_item.appendRow(group_item)
                self.ui.model.appendRow(part_item)
        self.ui.entitiesTreeView.expandAll()
