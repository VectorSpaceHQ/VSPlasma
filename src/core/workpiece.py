# -*- coding: utf-8 -*-
from PyQt5.QtGui import QPen, QColor, QBrush
from PyQt5.QtCore import QRectF

class Workpiece():
    def __init__(self, machine=None):
        self.machine = machine
        self.x0 = 0
        self.y0 = 0
        self.width = 24
        self.length = 24

    def check_bounds(self):
        """
        Make sure workpiece is within machine bounds.
        """
        cond1 = (self.x0 < self.machine.x0)
        cond2 = (self.x0 + self.width > self.machine.x0 + self.machine.width)
        cond3 = (-self.y0 < self.machine.y0)
        cond4 = (-self.y0 + self.length > self.machine.y0 + self.machine.length)
        if cond1 or cond2 or cond3 or cond4:
            print("WARNING: Workpiece is outside of Machine boundary.")
            return False
        else:
            return True

    def resize(self, width, length):
        self.width = width
        self.length = length

    def move(self, x0, y0):
        original_x = self.x0
        original_y = self.y0
        self.x0 = x0
        self.y0 = -y0

        if not self.check_bounds():
            self.x0 = original_x
            self.y0 = original_y

    def draw(self, canvas_scene):
        opacity = 50
        pen = QPen(QColor("red"))
        brush = QBrush(QColor(255,0,0, opacity))
        rect = QRectF(self.x0, self.y0, self.width, -self.length)
        canvas_scene.addRect(rect, pen, brush)
