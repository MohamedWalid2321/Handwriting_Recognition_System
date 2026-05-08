
def to_grayscale(
    rgb_grid: list[list[tuple[int, int, int]]],
) -> list[list[int]]:

    result: list[list[int]] = []

    for row in rgb_grid:
        gray_row: list[int] = []
        for r, g, b in row:
            luminance = int(0.299 * r + 0.587 * g + 0.114 * b)
            gray_row.append(luminance)
        result.append(gray_row)

    return result
