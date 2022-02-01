# -*- coding: utf-8 -*-

# All geometric entities are structured as follows:
# A Part has Groups which have Shapes
# A Shape is made of Elements

# Parts is a list of Part objects
# Groups is a list of Group objects
# Shapes is a list of Shape objects

import core.point as point
from PyQt5.QtGui import QPainterPath, QPen, QColor
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsPathItem, QStyle


class Geometry():
    def __init__(self, Parts=None, Groups=None, Shapes=None):
        self.parts = Parts
        self.groups = Groups
        self.shapes = Shapes


class Geos(list):
    def __init__(self, *args):
        list.__init__(self, *args)

    def abs_iter(self):
        for geo in list.__iter__(self):
            yield geo.abs_geo if geo.abs_geo else geo

    def abs_el(self, element):
        print("abs_el:",element)
        return self[element].abs_geo if self[element].abs_geo else self[element]


class Parts(list):
    def __init__(self):
        self.name = None

    def __str__(self):
        string = '\nThere are {} total Parts:\n'.format(str(len(self)))
        for part in self:
            string += "Part\n"
            string += "nr: "+ str(part.num) + "\n"
            string += "name: " + str(part.name) +"\n"
        return string


class Groups(list):
    """
    {"group_name": group_obj,
     }

    """
    def __init__(self):
        self.count = 0
        self.names = []

    def __str__(self):
        string = '\nThere are {} total Groups:\n'.format(str(len(self)))
        for group in self:
            string += "name: " + str(group.name) + "\n"
            string += "number: " + str(group.nr) + "\n"
        return string

    def add_group(self, group):
        if group.name not in self.names: # group names must be unique
            self.append(group)
            self.names.append(group.name)
            self.count += 1


class Shapes(list):
    def __init__(self):
        self.count = 0

    def __str__(self):
        string = '\nThere are {} total Shapes:'.format(self.count)
        for contour in self:
            string += str(contour) + "\n"
        return string

    def add_shape(self, new_shape):
        if new_shape not in self:
            self.append(new_shape)
            self.count += 1

    def get_selected(self):
        selected_shapes = []
        for shape in self:
            if shape.selected:
                selected_shapes.append(shape)
        return selected_shapes


class Part():
    def __init__(self, name=None, collector=None):
        self.name = name
        self.num = 0
        self.layers = None
        self.active = False
        self.base_x = 0
        self.base_y = 0
        self.x0 = 0
        self.y0 = 0
        self.base_point = point.Point(self.base_x, self.base_y)
        self.scale = 1
        self.angle = 0
        self.groups = []

        try:
            collector.append(self) # add to Parts collection
        except Exception as e:
            print("A part must belong to a parts")

    def add_group(self, new_group):
        for group in self.groups:
            if new_group.name == group.name:
                return
        self.groups.append(new_group)

    def copy(self):
        """
        Create a copy of the part
        """
        new_copy = self
        return new_copy

    def move(self):
        pass

    def rotate(self, deg):
        """
        Rotate all shapes in this part.
        """
        for shape in shapes:
            pathItem = shape.pathItem
            # pathItem
            pathItem.setRotation(deg)


class Group():
    """
    A group must belong to a part.
    Must contain shapes.
    """
    def __init__(self, nr=-1, part=None, name=None, collector=None, shapes=None):
        self.shapes = None
        self.active = False
        self.selected = False
        self.disabled = False
        self.locked = False
        self.nr = nr
        self.name = name

        self.shapes = []
        self.num_shapes = 0

        try:
            self.parent = part
            collector.add_group(self) # add to collection (Groups)
            self.parent.add_group(self) # add to parent (Part)
        except Exception as e:
            print("A group must belong to a part")

    def add_shape(self, new_shape):
        # print("ADDSHAPE", new_shape)
        # if new_shape not in self.shapes:
        self.shapes.append(new_shape)
        self.num_shapes += 1


class Shape():
    """
    One or more geometric shapes: Line, Arc, etc.
    """
    def __init__(self, nr=-1, group=None, closed=True, collector=None, geos=[], elements=[]):
        self.selected = False
        self.disabled = False
        self.locked = False
        self.nr = nr
        self.closed = closed
        self.start_point = None
        self.end_point = None
        self.BB = None
        self.geos = Geos(geos)
        self.pathItem = QGraphicsPathItem()
        self.elements = Elements(elements)  # this will eventually replace Geos

        # self.make_paint_path()

        try:
            self.parent = group
            group.add_shape(self) # add to parent (Group)
            collector.add_shape(self) # add to convenience collection (Shapes)
        except Exception as e:
            print("A shape must belong to a group.")
            print(e)

    def __str__(self):
        """
        Standard method to print the object
        @return: A string
        """
        return "\nShape:" +\
               "\nnr:          %i" % self.nr +\
               "\nclosed:      %s" % self.closed +\
               "\nGroup:       %s" % self.parent.name +\
               "\ngeos:        %s" % self.geos

    def setSelected(self, flag=False):
        self.selected = flag

    def isSelected(self):
        return self.selected

    def setDisable(self, flag=False):
        self.disabled = flag

    def isDisabled(self):
        return self.disabled

    def inner_offset(self):
        """
        Calculate inner offset of shape using Polygon Offsetting by Computing
        Winding Numbers (Chen, McMains) algorithm.
        Only works on straight lines??
        """
        # calc winding num
        # w > 0 is interior
        # w
        w = self.calc_winding_num()

    def calc_winding_num(self):
        # https://cs.stackexchange.com/questions/28656/calculate-winding-number
        P = 1
        theta = 1
        w = 0
        for i in len(vertices)-1:
            theta = vertices[i] * P - vertices[i+1] * P
        return w


    def calc_bounding_box(self):
        """
        Calculated the BoundingBox of the geometry and saves it into self.BB
        """
        self.BB = self.geos.abs_el(0).BB
        for geo in self.geos.abs_iter():
            self.BB = self.BB.joinBB(geo.BB)

    def make_path_item(self, canvas_scene):
        """
        Render shape with path technique. More flexible support of shapes found
        in vector formats but has to be done in correct order.
        """
        # pen = QPen()
        pen = QPen(QColor('black'), 0.1)
        path = QPainterPath()
        pathItem = myQGraphicsPathItem()

        if not self.disabled:
            for geo in self.geos:
                geo.make_path(path)

        pathItem.setPath(path)
        self.pathItem = pathItem
        canvas_scene.addItem(self.pathItem)


class Elements():
    def __init__(self, element):
        pass


class Element():
    """
    Elements make up shapes. Elements include Line, Arc, Spline, Ellipse, etc.
    """
    def __init__(self, start_point=None, end_point=None):
        self.start_point = start_point
        self.end_point = end_point

        self.calc_bounding_box()

    def __str__(self):
        pass

    def make_path(self):
        pass


class myQGraphicsPathItem(QGraphicsPathItem):
    def __init__(self):
        super().__init__()
        # self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

    def mousePressEvent(self, e):
        if self.isSelected():
            self.setSelected(False)
        else:
            self.setSelected(True)

        if self.isSelected():
            pen = QPen(QColor('blue'), 0.5)
        else:
            pen = QPen(QColor('black'), 0.1)
        self.setPen(pen)

    def mouseDoubleClickEvent(self, e):
        print("geometry.py: double click", e)

    def paint(self, painter, option, a):
        """
        Hide the dashed line on selected items
        """
        option.state = QStyle.State_None
        return super(myQGraphicsPathItem, self).paint(painter,option)


def initialize():
    return Geometry()
