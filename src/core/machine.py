# -*- coding: utf-8 -*-

import core.config as config

from PyQt5.QtGui import QPen, QColor, QBrush
from PyQt5.QtCore import QRectF

class Machine():
    def __init__(self):
        self.x0 = 0
        self.y0 = 0
        self.width = 48
        self.length = 48

    def resize(self, x0=None, y0=None, width=None, height=None):
        self.x0 = x0
        self.y0 = y0
        self.width = width
        self.height = height

    def draw(self, canvas_scene):
        opacity = 50
        pen = QPen(QColor("grey"))
        brush = QBrush(QColor(0,0,0, opacity))
        rect = QRectF(0, 0, self.width, -self.length)
        canvas_scene.addRect(rect, pen, brush)
