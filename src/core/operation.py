# -*- coding: utf-8 -*-

import globals.globals as g
import postprocessing.postprocessor as postprocessor

class Operations(list):
    """
    A list of Operation objects.
    """
    def __init__(self):
        self.count = len(self)

    def __str__(self):
        line = "Operations:\n"
        for op in self:
            line += op.nr + "\n"
        return line

    def add(self, new_operation):
        """
        Add an Operation() object to the Operations list.
        """
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


class Operation():
    """
    An operation assigns tool parameters to one or more contours.
    """
    def __init__(self, Contours, Tool, nr=-1):
        self.contours = Contours
        self.tool = Tool
        self.name = self.tool.name
        self.nr = nr
        self.path = None
        self.closed = True
        self.selected = False
        self.disabled = False
        self.locked = False

        self.stmove = None
        self.starrow = None
        self.enarrow = None

    def __del__(self):
        pass

    def __str__(self):
        output = """Operation:
        Name: {}
        Number: {}
        Tool: {}
        Contours: {}
        """.format(self.name, self.nr, self.tool, self.contours)
        return output

    # rewrite optimizeTSP and put it here
    def generate_path(self):
        """
        Find optimum path along contours.
        Return list of geometries in optimum order
        """
        # path_creation.optimizeTSP()

        starting_order = self.contours
        self.path = []
