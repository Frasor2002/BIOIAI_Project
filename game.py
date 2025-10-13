import chess
from teacher_engine import TeacherEngine
from agent import Agent
from utils import str_color
from typing import Optional, Dict

class Game:
  """Game class to handle the various matches."""

  board: chess.Board

  def __init__(self):
    """Initialize game object."""
    self.board = chess.Board()

  def reset_board(self):
    """Reset board state."""
    self.board = chess.Board()


  # TODO: function to get legal moves for each piece
  def get_pieces_moves(self) -> Dict[chess.Square, dict]:
    """Get all legal moves indexed by chess square."""
    pieces_moves = {}

    for move in self.board.legal_moves:
      if move.from_square not in pieces_moves:
        pieces_moves[move.from_square] = {
          'piece_type': self.board.piece_at(move.from_square),
          'moves': []
        }
      pieces_moves[move.from_square]['moves'].append(move)

    return pieces_moves

  def get_move(self, teacher: TeacherEngine, agent: Agent) -> chess.Move:
    """Get next move based on whose turn it is.
    Args:
      teacher (TeacherEngine): object to handle stockfish chess engine.
      agent (Agent): multiagent system to be optimized.
    Returns:
      chess.Move: move to do next.
    """
    current_turn = self.board.turn

    if current_turn == agent.color:
      move = agent.choose_move(list(self.board.legal_moves))
      to_move = "Agent"
    else:
      move = teacher.choose_move(self.board.fen())
      to_move = "Stockfish"
    
    #print(f"{to_move} ({str_color(current_turn)}) plays {move}")
    return move


  def play_match(self, teacher: TeacherEngine, agent: Agent) -> Optional[str]:
    """Play a single match of chess putting the teacher engine and the
    agent in competition.
    Args:
      teacher (TeacherEngine): object to handle stockfish chess engine.
      agent (Agent): multiagent system to be optimized.
    Returns:
      Optional[str]: if there is a winner return a string with the name.
    """
    # Reset game state
    self.reset_board()

    # Show game at the start
    #print(self.board)

    # Play until stalemate or checkmate is achieved
    while (not self.board.is_checkmate()) and (not self.board.is_stalemate()):
      move = self.get_move(teacher, agent)
      # Update board
      self.board.push(move)

    # Show game
    #print(self.board)

    if self.board.is_checkmate():
      winner = f"Stockfish ({str_color(teacher.color)})" if self.board.turn == agent.color else f"Agent ({str_color(agent.color)})" 
      print(f"Checkmate! {winner} Wins.")
      return winner
    
    return None
