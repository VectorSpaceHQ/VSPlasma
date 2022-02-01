# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from gui import treeview
from PyQt5.QtGui import QStandardItem
import PyQt5.QtCore

# from collections import deque

class PartsTab(QWidget):
    def __init__(self, ui, geometry):
        QWidget.__init__(self)
        self.ui = ui
        self.geometry = geometry

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

        self.part_table_init()

        

    def part_table_init(self):
        """
        Populate part table with geometry tree
        """

        self.ui.model.itemChanged.connect(self.alter_render)
        # self.ui.entities_tab.itemClicked.connect(self.load_parts)
        # self.ui.entitiesTreeView.itemClicked.connect(self.load_parts)
        # self.ui.actionImport.triggered.connect(self.load_parts)
        # self.geometry.changed.connect(self.load_parts)
        #  self.geometry.value_updated.connect(self.load_parts)
        # if self.geometry.parts:
        #     for part in self.geometry.parts:
        #         self.ui.model.appendRow(QStandardItem(part))

    def alter_render(self):
        return

    def load_parts(self, geometry):
        """
        """
        # self.importData(self.data)
        self.geometry = geometry
        
        if self.geometry.parts:
            for part_name, part_object in self.geometry.parts.items():
                part = QStandardItem(part_name)
                part.setCheckable(True)
                part.setCheckState(PyQt5.QtCore.Qt.Checked)
                for group_index, group_object in enumerate(part_object.groups):
                    # group = QStandardItem(str(group_index))
                    group = QStandardItem(group_object.name)
                    group.setCheckable(True)
                    group.setCheckState(PyQt5.QtCore.Qt.Checked)
                    # for index, shape in enumerate(group.contours): #should be shapes?
                    for shape_index, shape_object in enumerate(group_object.contours): #should be shapes?
                        shape = QStandardItem(str(shape_index))
                        shape.setCheckable(True)
                        shape.setCheckState(PyQt5.QtCore.Qt.Checked)
                        # self.ui.model.appendRow(QStandardItem(str(index)).setCheckable(True))
                        group.appendRow(shape)
                    part.appendRow(group)
                self.ui.model.appendRow(part)
        # for row in self.ui.model:
        #     row.setCheckable(True)

        # On a shape object, you can call shape_object.setDisabled(True) and it won't draw

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

     