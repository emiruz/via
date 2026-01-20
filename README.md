# Via (aka Routes)

Via ("route" in Italian and Latin) is a simple abstract
pen-and-paper 2 player strategy game. Its played on a
square grid with an even number of cells (e.g. 6x6, 8x8).
The players pick different colours and take turns colouring
in a square. A player wins by either making a route of
connected cells between opposing sides (left to right, top
to bottom), or by having the biggest connected block of
cells when no further moves are possible. Two cells are
connected if they are adjacent (diagonals are not
connected).

For example, green wins the following game because they
connected top to bottom.

```
    1  2  3  4  5  6
1  🟥  · 🟥 🟩  ·  ·
2   · 🟥 🟩 🟩  · 🟩
3   · 🟩 🟩 🟥 🟩 🟥
4   · 🟩 🟥  ·  ·  ·
5   · 🟩 🟥 🟩 🟥 🟥
6   · 🟩  · 🟥  ·  ·
```

Green wins the following game because they have the biggest
connected block (11 green cells, to 9 red).

```
    1  2  3  4  5  6
1  🟥 🟩 🟩 🟩 🟥 🟩
2  🟩 🟩 🟩 🟩 🟥 🟩
3  🟩 🟥 🟥 🟩 🟩 🟥
4  🟥 🟥 🟥 🟩 🟥 🟥
5  🟥 🟩 🟥 🟥 🟩 🟥
6  🟥 🟩 🟩 🟩 🟥 🟥
```

## Contents

This repository contains the *via* game as implemented in
the DeepMind "Open Spiel" framework, and a Monte Carlo Tree
Search (MCTS) based bot. 


## Setup

```
git clone https://github.com/emiruz/pyevidence.git
pip install open_spiel
```

## Play

Here are some examples of how to invoke the game script.
Use `300` for easy, `1000`, `2000` for hard and `5000`
for very hard.

To lay a game against the bot with default settings.
```
python3 game.py
```

To play a game against the bot with a calculation budget
of 5000 simulations.
```
python3 game.py 5000
```

To watch two bots play each with a calculaion budget
of 2000 MCTS simulations.
```
python3 game.py -2000
```

Here is an example of a human vs bot game invocation
with a 1000 MCTS simulation calculation budget. To
make a move type the row and column coordinate separated
by a comma.

```
>> python3 game.py 1000

MCTS simulations: 1000
Player 1: human Player 2: bot

  1 2 3 4 5 6
1 · · · · · · 
2 · · · · · · 
3 · · · · · · 
4 · · · · · · 
5 · · · · · · 
6 · · · · · · 

Your action (row,col): 3,2
```

For example, to mark cell at row `3` and column `2` you
would type `3,2`. The bot will then make its move and
return control to the human player.
