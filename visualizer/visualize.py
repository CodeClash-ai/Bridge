#!/usr/bin/env python3
"""Bridge game visualizer - replay games from log files."""

import argparse
import sys

from display import (
    print_header, 
    print_game_info, 
    print_bidding_phase, 
    print_playing_phase,
    clear_screen
)
from replay import GameReplay


def visualize_game(log_file: str, auto_play: bool = False, delay: float = 1.0, 
                   bidding_only: bool = False, tricks_only: bool = False):
    """
    Visualize a bridge game from a log file.
    
    Args:
        log_file: Path to the JSON log file
        auto_play: If True, automatically advance through game
        delay: Delay in seconds between steps (for auto_play)
        bidding_only: If True, only show bidding phase
        tricks_only: If True, only show playing phase
    """
    # Create replay controller
    replay = GameReplay(log_file, auto_play=auto_play, delay=delay)
    
    # Load the game
    if not replay.load():
        return 1
    
    data = replay.get_data()
    
    # Clear screen and show header
    if not auto_play:
        clear_screen()
    
    print_header()
    print_game_info(data)
    
    # Show bidding phase
    if not tricks_only:
        bids = data.get('bids', [])
        if bids:
            print_bidding_phase(bids, pause_callback=replay.pause if not auto_play else None)
            if not bidding_only:
                replay.pause()
    
    # Show playing phase
    if not bidding_only:
        tricks = data.get('played_tricks', [])
        if tricks:
            print_playing_phase(tricks, pause_callback=replay.pause if not auto_play else None)
    
    print("\n" + "=" * 70)
    print("Game replay complete!")
    print("=" * 70 + "\n")
    
    return 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Visualize Bridge game from log files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s logs/game.json                    # Interactive replay
  %(prog)s logs/game.json --auto             # Auto-replay with 1s delay
  %(prog)s logs/game.json --auto --delay 0.5 # Auto-replay with 0.5s delay
  %(prog)s logs/game.json --bidding-only     # Show only bidding
  %(prog)s logs/game.json --tricks-only      # Show only tricks
        """
    )
    
    parser.add_argument(
        'log_file',
        help='Path to the game log JSON file'
    )
    
    parser.add_argument(
        '--auto', '-a',
        action='store_true',
        help='Auto-play mode (no manual pauses)'
    )
    
    parser.add_argument(
        '--delay', '-d',
        type=float,
        default=1.0,
        help='Delay between steps in auto-play mode (default: 1.0 seconds)'
    )
    
    parser.add_argument(
        '--bidding-only', '-b',
        action='store_true',
        help='Show only the bidding phase'
    )
    
    parser.add_argument(
        '--tricks-only', '-t',
        action='store_true',
        help='Show only the playing phase (tricks)'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.bidding_only and args.tricks_only:
        print("Error: Cannot specify both --bidding-only and --tricks-only", 
              file=sys.stderr)
        return 1
    
    return visualize_game(
        args.log_file,
        auto_play=args.auto,
        delay=args.delay,
        bidding_only=args.bidding_only,
        tricks_only=args.tricks_only
    )


if __name__ == '__main__':
    sys.exit(main())
