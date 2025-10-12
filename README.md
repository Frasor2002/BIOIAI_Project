<div align="center">

# Bio-Inspired AI Project

</div>

Project for the "Bio-Inspired Artificial Intelligence" course at University of Trento.

## Installation and Execution
Follow the steps to run the project code:

1. Clone the repository:
   ```sh
   git clone https://github.com/Frasor2002/BIOIAI_Project.git
   cd BIOIAI_Project
   ```

2. Install modules:
   ```sh
   pip install -r requirements.txt
   ```

3. The project requires the Stockfish chess engine to run properly so it needs to be dowloaded on the machine. 
It can be dowloaded from: 
https://stockfishchess.org/download/ for every system.
An alternative linux installation can be done by running:
  ```sh
   apt-get install stockfish
   ```


4. Before running the project a `config.json` file must be created setting the stockfish path like in the example file `config.example.json`. If Stockfish has been installed with the linux method usually is in the path `usr/games/stockfish`.

5. To run the project the command is:
```sh
  python main.py
```