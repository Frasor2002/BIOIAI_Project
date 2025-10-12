from __future__ import annotations

import chess
import random
from stockfish import Stockfish

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
  from game import Game

class TeacherEngine:
  """TeacherEngine class wrapper around stockfish library."""

  stockfish: Stockfish
  color: chess.Color

  def __init__(self, path: str, color: chess.Color):
    """Initialize by loading stockfish and setting which color to play as.
    Args:
      path (str): filepath of stockfish binary.
      color (chess.Color): which color to play as.
    """
    self.stockfish = Stockfish(path)
    self.color = color

  def configStockfish(self, depth: Optional[int], skill_level: Optional[int]):
    """Configure stockfish parameters.
    Args:
      depth (Optional[int]): optional parameter to set depth of stockfish search.
      skill_level (Optional[int]): optional parameter to set skill level.
    """
    if depth is not None:
      self.stockfish.set_depth(depth)
    if skill_level is not None:
      self.stockfish.set_skill_level(skill_level)
  
  def getConfigStockfish(self):
    """Getter for Stockfish configuration parameters."""
    return self.stockfish.get_parameters()

  def syncWithGame(self, game: Game):
    """Given a game, synch internal stockfish state with the game state.
    Args:
      game (Game): game object containing the state of the match.
    """
    state = game.board.fen()
    self.stockfish.set_fen_position(state)


  def chooseMove(self, game: Game):
    """Given a game a move is returned.
    Args:
      game (Game): game object containing the state of the match.
    Returns:
      (chess.Move): move suggested by stockfish.
    """
    # Update internal state
    self.syncWithGame(game)

    # Choose the best move
    #move = self.stockfish.get_best_move()

    # Or we can choose one of the top k ones
    top_moves = self.stockfish.get_top_moves(3)
    move = random.choice([top_moves[1]["Move"], top_moves[2]["Move"]])
    
    # Convert move into usable format
    move = chess.Move.from_uci(move)
    return move