#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import time
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
import vsplasma as vsp
import PyQt5
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget
from PyQt5.QtCore import QSize

app = QApplication(sys.argv)
window = vsp.MainWindow(app)

class Test1inBox(unittest.TestCase):
    def setUp(self):
        window.open_file(filename="../tests/1in-box.dxf")

    def test_geometry_count(self):
        self.assertEqual(len(window.geometry.parts), 1)
        self.assertEqual(len(window.geometry.groups), 1)
        self.assertEqual(len(window.geometry.shapes), 8)

    def test_geometry_count2(self):
        self.assertEqual(len(window.geometry.parts), 1)
        self.assertEqual(len(window.geometry.groups), 1)
        self.assertEqual(len(window.geometry.shapes), 8)


class TestSquare(unittest.TestCase):
    def setUp(self):
        window.open_file(filename="../tests/100mm_square.dxf")

    def test_geometry_count(self):
        self.assertEqual(len(window.geometry.parts), 1)
        self.assertEqual(len(window.geometry.groups), 1)
        self.assertEqual(len(window.geometry.shapes), 1)


class TestCircleLayers(unittest.TestCase):
    def setUp(self):
        window.open_file(filename="../tests/circle-layers.dxf")

    def test_geometry_count(self):
        parts = window.geometry.parts
        part = parts[0]
        self.assertEqual(len(parts), 1, "Wrong number of parts")
        self.assertEqual(len(part.groups), 2, "Wrong number of groups")
        self.assertEqual(len(part.groups[0].shapes), 2, "Wrong number of shapes")
        self.assertEqual(len(part.groups[1].shapes), 2, "Wrong number of shapes")
        self.assertEqual(len(window.geometry.parts), 1)
        self.assertEqual(len(window.geometry.groups), 2)
        self.assertEqual(len(window.geometry.shapes), 4)


# class TestText(unittest.TestCase):
#     def setUp(self):
#         window.open_file(filename="../tests/text.dxf")

#     def test_geometry_count(self):
#         self.assertEqual(len(window.geometry.parts), 1)
#         self.assertEqual(len(window.geometry.groups), 2)
#         self.assertEqual(len(window.geometry.shapes), 4)


class TestTwoArcs(unittest.TestCase):
    def setUp(self):
        window.open_file(filename="../tests/two-arcs.dxf")

    def test_geometry_count(self):
        self.assertEqual(len(window.geometry.parts), 1)
        self.assertEqual(len(window.geometry.groups), 1)
        self.assertEqual(len(window.geometry.shapes), 2)


class TestTwoEllipses(unittest.TestCase):
    def setUp(self):
        window.open_file(filename="../tests/two-ellipses.dxf")

    def test_geometry_count(self):
        self.assertEqual(len(window.geometry.parts), 1)
        self.assertEqual(len(window.geometry.groups), 1)
        self.assertEqual(len(window.geometry.shapes), 2)


# class TestTwoSplines(unittest.TestCase):
#     def setUp(self):
#         window.open_file(filename="../tests/two-splines.dxf")

#     def test_geometry_count(self):
#         self.assertEqual(len(window.geometry.parts), 1)
#         self.assertEqual(len(window.geometry.groups), 1)
#         self.assertEqual(len(window.geometry.shapes), 2)


if __name__ == '__main__':
    unittest.main()
