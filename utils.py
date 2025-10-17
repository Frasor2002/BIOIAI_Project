import chess

def str_color(color: chess.Color):
  return "white" if color == chess.WHITE else "black"

def get_piece_score(piece_type: chess.PieceType):
    """Given a type return its score.
    Args:
      piece_type (chess.PieceType): type of piece.
    Returns:
      int: score of the piece.
    """
    # Standard chess scores
    scores = {
      chess.PAWN: 1,
      chess.KNIGHT: 3,
      chess.BISHOP: 3,
      chess.ROOK: 5,
      chess.QUEEN: 9,
      chess.KING: 10
    }
    return scores.get(piece_type)