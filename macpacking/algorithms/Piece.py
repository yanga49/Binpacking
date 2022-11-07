class Heuristic:
    def __init__(self, weight: int, category: str) -> None:
        self.weight = weight
        self.category = category

    def h(self, category: str):
        return 0


class Piece(Heuristic):

    def __init__(self, weight: int, category: str) -> None:
        super().__init__(weight, category)

    def h(self, category: int) -> str:
        return category
