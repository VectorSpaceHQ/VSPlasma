# -*- coding: utf-8 -*-
from PyQt5.QtGui import QPainterPath, QPen, QColor, QPainterPathStroker, QMouseEvent, QBrush
from PyQt5.QtCore import QRectF
from PyQt5.QtWidgets import QGraphicsItem
from PyQt5 import QtCore, QtWidgets
from core.point import Point
from core.linegeo import LineGeo

class Operations(list):
    """
    A list of Operation objects.
    """
    def __init__(self):
        self.rect = QtWidgets.QGraphicsRectItem()
        self.x0 = 0
        self.y0 = 0
        self.origin = Point(0,0)
        self.count = len(self)

    def __str__(self):
        line = "Operations:\n"
        for op in self:
            line += str(op.name) + "\n"
            line += str(op.nr) + "\n"
        return line

    def add(self, new_operation):
        """
        Add an Operation() object to the Operations list.
        """
        if new_operation is None:
            print("add failed")
            return

        # check if this operation already exists
        for existing_op in self:
            if ((new_operation.shapes == existing_op.shapes) and
                (new_operation.tool == existing_op.tool)):
                return

        self.append(new_operation)
        new_operation.nr = self.index(new_operation) + 1

    def remove(self, operation):
        """
        Remove an Operation() object from the Operations list.
        """
        self.pop(operation)

        # renumber operations
        for idx, op in enumerate(self):
            op.nr = idx + 1

    def generate_paths(self):
        """
        Generate Paths for each operation
        """
        self.gcode = ''

        # Additional gcode
        self.gcode += "G20 G40 G90\n"

        # Default feed rate
        self.gcode += "F1 \n"

        # Add each operation
        for operation in self:
            gcode = operation.write_gcode()
            self.gcode += gcode

    def draw_origin(self, canvas):
        try:
            canvas.removeItem(self.rect)
        except Exception as e:
            print(e)

        pen = QPen(QColor("green"))
        brush = QBrush(QColor(255,0,0, 50))
        rect = QRectF(self.x0-1, self.y0-1, 2, 2)
        rect_item = QtWidgets.QGraphicsRectItem(rect)
        rect_item.setPen(pen)
        self.rect = rect_item
        canvas.addItem(self.rect)


class Operation(object):
    """
    An operation assigns tool parameters to one or more shapes.
    """
    def __init__(self, Shapes, Tool, nr=-1, parent=None):
        self.shapes = Shapes
        self.tool = Tool
        self.name = self.tool.name
        self.nr = nr
        self.path = None
        self.closed = True
        self.selected = False
        self.disabled = False
        self.locked = False
        self.parent = parent

        self.stmove = None
        self.starrow = None
        self.enarrow = None

    def __new__(cls, Shapes, Tool, nr=-1, parent=None):
        if not Tool or not Shapes:
            print("Operation could not be made")
        else:
            print("Operation made")
            return object.__new__(cls)

    def __del__(self):
        pass

    def __str__(self):
        output = """Operation:
        Name: {}
        Number: {}
        Tool: {}
        Shapes: {}
        """.format(self.name, self.nr, self.tool, self.contours)
        return output

    # rewrite optimizeTSP and put it here
    def generate_path(self):
        """
        Find optimum path along shapes.
        Return list of geometries in optimum order
        """
        # path_creation.optimizeTSP()
        pass

    def write_gcode(self):
        # each shape is drawn of geos, those geos have direct Gcode translations
        gcode = ''

        # State Part name
        gcode += "(Part: {}\n)".format(self.shapes)

        # Set tool
        gcode += "M6 T{} ({})\n".format(self.tool.number, self.tool.name)

        #--------------- This needs work -------
        origin = LineGeo(Point(0,0), Point(0,0))
        last_geo = origin # origin start points
        #------------------------------

        for shape in self.shapes:
            for geo in shape.geos:
                if geo.Ps.x == last_geo.Pe.x and geo.Ps.y == last_geo.Pe.y:
                    # if start of this line matches end of last, G1
                    gcode += geo.move_to_end()
                else:
                    # else Rapid move G0
                    gcode += geo.rapid_to_start()
                    gcode += geo.move_to_end()

                last_geo = geo
        return gcode
