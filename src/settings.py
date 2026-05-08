
CANVAS_SIZE: int = 400

PEN_WIDTH: int = 10

PEN_COLOR: tuple[int, int, int] = (0, 0, 0)

GAUSSIAN_SIGMA: float = 2.5

KERNEL_SIZE: int = 9

STRUCTURING_ELEMENT_SIZE: int = 5

MIN_COMPONENT_AREA: int = 50

def _validate_settings() -> None:

    if not (400 <= CANVAS_SIZE <= 800):
        raise ValueError(
            f"Invalid configuration in settings.py: "
            f"CANVAS_SIZE must be in [400, 800], got {CANVAS_SIZE}."
        )
    if not (4 <= PEN_WIDTH <= 60):
        raise ValueError(
            f"Invalid configuration in settings.py: "
            f"PEN_WIDTH must be in [4, 60], got {PEN_WIDTH}."
        )
    if (
        not isinstance(PEN_COLOR, tuple)
        or len(PEN_COLOR) != 3
        or not all(isinstance(c, int) and 0 <= c <= 255 for c in PEN_COLOR)
    ):
        raise ValueError(
            f"Invalid configuration in settings.py: "
            f"PEN_COLOR must be a tuple of 3 ints in [0, 255], got {PEN_COLOR}."
        )
    if not (0.5 <= GAUSSIAN_SIGMA <= 5.0):
        raise ValueError(
            f"Invalid configuration in settings.py: "
            f"GAUSSIAN_SIGMA must be in [0.5, 5.0], got {GAUSSIAN_SIGMA}."
        )
    if not (3 <= KERNEL_SIZE <= 15):
        raise ValueError(
            f"Invalid configuration in settings.py: "
            f"KERNEL_SIZE must be in [3, 15], got {KERNEL_SIZE}."
        )
    if KERNEL_SIZE % 2 == 0:
        raise ValueError(
            f"Invalid configuration in settings.py: "
            f"KERNEL_SIZE must be an odd number, got {KERNEL_SIZE}."
        )
    if not (2 <= STRUCTURING_ELEMENT_SIZE <= 100):
        raise ValueError(
            f"Invalid configuration in settings.py: "
            f"STRUCTURING_ELEMENT_SIZE must be in [2, 100], got {STRUCTURING_ELEMENT_SIZE}."
        )
    if not (10 <= MIN_COMPONENT_AREA <= 500):
        raise ValueError(
            f"Invalid configuration in settings.py: "
            f"MIN_COMPONENT_AREA must be in [10, 500], got {MIN_COMPONENT_AREA}."
        )

_validate_settings()
