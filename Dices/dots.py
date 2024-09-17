
class Dots:
    face = ['']

    def draw(self) -> str:
        return "\n".join(self.face)
    
    def get_face(self) -> list[str]:
        return self.face
    
    def __str__(self) -> str:
        return "\n".join(self.face)

class OneDot(Dots):
    face = [
        " ------- ",
        "|       |",
        "|   ●   |",
        "|       |",
        " ------- "
        ]
    
class TwoDots(Dots):
    face = [
        " ------- ",
        "| ●     |",
        "|       |",
        "|     ● |",
        " ------- "
        ]
   
class ThreeDots(Dots):
    face = [
        " ------- ",
        "| ●     |",
        "|   ●   |",
        "|     ● |",
        " ------- "
        ]

class FourDots(Dots):
    face = [
        " ------- ",
        "| ●   ● |",
        "|       |",
        "| ●   ● |",
        " ------- "
        ]

class FiveDots(Dots):
    face = [
        " ------- ",
        "| ●   ● |",
        "|   ●   |",
        "| ●   ● |",
        " ------- "
        ]

class SixDots(Dots):
    face = [
        " ------- ",
        "| ●   ● |",
        "| ●   ● |",
        "| ●   ● |",
        " ------- "
        ]
