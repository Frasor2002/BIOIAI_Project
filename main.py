import json
from game import Game
from teacher_engine import TeacherEngine


if __name__ == "__main__":
  # Parse config file
  with open("config.json") as f:
    config = json.load(f)

  teacherEngine = TeacherEngine(config["stockfish_path"])
  teacherEngine.configStockfish(8, 20)

  game = Game()

  game.play_match(teacherEngine, None)