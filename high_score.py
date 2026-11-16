"""Keep the high score between games in a small JSON file."""

import json
from pathlib import Path

# Next to the code, wherever the game is started from.
HIGH_SCORE_FILE = Path(__file__).parent / "high_score.json"


def load_high_score(path: Path) -> int:
    """Return the high score saved in path, or 0 if there is none.

    A missing, unreadable or damaged file counts as no high score, so a
    bad file can never stop the game from starting.
    """
    try:
        data = json.loads(path.read_text())
    except (OSError, ValueError):
        # OSError: missing or unreadable file.
        # ValueError: not valid JSON, or not valid text at all.
        return 0

    score = data.get("high_score") if isinstance(data, dict) else None
    # bool is a subclass of int in Python, so rule it out explicitly.
    if isinstance(score, int) and not isinstance(score, bool) and score >= 0:
        return score
    return 0


def save_high_score(path: Path, score: int) -> None:
    """Save score as the high score in path.

    Write a temporary file first, then swap it in, so a crash halfway
    through can never leave a half-written file behind.
    """
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps({"high_score": score}) + "\n")
    temporary.replace(path)
