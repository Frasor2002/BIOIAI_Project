import chess
import random
from chess_piece import King, Queen, Rook, Bishop, Knight, Pawn

from typing import Optional

class Agent:

    color: chess.Color
    pieces: dict

    def __init__(self, color: chess.Color, genotypes: Optional[dict]):

        self.color = color
        self.pieces = {
            'king': King(color, genotypes),
            'queen': Queen(color, genotypes),
            'rook': ([Rook(color, genotypes) for _ in range(0,2)]),
            'bishop': ([Bishop(color, genotypes) for _ in range(0,2)]),
            'knight': ([Knight(color, genotypes) for _ in range(0,2)]),
            'pawn': ([Pawn(color, genotypes) for _ in range(0,8)])
        }
    
    # TODO
    def getMove(self, legal_moves: list) -> chess.Move:

        move = random.choice(legal_moves)
        return move