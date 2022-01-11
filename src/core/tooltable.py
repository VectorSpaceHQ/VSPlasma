# -*- coding: utf-8 -*-
############################################################################
#
#   Copyright (c) 2021 Adam Spontarelli <adam@vector-space.org>
#
#   This file is part of VSPlasma.
#
#   VSPlasma is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   VSPlasma is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with VSPlasma.  If not, see <http://www.gnu.org/licenses/>.
#
############################################################################

import os
import sys
import pprint
import logging
import yaml
import core.globals as g

from collections import OrderedDict
from configobj import ConfigObj, flatten_errors
from validate import Validator

from PyQt5 import QtCore


class ToolTable(dict):
    """
    A single ToolTable consists of many Tools.
    """
    def __init__(self):
        self._list = []
        self.folder = os.path.join('', g.DEFAULT_CONFIG_DIR)
        self.filename = os.path.join(self.folder, 'tooltable.cfg')
        self.tool_count = 0

        self.load_table()

    def load_table(self):
        """
        Load tool table from cfg file and create Tools.
        """
        if os.path.exists(self.filename):
            with open(self.filename, "r") as stream:
                try:
                    tools = yaml.safe_load(stream)
                    for tool in tools.values():
                        new_tool = Tool()
                        new_tool.create_from_dict(tool)
                        self.add_tool(new_tool)
                except yaml.YAMLError as exc:
                    print("EXCEPTION:", exc)
        else:
            self.make_default_table()

    def make_default_table(self):
        """
        If no table exists, make one.
        """
        default_tool = Tool()
        self.add_tool(default_tool)
        second_tool = Tool()
        second_tool.name = 'second'
        self.add_tool(second_tool)

        self.save_table()

    def save_table(self):
        """
        Save tool table to cfg file
        """
        with open(self.filename, "w") as outfile:
            for tool in self.values():
                outfile.writelines([tool.name, ":\n"])
                for k, v in dict(tool).items():
                    outfile.writelines(["    ", str(k), ": ", str(v), "\n"])

    def add_tool(self, tool=None):
        if not tool:
            tool = Tool()
        while tool.name in self.keys():
            tool.name += "1"
        self[tool.name] = tool
        self.tool_count += 1

    def remove_tool(self, tool_name):
        self.pop(tool_name)
        self.tool_count -= 1

    def change_tool_name(self, oldname, newname):
        self[newname] = self[oldname]
        del self[oldname]
        self[newname].name = newname
        self.save_table()


class Tool():
    def __init__(self):
        self.tool_type = 'plasma'
        self.name = 'default'
        self.number = int(0)
        self.diameter = float(1.0)
        self.feedrate = float(0.0)
        self.plunge_rate = float(0.0)
        self.pierce_delay = float(0.0)
        self.pierce_height = 0.25
        self.cut_height = 0.125
        self.lead_in = float(0.25)
        self.speed = 1.0
        self.start_radius = 0.1

    def __str__(self):
        """
        Standard method to print the object
        @return: A string
        """
        string = ''
        for attr, value in self.__dict__.items():
            string += "\n" + str(attr) + ":    " + str(value)
        return string

    def __iter__(self):
        for attr, value in self.__dict__.items():
            yield attr, value

    def create_from_dict(self, d):
        for attr, v in self:
            try:
                setattr(self, attr, d[attr])
            except Exception as e:
                print("Error:", e)
