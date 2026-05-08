
import os
import sys
import time
from typing import Any

_SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

import settings
from cv.grayscale import to_grayscale
from cv.gaussian import smooth
from cv.otsu import apply_otsu_threshold
from cv.morphology import create_structuring_element, apply_opening
from cv.connected_components import apply_connected_components
from recognition.features import extract_features

def _make_synthetic_stroke(size: int = 400) -> list[list[tuple[int, int, int]]]:

    canvas: list[list[tuple[int, int, int]]] = []
    for row in range(size):
        pixel_row: list[tuple[int, int, int]] = []
        for col in range(size):

            if abs(row - col) <= 5:
                pixel_row.append((0, 0, 0))
            else:
                pixel_row.append((255, 255, 255))
        canvas.append(pixel_row)
    return canvas

def _time_stage(name: str, fn, *args) -> tuple[float, Any]:

    start = time.perf_counter()
    result = fn(*args)
    elapsed = time.perf_counter() - start
    return elapsed, result

def run_profile(canvas_size: int = 400) -> None:

    print(f"\n{'='*52}")
    print(f"  Pipeline Performance Report  ({canvas_size}×{canvas_size} canvas)")
    print(f"{'='*52}")

    timings: list[tuple[str, float]] = []
    total_start = time.perf_counter()

    rgb_canvas = _make_synthetic_stroke(canvas_size)

    elapsed, gray = _time_stage("Grayscale Conversion", to_grayscale, rgb_canvas)
    timings.append(("Grayscale Conversion", elapsed))

    elapsed, smoothed = _time_stage(
        "Gaussian Smoothing",
        smooth,
        gray,
        settings.KERNEL_SIZE,
        settings.GAUSSIAN_SIGMA,
    )
    timings.append(("Gaussian Smoothing  ", elapsed))

    elapsed, binary = _time_stage("Otsu Threshold     ", apply_otsu_threshold, smoothed)
    timings.append(("Otsu Threshold     ", elapsed))

    kernel = create_structuring_element(settings.STRUCTURING_ELEMENT_SIZE)
    elapsed, morphed = _time_stage("Morphology (Open)  ", apply_opening, binary, kernel)
    timings.append(("Morphology (Open)  ", elapsed))

    elapsed, (labeled, areas) = _time_stage(
        "Connected Components",
        apply_connected_components,
        morphed,
        settings.MIN_COMPONENT_AREA,
    )
    timings.append(("Connected Components", elapsed))

    if areas:
        target_id = next(iter(areas))
        elapsed, features = _time_stage(
            "Feature Extraction ",
            extract_features,
            labeled,
            target_id,
        )
        timings.append(("Feature Extraction ", elapsed))
    else:
        timings.append(("Feature Extraction ", 0.0))
        print("  [NOTE] No components found — feature extraction skipped.")

    total_elapsed = time.perf_counter() - total_start

    print(f"\n  {'Stage':<24} {'Time':>10}")
    print(f"  {'-'*24} {'-'*10}")
    for stage_name, stage_time in timings:
        flag = " << SLOW" if stage_time > 0.1 else ""
        print(f"  {stage_name:<24} {stage_time*1000:>8.1f}ms{flag}")

    print(f"  {'-'*36}")
    target = 0.500
    status = "PASS" if total_elapsed < target else "FAIL"
    print(f"  {'TOTAL':<24} {total_elapsed*1000:>8.1f}ms  {status} (target <{target*1000:.0f}ms)")
    print(f"\n  Components found: {len(areas)}")
    print(f"{'='*52}\n")

if __name__ == "__main__":
    run_profile(canvas_size=400)
