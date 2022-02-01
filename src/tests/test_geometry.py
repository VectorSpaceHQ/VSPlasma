#!/usr/bin/env python3
# Unit tests against the geometry.py classes
import sys
import pytest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
import vsplasma as vsp


def test_basic(qtbot):
    app = QApplication(sys.argv)
    window = vsp.MainWindow(app)
    window.hide()
    qtbot.addWidget(window)

    qtbot.mouseClick(window.actionImport, QtCore.Qt.LeftButton)

    print(window.geometry.parts)

    assert 0
