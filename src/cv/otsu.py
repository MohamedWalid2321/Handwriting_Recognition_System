
from collections.abc import Sequence

def _ensure_integer_grid(
    image: Sequence[Sequence[int | float]],
) -> list[list[int]]:

    if not image:
        return []

    result: list[list[int]] = []
    _min = min
    _max = max
    _round = round
    result_append = result.append
    for row in image:
        int_row: list[int] = []
        int_row_append = int_row.append
        for pixel in row:
            int_row_append(_min(_max(_round(pixel), 0), 255))
        result_append(int_row)
    return result

def _build_histogram(image: list[list[int]]) -> list[int]:

    histogram: list[int] = [0] * 256
    for row in image:
        histogram_getitem = histogram.__getitem__
        for pixel in row:
            histogram[pixel] += 1
    return histogram

def _calculate_otsu_threshold(histogram: list[int]) -> int:

    total_pixels = 0
    global_sum = 0
    for intensity in range(256):
        total_pixels += histogram[intensity]
        global_sum += intensity * histogram[intensity]

    if total_pixels == 0:
        return 0

    max_variance = -1.0
    best_threshold = 0

    weight1 = 0
    sum1 = 0

    for t in range(255):
        weight1 += histogram[t]
        sum1 += t * histogram[t]

        if weight1 == 0:
            continue

        weight2 = total_pixels - weight1
        if weight2 == 0:
            break

        mean1 = sum1 / weight1
        mean2 = (global_sum - sum1) / weight2

        diff = mean1 - mean2
        variance = weight1 * weight2 * diff * diff

        if variance > max_variance:
            max_variance = variance
            best_threshold = t

    return best_threshold

def apply_otsu_threshold(
    image: Sequence[Sequence[int | float]],
) -> list[list[int]]:

    if not image:
        return []

    first_pixel = image[0][0]
    int_image: list[list[int]]
    if type(first_pixel) is int:
        int_image = image
    else:
        int_image = _ensure_integer_grid(image)

    histogram = _build_histogram(int_image)

    threshold = _calculate_otsu_threshold(histogram)

    binary: list[list[int]] = []
    binary_append = binary.append
    for row in int_image:
        binary_row: list[int] = []
        binary_row_append = binary_row.append
        for pixel in row:
            binary_row_append(0 if pixel <= threshold else 255)
        binary_append(binary_row)

    return binary
