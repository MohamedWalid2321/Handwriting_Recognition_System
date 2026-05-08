
_NUM_FEATURES: int = 11

class FeatureNormalizer:

    def __init__(self) -> None:
        self.min_bounds: list[float] = [float("inf")] * _NUM_FEATURES
        self.max_bounds: list[float] = [float("-inf")] * _NUM_FEATURES

    def update_bounds(self, vector: list[float]) -> None:

        for i in range(_NUM_FEATURES):
            v = vector[i]
            if v < self.min_bounds[i]:
                self.min_bounds[i] = v
            if v > self.max_bounds[i]:
                self.max_bounds[i] = v

    def normalize(self, vector: list[float]) -> list[float]:

        result: list[float] = [0.0] * _NUM_FEATURES
        for i in range(_NUM_FEATURES):
            range_i = self.max_bounds[i] - self.min_bounds[i]
            if range_i == 0.0:
                result[i] = 0.5
            else:
                result[i] = (vector[i] - self.min_bounds[i]) / range_i
        return result
