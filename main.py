from Dices.regular_dice import create_regular_six_sided_dice
from Dices.dice import Die

#########################################################
# Ska rensas
def throw(dice:list[Die]) -> None:
    for die in dice:
        die.roll()

def draw_dice_horizontal(dice: list[Die]) -> str:
    dice_faces = [die.side_up.face.get_face() for die in dice]
    dice_string = ''
    for row in range(len(dice_faces[0])):
        for die in dice_faces:
            dice_string += die[row] + ' '

        dice_string += '\n'
    
    return dice_string
#########################################################

def main():
    five_dice = [create_regular_six_sided_dice() for _ in range(5)]
    throw(five_dice)    
    print(draw_dice_horizontal(five_dice))
    throw(five_dice)    
    print(draw_dice_horizontal(five_dice))
    throw(five_dice[:3])
    print(draw_dice_horizontal(five_dice))


if __name__ == '__main__':
    main()