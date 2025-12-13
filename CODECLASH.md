# [CodeClash] Bridge
This is the starter codebase for the Bridge arena featured in CodeClash.

This codebase is heavily inspired by open source implementations, such as [here](https://github.com/jyang001/Bridge-Card-Game), [here](https://github.com/AGI-Eval-Official/CATArena/tree/main/bridgegame), and [here](https://github.com/jasujm/bridge?tab=readme-ov-file).
Our implementation aims to be lightweight - we maintain a simple `game_server/` that runs bridge, along with the `run_game.py` script to invoke a game.
The `bridge_agent.py` file is a basic, starter implementation of a bridge agent that simply does random actions.