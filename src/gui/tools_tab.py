# -*- coding: utf-8 -*-

import core.globals as g

from PyQt5.QtWidgets import QWidget


class ToolsTab(QWidget):
    def __init__(self, ui, tools):
        QWidget.__init__(self)
        self.ui = ui
        self.tools = tools
        print(self.tools)

        self.tool_table_init()

    def tool_table_init(self):
        """
        Populate tool table with tools from config file.
        """
        self.ui.tool_list_Widget.clear()

        self.ui.new_tool_button.clicked.connect(self.add_tool)
        self.ui.delete_active_tool_pushButton.clicked.connect(self.delete_tool)

        self.ui.tool_list_Widget.itemClicked.connect(self.load_active_tool)
        self.ui.tool_name_value.editingFinished.connect(self.update_active_tool)
        self.ui.tool_number_value.textChanged.connect(self.update_active_tool)
        self.ui.tool_diameter_value.textChanged.connect(self.update_active_tool)
        self.ui.tool_default_feedrate_value.textChanged.connect(self.update_active_tool)
        self.ui.tool_default_plungerate_value.textChanged.connect(self.update_active_tool)
        self.ui.tool_pierce_delay_value.textChanged.connect(self.update_active_tool)
        self.ui.tool_pierce_height_value.textChanged.connect(self.update_active_tool)
        self.ui.tool_lead_in_value.textChanged.connect(self.update_active_tool)

        for tool_name, tool in self.tools.items():
            self.ui.tool_list_Widget.addItem("[T" + str(tool.number) + "]  " + tool_name)
        self.ui.tool_list_Widget.setCurrentRow(0)
        self.load_active_tool()

    def add_tool(self):
        self.tools.add_tool()
        self.refresh_tool_list()
        rowcount = self.ui.tool_list_Widget.count()
        self.ui.tool_list_Widget.setCurrentRow(rowcount-1)
        self.load_active_tool()

    def delete_tool(self):
        tool_name = self.ui.tool_list_Widget.currentItem().text().split(']  ')[-1]
        if tool_name in self.tools:
            self.tools.remove_tool(tool_name)
            self.refresh_tool_list()

    def refresh_tool_list(self):
        currentRow = self.ui.tool_list_Widget.currentRow()
        self.ui.tool_list_Widget.clear()
        for tool_name, tool in self.tools.items():
            self.ui.tool_list_Widget.addItem("[T" + str(tool.number) + "]  " + tool_name)
        self.ui.tool_list_Widget.setCurrentRow(currentRow)

    def load_active_tool(self):
        """
        When tool name changes, load that tool's settings into UI
        """
        tool_name = self.ui.tool_list_Widget.currentItem().text().split(']  ')[-1]
        self.last_act_tool = tool_name
        act_tool = self.tools[tool_name]

        tool_number = str(act_tool.number)
        tool_diameter = str(act_tool.diameter)
        tool_feedrate = str(act_tool.feedrate)
        tool_plunge_rate = str(act_tool.plunge_rate)
        tool_pierce_delay = str(act_tool.pierce_delay)
        tool_pierce_height = str(act_tool.pierce_height)
        tool_lead_in = str(act_tool.lead_in)

        self.ui.tool_name_value.setText(tool_name)
        self.ui.tool_number_value.setText(tool_number)
        self.ui.tool_diameter_value.setText(tool_diameter)
        self.ui.tool_pierce_delay_value.setText(tool_pierce_delay)
        self.ui.tool_pierce_height_value.setText(tool_pierce_height)
        self.ui.tool_default_feedrate_value.setText(tool_feedrate)
        self.ui.tool_default_plungerate_value.setText(tool_plunge_rate)
        self.ui.tool_lead_in_value.setText(tool_lead_in)

    def update_active_tool(self):
        """
        When any tool setting changes, update internal values.
        """
        # tool_name = self.ui.tool_list_Widget.currentItem().text().split(']  ')[-1]
        tool_name = self.last_act_tool
        act_tool = self.tools[tool_name]

        try:
            act_tool.number = int(self.ui.tool_number_value.text())
            act_tool.diameter = float(self.ui.tool_diameter_value.text())
            act_tool.feedrate = float(self.ui.tool_default_feedrate_value.text())
            act_tool.plunge_rate = float(self.ui.tool_default_plungerate_value.text())
            act_tool.pierce_delay = float(self.ui.tool_pierce_delay_value.text())
            act_tool.pierce_height = float(self.ui.tool_pierce_height_value.text())
            act_tool.lead_in = float(self.ui.tool_lead_in_value.text())

            # change tool name
            new_tool_name = self.ui.tool_name_value.text()
            if new_tool_name != tool_name:
                self.tools.change_tool_name(tool_name, new_tool_name)
                self.last_act_tool = new_tool_name

            self.refresh_tool_list()
        except Exception as e:
            print("update_active_tool exception ", e)

        self.tools.save_table()
