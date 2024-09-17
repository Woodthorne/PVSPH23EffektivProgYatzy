from .dice import Dice, Side
from .dots import OneDot,TwoDots,ThreeDots,FourDots,FiveDots,SixDots
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
        Side(val.ONE, OneDot()),
        Side(val.TWO, TwoDots()),
        Side(val.THREE, ThreeDots()),
        Side(val.FOUR, FourDots()),
        Side(val.FIVE, FiveDots()),
        Side(val.SIX, SixDots())
        ]
    )