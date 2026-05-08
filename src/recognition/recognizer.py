
from __future__ import annotations

import math
from typing import TypedDict

TemplateLibrary = dict[str, list[list[float]]]

class RecognitionResult(TypedDict):

    best: str | None
    runner_up: str | None
    distance: float
    confidence: float

def euclidean_distance(v1: list[float], v2: list[float]) -> float:

    if len(v1) != len(v2):
        raise ValueError(
            f"Feature vector length mismatch: "
            f"input has {len(v1)} elements but template has {len(v2)} elements."
        )

    squared_sum: float = 0.0
    for i in range(len(v1)):
        diff = v1[i] - v2[i]
        squared_sum += diff * diff

    return math.sqrt(squared_sum)

def recognize(
    input_vector: list[float],
    template_library: TemplateLibrary,
) -> RecognitionResult:

    if not template_library:
        return RecognitionResult(
            best=None,
            runner_up=None,
            distance=0.0,
            confidence=0.0,
        )

    candidates: list[tuple[float, str]] = []

    for label, vectors in template_library.items():
        for template_vector in vectors:
            dist = euclidean_distance(input_vector, template_vector)
            candidates.append((dist, label))

    candidates.sort(key=lambda pair: (pair[0], pair[1]))

    best_distance, best_label = candidates[0]

    runner_up_label: str | None = None
    runner_up_distance: float | None = None

    for dist, label in candidates[1:]:
        if label != best_label:
            runner_up_label = label
            runner_up_distance = dist
            break

    if runner_up_distance is None:

        confidence = 0.0
    elif runner_up_distance == 0.0:

        confidence = 0.0
    else:
        confidence = 1.0 - (best_distance / runner_up_distance)

        if confidence < 0.0:
            confidence = 0.0
        if confidence > 1.0:
            confidence = 1.0

    return RecognitionResult(
        best=best_label,
        runner_up=runner_up_label,
        distance=best_distance,
        confidence=confidence,
    )
