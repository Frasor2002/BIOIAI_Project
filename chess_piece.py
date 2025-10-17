import chess
import random
from utils import get_piece_score

from typing import Optional

import math

class Piece(chess.Piece):
  """Parent chess piece class."""
  # Genotyope of chess piece used of decisions
  genotype: dict
  # Square on the grid of the piece
  square: chess.Square
  # Belief of the grid from the piece point of view
  belief: dict
  # Hunger value, when capturing is rest
  hunger: int
  # Turns that the piece has been still
  turns_still: int


  def __init__(self, piece_type: chess.PieceType, color: chess.Color, square: chess.Square, genotype: Optional[dict]):
    """Initialize the class.
    Args:
      piece_type (chess.PieceType): piece type.
      color (chess.Color): color of the team.
      square (chess.Square): location of the piece.
      genotype (Optional[dict]): genotype to be initialized.
    """
    super().__init__(piece_type, color)
    # If genotype not passed randomly initialize it
    self.genotype = self.set_random_genotype() if genotype is None else genotype

    self.square = square
    # At the start we have no belief
    self.belief = {}

    # Set starting state for hungers and turns still
    self.hunger = 0
    self.turns_still = 0

    
    
  def set_random_genotype(self):
    """Randomly initialize genotype."""
    genotype = {
      # Positional genes
      'radius': random.randint(2,7),
      'imm_danger': random.randint(-100,100),
      'hunger_lvl': random.randint(0,5),
      'turn': random.randint(0,5),
      'protection': random.randint(-100,100),

      # Action genes
      'capture': random.randint(-100,100),
      'fav_capture': random.randint(-100,100),
      'unf_capture': random.randint(-100,100),
      'dang_move': random.randint(-100,100),
      'def_move': random.randint(-100,100),
      'appr_opp_king': random.randint(-100,100), 
      'close_same_king': random.randint(-100,100), 
      'appr_high_value_opp_piece': random.randint(-100,100)
    }
    return genotype

  def get_genotype(self) -> dict:
    """Getter for the genotype."""
    return self.genotype
  

  def view_pieces(self, board: chess.Board) -> dict:
    """View the area of the board in radius and return a message.
    Args:
      board (chess.Board): Board of the game.
    Returns:
      dict: dictionary indexed by squares containing other pieces.
    """
    view = {}
    
    # Get piece position
    file = chess.square_file(self.square)
    rank = chess.square_rank(self.square)
    # Get view radius
    radius = self.get_genotype()['radius']

    # Iterate through all squares in radius
    for delta_file in range(-radius, radius + 1):
      for delta_rank in range(-radius, radius + 1):
        new_file = file + delta_file
        new_rank = rank + delta_rank

        # Stay inside board boundaries (0–7)
        if 0 <= new_file <= 7 and 0 <= new_rank <= 7:
          new_square = chess.square(new_file, new_rank)
          distance = math.trunc(math.sqrt(delta_file**2 + delta_rank**2))

          # Skip the piece itself
          if distance == 0:
            continue

          seen = board.piece_at(new_square)
          if seen:
            entry = {
              "piece": seen.piece_type,
              "color": seen.color
            }
          else:
            entry = {
              "piece": None,
              "color": None
            }

          view[new_square] = entry

    # Update belief
    self.belief = view

    # Can return only important pieces to broadcast to other agents
    msg = self.create_msg(view)

    return msg
  
  
  def create_msg(self, view: dict):
    """Given a view, filter low score pieces and returns only ones to broadcast to the teammates.
    Args:
      view (dict): View of the board.
    Returns:
      dict: message to broadcast to other pieces.  
    """
    msg = {}

    # Get the highest score in view
    highest_score = 1 # If we only see pawns, dont broadcast
    for entry in view.values():
      piece_type = entry["piece"]

      # Skip empty squares in radius
      if piece_type is None:
        continue

      score = get_piece_score(piece_type)
      if score > highest_score:
        highest_score = score

    # Get highest value pieces to broadcast
    for square, entry in view.items():
      piece_type = entry["piece"]
      color = entry["color"]

      # Skip empty squares in radius
      if piece_type is None:
        continue

      score = get_piece_score(piece_type)

      # Get king or highest value piece to broadcast
      if score == highest_score:
        msg[square] = {
          "piece": piece_type,
          "color": color
        }


    return msg
  

  def receive_msg(self, msg: dict):
    """Given a message, update belief adding only pieces not already known.
    Args:
      msg (dict): received message.
    """
    for square, entry in msg.items():
      msg_piece = entry["piece"]
      msg_color = entry["color"]

      # If never saw this square in view add It
      if square not in self.belief:
        self.belief[square] = {
          "piece": msg_piece,
          "color": msg_color
        }
      else:
        current_state = self.belief[square]
        current_piece = current_state["piece"]
        current_color = current_state["color"]

        # If current state wrong, update it
        if current_piece is None or current_piece != msg_piece or current_color != msg_color:
          self.belief[square] = {
          "piece": msg_piece,
          "color": msg_color
          }
          

  def get_square_states(self):

    # Init a dict that will hold the state for all 64 squares
    square_states = {square: {'attackers': [], 'protectors': []} for square in chess.SQUARES}

    # Create a new board from the agent belief
    belief_board = chess.Board()
    belief_board.clear()
    for square, entry in self.belief.items():
      if entry['piece'] is not None:
        piece = chess.Piece(entry['piece'], entry['color'])
        belief_board.set_piece_at(square, piece)
    
    # Add piece itself to board
    belief_board.set_piece_at(self.square, self)

    # Iterate on every piece on the board to know what are attacked squares
    for start_square, piece in belief_board.piece_map.items():
      # Get all squares attacked by this piece
      attacked_squares = belief_board.attacks(start_square)

      piece_info = {
        "piece": piece.piece_type,
        "color": piece.color
      }

      # Classify as attacked or protected based on color
      for end_squares in attacked_squares:
        if piece.color != self.color:
          square_states[end_squares]["attackers"].append(piece_info)
        else:
          square_states[end_squares]["protectors"].append(piece_info)
    return square_states

  
  def increase_hunger(self):
    self.hunger = self.hunger + 1

  def increase_turns_still(self):
    self.turns_still = self.turns_still +1

  def reset_hunger(self):
    self.hunger = 0

  def reset_turns_still(self):
    self.turns_still = 0


  # TODO
  def propose_move(self, board: chess.Board, legal_moves: list) -> tuple[chess.Move, int]:
    """Propose the best move for current piece."""
    state_score = 0 # Computed to be the same for every legal move

    # Get piece possible moves

    # State evaluation
    square_states = self.get_square_states()

    # Imminent danger
    attacking_pieces = square_states[self.square]["attackers"]
    if len(attacking_pieces) > 0:
      pass

    # Hunger

    # Turns still

    # Protection
    protecting_pieces = square_states[self.square]["protectors"]
    if len(protecting_pieces) > 0:
      pass
    

    # Update piece moves score
    for move in legal_moves:
      move_score = state_score

      # Capture (current move is a capture)

      # Favorable capture (current move is a capture and goes in a protected square)

      # Unfavorable capture (current move is a capture and goes in an attacked square)

      # Dangerous move (move not capure and goes in an attacked square)

      # Defended move (move not capure and goes in a protected square)

      # Approach opposing king (king is in belief and we get closer (just search for king in belief and compute distances))

      # Move Closer to Same Side King (opposing piece is in radius of king and we go closer to him (use belief))

      # Approach highest valued oppsoing piece (get closer to highest valued piece in belief, use distances and see if is closer)

    # Propose move with higher score

    return "", move_score

# PIECES

class King(Piece):
  def __init__(self, color: chess.Color, square: chess.Square, genotype: Optional[dict]):
    super().__init__(chess.KING, color, square, genotype)

class Queen(Piece):
  def __init__(self, color: chess.Color, square: chess.Square, genotype: Optional[dict]):
    super().__init__(chess.QUEEN, color, square, genotype)

class Rook(Piece):
  def __init__(self, color: chess.Color, square: chess.Square, genotypes: Optional[dict]):
    super().__init__(chess.ROOK, color, square, genotypes)

class Bishop(Piece):
  def __init__(self, color: chess.Color, square: chess.Square, genotype: Optional[dict]):
    super().__init__(chess.BISHOP, color, square, genotype)

class Knight(Piece):
  def __init__(self, color: chess.Color, square: chess.Square, genotype: Optional[dict]):
    super().__init__(chess.KNIGHT, color, square, genotype)

class Pawn(Piece):
  def __init__(self, color: chess.Color, square: chess.Square, genotype: Optional[dict]):
    super().__init__(chess.PAWN, color, square, genotype)
