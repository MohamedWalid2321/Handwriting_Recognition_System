
import math

def generate_kernel(size: int, sigma: float) -> list[list[float]]:

    kernel: list[list[float]] = []
    centre = size // 2
    two_sigma_sq = 2.0 * sigma * sigma

    total = 0.0
    for row_idx in range(size):
        row: list[float] = []
        for col_idx in range(size):
            dx = col_idx - centre
            dy = row_idx - centre
            weight = math.exp(-(dx * dx + dy * dy) / two_sigma_sq)
            row.append(weight)
            total += weight
        kernel.append(row)

    for row_idx in range(size):
        for col_idx in range(size):
            kernel[row_idx][col_idx] /= total

    return kernel

def _convolve_1d_horizontal(
    grid: list[list[int]] | list[list[float]],
    kernel_1d: list[float],
) -> list[list[float]]:

    height = len(grid)
    width = len(grid[0])
    k = len(kernel_1d)
    half = k // 2

    _grid = grid
    _k1d = kernel_1d
    _height = height
    _width = width

    result: list[list[float]] = []
    result_append = result.append

    for r in range(_height):
        row_in = _grid[r]
        row_out: list[float] = []
        row_out_append = row_out.append
        for c in range(_width):
            acc = 0.0
            for ki in range(k):
                src_c = c + ki - half
                if 0 <= src_c < _width:
                    acc += _k1d[ki] * row_in[src_c]
            row_out_append(acc)
        result_append(row_out)
    return result

def _convolve_1d_vertical(
    grid: list[list[float]],
    kernel_1d: list[float],
) -> list[list[int]]:

    height = len(grid)
    width = len(grid[0])
    k = len(kernel_1d)
    half = k // 2

    _grid = grid
    _k1d = kernel_1d
    _height = height
    _width = width
    _int = int

    result: list[list[int]] = []
    result_append = result.append

    for r in range(_height):
        row_out: list[int] = []
        row_out_append = row_out.append
        for c in range(_width):
            acc = 0.0
            for ki in range(k):
                src_r = r + ki - half
                if 0 <= src_r < _height:
                    acc += _k1d[ki] * _grid[src_r][c]
            row_out_append(_int(acc))
        result_append(row_out)
    return result

def smooth(
    grayscale_grid: list[list[int]],
    kernel_size: int,
    sigma: float,
) -> list[list[int]]:

    if not grayscale_grid:
        return []

    kernel_2d = generate_kernel(kernel_size, sigma)
    centre_row = kernel_2d[kernel_size // 2]
    total = sum(centre_row)
    kernel_1d = [w / total for w in centre_row]

    h_blurred = _convolve_1d_horizontal(grayscale_grid, kernel_1d)

    return _convolve_1d_vertical(h_blurred, kernel_1d)
