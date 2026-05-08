
from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QCheckBox,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ui.canvas_widget import CanvasWidget

class LeftPanel(QWidget):

    FIXED_WIDTH: int = 300

    recognize_requested = pyqtSignal()
    clear_requested = pyqtSignal()
    train_mode_toggled = pyqtSignal(bool)
    save_sample_requested = pyqtSignal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setFixedWidth(self.FIXED_WIDTH)
        self._build_ui()
        self._connect_internal_signals()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        self.canvas = CanvasWidget()
        self.canvas.setObjectName("canvas_widget")
        layout.addWidget(self.canvas)

        self._btn_recognize = QPushButton("Recognize")
        self._btn_recognize.setObjectName("btn_recognize")
        layout.addWidget(self._btn_recognize)

        self._btn_clear = QPushButton("Clear")
        self._btn_clear.setObjectName("btn_clear")
        layout.addWidget(self._btn_clear)

        self._chk_train_mode = QCheckBox("Train Mode")
        self._chk_train_mode.setObjectName("chk_train_mode")
        layout.addWidget(self._chk_train_mode)

        self._lbl_label = QLabel("Character Label:")
        layout.addWidget(self._lbl_label)

        self._txt_label = QLineEdit()
        self._txt_label.setObjectName("txt_label")
        self._txt_label.setPlaceholderText("Enter character label…")
        self._txt_label.setEnabled(False)
        layout.addWidget(self._txt_label)

        self._btn_save_sample = QPushButton("Save Sample")
        self._btn_save_sample.setObjectName("btn_save_sample")
        self._btn_save_sample.setEnabled(False)
        layout.addWidget(self._btn_save_sample)

        self._lbl_library = QLabel("Template Library:")
        layout.addWidget(self._lbl_library)

        self._lst_templates = QListWidget()
        self._lst_templates.setObjectName("lst_templates")
        layout.addWidget(self._lst_templates)

        layout.addStretch()

    def _connect_internal_signals(self) -> None:

        self._btn_recognize.clicked.connect(self.recognize_requested)

        self._btn_clear.clicked.connect(self.canvas.clear_canvas)
        self._btn_clear.clicked.connect(self.clear_requested)
        self._chk_train_mode.toggled.connect(self._on_train_mode_toggled)
        self._btn_save_sample.clicked.connect(self._on_save_sample_clicked)

    def _on_train_mode_toggled(self, active: bool) -> None:

        self._txt_label.setEnabled(active)
        self._btn_save_sample.setEnabled(active)
        self.train_mode_toggled.emit(active)

    def _on_save_sample_clicked(self) -> None:
        label = self._txt_label.text().strip()
        self.save_sample_requested.emit(label)

    @property
    def is_train_mode_active(self) -> bool:
        return self._chk_train_mode.isChecked()

    @property
    def label_input_text(self) -> str:
        return self._txt_label.text()

    @property
    def label_input_enabled(self) -> bool:
        return self._txt_label.isEnabled()

    @property
    def save_sample_enabled(self) -> bool:
        return self._btn_save_sample.isEnabled()
