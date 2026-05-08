
from __future__ import annotations

import settings
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QColorDialog,
    QDoubleSpinBox,
    QFrame,
    QGridLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpinBox,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

class _ColorButton(QPushButton):

    color_changed = pyqtSignal(tuple)

    def __init__(self, color: tuple[int, int, int], parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedHeight(28)
        self._color = color
        self._update_swatch()
        self.clicked.connect(self._pick_color)

    def _update_swatch(self) -> None:
        r, g, b = self._color
        self.setText(f"  rgb({r}, {g}, {b})")
        self.setStyleSheet(
            f"QPushButton {{"
            f"  background-color: rgb({r},{g},{b});"
            f"  color: {'black' if (r * 299 + g * 587 + b * 114) / 1000 > 128 else 'white'};"
            f"  border: 2px solid #555;"
            f"  border-radius: 4px;"
            f"  text-align: left;"
            f"  padding-left: 6px;"
            f"}}"
        )

    def _pick_color(self) -> None:
        r, g, b = self._color
        chosen = QColorDialog.getColor(QColor(r, g, b), self, "Choose Pen Color")
        if chosen.isValid():
            self._color = (chosen.red(), chosen.green(), chosen.blue())
            self._update_swatch()
            self.color_changed.emit(self._color)

    @property
    def color(self) -> tuple[int, int, int]:
        return self._color

class SettingsPanel(QWidget):

    PANEL_WIDTH: int = 300

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedWidth(self.PANEL_WIDTH)
        self._collapsed = False
        self._build_ui()
        self._connect_signals()

    def _build_ui(self) -> None:
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        header = QFrame()
        header.setObjectName("settings_header")
        header.setStyleSheet(
            "QFrame#settings_header {"
            "  background: qlineargradient(x1:0, y1:0, x2:0, y2:1,"
            "    stop:0 #f0f4f8, stop:1 #e2e8f0);"
            "  border-bottom: 1px solid #cbd5e1;"
            "}"
        )
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(8, 6, 8, 6)

        self._toggle_btn = QToolButton()
        self._toggle_btn.setObjectName("settings_toggle_btn")
        self._toggle_btn.setText("⚙  Settings ▾")
        self._toggle_btn.setCheckable(True)
        self._toggle_btn.setChecked(True)
        self._toggle_btn.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self._toggle_btn.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextOnly)
        self._toggle_btn.setStyleSheet(
            "QToolButton {"
            "  color: #1e3a5f;"
            "  font-weight: bold;"
            "  font-size: 13px;"
            "  text-align: left;"
            "  background: transparent;"
            "  border: none;"
            "  padding: 2px 4px;"
            "}"
            "QToolButton:hover { color: #2563eb; }"
        )
        header_layout.addWidget(self._toggle_btn)
        outer.addWidget(header)

        self._body = QFrame()
        self._body.setObjectName("settings_body")
        self._body.setStyleSheet(
            "QFrame#settings_body {"
            "  background: #ffffff;"
            "  border-right: 1px solid #cbd5e1;"
            "}"
        )
        body_layout = QVBoxLayout(self._body)
        body_layout.setContentsMargins(12, 10, 12, 10)
        body_layout.setSpacing(8)

        grid = QGridLayout()
        grid.setColumnStretch(1, 1)
        grid.setHorizontalSpacing(10)
        grid.setVerticalSpacing(8)
        row = 0

        def _section(title: str) -> None:
            nonlocal row
            sep = QLabel(title)
            sep.setStyleSheet(
                "color: #2563eb; font-size: 11px; font-weight: bold;"
                " padding-top: 6px;"
            )
            grid.addWidget(sep, row, 0, 1, 3)
            row += 1

        def _label(text: str) -> QLabel:
            lbl = QLabel(text)
            lbl.setStyleSheet("color: #374151; font-size: 12px;")
            return lbl

        def _range_label(text: str) -> QLabel:
            lbl = QLabel(text)
            lbl.setStyleSheet("color: #9ca3af; font-size: 10px;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            return lbl

        _section("── Canvas ──────────────────────────")

        self._spin_pen_width = QSpinBox()
        self._spin_pen_width.setObjectName("spin_pen_width")
        self._spin_pen_width.setRange(4, 60)
        self._spin_pen_width.setValue(settings.PEN_WIDTH)
        self._spin_pen_width.setSuffix(" px")
        _style_spin(self._spin_pen_width)
        grid.addWidget(_label("Pen Width"), row, 0)
        grid.addWidget(self._spin_pen_width, row, 1)
        grid.addWidget(_range_label("[4–60]"), row, 2)
        row += 1

        self._btn_pen_color = _ColorButton(settings.PEN_COLOR)
        self._btn_pen_color.setObjectName("btn_pen_color")
        grid.addWidget(_label("Pen Color"), row, 0)
        grid.addWidget(self._btn_pen_color, row, 1, 1, 2)
        row += 1

        _section("── Gaussian Smoothing ───────────────")

        self._spin_sigma = QDoubleSpinBox()
        self._spin_sigma.setObjectName("spin_sigma")
        self._spin_sigma.setRange(0.5, 5.0)
        self._spin_sigma.setSingleStep(0.1)
        self._spin_sigma.setDecimals(2)
        self._spin_sigma.setValue(settings.GAUSSIAN_SIGMA)
        _style_spin(self._spin_sigma)
        grid.addWidget(_label("Gaussian Sigma"), row, 0)
        grid.addWidget(self._spin_sigma, row, 1)
        grid.addWidget(_range_label("[0.5–5.0]"), row, 2)
        row += 1

        self._spin_kernel = QSpinBox()
        self._spin_kernel.setObjectName("spin_kernel_size")
        self._spin_kernel.setRange(3, 15)
        self._spin_kernel.setSingleStep(2)
        self._spin_kernel.setValue(settings.KERNEL_SIZE)
        self._spin_kernel.setSuffix(" (odd)")
        _style_spin(self._spin_kernel)
        grid.addWidget(_label("Kernel Size"), row, 0)
        grid.addWidget(self._spin_kernel, row, 1)
        grid.addWidget(_range_label("[3–15]"), row, 2)
        row += 1

        _section("── Morphology ───────────────────────")

        self._spin_struct = QSpinBox()
        self._spin_struct.setObjectName("spin_struct_size")
        self._spin_struct.setRange(2, 100)
        self._spin_struct.setValue(settings.STRUCTURING_ELEMENT_SIZE)
        self._spin_struct.setSuffix(" px")
        _style_spin(self._spin_struct)
        grid.addWidget(_label("Struct. Element Size"), row, 0)
        grid.addWidget(self._spin_struct, row, 1)
        grid.addWidget(_range_label("[2–100]"), row, 2)
        row += 1

        _section("── Connected Components ─────────────")

        self._spin_min_area = QSpinBox()
        self._spin_min_area.setObjectName("spin_min_area")
        self._spin_min_area.setRange(10, 500)
        self._spin_min_area.setValue(settings.MIN_COMPONENT_AREA)
        self._spin_min_area.setSuffix(" px²")
        _style_spin(self._spin_min_area)
        grid.addWidget(_label("Min Component Area"), row, 0)
        grid.addWidget(self._spin_min_area, row, 1)
        grid.addWidget(_range_label("[10–500]"), row, 2)
        row += 1

        body_layout.addLayout(grid)

        self._lbl_status = QLabel("")
        self._lbl_status.setObjectName("settings_status_label")
        self._lbl_status.setWordWrap(True)
        self._lbl_status.setStyleSheet("color: #16a34a; font-size: 11px;")
        body_layout.addWidget(self._lbl_status)

        body_layout.addStretch()
        outer.addWidget(self._body)
        outer.addStretch()

    def _connect_signals(self) -> None:
        self._toggle_btn.toggled.connect(self._on_toggle)

        self._spin_pen_width.valueChanged.connect(self._apply_pen_width)
        self._btn_pen_color.color_changed.connect(self._apply_pen_color)
        self._spin_sigma.valueChanged.connect(self._apply_sigma)
        self._spin_kernel.valueChanged.connect(self._apply_kernel_size)
        self._spin_struct.valueChanged.connect(self._apply_struct_size)
        self._spin_min_area.valueChanged.connect(self._apply_min_area)

    def _on_toggle(self, checked: bool) -> None:
        self._body.setVisible(checked)
        arrow = "▾" if checked else "▸"
        self._toggle_btn.setText(f"⚙  Settings {arrow}")

    def _show_status(self, msg: str, ok: bool = True) -> None:
        color = "#16a34a" if ok else "#dc2626"
        self._lbl_status.setStyleSheet(f"color: {color}; font-size: 11px;")
        self._lbl_status.setText(msg)

    def _apply_pen_width(self, value: int) -> None:
        settings.PEN_WIDTH = value
        self._show_status(f"PEN_WIDTH = {value} px")

    def _apply_pen_color(self, color: tuple) -> None:
        settings.PEN_COLOR = color
        r, g, b = color
        self._show_status(f"PEN_COLOR = rgb({r}, {g}, {b})")

    def _apply_sigma(self, value: float) -> None:
        settings.GAUSSIAN_SIGMA = value
        self._show_status(f"GAUSSIAN_SIGMA = {value:.2f}")

    def _apply_kernel_size(self, value: int) -> None:

        if value % 2 == 0:
            value = value + 1 if value < 15 else value - 1
            self._spin_kernel.blockSignals(True)
            self._spin_kernel.setValue(value)
            self._spin_kernel.blockSignals(False)
        settings.KERNEL_SIZE = value
        self._show_status(f"KERNEL_SIZE = {value}")

    def _apply_struct_size(self, value: int) -> None:
        settings.STRUCTURING_ELEMENT_SIZE = value
        self._show_status(f"STRUCTURING_ELEMENT_SIZE = {value}")

    def _apply_min_area(self, value: int) -> None:
        settings.MIN_COMPONENT_AREA = value
        self._show_status(f"MIN_COMPONENT_AREA = {value} px²")

def _style_spin(spin: QSpinBox | QDoubleSpinBox) -> None:

    spin.setStyleSheet(
        "QSpinBox, QDoubleSpinBox {"
        "  background: #f8fafc;"
        "  color: #1e293b;"
        "  border: 1px solid #cbd5e1;"
        "  border-radius: 4px;"
        "  padding: 2px 4px;"
        "  font-size: 12px;"
        "}"
        "QSpinBox:focus, QDoubleSpinBox:focus {"
        "  border: 1px solid #2563eb;"
        "}"
        "QSpinBox::up-button, QDoubleSpinBox::up-button,"
        "QSpinBox::down-button, QDoubleSpinBox::down-button {"
        "  background: #e2e8f0;"
        "  border: none;"
        "  width: 16px;"
        "}"
    )
