import chess
import random
from chess_piece import King, Queen, Rook, Bishop, Knight, Pawn

from typing import Optional, Dict

class Agent:
  """Class of the multiagent system made up of various pieces."""

  color: chess.Color
  pieces: Dict[chess.Square, Pawn | Rook | Knight | Bishop | Queen | King]

  def __init__(self, color: chess.Color, genotype: Optional[dict]):
    """Initialize the class.
    Args:
      color (chess.Color): color of the team to play as.
      genotype (Optional[dict]): genotype to be optimized.
    """
    self.color = color
    #self.pieces = {
    #  'king': King(color, genotype),
    #  'queen': Queen(color, genotype),
    #  'rook': ([Rook(color, genotype) for _ in range(0,2)]),
    #  'bishop': ([Bishop(color, genotype) for _ in range(0,2)]),
    #  'knight': ([Knight(color, genotype) for _ in range(0,2)]),
    #  'pawn': ([Pawn(color, genotype) for _ in range(0,8)])
    #}
    self.pieces = {}
  
  # TODO: create mapping between board and our internal state
  def init_pieces(self, genotype: Optional[dict]):
    pass
  

  # TODO: after we move we need to update our internal state
  def update_pieces(self, move: chess.Move):
    pass
    

  # TODO: given a piece location we have to return its view on the board
  def get_piece_view(self, board):
    pass
  
  # TODO: given list of locations of friends/foes we need to understand safe and unsafe squares
  def get_square_states(self, view, board):
    pass
  
  # TODO
  def choose_move(self, legal_moves: list) -> chess.Move:
    """Choose best move given all the proposals from the pieces.
    Args:
      legal_moves (list): list of possible legal moves.
    Returns:
      chess.Move: chosen move.
    """
  
  # Get the highest scoring move from the pieces
  # Handle in case of same score with some logic
    move = random.choice(legal_moves)
    return move