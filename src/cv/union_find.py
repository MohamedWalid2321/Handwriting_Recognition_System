
class UnionFind:

    def __init__(self) -> None:
        self._parent: dict[int, int] = {}
        self._rank: dict[int, int] = {}

    def make_set(self, label: int) -> None:

        if label not in self._parent:
            self._parent[label] = label
            self._rank[label] = 0

    def find(self, label: int) -> int:

        if self._parent[label] != label:
            self._parent[label] = self.find(self._parent[label])
        return self._parent[label]

    def union(self, label_a: int, label_b: int) -> None:

        root_a = self.find(label_a)
        root_b = self.find(label_b)
        if root_a == root_b:
            return

        rank_a = self._rank[root_a]
        rank_b = self._rank[root_b]

        if rank_a < rank_b:
            self._parent[root_a] = root_b
        elif rank_a > rank_b:
            self._parent[root_b] = root_a
        else:

            self._parent[root_b] = root_a
            self._rank[root_a] += 1
