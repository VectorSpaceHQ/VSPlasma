# -*- coding: utf-8 -*-
import core.point as point


class Entity():
    def __init__(self, nr=-1, parent=None, geoent=None):
        self.typ = ''
        self.parent = parent
        self.nr = nr
        self.geoent = geoent

        self.read_geoent()

    def __str__(self):
        string = "self.typ: {}".format(self.typ)
        string += "\nself.nr: {}".format(self.nr)
        string += "\nparent: {}".format(self.parent)
        return string

    def read_geoent(self):
        self.start_point = 0



class Line(Entity):
    def __init__(self):
        pass
