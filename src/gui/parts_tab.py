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
            if isinstance(item.data(), Shape):
                item.data().setDisable(True)
        elif state == "CHECKED":
            if isinstance(item.data(), Shape):
                item.data().setDisable(False)

        return


    def load_parts(self, geometry):
        """
        """
        self.geometry = geometry
        
        if self.geometry.parts:
            for part_name, part_object in self.geometry.parts.items():
                part = QStandardItem(part_name)
                part.setData(part_object)
                part.setCheckable(True)
                part.setCheckState(PyQt5.QtCore.Qt.Checked)
                for group_index, group_object in enumerate(part_object.groups):
                    group = QStandardItem(group_object.name)
                    group.setData(group_object)
                    group.setCheckable(True)
                    group.setCheckState(PyQt5.QtCore.Qt.Checked)
                    for shape_index, shape_object in enumerate(group_object.contours): #should be shapes?
                        shape = QStandardItem(str(shape_index))
                        shape.setData(shape_object)
                        shape.setCheckable(True)
                        shape.setCheckState(PyQt5.QtCore.Qt.Checked)
                        group.appendRow(shape)
                    part.appendRow(group)
                self.ui.model.appendRow(part)
        self.tree.expandAll()
        return