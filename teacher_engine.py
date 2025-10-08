import stockfish
import chess

class TeacherEngine:
  def __init__(self, path):
    self.stockfish = stockfish.Stockfish(path)

  def configStockfish(self, depth, skill_level):
    self.stockfish.set_depth(depth)
    self.stockfish.set_skill_level(skill_level)

  def syncWithGame(self, game):
    self.stockfish.set_fen_position(game.board.fen())

  def chooseMove(self):
    move = self.stockfish.get_best_move()

    # Or we can choose one of the top k ones
    #stockfish.get_top_moves(3)
    
    # Convert move into usable format
    move = chess.Move.from_uci(move)
    return move