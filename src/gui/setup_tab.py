# -*- coding: utf-8 -*-

class SetupTab():
    def __init__(self, mw, ui, workpiece, canvas_scene):
        self.mw = mw
        self.ui = ui
        self.canvas_scene = canvas_scene
        self.workpiece = workpiece

        self.load_values()

        self.ui.workpiece_width_lineEdit.editingFinished.connect(self.update_workpiece)
        self.ui.workpiece_length_lineEdit.editingFinished.connect(self.update_workpiece)
        self.ui.x_origin_lineEdit.editingFinished.connect(self.update_workpiece)
        self.ui.y_origin_lineEdit.editingFinished.connect(self.update_workpiece)

    def load_values(self):
        self.ui.workpiece_width_lineEdit.setText(str(self.workpiece.width))
        self.ui.workpiece_length_lineEdit.setText(str(self.workpiece.length))

    def update_workpiece(self):

        # self.workpiece.x0 = float(self.ui.workpiece_width_lineEdit.text())
        # self.workpiece.y0 = float(self.ui.workpiece_width_lineEdit.text())
        self.workpiece.width = _to_float_(self.ui.workpiece_width_lineEdit.text())
        self.workpiece.length = _to_float_(self.ui.workpiece_length_lineEdit.text())

        self.mw.refresh()
        print("UPDATE WORKIECE")


def _to_float_(text):
    if text == '':
        val = 0
    else:
        val = float(text)
    return val
