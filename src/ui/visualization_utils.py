
from __future__ import annotations

from PyQt6.QtGui import QColor, QImage

LABEL_PALETTE: list[tuple[int, int, int]] = [
    (220,  50,  47),
    ( 38, 139,  82),
    ( 38, 139, 210),
    (181, 137,   0),
    (211,  54, 130),
    ( 42, 161, 152),
    (203,  75,  22),
    (108, 113, 196),
]

def grid_to_qimage_grayscale(grid: list[list[int]]) -> QImage:

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    image = QImage(cols, rows, QImage.Format.Format_RGB32)
    for r in range(rows):
        row = grid[r]
        for c in range(cols):
            v = row[c]
            image.setPixelColor(c, r, QColor(v, v, v))
    return image

def grid_to_qimage_binary(grid: list[list[int]]) -> QImage:

    return grid_to_qimage_grayscale(grid)

def grid_to_qimage_labels(grid: list[list[int]]) -> QImage:

    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    palette_len = len(LABEL_PALETTE)
    image = QImage(cols, rows, QImage.Format.Format_RGB32)
    for r in range(rows):
        row = grid[r]
        for c in range(cols):
            label = row[c]
            if label == 0:
                image.setPixelColor(c, r, QColor(255, 255, 255))
            else:
                rgb = LABEL_PALETTE[(label - 1) % palette_len]
                image.setPixelColor(c, r, QColor(rgb[0], rgb[1], rgb[2]))
    return image
