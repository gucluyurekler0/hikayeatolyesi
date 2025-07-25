from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen, QMouseEvent, QColor
from PySide6.QtGui import QPainter, QPen, QColor, QImage

from PySide6.QtCore import Qt, QPoint

class DrawingArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(400, 300)
        self.image = QImage(self.size(), QImage.Format_RGB32)

        self.image.fill(Qt.white)
        self.last_point = QPoint()
        self.drawing = False
        self.pen_color = Qt.black

    def set_pen_color(self, color: QColor):
        self.pen_color = color

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.last_point = event.position().toPoint()
            self.drawing = True

    def mouseMoveEvent(self, event: QMouseEvent):
        if (event.buttons() & Qt.LeftButton) and self.drawing:
            painter = QPainter(self.image)
            pen = QPen(self.pen_color, 3, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
            painter.setPen(pen)
            painter.drawLine(self.last_point, event.position().toPoint())
            self.last_point = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        canvas = QPainter(self)
        canvas.drawImage(self.rect(), self.image, self.image.rect())

    def clear(self):
        self.image.fill(Qt.white)
        self.update()
