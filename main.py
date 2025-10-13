import json
import argparse
import chess
import random

from game import Game
from teacher_engine import TeacherEngine
from agent import Agent
from utils import str_color


if __name__ == "__main__":

  # Get command line args
  parser = argparse.ArgumentParser()
  parser.add_argument('-c', '--agent_color', type=str, choices=['white', 'black', 'random'], default="white", help="Agent piece color")
  args = parser.parse_args()

  # Parse config file
  with open("config.json") as f:
    config = json.load(f)

  # Define agent piece colors
  agent_color = None
  if args.agent_color == 'random': 
    agent_color = random.choice([chess.WHITE, chess.BLACK])
  else: 
    agent_color = chess.WHITE if args.agent_color == 'white' else chess.BLACK
  engine_color = chess.WHITE if agent_color == chess.BLACK else chess.BLACK

  teacherEngine = TeacherEngine(config["stockfish_path"], engine_color)
  teacherEngine.config_stockfish(8, 20)
  agent = Agent(agent_color, None)

  if agent_color == chess.WHITE:
    print(f"Playing: Agent ({str_color(agent_color)}), Stockfish ({str_color(engine_color)})")
  else:
    print(f"Playing: Stockfish ({str_color(engine_color)}), Agent ({str_color(agent_color)})")

  game = Game()
  result = game.play_match(teacherEngine, agent)
  print("game.play_match result:", result)