
import dataclasses

@dataclasses.dataclass
class PipelineState:

    raw_pixels: list[list[tuple[int, int, int]]]

    grayscale: list[list[int]]

    smoothed: list[list[int]]

    binary: list[list[int]]

    morphed: list[list[int]]

    labels: list[list[int]]

    feature_vector: list[float]

    prediction: str | None

    confidence: float | None

    runner_up: str | None

def empty_state(canvas_size: int) -> PipelineState:

    empty_rgb_row: list[tuple[int, int, int]] = [(0, 0, 0)] * canvas_size
    empty_rgb_grid: list[list[tuple[int, int, int]]] = [
        list(empty_rgb_row) for _ in range(canvas_size)
    ]
    empty_grid: list[list[int]] = [
        [0] * canvas_size for _ in range(canvas_size)
    ]
    return PipelineState(
        raw_pixels=empty_rgb_grid,
        grayscale=empty_grid,
        smoothed=empty_grid,
        binary=empty_grid,
        morphed=empty_grid,
        labels=empty_grid,
        feature_vector=[],
        prediction=None,
        confidence=None,
        runner_up=None,
    )
