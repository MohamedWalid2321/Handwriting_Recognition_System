
from __future__ import annotations

import settings
from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QColor, QImage, QPainter, QPen
from PyQt6.QtWidgets import QWidget

class CanvasWidget(QWidget):

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._size = settings.CANVAS_SIZE
        self.setFixedSize(self._size, self._size)
        self._drawing: bool = False
        self._last_point: QPoint = QPoint()
        self._init_image()

    def _init_image(self) -> None:

        self._image = QImage(
            self._size, self._size, QImage.Format.Format_RGB32
        )
        self._image.fill(QColor(255, 255, 255))

    def paintEvent(self, event) -> None:

        painter = QPainter(self)
        painter.drawImage(0, 0, self._image)

    def mousePressEvent(self, event) -> None:

        if event.button() == Qt.MouseButton.LeftButton:
            self._drawing = True
            self._last_point = event.position().toPoint()

            self._draw_line(self._last_point, self._last_point)
            self.update()

    def mouseMoveEvent(self, event) -> None:

        if self._drawing and (event.buttons() & Qt.MouseButton.LeftButton):
            current_point = event.position().toPoint()
            self._draw_line(self._last_point, current_point)
            self._last_point = current_point
            self.update()

    def mouseReleaseEvent(self, event) -> None:

        if event.button() == Qt.MouseButton.LeftButton:
            self._drawing = False

    def _draw_line(self, start: QPoint, end: QPoint) -> None:

        painter = QPainter(self._image)
        r, g, b = settings.PEN_COLOR
        pen = QPen(
            QColor(r, g, b),
            settings.PEN_WIDTH,
            Qt.PenStyle.SolidLine,
            Qt.PenCapStyle.RoundCap,
            Qt.PenJoinStyle.RoundJoin,
        )
        painter.setPen(pen)
        painter.drawLine(start, end)
        painter.end()

    def clear_canvas(self) -> None:

        self._image.fill(QColor(255, 255, 255))
        self.update()

    def export_pixels(self) -> list[list[tuple[int, int, int]]]:

        grid: list[list[tuple[int, int, int]]] = []
        for y in range(self._size):
            row: list[tuple[int, int, int]] = []
            for x in range(self._size):
                colour = self._image.pixelColor(x, y)
                row.append((colour.red(), colour.green(), colour.blue()))
            grid.append(row)
        return grid
