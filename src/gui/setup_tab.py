# -*- coding: utf-8 -*-
from core.utils import to_float

class SetupTab():
    def __init__(self, mw, operations):
        self.mw = mw
        self.ui = mw.ui
        self.operations = operations
        self.canvas_scene = mw.canvas_scene
        self.workpiece = mw.workpiece
        self.machine = mw.machine
        self.geometry = mw.geometry

        self.load_values()
        self.setup_origin()

        self.ui.workpiece_width_lineEdit.editingFinished.connect(self.update_workpiece)
        self.ui.workpiece_length_lineEdit.editingFinished.connect(self.update_workpiece)


    def setup_origin(self):
        self.ui.x_origin_lineEdit.editingFinished.connect(self.update_workpiece)
        self.ui.y_origin_lineEdit.editingFinished.connect(self.update_workpiece)
        self.ui.origin_relative_comboBox.currentIndexChanged.connect(self.update_origin)
        self.ui.top_left_Button.toggled.connect(self.update_origin)
        self.ui.top_center_Button.toggled.connect(self.update_origin)
        self.ui.top_right_Button.toggled.connect(self.update_origin)
        self.ui.center_left_Button.toggled.connect(self.update_origin)
        self.ui.center_Button.toggled.connect(self.update_origin)
        self.ui.center_right_Button.toggled.connect(self.update_origin)
        self.ui.bot_left_Button.toggled.connect(self.update_origin)
        self.ui.bot_center_Button.toggled.connect(self.update_origin)
        self.ui.bot_right_Button.toggled.connect(self.update_origin)

    def update_origin(self,e):
        x_offset = 0
        y_offset = 0
        relative_to = self.ui.origin_relative_comboBox.currentText()

        if relative_to == "Part":
            # rough hack for testing
            try:
                k,v = self.geometry.parts.items()
                active_part = v[0]
                relative_obj = active_part
            except:
                print("no parts selected")
                return
        elif relative_to == "Workpiece":
            active_part = self.workpiece
            relative_obj = active_part
        elif relative_to == "Machine":
            active_part = self.machine
            relative_obj = active_part

        if self.ui.top_left_Button.isChecked():
            x_offset = relative_obj.x0
            y_offset = relative_obj.y0 - relative_obj.length
        elif self.ui.top_center_Button.isChecked():
            x_offset = relative_obj.x0 + (relative_obj.width / 2)
            y_offset = relative_obj.y0 - relative_obj.length
        elif self.ui.top_right_Button.isChecked():
            x_offset = relative_obj.x0 + relative_obj.width
            y_offset = relative_obj.y0 - relative_obj.length
        elif self.ui.center_left_Button.isChecked():
            x_offset = relative_obj.x0
            y_offset = relative_obj.y0 - (relative_obj.length / 2)
        elif self.ui.center_Button.isChecked():
            x_offset = relative_obj.x0 + (relative_obj.width / 2)
            y_offset = relative_obj.y0 - (relative_obj.length / 2)
        elif self.ui.center_right_Button.isChecked():
            x_offset = relative_obj.x0 + relative_obj.width
            y_offset = relative_obj.y0 - (relative_obj.length / 2)
        elif self.ui.bot_left_Button.isChecked():
            x_offset = relative_obj.x0
            y_offset = relative_obj.y0
        elif self.ui.bot_center_Button.isChecked():
            x_offset = relative_obj.x0 + (relative_obj.width / 2)
            y_offset = relative_obj.y0
        elif self.ui.bot_right_Button.isChecked():
            x_offset = relative_obj.x0 + relative_obj.width
            y_offset = relative_obj.y0

        self.operations.x0 = relative_obj.x0 + x_offset
        self.operations.y0 = relative_obj.y0 + y_offset

        self.operations.draw_origin(self.canvas_scene)


    def load_values(self):
        self.ui.x_origin_lineEdit.setText(str(self.workpiece.x0))
        self.ui.y_origin_lineEdit.setText(str(self.workpiece.y0))
        self.ui.workpiece_width_lineEdit.setText(str(self.workpiece.width))
        self.ui.workpiece_length_lineEdit.setText(str(self.workpiece.length))

    def update_workpiece(self):
        new_x = to_float(self.ui.x_origin_lineEdit.text())
        new_y = to_float(self.ui.y_origin_lineEdit.text())
        self.workpiece.move(new_x, new_y)
        self.workpiece.width = to_float(self.ui.workpiece_width_lineEdit.text())
        self.workpiece.length = to_float(self.ui.workpiece_length_lineEdit.text())

        self.mw.refresh()
