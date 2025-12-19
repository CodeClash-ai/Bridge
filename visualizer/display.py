"""Display utilities for Bridge game visualization."""

POSITIONS = {0: "North", 1: "East", 2: "South", 3: "West"}
POSITION_SYMBOLS = {0: "N", 1: "E", 2: "S", 3: "W"}
SUIT_SYMBOLS = {"S": "♠", "H": "♥", "D": "♦", "C": "♣", "NT": "NT"}


def format_card(card: str) -> str:
    """Format a card with suit symbol."""
    if not card or len(card) < 2:
        return card
    rank = card[:-1]
    suit = card[-1]
    return f"{rank}{SUIT_SYMBOLS.get(suit, suit)}"


def format_bid(bid: str) -> str:
    """Format a bid with suit symbol."""
    if bid in ["PASS", "DOUBLE", "REDOUBLE"]:
        return bid
    if len(bid) >= 2:
        level = bid[0]
        suit = bid[1:]
        return f"{level}{SUIT_SYMBOLS.get(suit, suit)}"
    return bid


def print_header():
    """Print the visualizer header."""
    print("=" * 70)
    print("BRIDGE GAME VISUALIZER".center(70))
    print("=" * 70)


def print_section(title: str):
    """Print a section divider."""
    print("\n" + "-" * 70)
    print(f"  {title}")
    print("-" * 70)


def print_game_info(data: dict):
    """Print basic game information."""
    print_section("GAME INFORMATION")
    print(f"Game ID: {data.get('game_id', 'N/A')}")

    contract = data.get("contract")
    if contract:
        suit_symbol = SUIT_SYMBOLS.get(contract["suit"], contract["suit"])
        declarer = POSITIONS[contract["declarer"]]
        doubled = " DOUBLED" if contract.get("doubled") else ""
        redoubled = " REDOUBLED" if contract.get("redoubled") else ""
        print(f"Contract: {contract['level']}{suit_symbol}{doubled}{redoubled}")
        print(f"Declarer: {declarer}")

    tricks = data.get("tricks_won", {})
    print(f"\nTricks Won: NS={tricks.get('NS', 0)} | EW={tricks.get('EW', 0)}")

    raw_score = data.get("raw_score", {})
    print(f"Raw Score: NS={raw_score.get('NS', 0)} | EW={raw_score.get('EW', 0)}")

    norm_score = data.get("normalized_score", {})
    print(
        f"Normalized Score: NS={norm_score.get('NS', 0):.1f} | EW={norm_score.get('EW', 0):.1f}"
    )


def print_bidding_phase(bids: list, pause_callback=None):
    """Replay the bidding phase."""
    print_section("BIDDING PHASE")

    print("\n{:<8} {:<10} {:<10}".format("Round", "Position", "Bid"))
    print("-" * 35)

    round_num = 1
    for i, bid_record in enumerate(bids):
        position = bid_record["position"]
        bid = bid_record["bid"]
        pos_name = POSITIONS[position]
        formatted_bid = format_bid(bid)

        if i % 4 == 0 and i > 0:
            round_num += 1

        print(f"{round_num:<8} {pos_name:<10} {formatted_bid:<10}")

        if pause_callback:
            pause_callback()


def print_trick_header():
    """Print the trick table header."""
    print("\n{:<8} {:<10} {:<10} {:<15}".format("Trick", "Leader", "Winner", "Cards"))
    print("-" * 60)


def print_trick(trick_num: int, trick: list, pause_callback=None):
    """Display a single trick."""
    if not trick:
        return

    # Find leader and cards played
    leader_pos = trick[0]["position"]
    leader_name = POSITION_SYMBOLS[leader_pos]

    # Format cards in play order
    cards = []
    for play in trick:
        pos_symbol = POSITION_SYMBOLS[play["position"]]
        card = format_card(play["card"])
        cards.append(f"{pos_symbol}:{card}")

    # For now, we don't calculate winner (would need trump suit and lead suit logic)
    # Just display the trick
    cards_str = " ".join(cards)

    print(f"{trick_num:<8} {leader_name:<10} {'?':<10} {cards_str}")

    if pause_callback:
        pause_callback()


def print_playing_phase(tricks: list, pause_callback=None):
    """Replay the playing phase."""
    print_section("PLAYING PHASE")
    print_trick_header()

    for i, trick in enumerate(tricks):
        print_trick(i + 1, trick, pause_callback)


def clear_screen():
    """Clear the terminal screen."""
    import os

    os.system("clear" if os.name != "nt" else "cls")
