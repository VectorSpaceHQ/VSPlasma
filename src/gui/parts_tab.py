# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from gui import treeview
from PyQt5.QtGui import QStandardItem
import PyQt5.QtCore
from core.geometry import Shape

# from collections import deque

class PartsTab(QWidget):
    def __init__(self, mainwindow, ui, geometry):
        QWidget.__init__(self)
        self.ui = ui
        self.geometry = geometry
        self.mainwindow = mainwindow

        self.tree = self.ui.entitiesTreeView
        
        self.ui.model = treeview.QStandardItemModel()
        # self.ui.model.setHorizontalHeaderLabels(['Name', 'Height', 'Weight'])
        self.tree.setModel(self.ui.model)


        # self.data = [
        #     {'unique_id': 1, 'parent_id': 0, 'short_name': '', 'height': ' ', 'weight': ' '},
        #     {'unique_id': 2, 'parent_id': 1, 'short_name': 'Class 1', 'height': ' ', 'weight': ' '},
        #     {'unique_id': 3, 'parent_id': 2, 'short_name': 'Lucy', 'height': '162', 'weight': '50'},
        #     {'unique_id': 4, 'parent_id': 2, 'short_name': 'Joe', 'height': '175', 'weight': '65'},
        #     {'unique_id': 5, 'parent_id': 1, 'short_name': 'Class 2', 'height': ' ', 'weight': ' '},
        #     {'unique_id': 6, 'parent_id': 5, 'short_name': 'Lily', 'height': '170', 'weight': '55'},
        #     {'unique_id': 7, 'parent_id': 5, 'short_name': 'Tom', 'height': '180', 'weight': '75'},
        #     {'unique_id': 8, 'parent_id': 1, 'short_name': 'Class 3', 'height': ' ', 'weight': ' '},
        #     {'unique_id': 9, 'parent_id': 8, 'short_name': 'Jack', 'height': '178', 'weight': '80'},
        #     {'unique_id': 10, 'parent_id': 8, 'short_name': 'Tim', 'height': '172', 'weight': '60'}
        # ]  


        # self.importData(self.data)
        # self.tree.expandAll()

        self.ui.model.itemChanged.connect(self.on_item_changed)
        # self.part_table_init()

        

    def part_table_init(self):
        """
        Populate part table with geometry tree
        """

        self.ui.model.itemChanged.connect(self.on_item_changed)
        # self.ui.entities_tab.itemClicked.connect(self.load_parts)
        # self.ui.entitiesTreeView.itemClicked.connect(self.load_parts)
        # self.ui.actionImport.triggered.connect(self.load_parts)
        # self.geometry.changed.connect(self.load_parts)
        #  self.geometry.value_updated.connect(self.load_parts)
        # if self.geometry.parts:
        #     for part in self.geometry.parts:
        #         self.ui.model.appendRow(QStandardItem(part))

    def on_item_changed(self, item):
        # state = ['UNCHECKED', 'TRISTATE',  'CHECKED'][item.checkState()]
        # print("Item with text '%s', is at state %s\n" % ( item.text(),  state))
        # combination of item.hasChildren(), item.rowCount(), and item.child(#)
        self.ui.model.blockSignals(True) # Prevents infinite recursion when changing items
        self.set_visible_state(item, True)
        self.ui.model.blockSignals(False)
        # if isinstance(checkbox_object_data, Part):
        #     for group_index, group_object in enumerate(checkbox_object_data.groups):
        #         for shape_index, shape_object in enumerate(group_object.contours): #should be shapes?
        #             self.set_visible_state(shape_object, state)
        # elif isinstance(checkbox_object_data, Group):
        #     for shape_index, shape_object in enumerate(checkbox_object_data.contours): #should be shapes?
        #             self.set_visible_state(shape_object, state)
        # elif isinstance(checkbox_object_data, Shape):
        #     self.set_visible_state(checkbox_object_data, state)
        # else:
        #     pass
        
        self.mainwindow.refresh()
        return

    def set_visible_state(self, item, is_top):
        state = ['UNCHECKED', 'TRISTATE',  'CHECKED'][item.checkState()]

        if item.hasChildren():
            for row_index in range(item.rowCount()):
                self.set_visible_state(item.child(row_index), False)

        if is_top:
            if state == "UNCHECKED":
                if isinstance(item.data(), Shape):
                    item.data().setDisable(True)
            elif state == "CHECKED":
                if isinstance(item.data(), Shape):
                    item.data().setDisable(False)
        else:
            if state == "UNCHECKED":
                item.setCheckState(PyQt5.QtCore.Qt.Checked)
                if isinstance(item.data(), Shape):
                    item.data().setDisable(False)
            elif state == "CHECKED":
                item.setCheckState(PyQt5.QtCore.Qt.Unchecked)
                if isinstance(item.data(), Shape):
                    item.data().setDisable(True)

        return

    def load_parts(self, geometry):
        """
        """
        # self.importData(self.data)
        self.geometry = geometry
        
        if self.geometry.parts:
            for part_name, part_object in self.geometry.parts.items():
                part = QStandardItem(part_name)
                part.setData(part_object)
                part.setCheckable(True)
                part.setCheckState(PyQt5.QtCore.Qt.Checked)
                for group_index, group_object in enumerate(part_object.groups):
                    # group = QStandardItem(str(group_index))
                    group = QStandardItem(group_object.name)
                    group.setData(group_object)
                    group.setCheckable(True)
                    group.setCheckState(PyQt5.QtCore.Qt.Checked)
                    # for index, shape in enumerate(group.contours): #should be shapes?
                    for shape_index, shape_object in enumerate(group_object.contours): #should be shapes?
                        shape = QStandardItem(str(shape_index))
                        # shape.setData(shape_object, role=PyQt5.QtCore.Qt.UserRole)
                        shape.setData(shape_object)
                        shape.setCheckable(True)
                        shape.setCheckState(PyQt5.QtCore.Qt.Checked)
                        # self.ui.model.appendRow(QStandardItem(str(index)).setCheckable(True))
                        group.appendRow(shape)
                    part.appendRow(group)
                self.ui.model.appendRow(part)
        # for row in self.ui.model:
        #     row.setCheckable(True)

        # On a shape object, you can call shape_object.setDisable(True) and it won't draw

        self.tree.expandAll()



    # def importData(self, data, root=None):
    #     self.ui.model.setRowCount(0)
    #     if root is None:
    #         root = self.ui.model.invisibleRootItem()
    #     seen = {}   # List of  QStandardItem
    #     values = deque(data)
    #     while values:
    #         value = values.popleft()
    #         if value['unique_id'] == 1:
    #             parent = root
    #         else:
    #             pid = value['parent_id']
    #             if pid not in seen:
    #                 values.append(value)
    #                 continue
    #             parent = seen[pid]
    #         unique_id = value['unique_id']
    #         parent.appendRow([
    #             QStandardItem(value['short_name']),
    #             QStandardItem(value['height']),
    #             QStandardItem(value['weight'])
    #         ])
    #         seen[unique_id] = parent.child(parent.rowCount() - 1)

     