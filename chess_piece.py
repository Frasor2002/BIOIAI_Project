import chess
import random

from typing import Optional

import math

class Piece(chess.Piece):
  """Parent chess piece class."""
  genotype: dict
  square: chess.Square
  # TODO: add hunger and turns still vars
  # TODO: add belief of enemy locations (receive locations from others)
  # TODO: add scores to know important pieces (king is inf)

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


  # TODO: given a piece location we have to return its view on the board
  def view_pieces(self, board: chess.Board):
    view = {}
    
    # Get piece position
    file = chess.square_file(self.square)
    rank = chess.square_rank(self.square)
    # Get view radius
    radius = self.get_genotype()['radius']

    # Iterate through all squares in radius
    for delta_file in range(-radius, radius + 1):
      for delta_rank in range(-radius, radius + 1):
        new_file = file + delta_file
        new_rank = rank + delta_rank

        # Stay inside board boundaries (0–7)
        if 0 <= new_file <= 7 and 0 <= new_rank <= 7:
          new_square = chess.square(new_file, new_rank)
          distance = math.trunc(math.sqrt(delta_file**2 + delta_rank**2))

          # Skip the piece itself
          if distance == 0:
            continue

          seen = board.piece_at(new_square)
          if seen:
            entry = {
              "piece": seen.piece_type,
              "color": seen.color,
              "distance": distance
            }
          else:
            entry = {
              "piece": None,
              "color": None,
              "distance": distance
            }

          view[new_square] = entry


    #self.view = view
    # Can return only important pieces to broadcast to other agents
    return view
  
  # TODO: given list of locations of friends/foes we need to understand safe and unsafe squares
  def get_square_states(self, view, board):
    pass

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
