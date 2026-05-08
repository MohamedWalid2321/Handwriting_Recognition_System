
from __future__ import annotations

import settings
from cv.grayscale import to_grayscale
from cv.gaussian import smooth
from cv.otsu import apply_otsu_threshold
from cv.morphology import apply_opening, apply_closing, create_structuring_element
from cv.connected_components import apply_connected_components
from recognition.features import extract_features
from recognition.normalization import FeatureNormalizer
from recognition.recognizer import recognize
from persistence.training import TrainingManager
from pipeline.state import PipelineState

def _largest_component_id(labels: list[list[int]]) -> int:

    counts: dict[int, int] = {}
    for row in labels:
        for cell in row:
            if cell != 0:
                counts[cell] = counts.get(cell, 0) + 1
    if not counts:
        return 0
    best_id = 0
    best_count = 0
    for label_id, count in counts.items():
        if count > best_count:
            best_count = count
            best_id = label_id
    return best_id

class PipelineController:

    def __init__(self) -> None:
        self.training_manager = TrainingManager()
        self.training_manager.load_from_disk()

    def run(self, pixels: list[list[tuple[int, int, int]]]) -> PipelineState:

        if not pixels or not pixels[0]:
            raise ValueError("pixels must be a non-empty grid")

        height = len(pixels)
        width = len(pixels[0])

        if height != settings.CANVAS_SIZE or width != settings.CANVAS_SIZE:
            raise ValueError(
                f"pixels must be {settings.CANVAS_SIZE}×{settings.CANVAS_SIZE}, "
                f"got {height}×{width}"
            )

        raw_pixels = pixels

        grayscale = to_grayscale(raw_pixels)

        smoothed = smooth(grayscale, settings.KERNEL_SIZE, settings.GAUSSIAN_SIGMA)

        binary = apply_otsu_threshold(smoothed)

        se = create_structuring_element(settings.STRUCTURING_ELEMENT_SIZE)
        morphed = apply_closing(apply_opening(binary, se), se)

        labels, _areas = apply_connected_components(morphed, settings.MIN_COMPONENT_AREA)

        target_id = _largest_component_id(labels)
        raw_feature_vector = extract_features(labels, target_id)

        normalizer = self.training_manager.normalizer
        feature_vector = normalizer.normalize(raw_feature_vector)

        normalized_library: dict[str, list[list[float]]] = {}
        for label, raw_vectors in self.training_manager.library.items():
            normalized_library[label] = [
                normalizer.normalize(v) for v in raw_vectors
            ]

        result = recognize(feature_vector, normalized_library)
        prediction = result["best"]
        confidence = result["confidence"]
        runner_up = result["runner_up"]

        return PipelineState(
            raw_pixels=raw_pixels,
            grayscale=grayscale,
            smoothed=smoothed,
            binary=binary,
            morphed=morphed,
            labels=labels,
            feature_vector=feature_vector,
            prediction=prediction,
            confidence=confidence,
            runner_up=runner_up,
        )

    def save_sample(self, label: str, pixels: list[list[tuple[int, int, int]]]) -> bool:

        if not pixels or not pixels[0]:
            return False

        grayscale = to_grayscale(pixels)
        smoothed = smooth(grayscale, settings.KERNEL_SIZE, settings.GAUSSIAN_SIGMA)
        binary = apply_otsu_threshold(smoothed)
        se = create_structuring_element(settings.STRUCTURING_ELEMENT_SIZE)
        morphed = apply_closing(apply_opening(binary, se), se)
        labels, _areas = apply_connected_components(morphed, settings.MIN_COMPONENT_AREA)
        target_id = _largest_component_id(labels)
        raw_features = extract_features(labels, target_id)

        return self.training_manager.save_sample(label, raw_features)
