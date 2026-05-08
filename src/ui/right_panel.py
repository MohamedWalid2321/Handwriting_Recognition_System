
from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QFrame, QGridLayout, QLabel, QSizePolicy,
    QTextEdit, QVBoxLayout, QWidget,
)

from ui.visualization_utils import (
    grid_to_qimage_grayscale,
    grid_to_qimage_binary,
    grid_to_qimage_labels,
)

_STAGE_NAMES: list[str] = [
    "Grayscale", "Gaussian", "Binary (Otsu)",
    "Morphological", "Labels", "Features",
]

_THUMB_W = 180
_THUMB_H = 135

_GRID_COLS = 2

class RightPanel(QWidget):

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        self._lbl_prediction = QLabel("Prediction: —")
        self._lbl_prediction.setObjectName("lbl_prediction")
        layout.addWidget(self._lbl_prediction)

        self._lbl_confidence = QLabel("Confidence: —")
        self._lbl_confidence.setObjectName("lbl_confidence")
        layout.addWidget(self._lbl_confidence)

        self._lbl_runner_up = QLabel("Runner-up: —")
        self._lbl_runner_up.setObjectName("lbl_runner_up")
        layout.addWidget(self._lbl_runner_up)

        grid = QGridLayout()
        grid.setSpacing(4)
        self._vis_labels: list[QLabel] = []
        for idx, name in enumerate(_STAGE_NAMES):
            safe = name.lower().replace(" ", "_").replace("(", "").replace(")", "")
            lbl = QLabel(name)
            lbl.setObjectName(f"vis_{safe}")
            lbl.setFrameShape(QFrame.Shape.Box)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setMinimumSize(_THUMB_W, _THUMB_H)
            self._vis_labels.append(lbl)
            grid.addWidget(lbl, idx // _GRID_COLS, idx % _GRID_COLS)
        layout.addLayout(grid)

        layout.addWidget(QLabel("Feature Vector:"))
        self._txt_feature_vector = QTextEdit()
        self._txt_feature_vector.setObjectName("txt_feature_vector")
        self._txt_feature_vector.setReadOnly(True)
        self._txt_feature_vector.setMaximumHeight(80)
        self._txt_feature_vector.setPlaceholderText("Feature vector appears here after recognition…")
        layout.addWidget(self._txt_feature_vector)
        layout.addStretch()

    def update_prediction(self, prediction: str | None, confidence: float | None, runner_up: str | None) -> None:
        self._lbl_prediction.setText(f"Prediction: {prediction or '—'}")
        conf_str = f"{confidence:.2%}" if confidence is not None else "—"
        self._lbl_confidence.setText(f"Confidence: {conf_str}")
        self._lbl_runner_up.setText(f"Runner-up: {runner_up or '—'}")

    def update_feature_vector(self, vector: list[float]) -> None:
        self._txt_feature_vector.setPlainText(str(vector))

    def update_visualizations(self, state: object) -> None:

        def _set_thumb(index: int, qimage) -> None:
            pixmap = QPixmap.fromImage(qimage)
            scaled = pixmap.scaled(
                _THUMB_W, _THUMB_H,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            lbl = self._vis_labels[index]
            lbl.setPixmap(scaled)

        grayscale = getattr(state, "grayscale", None)
        smoothed   = getattr(state, "smoothed",   None)
        binary     = getattr(state, "binary",     None)
        morphed    = getattr(state, "morphed",    None)
        labels     = getattr(state, "labels",     None)
        features   = getattr(state, "feature_vector", [])

        if grayscale:
            _set_thumb(0, grid_to_qimage_grayscale(grayscale))
        if smoothed:
            _set_thumb(1, grid_to_qimage_grayscale(smoothed))
        if binary:
            _set_thumb(2, grid_to_qimage_binary(binary))
        if morphed:
            _set_thumb(3, grid_to_qimage_binary(morphed))
        if labels:
            _set_thumb(4, grid_to_qimage_labels(labels))

        if features:
            formatted = ", ".join(f"{v:.4f}" for v in features)
            self._txt_feature_vector.setPlainText(formatted)

            self._vis_labels[5].setText(f"n={len(features)}")

    def clear_visualizations(self) -> None:

        for idx, name in enumerate(_STAGE_NAMES):
            lbl = self._vis_labels[idx]
            lbl.setPixmap(QPixmap())
            lbl.setText(name)

        self._txt_feature_vector.clear()

    def clear_results(self) -> None:

        self._lbl_prediction.setText("Prediction: —")
        self._lbl_confidence.setText("Confidence: —")
        self._lbl_runner_up.setText("Runner-up: —")
        self.clear_visualizations()
