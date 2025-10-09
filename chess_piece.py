import chess
import random

from typing import Optional

class Piece(chess.Piece):

    genotypes: dict

    def __init__(self, piece_type: chess.PieceType, color: chess.Color, genotypes: Optional[dict]):

        super().__init__(piece_type, color)
        self.genotypes = self.setRandomGenotypes() if genotypes is None else genotypes
        return
    
    def setRandomGenotypes(self):

        self.genotypes = {
            # Positional genes
            'radius': random.randint(2,7),
            'imm_danger': random.randint(-100,100),
            'hunger_lvl': random.randint(0,5),
            'turn': random.randint(0,5),
            'protection': random.randint(-100,100),
            # Action genes
            'capture': random.randint(-100,100),
            'fav_capture': random.randint(-100,100),
            'unf_capture': random.randint(-100,100),
            'dang_move': random.randint(-100,100),
            'def_move': random.randint(-100,100),
            'appr_opp_king': random.randint(-100,100), 
            'close_same_king': random.randint(-100,100), 
            'appr_high_value_opp_piece': random.randint(-100,100)
        }

    def getGenotypes(self):
        return self.genotypes

    # TODO
    def proposeMove(self) -> tuple[chess.Move, int]:

        move_score = 0

        # Get piece possible moves

        # Update piece state 

        # Update piece moves score

        # Propose move with higher score

        return

# PIECES

class King(Piece):

    def __init__(self, color: chess.Color, genotypes: Optional[dict]):
        super().__init__(chess.KING, color, genotypes)
        return

class Queen(Piece):

    def __init__(self, color: chess.Color, genotypes: Optional[dict]):
        super().__init__(chess.QUEEN, color, genotypes)
        return

class Rook(Piece):

    def __init__(self, color: chess.Color, genotypes: Optional[dict]):
        super().__init__(chess.ROOK, color, genotypes)
        return

class Bishop(Piece):

    def __init__(self, color: chess.Color, genotypes: Optional[dict]):
        super().__init__(chess.BISHOP, color, genotypes)
        return

class Knight(Piece):

    def __init__(self, color: chess.Color, genotypes: Optional[dict]):
        super().__init__(chess.KNIGHT, color, genotypes)
        return

class Pawn(Piece):
    
    def __init__(self, color: chess.Color, genotypes: Optional[dict]):
        super().__init__(chess.PAWN, color, genotypes)
        return