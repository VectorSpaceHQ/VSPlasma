# -*- coding: utf-8 -*-

# All geometric entities are structured as follows:
# A Part has Layers which have Shapes
# A Contour is made of points

import core.shape as shape
import core.point as point

class Parts(dict):
    def __init__(self):
        self.name = None

    def __str__(self):
        string = 'There are {} total Parts:\n'.format(str(len(self)))
        i = 1
        for k, v in self.items():
            string += "Part num "+ str(i) + " " + str(k) + ": " + str(v)
            i += 1
        return string


class Part(dict):
    def __init__(self, name=None):
        self.name = name
        self.layers = None
        self.active = False
        self.base_x = 0
        self.base_y = 0
        self.base_point = point.Point(self.base_x, self.base_y)
        self.scale = 1
        self.angle = 0
        self.groups = []

        try:
            parts[self.name] = self # add to collection
        except Exception as e:
            print("A group must belong to a part")

    def add_group(self, group):
        if group not in self:
            self[group.name] = group
            self.groups.append(group)

    def copy(self):
        """
        Create a copy of the part
        """
        new_copy = self
        return new_copy

    def move(self):
        pass

    def rotate(self):
        pass


class Group():
    """
    A group of contours, often called a Layer in 2D drawing.
    A group must belong to a part.
    """
    def __init__(self, nr=-1, part=None, name=None):
        self.shapes = None
        self.active = False
        self.selected = False
        self.disabled = False
        self.locked = False
        self.nr = nr
        self.name = name

        self.contours = []
        self.num_contours = 0

        try:
            self.parent = part
            groups.add_group(self) # add to collection
            part.add_group(self) # add to parent
        except Exception as e:
            print("A group must belong to a part")

    def add_contour(self, contour):
        if contour not in self.contours:
            self.contours.append(contour)
            self.num_contours += 1


class Groups(dict):
    """
    """
    def __init__(self, group=None):
        self.count = 0
        self.names = []

    def __str__(self):
        string = ''
        for l in self.values():
            string += "name: " + str(l.name) + "\n"
            string += "number: " + str(l.nr) + "\n"
        return string

    def add_group(self, group):
        if group not in self.values():
            self[group.name] = group
            self.names.append(group.name)
            self.count += 1


class Contours(list):
    def __init__(self):
        self.count = 0

    def __str__(self):
        string = 'There are {} total Contours.'.format(self.count)
        for contour in self:
            string += str(contour) + "\n"
        return string

    def add_contour(self, contour):
        if contour not in self:
            self.append(contour)
            self.count += 1


class Contour():
    """
    A Shape is a single continuous contour.
    """
    def __init__(self, nr=-1, group=None, closed=True, geos=[]):
        self.active = False
        self.selected = False
        self.disabled = False
        self.locked = False
        self.nr = nr
        self.closed = closed

        self.geos = shape.Geos(geos)

        try:
            self.parent = group
            group.add_contour(self) # add to parent
            contours.add_contour(self) # add to convenience collection
        except Exception as e:
            print("A contour must belong to a group.")
            print(e)

    def __str__(self):
        """
        Standard method to print the object
        @return: A string
        """
        return "\nContour:" +\
               "\nnr:          %i" % self.nr +\
               "\nclosed:      %s" % self.closed +\
               "\ngeos:        %s" % self.geo

    def setSelected(self, flag=False):
        self.selected = flag

    def isSelected(self):
        return self.selected

    def setDisable(self, flag=False):
        self.disabled = flag

    def isDisabled(self):
        return self.disabled

    def calc_bounding_box(self):
        """
        Calculated the BoundingBox of the geometry and saves it into self.BB
        """
        self.BB = self.geos.abs_el(0).BB
        for geo in self.geos.abs_iter():
            self.BB = self.BB.joinBB(geo.BB)

    def get_start_end_points(self, start_point=None, angles=None):
        if start_point is None:
            return (self.geos.abs_el(0).get_start_end_points(True, angles),
                    self.geos.abs_el(-1).get_start_end_points(False, angles))
        elif start_point:
            return self.geos.abs_el(0).get_start_end_points(True, angles)
        else:
            return self.geos.abs_el(-1).get_start_end_points(False, angles)


def build_from_dxf(dxfobj):
    """
    Takes a ReadDXF object and translates into Parts, Layers, and Shapes
    Entities -> parts
    Blocks
    Layers -> groups
    Geo -> contours
    """

    filename = dxfobj.filename
    p = Part(name=filename)

    for idx, l in enumerate(dxfobj.layers):
        g = Group(part=p, nr=idx, name=l.name)


    print("\n\n",groups)

    print("\nblocks:\n", dxfobj.blocks)

    print("\nentities:\n", dxfobj.entities)
    for e in dxfobj.entities.geo:
        # connect geo to group
        layer_nr = e.Layer_Nr
        g = None
        for group in groups.values():
            if group.nr == layer_nr:
                g = group

        c = Contour(group=g)
        c.nr = e.Nr
        c.parent_layer = e.Layer_Nr
        c.geo = e.geo


    # print("report:\n\n")
    # print(parts)
    # print(parts[filename])
    # print(parts[filename].groups)
    # print("group names",groups.names)
    # print(groups[groups.names[0]])
    # print(groups[groups.names[0]].name)
    # print("num contours:", groups[groups.names[0]].num_contours)
    # print(groups[groups.names[0]].contours)
    # print(contours)
    # print(contours[0].geo)

    # print(contours)

contours = Contours()
groups = Groups()
parts = Parts()
