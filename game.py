import chess
import random # random agent

class Game:
  def __init__(self):
    self.board = chess.Board()

  def resetBoard(self):
    self.board = chess.Board()

  def play_match(self, engine, agent):
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
        # Update stockfish
        engine.stockfish.set_fen_position(self.board.fen())

        move = engine.chooseMove()
        print(f"White (Stockfish) plays {move}")

      # Black team
      if self.board.turn == chess.BLACK:
        # Here the agent system should get best move
        # move = agent.getMove()

        # Get legal move list
        legal_moves_list = list(self.board.legal_moves)
        # Choose a random move
        move = random.choice(legal_moves_list)
        print(f"Black (Random) plays: {move}")

      # Update board
      self.board.push(move)

    # Show game
    print(self.board)


    if self.board.is_checkmate():
      winner = "White (Stockfish)" if self.board.turn == chess.BLACK else "Black (Random)"
      print(f"Checkmate! {winner} Wins.")
      return winner
    return None
