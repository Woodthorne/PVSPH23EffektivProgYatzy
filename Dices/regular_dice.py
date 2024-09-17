from .dice import Dice, Side
from .dots import OnePip, TwoPips, ThreePips, FourPips, FivePips, SixPips
from enum import Enum

class RegularDiceValuesEnum(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6


def create_regular_six_sided_dice() -> Dice:
    val = RegularDiceValuesEnum
    return Dice(
        [
        Side(val.ONE, OnePip()),
        Side(val.TWO, TwoPips()),
        Side(val.THREE, ThreePips()),
        Side(val.FOUR, FourPips()),
        Side(val.FIVE, FivePips()),
        Side(val.SIX, SixPips())
        ]
    )