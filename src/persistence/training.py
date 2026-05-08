
from __future__ import annotations

import json
import os
import pathlib

from recognition.normalization import FeatureNormalizer

LABEL_MAX_LEN: int = 10

_NUM_FEATURES: int = 11

class TrainingManager:

    def __init__(self, storage_path: pathlib.Path | None = None) -> None:
        if storage_path is None:

            _repo_root = pathlib.Path(__file__).parent.parent.parent
            storage_path = _repo_root / "data" / "template_library.json"

        self.storage_path: pathlib.Path = pathlib.Path(storage_path)
        self.library: dict[str, list[list[float]]] = {}
        self.normalizer: FeatureNormalizer = FeatureNormalizer()

    def save_sample(self, label: str, raw_features: list[float]) -> bool:

        label = label.strip()
        if not label:
            return False
        if len(label) > LABEL_MAX_LEN:
            return False

        if len(raw_features) != _NUM_FEATURES:
            return False

        self.normalizer.update_bounds(raw_features)

        if label not in self.library:
            self.library[label] = []
        self.library[label].append(list(raw_features))

        self._save_to_disk()
        return True

    def load_from_disk(self) -> None:

        path = self.storage_path
        if not path.exists():
            return

        try:
            with open(path, "r", encoding="utf-8") as fh:
                data = json.load(fh)

            raw_library = data.get("library", {})
            self.library = {}
            for lbl, vectors in raw_library.items():
                self.library[lbl] = [list(v) for v in vectors]

            raw_bounds = data.get("bounds", {})
            self.normalizer = FeatureNormalizer()
            for i in range(_NUM_FEATURES):
                key = str(i)
                if key in raw_bounds:
                    entry = raw_bounds[key]
                    self.normalizer.min_bounds[i] = float(entry["min"])
                    self.normalizer.max_bounds[i] = float(entry["max"])

        except (json.JSONDecodeError, KeyError, TypeError, ValueError):

            bak_path = path.with_suffix(path.suffix + ".bak")
            try:
                os.replace(str(path), str(bak_path))
            except OSError:
                pass

            self.library = {}
            self.normalizer = FeatureNormalizer()
            print(
                f"[training] WARNING: Corrupt template library detected. "
                f"Backed up to '{bak_path}'. Starting with empty library."
            )

    def _save_to_disk(self) -> None:

        path = self.storage_path
        path.parent.mkdir(parents=True, exist_ok=True)

        bounds_dict: dict[str, dict[str, float]] = {}
        for i in range(_NUM_FEATURES):
            bounds_dict[str(i)] = {
                "min": self.normalizer.min_bounds[i],
                "max": self.normalizer.max_bounds[i],
            }

        payload = {
            "bounds": bounds_dict,
            "library": self.library,
        }

        tmp_path = path.with_suffix(path.suffix + ".tmp")
        with open(tmp_path, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2)

        os.replace(str(tmp_path), str(path))

    def get_class_counts(self) -> dict[str, int]:

        result: dict[str, int] = {}
        for label, vectors in self.library.items():
            result[label] = len(vectors)
        return result
