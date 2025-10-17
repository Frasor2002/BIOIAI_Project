import chess
import random
from stockfish import Stockfish

from typing import Optional

class TeacherEngine:
  """TeacherEngine class wrapper around stockfish library."""

  stockfish: Stockfish
  color: chess.Color

  def __init__(self, path: str, color: chess.Color):
    """Initialize by loading stockfish and setting which color to play as.
    Args:
      path (str): filepath of stockfish binary.
      color (chess.Color): which color stockfish will to play as.
    """
    self.stockfish = Stockfish(path)
    self.color = color

  def config_stockfish(self, depth: Optional[int], skill_level: Optional[int]):
    """Configure stockfish parameters.
    Args:
      depth (Optional[int]): optional parameter to set depth of stockfish search.
      skill_level (Optional[int]): optional parameter to set skill level.
    """
    if depth is not None:
      self.stockfish.set_depth(depth)
    if skill_level is not None:
      self.stockfish.set_skill_level(skill_level)
  
  def get_config_stockfish(self) -> dict:
    """Getter for Stockfish configuration parameters.
    Returns:
      dict: dictionary containing Stockfish config parameters.
    """
    return self.stockfish.get_parameters()

  def sync_with_game(self, board_state: str):
    """Given a game, synch internal stockfish state with the game state.
    Args:
      board_state (str): state of the match in fen format.
    """
    self.stockfish.set_fen_position(board_state)


  def choose_move(self, board_state: str) -> chess.Move:
    """Given a game a move is returned.
    Args:
      board_state (str): state of the match in fen format.
    Returns:
      (chess.Move): move suggested by stockfish.
    """
    # Update internal state
    self.sync_with_game(board_state)

    # Choose one of the top k ones
    top_moves = self.stockfish.get_top_moves(3)
    if len(top_moves) == 3:
      move = random.choice([top_moves[1]["Move"], top_moves[2]["Move"]])
    elif len(top_moves) == 2:
      print("Only 2 top moves")
      move = top_moves[1]["Move"]
    else:
      print("Only one top move")
      move = top_moves[0]["Move"]
    
    # Convert move into usable format
    move = chess.Move.from_uci(move)
    return move