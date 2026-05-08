
from __future__ import annotations
import sys

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QMainWindow, QWidget

from .left_panel import LeftPanel
from .right_panel import RightPanel
from .settings_panel import SettingsPanel

class MainWindow(QMainWindow):

    MINIMUM_WIDTH: int = 1350
    MINIMUM_HEIGHT: int = 600

    recognize_requested = pyqtSignal()
    clear_requested = pyqtSignal()
    train_mode_toggled = pyqtSignal(bool)
    save_sample_requested = pyqtSignal(str)

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Handwriting Recognition System")
        self.setMinimumSize(self.MINIMUM_WIDTH, self.MINIMUM_HEIGHT)
        self._build_ui()
        self._connect_signals()

    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.left_panel = LeftPanel()
        self.right_panel = RightPanel()
        self.settings_panel = SettingsPanel()

        layout.addWidget(self.left_panel)
        layout.addWidget(self.right_panel)
        layout.addWidget(self.settings_panel)

    def _connect_signals(self) -> None:

        self.left_panel.recognize_requested.connect(self.recognize_requested)
        self.left_panel.clear_requested.connect(self.clear_requested)
        self.left_panel.train_mode_toggled.connect(self.train_mode_toggled)
        self.left_panel.save_sample_requested.connect(self.save_sample_requested)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
