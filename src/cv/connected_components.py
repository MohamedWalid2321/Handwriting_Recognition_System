
from cv.union_find import UnionFind

_BG = 255
_LABEL_BG = 0

_NEIGHBOURS_8 = (
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),
)

def apply_connected_components(
    image: list[list[int]],
    min_area_threshold: int = 10,
) -> tuple[list[list[int]], dict[int, int]]:

    if not image:
        return [], {}

    height = len(image)
    width = len(image[0])

    uf = UnionFind()
    uf_make = uf.make_set
    uf_union = uf.union

    next_label = 1

    provisional: list[int] = [_LABEL_BG] * (height * width)

    for r in range(height):
        row = image[r]
        base = r * width
        for c in range(width):
            if row[c] == _BG:
                continue

            neighbour_labels: list[int] = []
            for dr, dc in _NEIGHBOURS_8:
                nr = r + dr
                nc = c + dc
                if 0 <= nr < height and 0 <= nc < width:
                    nb_lbl = provisional[nr * width + nc]
                    if nb_lbl != _LABEL_BG:
                        neighbour_labels.append(nb_lbl)

            if not neighbour_labels:

                uf_make(next_label)
                provisional[base + c] = next_label
                next_label += 1
            else:

                min_lbl = neighbour_labels[0]
                for lbl in neighbour_labels[1:]:
                    if lbl < min_lbl:
                        min_lbl = lbl
                provisional[base + c] = min_lbl
                for lbl in neighbour_labels:
                    uf_union(min_lbl, lbl)

    uf_find = uf.find
    raw_areas: dict[int, int] = {}
    root_of: list[int] = [_LABEL_BG] * (height * width)

    for idx in range(height * width):
        prov = provisional[idx]
        if prov == _LABEL_BG:
            continue
        root = uf_find(prov)
        root_of[idx] = root
        if root in raw_areas:
            raw_areas[root] += 1
        else:
            raw_areas[root] = 1

    remap: dict[int, int] = {}
    dense_id = 1
    for root in sorted(raw_areas):
        if raw_areas[root] >= min_area_threshold:
            remap[root] = dense_id
            dense_id += 1

    component_areas: dict[int, int] = {}
    labeled: list[list[int]] = [[_LABEL_BG] * width for _ in range(height)]

    for r in range(height):
        lbl_row = labeled[r]
        base = r * width
        for c in range(width):
            root = root_of[base + c]
            if root == _LABEL_BG:
                continue
            new_id = remap.get(root, _LABEL_BG)
            if new_id != _LABEL_BG:
                lbl_row[c] = new_id
                if new_id in component_areas:
                    component_areas[new_id] += 1
                else:
                    component_areas[new_id] = 1

    return labeled, component_areas
