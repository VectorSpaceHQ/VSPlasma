# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget
from gui import treeview
from PyQt5.QtGui import QStandardItem
import PyQt5.QtCore
from core.geometry import Shape


class PartsTab(QWidget):
    def __init__(self, ui, geometry, refresh):
        QWidget.__init__(self)
        self.refresh = refresh
        self.ui = ui
        self.geometry = geometry

        self.tree = self.ui.entitiesTreeView
        self.ui.model = treeview.QStandardItemModel()
        self.tree.setModel(self.ui.model)
        self.ui.model.itemChanged.connect(self.on_item_changed)
        return

    def on_item_changed(self, item):
        self.ui.model.blockSignals(True) # Prevents infinite recursion when changing items
        self.set_visible_state(item, item.checkState())
        self.ui.model.blockSignals(False)
        self.refresh()
        return


    def set_visible_state(self, item, parent_state):
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

        return


    def load_parts(self, geometry):
        """
        """
        self.geometry = geometry
        
        if self.geometry.parts:
            for part in self.geometry.parts:
                part_item = QStandardItem(part.name)
                part_item.setData(part)
                part_item.setCheckable(True)
                part_item.setCheckState(PyQt5.QtCore.Qt.Checked)
                for group in part.groups:
                    group_item = QStandardItem(group.name)
                    group_item.setData(group)
                    group_item.setCheckable(True)
                    group_item.setCheckState(PyQt5.QtCore.Qt.Checked)
                    for shape_index, shape in enumerate(group.shapes):
                        shape_item = QStandardItem(str(shape_index))
                        shape_item.setData(shape)
                        shape_item.setCheckable(True)
                        shape_item.setCheckState(PyQt5.QtCore.Qt.Checked)
                        group_item.appendRow(shape_item)
                    part_item.appendRow(group_item)
                self.ui.model.appendRow(part_item)
        self.tree.expandAll()
        return