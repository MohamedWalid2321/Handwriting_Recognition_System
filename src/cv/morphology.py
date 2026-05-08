
_BG = 255
_FG = 0

def create_structuring_element(size: int) -> list[list[int]]:

    if size % 2 == 0:
        raise ValueError(
            f"Structuring element size must be an odd integer, got {size}."
        )
    return [[1] * size for _ in range(size)]

def apply_erosion(
    image: list[list[int]],
    kernel: list[list[int]],
) -> list[list[int]]:

    if not image:
        return []

    height = len(image)
    width = len(image[0])
    k_size = len(kernel)
    half = k_size // 2

    row_fg_range: list[tuple[int, int] | None] = []
    for row in image:
        min_c = max_c = -1
        for ci, v in enumerate(row):
            if v == _FG:
                if min_c == -1:
                    min_c = ci
                max_c = ci
        row_fg_range.append((min_c, max_c) if min_c != -1 else None)

    output: list[list[int]] = []
    output_append = output.append

    for r in range(height):
        rng = row_fg_range[r]
        if rng is None:

            output_append([_BG] * width)
            continue

        row_in = image[r]
        row_out: list[int] = []
        row_out_append = row_out.append

        r_at_border = (r - half < 0) or (r + half >= height)

        for c in range(width):
            if row_in[c] != _FG:
                row_out_append(_BG)
                continue

            if r_at_border or (c - half < 0) or (c + half >= width):
                row_out_append(_BG)
                continue

            eroded = False
            for kr in range(k_size):
                nr = r + kr - half
                nb_row = image[nr]
                for kc in range(k_size):
                    nc = c + kc - half
                    if nb_row[nc] != _FG:
                        eroded = True
                        break
                if eroded:
                    break
            row_out_append(_FG if not eroded else _BG)
        output_append(row_out)

    return output

def apply_dilation(
    image: list[list[int]],
    kernel: list[list[int]],
) -> list[list[int]]:

    if not image:
        return []

    height = len(image)
    width = len(image[0])
    k_size = len(kernel)
    half = k_size // 2

    row_fg_range: list[tuple[int, int] | None] = []
    for row in image:
        min_c = max_c = -1
        for ci, v in enumerate(row):
            if v == _FG:
                if min_c == -1:
                    min_c = ci
                max_c = ci
        row_fg_range.append((min_c, max_c) if min_c != -1 else None)

    output: list[list[int]] = []
    output_append = output.append

    for r in range(height):
        row_in = image[r]

        min_fg_col = width
        max_fg_col = -1
        for kr in range(k_size):
            nr = r + kr - half
            if 0 <= nr < height:
                rng = row_fg_range[nr]
                if rng is not None:
                    lo = rng[0] - half
                    hi = rng[1] + half
                    if lo < min_fg_col:
                        min_fg_col = lo
                    if hi > max_fg_col:
                        max_fg_col = hi

        if max_fg_col < 0:
            output_append([_BG] * width)
            continue

        c_lo = max(0, min_fg_col)
        c_hi = min(width - 1, max_fg_col)

        row_out: list[int] = [_BG] * width
        for c in range(c_lo, c_hi + 1):
            if row_in[c] == _FG:
                row_out[c] = _FG
                continue

            dilated = False
            for kr in range(k_size):
                nr = r + kr - half
                if nr < 0 or nr >= height or row_fg_range[nr] is None:
                    continue
                nb_row = image[nr]
                for kc in range(k_size):
                    nc = c + kc - half
                    if nc < 0 or nc >= width:
                        continue
                    if nb_row[nc] == _FG:
                        dilated = True
                        break
                if dilated:
                    break
            if dilated:
                row_out[c] = _FG
        output_append(row_out)

    return output

def apply_opening(
    image: list[list[int]],
    kernel: list[list[int]],
) -> list[list[int]]:

    if not image:
        return []
    return apply_dilation(apply_erosion(image, kernel), kernel)

def apply_closing(
    image: list[list[int]],
    kernel: list[list[int]],
) -> list[list[int]]:

    if not image:
        return []
    return apply_erosion(apply_dilation(image, kernel), kernel)
