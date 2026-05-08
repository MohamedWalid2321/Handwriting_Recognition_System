
import math

_INF = float("inf")

IDX_AREA        = 0
IDX_CENTROID_X  = 1
IDX_CENTROID_Y  = 2
IDX_WIDTH       = 3
IDX_HEIGHT      = 4
IDX_ASPECT      = 5
IDX_COMPACT     = 6
IDX_MU20        = 7
IDX_MU02        = 8
IDX_MU11        = 9
IDX_ORIENTATION = 10

_ZERO_VECTOR: list[float] = [0.0] * 11

def extract_features(
    labeled: list[list[int]],
    target_id: int,
) -> list[float]:

    if not labeled:
        return list(_ZERO_VECTOR)

    height = len(labeled)
    width  = len(labeled[0])

    m00: float = 0.0
    m10: float = 0.0
    m01: float = 0.0
    m20: float = 0.0
    m02: float = 0.0
    m11: float = 0.0

    min_c = width
    max_c = -1
    min_r = height
    max_r = -1

    perimeter: int = 0

    for r in range(height):
        row = labeled[r]
        for c in range(width):
            if row[c] != target_id:
                continue

            cf = float(c)
            rf = float(r)
            m00 += 1.0
            m10 += cf
            m01 += rf
            m20 += cf * cf
            m02 += rf * rf
            m11 += rf * cf

            if c < min_c:
                min_c = c
            if c > max_c:
                max_c = c
            if r < min_r:
                min_r = r
            if r > max_r:
                max_r = r

            is_boundary = (
                r == 0 or labeled[r - 1][c] != target_id
                or r == height - 1 or labeled[r + 1][c] != target_id
                or c == 0 or row[c - 1] != target_id
                or c == width - 1 or row[c + 1] != target_id
            )
            if is_boundary:
                perimeter += 1

    if m00 == 0.0:
        return list(_ZERO_VECTOR)

    cx: float = m10 / m00
    cy: float = m01 / m00

    bb_w: float = float(max_c - min_c + 1)
    bb_h: float = float(max_r - min_r + 1)

    aspect: float = bb_w / bb_h if bb_h != 0.0 else 0.0

    perim_f = float(perimeter)
    compactness: float = (
        4.0 * math.pi * m00 / (perim_f * perim_f)
        if perim_f > 0.0
        else 0.0
    )

    mu20: float = m20 - cx * m10
    mu02: float = m02 - cy * m01
    mu11: float = m11 - cy * m10

    orientation: float = 0.5 * math.atan2(2.0 * mu11, mu20 - mu02)

    return [
        m00,
        cx,
        cy,
        bb_w,
        bb_h,
        aspect,
        compactness,
        mu20,
        mu02,
        mu11,
        orientation,
    ]
