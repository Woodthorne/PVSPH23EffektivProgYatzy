
class Pips:
    face = ['']

    def draw(self) -> str:
        return "\n".join(self.face)
    
    def get_face(self) -> list[str]:
        return self.face
    
    def __str__(self) -> str:
        return "\n".join(self.face)

class OnePip(Pips):
    face = [
        " ------- ",
        "|       |",
        "|   ●   |",
        "|       |",
        " ------- "
        ]
    
class TwoPips(Pips):
    face = [
        " ------- ",
        "| ●     |",
        "|       |",
        "|     ● |",
        " ------- "
        ]
   
class ThreePips(Pips):
    face = [
        " ------- ",
        "| ●     |",
        "|   ●   |",
        "|     ● |",
        " ------- "
        ]

class FourPips(Pips):
    face = [
        " ------- ",
        "| ●   ● |",
        "|       |",
        "| ●   ● |",
        " ------- "
        ]

class FivePips(Pips):
    face = [
        " ------- ",
        "| ●   ● |",
        "|   ●   |",
        "| ●   ● |",
        " ------- "
        ]

class SixPips(Pips):
    face = [
        " ------- ",
        "| ●   ● |",
        "| ●   ● |",
        "| ●   ● |",
        " ------- "
        ]
