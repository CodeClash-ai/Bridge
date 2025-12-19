"""Bridge game replay controller."""

import json
import sys
import time
from pathlib import Path


class GameReplay:
    """Controller for replaying a bridge game from logs."""

    def __init__(self, log_file: str, auto_play: bool = False, delay: float = 1.0):
        """
        Initialize game replay.

        Args:
            log_file: Path to the JSON log file
            auto_play: If True, automatically advance through game
            delay: Delay in seconds between steps (for auto_play)
        """
        self.log_file = Path(log_file)
        self.auto_play = auto_play
        self.delay = delay
        self.data = None

    def load(self) -> bool:
        """Load the game log file."""
        try:
            with open(self.log_file, "r") as f:
                self.data = json.load(f)
            return True
        except FileNotFoundError:
            print(f"Error: Log file not found: {self.log_file}", file=sys.stderr)
            return False
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in log file: {self.log_file}", file=sys.stderr)
            return False

    def pause(self):
        """Handle pause between steps."""
        if self.auto_play:
            time.sleep(self.delay)
        else:
            input("\nPress Enter to continue...")

    def get_data(self) -> dict:
        """Get the loaded game data."""
        return self.data
