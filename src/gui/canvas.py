# -*- coding: utf-8 -*-

from core.boundingbox import BoundingBox

from PyQt5.QtWidgets import QGraphicsItem, QGraphicsView, QRubberBand, QGraphicsScene, QGraphicsLineItem
from PyQt5.QtGui import QPainterPath, QPen, QColor, QPainterPathStroker, QMouseEvent
from PyQt5 import QtCore


def Canvas(parent=None):
    """
    Called by vsplasma_ui.py to create ui.canvasView, which then becomes
    self.ui.canvas in vsplasma.py.
    """
    return MyGraphicsView(parent)


class CanvasBase(QGraphicsView):
    def __init__(self, parent=None):
        super(CanvasBase, self).__init__(parent)

        self.isPanning = False
        self.isRotating = False
        self.isMultiSelect = False

        self.setMouseTracking (True)

    def updateModifiers(self, event):
        """
        Handle all canvas keyboard modifiers in one place.
        """

        if type (event) == QMouseEvent:
            buttons = event.buttons()
        else:
            buttons = QApplication.mouseButtons()

        if type (event) == QKeyEvent:
            modifiers = event.modifiers()
        else:
            modifiers = QApplication.keyboardModifiers()

        # allow only clean modifiers, no combos
        wantMultiSelect = (modifiers == Qt.ControlModifier)
        self.isMultiSelect = wantMultiSelect and ((buttons == Qt.NoButton) or (buttons == Qt.LeftButton))
        wantPanning = (modifiers == Qt.ShiftModifier)
        self.isPanning = wantPanning and (buttons == Qt.LeftButton)
        wantRotating = (modifiers == Qt.AltModifier)
        self.isRotating = wantRotating and (buttons == Qt.LeftButton)

        if self.isPanning or self.isRotating:
            self.setCursor(Qt.ClosedHandCursor)
            print("CANVAS.PY -> IS PANNING")
        elif wantPanning:
            self.setCursor(Qt.OpenHandCursor)
            print("CANVAS.PY -> WANT PANNING")
        elif wantRotating:
            self.setCursor(Qt.PointingHandCursor)
        elif wantMultiSelect:
            self.setCursor(Qt.CrossCursor)
        else:
            self.unsetCursor()


class MyGraphicsView(CanvasBase):
    """
    The QGraphicsView class provides a widget for displaying the contents of
    a QGraphicsScene.

    MyGraphicsView controls the UI.
    MyGraphicsScene controls the canvas rendering.
    """

    def __init__(self, parent=None):
        """
        Initialisation of the View Object. This is called by the gui created
        with the QTDesigner.
        @param parent: Main is passed as a pointer for reference.
        """
        super(MyGraphicsView, self).__init__(parent)
        self.currentItem = None

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)

        self.parent = parent

    def tr(self, string_to_translate):
        """
        Translate a string using the QCoreApplication translation framework
        @param string_to_translate: a unicode string
        @return: the translated unicode string if it was possible to translate
        """
        return str(QtCore.QCoreApplication.translate('MyGraphicsView',
                                                           string_to_translate))

    def contextMenuEvent(self, event):
        """
        Create the contextmenu.
        @purpose: Links the new Class of ContextMenu to Graphicsview.
        """
        pass

    def wheelEvent(self, event):
        """
        With Mouse Wheel the object is scaled
        @purpose: Scale by mouse wheel
        @param event: Event Parameters passed to function
        """
        delta = event.angleDelta().y()
        scale = (1000 + delta) / 1000.0
        self.scale(scale, scale)

    # def mousePressEvent(self, event):
    #     """
    #     Right Mouse click shall have no function, Therefore pass only left
    #     click event
    #     @purpose: Change inherited mousePressEvent
    #     @param event: Event Parameters passed to function
    #     """
    #     event.ignore()
    #     print("mousePressEvent VIEW", event)
    #     if event.button() == QtCore.Qt.MidButton:
    #         self.setDragMode(QGraphicsView.ScrollHandDrag)
    #         # self.original_event = event
    #         # handmade_event = QMouseEvent(QtCore.QEvent.MouseButtonPress,QtCore.QPointF(event.pos()),QtCore.Qt.LeftButton,event.buttons(),QtCore.Qt.KeyboardModifiers())
    #         # self.mousePressEvent(handmade_event)
    #         # super(MyGraphicsView, self).mousePressEvent(event)


    def mouseReleaseEvent(self, event):
        """
        Right Mouse click shall have no function, Therefore pass only left
        click event
        @purpose: Change inherited mousePressEvent
        @param event: Event Parameters passed to function
        """
        if event.button() == QtCore.Qt.MidButton:
            self.setDragMode(QGraphicsView.NoDrag)

        if self.dragMode() == 1:
            # if (event.key() == QtCore.Qt.Key_Shift):
            # self.setDragMode(QGraphicsView.NoDrag)
            super(MyGraphicsView, self).mouseReleaseEvent(event)

        # Selection only enabled for left Button
        elif event.button() == QtCore.Qt.LeftButton:
            self.currentItems = []

    def mouseMoveEvent(self, event):
        """
        MouseMoveEvent of the Graphiscview. May also be used for the Statusbar.
        @purpose: Get the MouseMoveEvent and use it for the Rubberband Selection
        @param event: Event Parameters passed to function
        """
        # How can this set a label in the main window?
        super(MyGraphicsView, self).mouseMoveEvent(event)

        # print(event.pos())
        # print(self.obj_pos_label.text())
        # print(self.parent)
        # print(self.parent.ui)

    def autoscale(self):
        """
        Automatically zooms to the full extend of the current GraphicsScene
        """
        scene = self.scene()
        width = scene.BB.Pe.x - scene.BB.Ps.x
        height = scene.BB.Pe.y - scene.BB.Ps.y
        scext = QtCore.QRectF(scene.BB.Ps.x, -scene.BB.Pe.y, width * 1.05, height * 1.05)
        self.fitInView(scext, QtCore.Qt.KeepAspectRatio)
        logger.debug(self.tr("Autoscaling to extend: %s") % scext)

    def setShowPathDirections(self, flag):
        """
        This function is called by the Main Window from the Menubar.
        @param flag: This flag is true if all Path Direction shall be shown
        """
        scene = self.scene()
        for shape in scene.shapes:
            shape.starrow.setallwaysshow(flag)
            shape.enarrow.setallwaysshow(flag)
            shape.stmove.setallwaysshow(flag)

    def resetAll(self):
        """
        Deletes the existing GraphicsScene.
        """
        scene = self.scene()
        del scene


class MyGraphicsScene(QGraphicsScene):
    """
    The QGraphicsScene class provides a surface for managing a large number of
    2D graphical items.

    MyGraphicsView controls the UI.
    MyGraphicsScene controls the canvas rendering.
    """
    def __init__(self, workpiece=None, machine=None):
        QGraphicsScene.__init__(self)

        self.shapes = []
        self.wpzero = None
        self.routearrows = []
        self.routetext = []
        self.expprv = None
        self.expcol = None
        self.expnr = 0

        self.showDisabledPaths = False

        self.BB = BoundingBox()

        self.draw_machine(machine)
        self.draw_workpiece(workpiece)


    def tr(self, string_to_translate):
        """
        Translate a string using the QCoreApplication translation framework
        @param string_to_translate: a unicode string
        @return: the translated unicode string if it was possible to translate
        """
        return str(QtCore.QCoreApplication.translate('MyGraphicsScene',
                                                           string_to_translate))

    def plotAll(self, shapes):
        """
        Instance is called by the Main Window after the defined file is loaded.
        It generates all ploting functionality. The parameters are generally
        used to scale or offset the base geometry (by Menu in GUI).
        """
        for shape in shapes:
            self.paint_shape(shape)
            self.addItem(shape)
            self.shapes.append(shape)
        self.draw_wp_zero()
        self.update()

    def draw_all(self, mw):
        self.draw_machine(mw.machine)
        self.draw_workpiece(mw.workpiece)
        self.draw_shapes(mw.geometry)
        # self.draw_operations(ui.operations)

    def draw_shapes(self, geometry):
        if not geometry.shapes: # file not opened yet
            return

        for idx, shape in enumerate(geometry.shapes):
            shape.make_path_item(self)
            # shape.paint_shape(self)

    def draw_operations(self, operations):
        pass

    def draw_workpiece(self, workpiece):
        workpiece.draw(self)

    def draw_machine(self, machine):
        machine.draw(self)
