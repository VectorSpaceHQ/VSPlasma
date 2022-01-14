# -*- coding: utf-8 -*-
from core.utils import to_float

class SetupTab():
    def __init__(self, mw):
        self.mw = mw
        self.ui = mw.ui
        self.canvas_scene = mw.canvas_scene
        self.workpiece = mw.workpiece

        self.load_values()

        self.ui.workpiece_width_lineEdit.editingFinished.connect(self.update_workpiece)
        self.ui.workpiece_length_lineEdit.editingFinished.connect(self.update_workpiece)
        self.ui.x_origin_lineEdit.editingFinished.connect(self.update_workpiece)
        self.ui.y_origin_lineEdit.editingFinished.connect(self.update_workpiece)

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
