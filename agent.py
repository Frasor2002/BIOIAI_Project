import chess
import random
from chess_piece import King, Queen, Rook, Bishop, Knight, Pawn, Piece

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
      chess.PAWN : [],
      chess.ROOK : [],
      chess.KNIGHT : [],
      chess.BISHOP : [],
      chess.QUEEN : [],
      chess.KING : []
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
      self.pieces[chess.PAWN].append(Pawn(self.color, square, genotype))

    # Order of back rank pieces with key and class to init
    back_layout = [
      (chess.ROOK,   Rook),
      (chess.KNIGHT, Knight),
      (chess.BISHOP, Bishop),
      (chess.QUEEN,  Queen),
      (chess.KING,   King),
      (chess.BISHOP, Bishop),
      (chess.KNIGHT, Knight),
      (chess.ROOK,   Rook)
    ]

    # Init back pieces
    for file, (key, piece_class) in enumerate(back_layout):
      square = chess.square(file, back_rank)
      self.pieces[key].append(piece_class(self.color, square, genotype))
        

  # TODO: after we move we need to update our internal state
  def update_pieces(self, move: chess.Move, board: chess.Board):
    """Updates pieces states after every turn.
    Args:
      move (chess.Move): move to do.
      board (chess.Board): board of the game.
    """
    start_square = move.from_square
    end_square = move.to_square

    # Find the piece that is going to move
    moving_piece = self.get_piece_at(start_square)

    # Update internal state
    for piece_list in self.pieces.values():
      for piece in piece_list:
        piece.increase_hunger()
        piece.increase_turns_still()

    is_capture = board.is_capture(move)
    moving_piece.reset_turns_still()
    if is_capture:
      moving_piece.reset_hunger()

    # Two special cases must be handles: promotion and castling
    if move.promotion:
      # Moving piece must be a pawn
      assert type(moving_piece) == Pawn
      promoted_to = move.promotion

      # Map piece type to constructor
      class_map = {
        chess.QUEEN: Queen,
        chess.ROOK: Rook,
        chess.BISHOP: Bishop,
        chess.KNIGHT: Knight
      }

      # Create new promoted piece, inheriting genotype
      new_piece_class = class_map[promoted_to]
      new_piece = new_piece_class(self.color, end_square, moving_piece.get_genotype())
      # Add the new piece to the list
      self.pieces[promoted_to].append(new_piece)
      self.pieces[chess.PAWN].remove(moving_piece)
      moving_piece = new_piece
    else: # Standard move
      moving_piece.square = end_square

      # If castling both the king and rook must be moved
      if board.is_castling(move):
        if self.color == chess.WHITE:
          rook_from = chess.H1 if end_square == chess.G1 else chess.A1
          rook_to = chess.F1 if end_square == chess.G1 else chess.D1
        else:  # Black
          rook_from = chess.H8 if end_square == chess.G8 else chess.A8
          rook_to = chess.F8 if end_square == chess.G8 else chess.D8
            
        # Find the specific rook and update its square
        castling_rook = self.get_piece_at(rook_from)
        castling_rook.square = rook_to
        castling_rook.reset_turns_still()
    


    
  
  def get_piece_at(self, square: chess.square) -> Optional[Piece]:
    """Utility to get a piece at a certain square.
    Args:
      square: square on the board.
    Returns:
      Optional[Piece]: piece on the board.
    """
    for piece_list in self.pieces.values():
      for piece in piece_list:
        if piece.square == square:
          return piece
    return None
  
  
  # TODO
  def choose_move(self, legal_moves: list, board: chess.Board) -> chess.Move:
    """Choose best move given all the proposals from the pieces.
    Args:
      legal_moves (list): list of possible legal moves.
    Returns:
      chess.Move: chosen move.
    """
  
    # Pieces must look around the board in their sight radius
    messages = []
    for piece_list in self.pieces.values():
      for piece in piece_list:
        # After looking around a message is prepared
        msg = piece.view_pieces(board)
        messages.append(msg)

    # Pieces receive communication on enemy pieces from teammates
    # They also receive their own message but it wont change their belief
    for piece_list in self.pieces.values():
        for piece in piece_list:
          for msg in messages:
            piece.receive_msg(msg)

    moves = []
    for piece_list in self.pieces.values():
        for piece in piece_list:
          #move = piece.propose_move(legal_moves)
          pass

    #self.update_pieces(best_move)

    # Get the highest scoring move from the pieces
    # Handle in case of same score with some logic
    move = random.choice(legal_moves)
    return move