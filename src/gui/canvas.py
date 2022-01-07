# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QGraphicsItem, QGraphicsView, QRubberBand, QGraphicsScene, QGraphicsLineItem
from PyQt5.QtGui import QPainterPath, QPen, QColor, QPainterPathStroker, QMouseEvent
from PyQt5 import QtCore


def Canvas(parent=None):
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
            print("CanvasBase QMouseEvent")
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
    This is the used Canvas to print the graphical interface of dxf2gcode.
    All GUI things should be performed in the View and plotting functions in
    the scene
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

        # self.setDragMode(QGraphicsView.RubberBandDrag )
        self.setDragMode(QGraphicsView.NoDrag)

        self.parent = parent
        self.mppos = None

        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.prvRectRubberBand = QtCore.QRect()

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
        position = self.mapToGlobal(event.pos())
        GVPos = self.mapToScene(event.pos())
        real_pos = Point(GVPos.x(), -GVPos.y())

        menu = MyDropDownMenu(self.scene(), position, real_pos)

    def wheelEvent(self, event):
        """
        With Mouse Wheel the object is scaled
        @purpose: Scale by mouse wheel
        @param event: Event Parameters passed to function
        """
        delta = event.angleDelta().y()
        scale = (1000 + delta) / 1000.0
        self.scale(scale, scale)

    def mousePressEvent(self, event):
        """
        Right Mouse click shall have no function, Therefore pass only left
        click event
        @purpose: Change inherited mousePressEvent
        @param event: Event Parameters passed to function
        """
        if event.button() == QtCore.Qt.MidButton:
            self.setDragMode(QGraphicsView.ScrollHandDrag)
            self.original_event = event
            handmade_event = QMouseEvent(QtCore.QEvent.MouseButtonPress,QtCore.QPointF(event.pos()),QtCore.Qt.LeftButton,event.buttons(),QtCore.Qt.KeyboardModifiers())
            self.mousePressEvent(handmade_event)
            super(MyGraphicsView, self).mousePressEvent(event)
        if self.dragMode() == 1:
            super(MyGraphicsView, self).mousePressEvent(event)
        elif event.button() == QtCore.Qt.LeftButton:
            self.mppos = event.pos()
        else:
            pass

    def mouseReleaseEvent(self, event):
        """
        Right Mouse click shall have no function, Therefore pass only left
        click event
        @purpose: Change inherited mousePressEvent
        @param event: Event Parameters passed to function
        """
        delta = 2

        if event.button() == QtCore.Qt.MidButton:
            self.setDragMode(QGraphicsView.NoDrag)

        if self.dragMode() == 1:
            # if (event.key() == QtCore.Qt.Key_Shift):
            # self.setDragMode(QGraphicsView.NoDrag)
            super(MyGraphicsView, self).mouseReleaseEvent(event)

        # Selection only enabled for left Button
        elif event.button() == QtCore.Qt.LeftButton:
            self.currentItems = []
            scene = self.scene()
            if scene and not self.isMultiSelect:
                for item in scene.selectedItems():
                    item.setSelected(False, False)
            # If the mouse button is pressed without movement of rubberband
            if self.rubberBand.isHidden():
                rect = QtCore.QRect(event.pos().x()-delta,
                                    event.pos().y() - delta,
                                    2 * delta, 2*delta)
                # logger.debug(rect)

                point = self.mapToScene(event.pos())
                min_distance = float(0x7fffffff)
                for item in self.items(rect):
                    itemDistance = item.contains_point(point)
                    if itemDistance < min_distance:
                        min_distance = itemDistance
                        self.currentItems = item
                if self.currentItems:
                    if self.currentItems.isSelected():
                        self.currentItems.setSelected(False, False)
                    else:
                        self.currentItems.setSelected(True, False)
            else:
                rect = self.rubberBand.geometry()
                self.currentItems = self.items(rect)
                self.rubberBand.hide()
                # logger.debug("Rubberband Selection")

                # All items in the selection
                # self.currentItems = self.items(rect)
                # print self.currentItems
                # logger.debug(rect)

                for item in self.currentItems:
                    if item.isSelected():
                        item.setSelected(False, False)
                    else:
                        # print (item.flags())
                        item.setSelected(True, False)

        else:
            pass

        self.mppos = None
        # super(MyGraphicsView, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        """
        MouseMoveEvent of the Graphiscview. May also be used for the Statusbar.
        @purpose: Get the MouseMoveEvent and use it for the Rubberband Selection
        @param event: Event Parameters passed to function
        """
        if self.mppos is not None:
            Point = event.pos() - self.mppos
            if Point.manhattanLength() > 3:
                # print 'the mouse has moved more than 3 pixels since the oldPosition'
                # print "Mouse Pointer is currently hovering at: ", event.pos()
                rect = QtCore.QRect(self.mppos, event.pos())
                '''
                The following is needed because of PyQt5 doesn't like to switch from sign
                 it will keep displaying last rectangle, i.e. you can end up will multiple rectangles
                '''
                if self.prvRectRubberBand.width() > 0 and not rect.width() > 0 or rect.width() == 0 or\
                   self.prvRectRubberBand.height() > 0 and not rect.height() > 0 or rect.height() == 0:
                    self.rubberBand.hide()
                self.rubberBand.setGeometry(rect.normalized())
                self.rubberBand.show()
                self.prvRectRubberBand = rect

        scpoint = self.mapToScene(event.pos())

        # self.setStatusTip('X: %3.1f; Y: %3.1f' % (scpoint.x(), -scpoint.y()))
        # works not as supposed to
        self.setToolTip('X: %3.1f; Y: %3.1f' %(scpoint.x(), -scpoint.y()))

        super(MyGraphicsView, self).mouseMoveEvent(event)

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
    This is the Canvas used to print the graphical interface of dxf2gcode.
    The Scene is rendered into the previously defined mygraphicsView class.
    All performed plotting functions should be defined here.
    @sideeffect: None
    """
    def __init__(self):
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

    def repaint_shape(self, shape):
        # setParentItem(None) might let it crash, hence we rely on the garbage collector
        shape.stmove.hide()
        shape.starrow.hide()
        shape.enarrow.hide()
        del shape.stmove
        del shape.starrow
        del shape.enarrow
        self.paint_shape(shape)
        if not shape.isSelected():
            shape.stmove.hide()
            shape.starrow.hide()
            shape.enarrow.hide()

    def paint_shape(self, shape):
        """
        Create all plotting related parts of one shape.
        @param shape: The shape to be plotted.
        """
        start, start_ang = shape.get_start_end_points(True, True)
        shape.path = QPainterPath()
        shape.path.moveTo(start.x, -start.y)
        drawHorLine = lambda caller, start, end: shape.path.lineTo(end.x, -end.y)
        drawVerLine = lambda caller, start: None  # Not used in 2D mode
        shape.make_path(drawHorLine, drawVerLine)

        self.BB = self.BB.joinBB(shape.BB)

        shape.stmove = self.createstmove(shape)
        shape.starrow = self.createstarrow(shape)
        shape.enarrow = self.createenarrow(shape)
        shape.stmove.setParentItem(shape)
        shape.starrow.setParentItem(shape)
        shape.enarrow.setParentItem(shape)

    def draw_wp_zero(self):
        """
        This function is called while the drawing of all items is done. It plots
        the WPZero to the Point x=0 and y=0. This item will be enabled or
        disabled to be shown or not.
        """
        self.wpzero = WpZero(QtCore.QPointF(0, 0))
        self.addItem(self.wpzero)

    def createstarrow(self, shape):
        """
        This function creates the Arrows at the end point of a shape when the
        shape is selected.
        @param shape: The shape for which the Arrow shall be created.
        """

        length = 20
        start, start_ang = shape.get_start_end_points_physical(True, True)
        arrow = Arrow(startp=start,
                      length=length,
                      angle=start_ang,
                      color=QColor(50, 200, 255),
                      pencolor=QColor(50, 100, 255))
        return arrow

    def createenarrow(self, shape):
        """
        This function creates the Arrows at the end point of a shape when the
        shape is selected.
        @param shape: The shape for which the Arrow shall be created.
        """
        length = 20
        end, end_ang = shape.get_start_end_points_physical(False, True)
        arrow = Arrow(startp=end,
                      length=length,
                      angle=end_ang,
                      color=QColor(0, 245, 100),
                      pencolor=QColor(0, 180, 50),
                      startarrow=False)
        return arrow

    def createstmove(self, shape):
        """
        This function creates the Additional Start and End Moves in the plot
        window when the shape is selected
        @param shape: The shape for which the Move shall be created.
        """
        stmove = StMoveGUI(shape)
        return stmove

    def delete_opt_paths(self):
        """
        This function deletes all the plotted export routes.
        """
        # removeItem might let it crash, hence we rely on the garbage collector
        while self.routearrows:
            item = self.routearrows.pop()
            item.hide()
            del item

        while self.routetext:
            item = self.routetext.pop()
            item.hide()
            del item

    def addexproutest(self):
        self.expprv = Point(g.config.vars.Plane_Coordinates['axis1_start_end'],
                            g.config.vars.Plane_Coordinates['axis2_start_end'])
        self.expcol = QtCore.Qt.darkRed

    def addexproute(self, exp_order, layer_nr):
        """
        This function initialises the Arrows of the export route order and its numbers.
        """
        for shape_nr in range(len(exp_order)):
            shape = self.shapes[exp_order[shape_nr]]
            st = self.expprv
            en, self.expprv = shape.get_start_end_points_physical()
            self.routearrows.append(Arrow(startp=en,
                                          endp=st,
                                          color=self.expcol,
                                          pencolor=self.expcol))

            self.expcol = QtCore.Qt.darkGray

            self.routetext.append(RouteText(text=("%s,%s" % (layer_nr, shape_nr+1)),
                                            startp=en))
            # self.routetext[-1].ItemIgnoresTransformations

            self.addItem(self.routearrows[-1])
            self.addItem(self.routetext[-1])

    def addexprouteen(self):
        st = self.expprv
        en = Point(g.config.vars.Plane_Coordinates['axis1_start_end'],
                   g.config.vars.Plane_Coordinates['axis2_start_end'])
        self.expcol = QtCore.Qt.darkRed

        self.routearrows.append(Arrow(startp=en,
                                      endp=st,
                                      color=self.expcol,
                                      pencolor=self.expcol))

        self.addItem(self.routearrows[-1])

    def setShowDisabledPaths(self, flag):
        """
        This function is called by the Main Menu and is passed from Main to
        MyGraphicsView to the Scene. It performs the showing or hiding
        of enabled/disabled shapes.

        @param flag: This flag is true if hidden paths shall be shown
        """
        self.showDisabledPaths = flag

        for shape in self.shapes:
            if flag and shape.isDisabled():
                shape.show()
            elif not flag and shape.isDisabled():
                shape.hide()
