import chess

from teacher_engine import TeacherEngine
from agent import Agent
from utils import str_color

class Game:
  """Game class to handle the various matches."""

  board: chess.Board

  def __init__(self):
    """Initialize game object."""
    self.board = chess.Board()

  def resetBoard(self):
    """Reset board state."""
    self.board = chess.Board()


  def play_match(self, teacher: TeacherEngine, agent: Agent):
    """Play a single match of chess putting the teacher engine and the
    agent in competition.
    Args:
      teacher (TeacherEngine): object to handle stockfish chess engine.
      agent (Agent): multiagent system to be optimized.
    Returns:
      Optional[str]: if there is a winner return a string with the name.
    """
    # Reset game state
    self.resetBoard()

    # Show game at the start
    print(self.board)

    # Play until stalemate or checkmate is achieved
    while (not self.board.is_checkmate()) and (not self.board.is_stalemate()):

      # White team
      if self.board.turn == chess.WHITE:
        # Agent turn
        if agent.color == chess.WHITE:
          move = agent.getMove(list(self.board.legal_moves))
          print(f"Agent (white) plays {move}")
        # Engine turn
        else:
          move = teacher.chooseMove(self)
          print(f"Stockfish (white) plays {move}")

      # Black team
      if self.board.turn == chess.BLACK:
        # Agent turn
        if agent.color == chess.BLACK:
          move = agent.getMove(list(self.board.legal_moves))
          print(f"Agent (black) plays {move}")
        # Engine turn
        else:
          move = teacher.chooseMove(self)
          print(f"Stockfish (black) plays {move}")

      # Update board
      self.board.push(move)

    # Show game
    print(self.board)

    if self.board.is_checkmate():
      winner = f"Stockfish ({str_color(teacher.color)})" if self.board.turn == agent.color else f"Agent ({str_color(agent.color)})" 
      print(f"Checkmate! {winner} Wins.")
      return winner
    
    return None
