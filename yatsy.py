from score_sheet import ScoreSheet, ScoreSlotsEnum, Player
from calculate_score import ScoreSlotsEnum, CalculateScore
from Dices.regular_dice import create_regular_six_sided_dice, Side
from Dices.dice import Face
from functools import wraps

class Yatzy:
    """
    Main class for playing Yatzy! 

    There is 5 dices, id 1,2,3,4 and 5 to play with.

    To start the game, invoke the start_game method! ⚠️Elsewise some methods are in a invalid state!⚠️

    Play the game by rolling the dices for current player and set points for choosen slot! 
    The game will write 0 points to a slot if an invalid dice setup is passed to that slot.
    You have 3 rolls per player per turn. After that you must choose a open slot for current player. 
    Next players turn will automaticly be set after current player has set his points.
    """
    ROUNDS = 13

    def __init__(self, players:list[Player]) -> None:
        self._players = players.copy()
        self._score_sheet = ScoreSheet(players)
        self._game_dices = {dice_id:create_regular_six_sided_dice() for dice_id in range(1,6)}
        self._score_calculator = CalculateScore()
        self._game_started = False
        self._is_done = False


    def roll_counter(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if self._current_players_roll_count < 3:
                resultat = func(self, *args, **kwargs)
                self._current_players_roll_count += 1
            else:
                resultat = None
            # could implemet some logic to signal that player must set_current_players_point!
            return resultat
        return wrapper

    @roll_counter
    def roll_all_dices(self) -> None:
        for dice in self._game_dices.values(): 
            dice.roll()

    @roll_counter
    def roll_a_subset_of_dices(self, dice_ids:list[int]) -> None:
        for dice_id in dice_ids:
            self._game_dices[dice_id].roll()


    def get_dices_side_up(self) -> list[Side]:
        return [d.side_up for d in self._game_dices.values()]


    def get_current_players_turn(self) -> Player:
        return self._current_players_turn


    def get_current_players_unscored_slots(self) -> list[ScoreSlotsEnum]:
        return self._score_sheet.get_unscored_slots(self._current_players_turn)


    def set_current_players_score(self, slot:ScoreSlotsEnum) -> None:
        method = self._score_calculator.get_method_by_ScoreSlotsEnum(slot)

        if not method: 
            raise ValueError(f"Error occured when trying to fetch method for slot:{slot}!")
        
        points = method(self._game_dices.values())

        if self._score_sheet.write_points(
            self._current_players_turn,
            slot,
            points):
            self._start_next_players_turn()
            return True
        return False

    def start_game(self) -> None:
        assert not self._game_started
        self._game_started = True
        self._round = 0
        self._start_new_round()


    def _start_next_players_turn(self) -> None:
        try:
            self._current_players_turn = next(self._player_sequens_turns)
        except StopIteration:
            self._start_new_round()


    def _end_game(self) -> None:
        for player in self._players:
            self._score_sheet.calculate_bonus(player)
            self._score_sheet.calculate_points(player)


    def _start_new_round(self) -> None:
        if self._round < 15:
            self._round += 1
            self._player_sequens_turns = iter(player for player in self._players)
            self._current_players_turn = next(self._player_sequens_turns)
            self._current_players_roll_count = 0
        else:
            self._is_done = True
            self._end_game()


def draw_faces_horizontal(faces:list[Face]) -> str:
    f = [face.get_face() for face in faces]
    face_string = ''
    for row in range(len(f[0])):
        for dice in f:
            face_string += dice[row] + ' '

        face_string += '\n'
    # Needs to be made generic
    face_string += " ## 1 ##   ## 2 ##   ## 3 ##   ## 4 ##   ## 5 ##  \n"
    return face_string


def main():
    players = []
    print(f'##\tYATZY\t##')
    nr_of_players = input("Antal spelare (2-5): ")
    for n in range(int(nr_of_players)):
        player_name = input(f'Namn spelare {n+1}: ')
        players.append(Player(player_name))


    yatzy = Yatzy(players)
    yatzy.start_game()
    yatzy.roll_all_dices()
    while not yatzy._is_done:
        dices_side_up = yatzy.get_dices_side_up()
        print(draw_faces_horizontal([side.face for side in dices_side_up]))
        current_player = yatzy.get_current_players_turn()
        print(f"Det är {current_player.name.upper()} tur att spela!")
        slots = yatzy.get_current_players_unscored_slots()
        for slot in slots:
            print(f'{slot.name}: {slot.value}')
        
        print("#####################################")
        print("[Enter] för att slå om alla tärningar")
        print("Välj tärningar att kasta om (Ex: 23 tärningar 2 och 3)")
        print("[S] för att spara poängen")
        print("[Q] för att avsluta spelet")
        
        val = input("Val: ")
        if val == "Q" or val == "q":
            break
        if val == "S" or val == "s":
            while True:
                score_slot = input("Välj scoreslot: ")
                if yatzy.set_current_players_score(ScoreSlotsEnum(int(score_slot))):
                    break
                else:
                    print("Poängslot ej tillgänglig!")
                    
            yatzy.roll_all_dices()
        elif val == "": 
            yatzy.roll_all_dices()
        else:
            re_roll = [int(n) for n in val]
            print(re_roll)
            yatzy.roll_a_subset_of_dices(re_roll)
    if yatzy._is_done:
        for player in yatzy._score_sheet._players.keys():
            print(f'{player}: {yatzy._score_sheet._players[player][ScoreSlotsEnum.TOTAL_SCORE]}')


if __name__ == "__main__":
    main()