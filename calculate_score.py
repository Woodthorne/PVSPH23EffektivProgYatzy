from Dices.dice import Die
from Dices.regular_dice import RegularDieValuesEnum
from score_sheet import ScoreSlotsEnum
from collections import defaultdict
from typing import Callable


class CalculateScore:
    """
    This class calculates score/points for playing Yatsy.
    
    Assumes the game is played with regular dice! -> ⚀⚁⚂⚃⚄⚅

    Returns 0 if invalid collection of dice is passed for specific method.

    Exampel: if ⚃⚄⚄⚄⚄ is passed to two_pairs the result would be 0
    since there ain't two valid pairs among the five dice.


    """
    def __init__(self) -> None:
        self.rdv = RegularDieValuesEnum    

    def ones(self, dice:list[Die]) -> int:
        return self._single_values(dice, ScoreSlotsEnum.ONES)
    
    def twos(self, dice:list[Die]) -> int:
        return self._single_values(dice, ScoreSlotsEnum.TWOS)
    
    def threes(self, dice:list[Die]) -> int:
        return self._single_values(dice, ScoreSlotsEnum.THREES)
        
    def fours(self, dice:list[Die]) -> int:
        return self._single_values(dice, ScoreSlotsEnum.FOURS)
    
    def fives(self, dice:list[Die]) -> int:
        return self._single_values(dice, ScoreSlotsEnum.FIVES)

    def sixes(self, dice:list[Die]) -> int:
        return self._single_values(dice, ScoreSlotsEnum.SIXES)
    
    def one_pair(self, dice:list[Die]) -> int:
        unique_dice_frequency = self._get_frequency_of_unique_die_values(dice)
        nr_unique_dice = len(unique_dice_frequency)

        if nr_unique_dice == 5: 
            return 0

        elif nr_unique_dice == 4:
            max_value_pair = max(unique_dice_frequency, key=lambda x: unique_dice_frequency[x])
        
        elif nr_unique_dice >= 2:
            pair1, pair2 = [d for d,freq in unique_dice_frequency.items() if freq > 1]
            max_value_pair = pair1 if pair1.value > pair2.value else pair2

        else:
            max_value_pair = list(unique_dice_frequency)[0]

        return 2 * max_value_pair.value 


    def two_pais(self, dice:list[Die]) -> int:
        unique_dice_frequency = self._get_frequency_of_unique_die_values(dice)
        nr_unique_dice = len(unique_dice_frequency)

        if nr_unique_dice >= 4 or nr_unique_dice == 1: 
            return 0

        if 4 in unique_dice_frequency.values(): 
            return 0

        pair1,pair2 = [d for d,freq in unique_dice_frequency.items() if freq > 1]

        return 2 * pair1.value + 2 * pair2.value


    def three_of_a_kind(self, dice:list[Die]) -> int:
        unique_dice_frequency = self._get_frequency_of_unique_die_values(dice)
        nr_unique_dice = len(unique_dice_frequency)

        if nr_unique_dice > 3: return 0

        three_dices = max(unique_dice_frequency, key=lambda x: unique_dice_frequency[x])
        return 3 * three_dices.value 


    def four_of_a_kind(self, dice:list[Die]) -> int:
        unique_dice_frequency = self._get_frequency_of_unique_die_values(dice)
        nr_unique_dice = len(unique_dice_frequency)

        if nr_unique_dice > 2: return 0

        four_dices = max(unique_dice_frequency, key=lambda x: unique_dice_frequency[x])
        return 4 * four_dices.value 


    def small_straight(self, dice:list[Die]) -> int:
        unique_dice_frequency = self._get_frequency_of_unique_die_values(dice)
        nr_unique_dice = len(unique_dice_frequency)

        if nr_unique_dice != 5: return 0

        small_s = [
            self.rdv.ONE,
            self.rdv.TWO,
            self.rdv.THREE,
            self.rdv.FOUR,
            self.rdv.FIVE
            ]
        
        if all([True if dv in unique_dice_frequency else False for dv in small_s]):
            return 15
        else:
            return 0

    def large_straight(self, dice:list[Die]) -> int:
        unique_dice_frequency = self._get_frequency_of_unique_die_values(dice)
        nr_unique_dice = len(unique_dice_frequency)

        if nr_unique_dice != 5: return 0

        large_s = [
            self.rdv.TWO,
            self.rdv.THREE,
            self.rdv.FOUR,
            self.rdv.FIVE,
            self.rdv.SIX
            ]

        if all([True if dv in unique_dice_frequency else False for dv in large_s]):
            return 15
        else:
            return 0

    def full_house(self, dice:list[Die]) -> int:
        unique_dice_frequency = self._get_frequency_of_unique_die_values(dice)

        if len(unique_dice_frequency) != 2: 
            return 0

        if any((True for freq in unique_dice_frequency.values() if freq > 3)):
            return 0
        
        return sum([d.value*count for d,count in unique_dice_frequency.items()])


    def chance(self, dice:list[Die]) -> int:
        unique_dice_frequency = self._get_frequency_of_unique_die_values(dice)

        return sum([d.value*count for d,count in unique_dice_frequency.items()])


    def yatzy(self, dice:list[Die]) -> int:
        unique_dice_frequency = self._get_frequency_of_unique_die_values(dice)

        return 50 if len(unique_dice_frequency) == 1 else 0


    def get_method_by_ScoreSlotsEnum(self, slot:ScoreSlotsEnum) -> Callable[[list[Die]],int]|None:
        """Returns method for current class given a specific ScoreSlotsEnum"""
        match slot:
            case ScoreSlotsEnum.ONES: self.ones
            case ScoreSlotsEnum.TWOS: self.twos
            case ScoreSlotsEnum.THREES: self.threes
            case ScoreSlotsEnum.FOURS: self.fours
            case ScoreSlotsEnum.FIVES: self.fives
            case ScoreSlotsEnum.SIXES: self.sixes
            case ScoreSlotsEnum.ONE_PAIR: self.one_pair
            case ScoreSlotsEnum.TWO_PAIR: self.two_pais
            case ScoreSlotsEnum.THREE_OF_A_KIND: self.three_of_a_kind
            case ScoreSlotsEnum.FOUR_OF_A_KIND: self.four_of_a_kind
            case ScoreSlotsEnum.SMALL_STRAIGHT: self.small_straight
            case ScoreSlotsEnum.LARGE_STRAIGHT: self.large_straight
            case ScoreSlotsEnum.FULL_HOUSE: self.full_house
            case ScoreSlotsEnum.CHANCE: self.chance
            case ScoreSlotsEnum.YATZY: self.yatzy
            case _:
                raise None

    def _get_dice_values(self, dice:list[Die]) -> list[RegularDieValuesEnum]:
        return [d.side_up.value for d in dice]


    def _get_frequency_of_unique_die_values(self, dice:list[Die]) -> dict[RegularDieValuesEnum,int]:
        """
        Returns a dictionary with the frequence of occuring dice.
        Example: ⚀⚁⚄⚁⚄ -> {⚀:1, ⚁:2, ⚄:2}
        """
        dice_values = self._get_dice_values(dice)

        unique_dice_frequency = defaultdict(int)

        for val in dice_values:
            unique_dice_frequency[val] += 1

        return unique_dice_frequency
    
    def _single_values(self, dice: list[Die], sc: ScoreSlotsEnum) -> int:
        """
        Function to calculate either ones, twos, threes, fours, fives or sixes!
        """

        match sc:
            case ScoreSlotsEnum.ONES: dv = self.rdv.ONE
            case ScoreSlotsEnum.TWOS: dv = self.rdv.TWO
            case ScoreSlotsEnum.THREES: dv = self.rdv.THREE
            case ScoreSlotsEnum.FOURS: dv = self.rdv.FOUR
            case ScoreSlotsEnum.FIVES: dv = self.rdv.FIVE
            case ScoreSlotsEnum.SIXES: dv = self.rdv.SIX
            case _:
                raise ValueError('Can only calculate ones, twos, threes, fours, fives or sixes!')

        dice_values = self._get_dice_values(dice)
        nr_of_dice = dice_values.count(dv)
        return nr_of_dice * dv.value