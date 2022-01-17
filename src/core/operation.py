# -*- coding: utf-8 -*-


class Operations(list):
    """
    A list of Operation objects.
    """
    def __init__(self):
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
        pass


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
        for shape in self.shapes:
            for geo in shape.geos:
                gcode += geo.Write_GCode()
        print(gcode)
