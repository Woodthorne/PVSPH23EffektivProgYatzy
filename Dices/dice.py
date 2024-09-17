import random
from typing import  Protocol, TypeVar

T = TypeVar('T')

class Face(Protocol):
    face : list[str]
    def draw(self) -> str:
        ...
    
    def get_face(self) -> list[str]:
        ...


class Side:
    """
    A side of a dice has a value and a face. A face may be a symbol, number, letter
    or text and follows the protocol Face!

    value = int
    face = Face
    """
    def __init__(self, value: T, face:Face) -> None:
        self._value = value
        self._face:Face = face

    @property
    def value(self) -> T:
        return self._value
    
    @property
    def face(self) -> Face:
        return self._face


class Dice:
    """
    A dice is a generic object that has n sides with symbols and values🎲
    """

    def __init__(self,sides:list[Side]) -> None:    

        self._sides = sides
        self._nr_of_sides = len(sides)
        self.roll()


    @property
    def side_up(self) -> Side:
        return self._side_up
    
    @property
    def nr_of_sides(self) -> int:
        return self._nr_of_sides

    def roll(self):
        self._side_up = random.choice(self._sides)

