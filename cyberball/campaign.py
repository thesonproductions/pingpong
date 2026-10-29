"""Short Lab Tour challenges built on top of the original Cyberball engine."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Challenge:
    number: int
    name: str
    objective: str
    difficulty: str
    points: int
    seconds: int
    boss: bool = False
    chaos: bool = False


CHALLENGES = (
    Challenge(1, "ROOKIE BOT", "Learn to return the ball.", "easy", 3, 65),
    Challenge(2, "SMART TRACKER", "Outplay a faster opponent.", "medium", 3, 70),
    Challenge(3, "PREDICTOR PRO", "Beat its ball-intercept strategy.", "hard", 3, 75),
    Challenge(4, "CHAOS ARENA", "Survive power-up storms.", "extreme", 3, 80, chaos=True),
    Challenge(5, "BOSS GAUNTLET", "Face the Titan boss.", "extreme", 3, 90, boss=True, chaos=True),
)


def challenge(number):
    if not 1 <= number <= len(CHALLENGES):
        raise ValueError("Challenge must be 1..5")
    return CHALLENGES[number - 1]
