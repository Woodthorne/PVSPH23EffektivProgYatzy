from dataclasses import dataclass
from enum import Enum


@dataclass
class Player:
    name:str

    def __hash__(self) -> int:
        return hash(self.name)

class ScoreSlotsEnum(Enum):
    ONES = 1
    TWOS = 2
    THREES = 3
    FOURS = 4
    FIVES = 5
    SIXES = 6
    BONUS = 7
    ONE_PAIR = 8
    TWO_PAIR = 9
    THREE_OF_A_KIND = 10
    FOUR_OF_A_KIND = 11
    SMALL_STRAIGHT = 12
    LARGE_STRAIGHT = 13
    FULL_HOUSE = 14
    CHANCE = 15
    YATZY = 16
    TOTAL_SCORE = 17

def score_slot_dict() -> dict[ScoreSlotsEnum,None]:
    return {slot:None for slot in list(ScoreSlotsEnum)}

class ScoreSheet:

    def __init__(self, players:list[Player]) -> None:
        self._players = {player:score_slot_dict() for player in players}

    def write_points(
            self, 
            player:Player, 
            slot:ScoreSlotsEnum,
            points:int
            ) -> None:
        
        if self._players[player][slot] == None:
            message = f'Score already set for {slot.name} for player:{player}!'
            raise ValueError(message)
        
        self._players[player][slot] = points

    def calculate_bonus(self, player:Player, threshold:int=63, bonus:int=50) -> None:
        """Assumes that values for ones, twos, threes, fours, fives and sixes are set!"""
        sc = ScoreSlotsEnum

        bonus_criteria = [
            sc.ONES, 
            sc.TWOS,
            sc.THREES,
            sc.FOURS,
            sc.FIVES,
            sc.SIXES
            ]
        
        points = sum(self._players[player][slot] for slot in bonus_criteria)

        self._players[player][sc.BONUS] = bonus if points >= threshold else 0

    
    def calculate_points(self, player:Player) -> None:
        total_score = ScoreSlotsEnum.TOTAL_SCORE

        to_be_summed = list(ScoreSlotsEnum)

        to_be_summed.remove(total_score)

        self._players[player][total_score] = sum(self._players[player][slot] for slot in to_be_summed)


    def get_unscored_slots(self, player:Player) -> list[ScoreSlotsEnum]:
        return [slot for slot,val in self._players[player].items() if val == None]
