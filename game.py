import via, pyspiel, random, sys
from open_spiel.python.algorithms import mcts


sims   = 1000 if len(sys.argv) < 2 else int(sys.argv[1])
is_bot = True if sims < 0 else False
sims   = abs(sims)
game   = pyspiel.load_game("via")
state  = game.new_initial_state()
evals  = mcts.RandomRolloutEvaluator(n_rollouts=5)
bot    = mcts.MCTSBot(
    game,
    uct_c           = 2**0.5,
    max_simulations = sims,
    evaluator       = evals,
    solve           = True,
    verbose         = False)

print ("MCTS simulations:", sims)
print ("Player 1:", "bot" if is_bot else "human",
       "Player 2:", "bot\n")

while not state.is_terminal():
    print(state)
    p = state.current_player()
    if is_bot:
        state.apply_action(bot.step(state))
        continue
    if p == 0:
        legal = state.legal_actions()
        a     = input("Your action (row,col): ").split(",")
        r, c  = int(a[0]), int(a[1])
        x     = state.to_1d(r,c)
        if x not in legal:
            print("Illegal move.")
            continue
        state.apply_action(x)
    else:
        state.apply_action(bot.step(state))

print(state)
returns = state.returns()
print("Terminal returns:", returns)
