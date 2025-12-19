# Bridge Game Visualizer

A command-line tool to replay and visualize Bridge games from JSON log files.

## Features

- **Bidding Phase Replay**: See all bids in order with player positions
- **Playing Phase Replay**: Watch each trick unfold card by card
- **Interactive or Auto Mode**: Step through manually or auto-play
- **Suit Symbols**: Pretty display with ♠ ♥ ♦ ♣ symbols
- **Flexible Viewing**: View full game, bidding only, or tricks only

## Usage

### Basic Usage

```bash
# Interactive mode (press Enter to advance)
python visualizer/visualize.py logs/game.json

# Auto-play mode with 1 second delay
python visualizer/visualize.py logs/game.json --auto

# Auto-play with custom delay
python visualizer/visualize.py logs/game.json --auto --delay 0.5
```

### View Specific Phases

```bash
# Show only bidding phase
python visualizer/visualize.py logs/game.json --bidding-only

# Show only playing phase (tricks)
python visualizer/visualize.py logs/game.json --tricks-only
```

### Command-Line Options

- `log_file`: Path to the game log JSON file (required)
- `--auto`, `-a`: Auto-play mode (no manual pauses)
- `--delay`, `-d`: Delay between steps in auto-play mode (default: 1.0 seconds)
- `--bidding-only`, `-b`: Show only the bidding phase
- `--tricks-only`, `-t`: Show only the playing phase

## Examples

```bash
# Quick review of a game
./visualizer/visualize.py logs/20251218_160143_603801.json --auto --delay 0.3

# Study the bidding carefully
./visualizer/visualize.py logs/20251218_160143_603801.json -b

# Analyze trick play step by step
./visualizer/visualize.py logs/20251218_160143_603801.json -t
```

## Output Format

The visualizer displays:
1. **Game Information**: Game ID, contract, declarer, scores
2. **Bidding Phase**: Round-by-round bidding sequence
3. **Playing Phase**: All 13 tricks with cards played by each position

## Module Structure

- `visualize.py`: Main entry point and command-line interface
- `display.py`: Display formatting and rendering functions
- `replay.py`: Game replay controller with pause/auto-play logic
