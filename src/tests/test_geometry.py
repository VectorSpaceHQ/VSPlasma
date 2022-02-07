#!/usr/bin/env python3
# Unit tests against the geometry.py classes
import time
import sys
import pytest

import vsplasma as vsp
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QApplication
from PyQt5.QtCore import QSize

class HelloWindow(QMainWindow):
    configuration_changed = QtCore.pyqtSignal()

    def __init__(self, app):
        QMainWindow.__init__(self)
        self.app = app

        self.setMinimumSize(QSize(640, 480))
        self.setWindowTitle("Hello world - pythonprogramminglanguage.com")

        centralWidget = QWidget(self)
        self.setCentralWidget(centralWidget)

        gridLayout = QGridLayout(self)
        centralWidget.setLayout(gridLayout)

        title = QLabel("Hello World from PyQt", self)
        title.setAlignment(QtCore.Qt.AlignCenter)
        gridLayout.addWidget(title, 0, 0)

        self.title = title


def test_1in_box(qtbot, monkeypatch):
    exit_calls = []

    app = QApplication(sys.argv)
    # app = monkeypatch.setattr(QApplication, "exit", lambda: exit_calls.append(1))

    window = vsp.MainWindow(app)
    # qtbot.waitForWindowShown(window)
    # qtbot.addWidget(window)



    # time.sleep(3)
    # window.open_file()

    # assert len(window.geometry.parts) == 1
    assert 1==1

def test_hello(qtbot):
    widget = HelloWindow(sys.argv)
    qtbot.addWidget(widget)

    assert widget.title.text() == "Hello World from PyQt"


if __name__ == "__main__":
    # app = QtWidgets.QApplication(sys.argv)
    # mainWin = HelloWindow(app)
    # mainWin.show()
    # sys.exit( app.exec_() )

    # app = QApplication(sys.argv)
    # window = vsp.MainWindow(app)
    # window.setWindowTitle('VSPlasma')
    # window.show()
    # sys.exit(app.exec_())
    print("main")
    app = QApplication(sys.argv)

    window = vsp.MainWindow(app)
    window.setWindowTitle('VSPlasma')
    window.setWindowIcon(QIcon('./images/vsp_icon.png'))
    print("main")

    window.show()
    sys.exit(app.exec_())
