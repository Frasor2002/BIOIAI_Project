import chess
import random

from typing import Optional

class Piece(chess.Piece):
  """Parent chess piece class."""
  genotype: dict
  square: chess.Square

  def __init__(self, piece_type: chess.PieceType, color: chess.Color, square: chess.Square, genotype: Optional[dict]):
    """Initialize the class.
    Args:
      piece_type (chess.PieceType): piece type.
      color (chess.Color): color of the team.
      square (chess.Square): location of the piece.
      genotype (Optional[dict]): genotype to be initialized.
    """
    super().__init__(piece_type, color)
    self.square = square
    # If genotype not passed randomly initialize it
    self.genotype = self.set_random_genotype() if genotype is None else genotype
    
    
  def set_random_genotype(self):
    """Randomly initialize genotype."""
    genotype = {
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
    return genotype

  def get_genotype(self):
    """Getter for the genotype."""
    return self.genotype

  # TODO
  def propose_move(self, board: chess.Board, legal_moves: list) -> tuple[chess.Move, int]:
    """Propose the best move for current piece."""
    move_score = 0

    # Get piece possible moves

    # Update piece state 

    # Update piece moves score

    # Propose move with higher score

    return "", move_score

# PIECES

class King(Piece):
  def __init__(self, color: chess.Color, square: chess.Square, genotype: Optional[dict]):
    super().__init__(chess.KING, color, square, genotype)

class Queen(Piece):
  def __init__(self, color: chess.Color, square: chess.Square, genotype: Optional[dict]):
    super().__init__(chess.QUEEN, color, square, genotype)

class Rook(Piece):
  def __init__(self, color: chess.Color, square: chess.Square, genotypes: Optional[dict]):
    super().__init__(chess.ROOK, color, square, genotypes)

class Bishop(Piece):
  def __init__(self, color: chess.Color, square: chess.Square, genotype: Optional[dict]):
    super().__init__(chess.BISHOP, color, square, genotype)

class Knight(Piece):
  def __init__(self, color: chess.Color, square: chess.Square, genotype: Optional[dict]):
    super().__init__(chess.KNIGHT, color, square, genotype)

class Pawn(Piece):
  def __init__(self, color: chess.Color, square: chess.Square, genotype: Optional[dict]):
    super().__init__(chess.PAWN, color, square, genotype)
