import chess
import random
from chess_piece import King, Queen, Rook, Bishop, Knight, Pawn

from typing import Optional

class Agent:
  """Class of the multiagent system made up of various pieces."""

  color: chess.Color
  pieces: dict

  def __init__(self, color: chess.Color, genotype: Optional[dict]):
    """Initialize the class.
    Args:
      color (chess.Color): color of the team to play as.
      genotype (Optional[dict]): genotype to be optimized.
    """
    self.color = color

    self.pieces = {
      'pawn': [],
      'rook': [],
      'knight': [],
      'bishop': [],
      'queen': [],
      'king': []
    }
    self.init_pieces(genotype)
  
  def init_pieces(self, genotype: Optional[dict]):
    """Create and init pieces with their starting positions.
    Args:
      genotype (Optional[dict]): optional genotype to init pieces.
    """
    # Starting rank and piece positions for each color
    if self.color == chess.WHITE:
      back_rank = 0 # row 1
      pawn_rank = 1 # row 2
    else:
      back_rank = 7 # row 8
      pawn_rank = 6 # row 7
    
    # Init pawns
    for file in range(8): # files from A to H
      square = chess.square(file, pawn_rank)
      self.pieces["pawn"].append(Pawn(self.color, square, genotype))

    # Order of back rank pieces with key and class to init
    back_layout = [
      ("rook",   Rook),
      ("knight", Knight),
      ("bishop", Bishop),
      ("queen",  Queen),
      ("king",   King),
      ("bishop", Bishop),
      ("knight", Knight),
      ("rook",   Rook)
    ]

    # Init back pieces
    for file, (key, piece_class) in enumerate(back_layout):
      square = chess.square(file, back_rank)
      self.pieces[key].append(piece_class(self.color, square, genotype))
        

  # TODO: after we move we need to update our internal state
  def update_pieces(self, move: chess.Move, board: chess.Board):
    pass
    

  
  
  # TODO
  def choose_move(self, legal_moves: list) -> chess.Move:
    """Choose best move given all the proposals from the pieces.
    Args:
      legal_moves (list): list of possible legal moves.
    Returns:
      chess.Move: chosen move.
    """
  
  # Pieces must look around the board in their sight radius

  # Pieces send communications on important enemy pieces

  # Get the highest scoring move from the pieces
  # Handle in case of same score with some logic
    move = random.choice(legal_moves)
    return move