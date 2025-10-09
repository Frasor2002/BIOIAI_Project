import chess

from agent import Agent
from utils import str_color

class Game:
  def __init__(self):
    self.board = chess.Board()

  def resetBoard(self):
    self.board = chess.Board()

  def play_match(self, engine, agent: Agent):
    # Reset game state
    self.resetBoard()
    # Reset stockfish state
    engine.syncWithGame(self)

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
          # Update stockfish
          engine.syncWithGame(self)
          move = engine.chooseMove()
          print(f"Stockfish (white) plays {move}")

      # Black team
      if self.board.turn == chess.BLACK:
        # Agent turn
        if agent.color == chess.BLACK:
          move = agent.getMove(list(self.board.legal_moves))
          print(f"Agent (black) plays {move}")
        # Engine turn
        else:
          # Update stockfish
          engine.syncWithGame(self)
          move = engine.chooseMove()
          print(f"Stockfish (black) plays {move}")

      # Update board
      self.board.push(move)

    # Show game
    print(self.board)

    if self.board.is_checkmate():
      winner = f"Stockfish ({str_color(engine.color)})" if self.board.turn == agent.color else f"Agent ({str_color(agent.color)})" 
      print(f"Checkmate! {winner} Wins.")
      return winner
    
    return None
