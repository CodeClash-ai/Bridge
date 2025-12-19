#!/usr/bin/env python3
"""Bridge game runner - executes a single bridge game with agent scripts."""

import argparse
import importlib.util
import json
import sys
from datetime import datetime
from pathlib import Path

# Add game_server to path
sys.path.insert(0, str(Path(__file__).parent / "game_server"))

from game import BridgeGame


def load_agent(agent_path: str, name: str):
    """Dynamically load an agent module."""
    spec = importlib.util.spec_from_file_location(f"agent_{name}", agent_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_game(agent_paths: list[str], seed: int = 0, dealer: int = 0) -> dict:
    """Run a single Bridge game with the given agents."""
    # Create game
    game = BridgeGame(seed=seed, dealer=dealer)

    # Load agents
    agents = []
    names = ['North', 'East', 'South', 'West']
    for i, path in enumerate(agent_paths):
        try:
            agent = load_agent(path, names[i])
            agents.append(agent)
            game.add_player(i, names[i])
        except Exception as e:
            print(f"Error loading agent {path}: {e}", file=sys.stderr)
            return {"error": f"Failed to load agent {i}: {e}"}

    # Start game
    if not game.start_game():
        return {"error": "Failed to start game"}

    # Bidding phase
    while game.phase == 'bidding':
        pos = game.current_player
        state = game.get_state(pos)

        agent_state = {
            'position': pos,
            'hand': state.get('hand', game.hands.get(pos, [])),
            'bids': state['bids'],
            'legal_bids': game.get_legal_bids(pos),
            'dealer': state['dealer'],
            'vulnerability': state['vulnerability'],
        }

        try:
            bid = agents[pos].get_bid(agent_state)
        except Exception as e:
            print(f"Agent {names[pos]} error in get_bid: {e}", file=sys.stderr)
            bid = "PASS"

        if not game.make_bid(pos, bid):
            game.make_bid(pos, "PASS")

    # Playing phase
    while game.phase == 'playing':
        pos = game.current_player
        state = game.get_state(pos)

        agent_state = {
            'position': pos,
            'hand': state.get('hand', game.hands.get(pos, [])),
            'current_trick': state['current_trick'],
            'legal_cards': game.get_legal_cards(pos),
            'contract': state['contract'],
            'tricks_won': state['tricks_won'],
        }

        try:
            card = agents[pos].play_card(agent_state)
        except Exception as e:
            print(f"Agent {names[pos]} error in play_card: {e}", file=sys.stderr)
            legal = game.get_legal_cards(pos)
            card = legal[0] if legal else None

        if card and not game.play_card(pos, card):
            legal = game.get_legal_cards(pos)
            if legal:
                game.play_card(pos, legal[0])

    return game.get_result()


def main():
    parser = argparse.ArgumentParser(description='Run a Bridge game')
    parser.add_argument('agents', nargs=4, help='Paths to 4 agent scripts')
    parser.add_argument('--seed', type=int, default=0, help='Random seed')
    parser.add_argument('--dealer', type=int, default=0, help='Dealer position (0-3)')
    parser.add_argument('--output-file', '-o', help='Output file for game results')

    args = parser.parse_args()

    result = run_game(args.agents, seed=args.seed, dealer=args.dealer)

    if args.output_file:
        # Create parent directory if it doesn't exist
        output_path = Path(args.output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write to the specified file
        output = json.dumps(result, indent=2)
        with open(output_path, 'w') as f:
            f.write(output)


if __name__ == '__main__':
    main()
