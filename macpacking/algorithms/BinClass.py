from .Piece import Piece

class BinClass:
    def __init__(self, capacity: int, classID: str) -> None:
        self.pieces = []
        self.capacity = capacity
        self.remaining = capacity
        self.classID = classID
    def add_piece(self, x: Piece) -> None:
        self.pieces.append(x)
        self.remaining -= x.weight
    def return_pieces(self) -> list[Piece]:
        return self.pieces
