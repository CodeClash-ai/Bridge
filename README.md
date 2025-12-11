# Bridge Arena Game Server

This repository contains the game server and bot examples for the **Bridge** arena in [CodeClash](https://github.com/CodeClash-ai/CodeClash).

## Overview

Bridge is a 4-player trick-taking card game played in teams:
- **North/South** (positions 0/2) vs **East/West** (positions 1/3)

## Repository Structure

```
Bridge/
├── game_server/          # Core game logic
│   ├── game.py           # BridgeGame class - main game state manager
│   ├── deck.py           # Card deck management and comparison
│   └── scoring.py        # Bridge scoring rules
├── examples/
│   └── random_agent.py   # Example bot implementation
└── README.md
```

## Bot Interface

Your bot must implement two functions in `bridge_agent.py`:

### `get_bid(game_state) -> str`

Make bidding decisions during the auction phase.

**game_state contains:**
- `position`: Your position (0=North, 1=East, 2=South, 3=West)
- `hand`: List of cards in your hand (e.g., `["AS", "KH", "7D"]`)
- `bids`: List of previous bids
- `legal_bids`: List of legal bids you can make
- `dealer`: Position of the dealer
- `vulnerability`: Which teams are vulnerable

**Returns:** A bid string like `"PASS"`, `"1H"`, `"2NT"`, `"3S"`

### `play_card(game_state) -> str`

Play a card during the playing phase.

**game_state contains:**
- `position`: Your position (0=North, 1=East, 2=South, 3=West)
- `hand`: List of cards currently in your hand
- `current_trick`: Cards played so far in current trick
- `legal_cards`: List of legal cards you can play
- `contract`: The current contract (level, suit, declarer)
- `tricks_won`: Tricks won by each team so far

**Returns:** A card string like `"AS"`, `"7H"`, `"KD"`

## Card Notation

- Cards are represented as 2 characters: `<rank><suit>`
- **Ranks:** A, K, Q, J, T (10), 9, 8, 7, 6, 5, 4, 3, 2
- **Suits:** S (Spades), H (Hearts), D (Diamonds), C (Clubs)
- Examples: `"AS"` = Ace of Spades, `"7H"` = 7 of Hearts, `"TD"` = 10 of Diamonds

## Bidding

- **Pass:** `"PASS"`
- **Suit bids:** Level (1-7) + Suit (C, D, H, S, NT)
  - Examples: `"1H"`, `"2NT"`, `"4S"`, `"7NT"`

## Scoring

Games are scored using standard Bridge scoring rules, then normalized to Victory Points (VP) on a 0-1 scale.

## Example Bot

See `examples/random_agent.py` for a simple random bot implementation.

```python
def get_bid(game_state):
    legal_bids = game_state.get("legal_bids", ["PASS"])
    # Your bidding logic here
    return "PASS"

def play_card(game_state):
    legal_cards = game_state.get("legal_cards", [])
    # Your card playing logic here
    return legal_cards[0]
```

## License

MIT License - See CodeClash repository for details.
