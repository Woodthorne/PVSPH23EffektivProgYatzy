from Dices.regular_dice import create_regular_six_sided_dice
from Dices.dice import Dice

#########################################################
# Ska rensas
def throw(dices:list[Dice]) -> None:
    for dice in dices:
        dice.roll()

def draw_dices_horizontal(dices:list[Dice]) -> str:
    d = [dice.side_up.face.get_face() for dice in dices]
    dice_string = ''
    for row in range(len(d[0])):
        for dice in d:
            dice_string += dice[row] + ' '

        dice_string += '\n'
    
    return dice_string
#########################################################

def main():
    five_dices = [create_regular_six_sided_dice() for _ in range(5)]
    throw(five_dices)    
    print(draw_dices_horizontal(five_dices))
    throw(five_dices)    
    print(draw_dices_horizontal(five_dices))
    throw(five_dices[:3])
    print(draw_dices_horizontal(five_dices))


if __name__ == '__main__':
    main()