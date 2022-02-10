# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPalette, QFont, QStandardItem
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from gui import treeview


class OperationsTab(QWidget):
    """
    Creates GUI behavior of Operations Tab.
    ui: the GUI
    """
    def __init__(self, ui, tools, geometry, PartsTab, refresh):
        QWidget.__init__(self)
        self.ui = ui
        self.tools = tools
        self.geometry = geometry
        self.active_shapes = []
        self.group_item_model = None
        self.groups_list = None
        self.op = None
        self.PartsTab_model = PartsTab.ui.model
        self.PartsTab_checkbox_changed = PartsTab.checkbox_changed
        self.model = treeview.QStandardItemModel()
        self.refresh = refresh

        self.black_palette = QPalette()
        self.grey_palette = QPalette()
        self.grey_palette.setColor(QPalette.Text, QtCore.Qt.gray)

        self.init_signals_and_slots()
        self.init_operation_values()
        self.load_tools()
        self.load_geometry()

    def load_tools(self):
        """
        Load all tools from the Tools tab
        """
        tool_combo_box = self.ui.op_tab_tool_comboBox
        for tool in self.tools.values():
            tool_combo_box.addItem(tool.name)

    def load_geometry(self):
        """
        Load all active shapes from the Entities tab.
        """
        if self.geometry.parts is None:
            return

        for part in self.geometry.parts:
            if not part.isDisabled():
                # show part
                for group in part.groups:
                    if not group.isDisabled():
                        # show group
                        for shape in group.shapes:
                            if not shape.isDisabled():
                                # show shape
                                pass

    def init_signals_and_slots(self):
        self.ui.layersShapesTreeView.setModel(self.model)
        # self.PartsTab_model.itemChanged.connect(self.update_layer_tree)
        # self.PartsTab_checkbox_changed.connect(self.update_layer_tree)
        self.PartsTab_checkbox_changed.connect(self.build_layer_tree)

        # self.ui.layers_shapes_treeView.selectionModel().selectionChanged.connect(self.update_shape_selection)
        self.ui.save_operation_pushButton.clicked.connect(self.save_operation)
        self.ui.delete_operation_pushButton.clicked.connect(self.delete_operation)
        self.ui.operations_listView.doubleClicked.connect(self.load_operation)
        self.ui.op_tab_tool_comboBox.currentIndexChanged.connect(self.load_default_operations)

        # self.ui.op_tab_tool_comboBox.currentIndexChanged.connect(self.update_active_tool)
        self.ui.op_feedrate_lineEdit.editingFinished.connect(self.update_active_operation)
        self.ui.op_plunge_rate_lineEdit.editingFinished.connect(self.update_active_operation)
        self.ui.op_pierce_delay_lineEdit.editingFinished.connect(self.update_active_operation)
        self.ui.op_pierce_height_lineEdit.editingFinished.connect(self.update_active_operation)
        self.ui.op_cut_height_lineEdit.editingFinished.connect(self.update_active_operation)
        # self.ui.tool_lead_in_value.textChanged.connect(self.update_active_tool)

    def load_default_operations(self, idx):
        """
        Load default values from the selected tool.
        Default values load grey.
        """
        tool_name = self.ui.op_tab_tool_comboBox.currentText()
        if tool_name:
            self.active_tool = self.tools[tool_name]
        else:
            return

        feedrate = self.active_tool.feedrate
        plunge_rate = self.active_tool.plunge_rate
        pierce_delay = self.active_tool.pierce_delay
        pierce_height = self.active_tool.pierce_height
        cut_height = self.active_tool.cut_height

        self.ui.op_feedrate_lineEdit.setText(str(feedrate))
        self.ui.op_plunge_rate_lineEdit.setText(str(plunge_rate))
        self.ui.op_pierce_delay_lineEdit.setText(str(pierce_delay))
        self.ui.op_pierce_height_lineEdit.setText(str(pierce_height))
        self.ui.op_cut_height_lineEdit.setText(str(cut_height))

        self.ui.op_feedrate_lineEdit.setPalette(self.grey_palette)
        self.ui.op_plunge_rate_lineEdit.setPalette(self.grey_palette)
        self.ui.op_pierce_delay_lineEdit.setPalette(self.grey_palette)
        self.ui.op_pierce_height_lineEdit.setPalette(self.grey_palette)
        self.ui.op_cut_height_lineEdit.setPalette(self.grey_palette)

        if self.active_shapes and self.active_tool:
            # print("active shapes:", self.active_shapes)
            # print("active tool:", self.active_tool)
            self.op = Operation(self.active_shapes, self.active_tool)

    def init_operation_values(self):
        """
        When a tool is selected for a layer or shape, apply the tool's default
        attributes to the operation's options.
        Default values should be grey and become black when modified.
        Changing to a new tool should reset to default values.
        """
        for shape in self.active_shapes:
            # print("\nactive shapes: ", active_shapes)
            op = Operation(shape, self.tools['adam'])
            ops.add_operation(op)
            # for active_shape in active_shapes:
            #     print(active_shape)

    def update_shape_selection(self, parent, selected, deselected):
        # print("update_shape_selection: ",parent, selected, deselected)
        # print(self.active_shapes)

        if self.active_shapes and self.active_tool:
            self.op = Operation(self.active_shapes, self.active_tool)

    def update_active_tool(self):
        print(self.tool.name)

    def update_active_operation(self):
        """
        On text change or shape selection change, update the active operation's parameters
        """
        self.active_tool.feedrate = self.ui.op_feedrate_lineEdit.text()
        self.active_tool.plunge_rate = self.ui.op_plunge_rate_lineEdit.text()
        self.active_tool.pierce_delay = self.ui.op_pierce_delay_lineEdit.text()
        self.active_tool.pierce_height = self.ui.op_pierce_height_lineEdit.text()
        self.active_tool.cut_height = self.ui.op_cut_height_lineEdit.text()

        self.sender().setPalette(self.black_palette)

        self.active_shapes = self.tree_handler.active_shapes

        if self.active_shapes and self.active_tool:
            # print("active shapes:", self.active_shapes)
            # print("active tool:", self.active_tool)
            self.op = Operation(self.active_shapes, self.active_tool)

    def save_operation(self):
        self.active_shapes = self.tree_handler.active_shapes

        if not self.op:
            return

        g.Operations.add(self.op)

        # update operations list view
        self.ui.operations_listView.clear()
        for o in g.Operations:
            self.ui.operations_listView.addItem(str(o.nr) + ", " + o.name)

    def load_operation(self):
        """
        When operation is double clicked, load its parameters into fields.
        """
        active_operation = self.ui.operations_listView.currentItem().text()
        active_operation_idx = int(active_operation.split(",")[0]) - 1
        self.op = g.Operations[active_operation_idx]

        self.ui.op_feedrate_lineEdit.setText(str(self.op.tool.feedrate))
        self.ui.op_plunge_rate_lineEdit.setText(str(self.op.tool.plunge_rate))
        self.ui.op_pierce_delay_lineEdit.setText(str(self.op.tool.pierce_delay))
        self.ui.op_pierce_height_lineEdit.setText(str(self.op.tool.pierce_height))
        self.ui.op_cut_height_lineEdit.setText(str(self.op.tool.cut_height))

        # highlight active operation
        for i in range(self.ui.operations_listView.count()):
            item = self.ui.operations_listView.item(i)
            item.setFont(QFont('Sans Serif 10', 10, QFont.Normal))
        self.ui.operations_listView.currentItem().setFont(QFont('Verdana', 10, QFont.Bold))


    def delete_operation(self):
        active_operation = self.ui.operations_listView.currentItem().text()
        active_operation_idx = int(active_operation.split(",")[0]) - 1
        try:
            g.Operations.remove(active_operation_idx)
            self.ui.operations_listView.clear()
            for o in g.Operations:
                self.ui.operations_listView.addItem(str(o.nr) + ", " + o.name)
        except Exception as e:
            print("cannot remove operation:", active_operation)
            print(e)

    def build_layer_tree(self, geometry):
        """
        Display Parts, groups and shapes in a layertree
        """
        self.geometry = geometry
        
        if self.geometry.parts is None:
            return

        self.model.clear()

        for part in self.geometry.parts:
            if not part.isDisabled():
                part_item = QStandardItem(part.name)
                part_item.setData(part)
                part_item.setCheckable(True)
                part_item.setCheckState(Qt.Checked)
                for group in part.groups:
                    if not group.isDisabled():
                        group_item = QStandardItem("_".join([part_item.text(), group.name]))
                        group_item.setData(group)
                        group_item.setCheckable(True)
                        group_item.setCheckState(Qt.Checked)
                        for shape_index, shape in enumerate(group.shapes):
                            if not shape.isDisabled():
                                shape_item = QStandardItem("_".join([group_item.text(), str(shape_index)]))
                                shape_item.setData(shape)
                                shape_item.setCheckable(True)
                                shape_item.setCheckState(Qt.Checked)
                                group_item.appendRow(shape_item)
                        part_item.appendRow(group_item)
                self.model.appendRow(part_item)

        self.ui.layersShapesTreeView.expandAll()
        return
