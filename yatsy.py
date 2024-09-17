from score_sheet import ScoreSheet, ScoreSlotsEnum, Player
from calculate_score import ScoreSlotsEnum, CalculateScore
from Dices.regular_dice import create_regular_six_sided_die, Side
from Dices.dice import Face
from functools import wraps

class Yatzy:
    """
    Main class for playing Yatzy! 

    There is 5 dice, id 1,2,3,4 and 5 to play with.

    To start the game, invoke the start_game method! ⚠️Elsewise some methods are in a invalid state!⚠️

    Play the game by rolling the dice for current player and set points for choosen slot! 
    The game will write 0 points to a slot if an invalid die setup is passed to that slot.
    You have 3 rolls per player per turn. After that you must choose a open slot for current player. 
    Next players turn will automaticly be set after current player has set his points.
    """
    ROUNDS = 13

    def __init__(self, players:list[Player]) -> None:
        self._players = players.copy()
        self._score_sheet = ScoreSheet(players)
        self._game_dice = {die_id: create_regular_six_sided_die() for die_id in range(1,6)}
        self._score_calculator = CalculateScore()
        self._game_started = False


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
    def roll_all_dice(self) -> None:
        for die in self._game_dice.values(): 
            die.roll()

    @roll_counter
    def roll_a_subset_of_dice(self, die_ids:list[int]) -> None:
        for die_id in die_ids:
            self._game_dice[die_id].roll()


    def get_dices_side_up(self) -> list[Side]:
        return [die.side_up for die in self._game_dice.values()]


    def get_current_players_turn(self) -> Player:
        return self._current_players_turn


    def get_current_players_unscored_slots(self) -> list[ScoreSlotsEnum]:
        return self._score_sheet.get_unscored_slots(self._current_players_turn)


    def set_current_players_score(self, slot:ScoreSlotsEnum) -> None:
        method = self._score_calculator.get_method_by_ScoreSlotsEnum(slot)

        if not method: 
            raise ValueError(f"Error occured when trying to fetch method for slot:{slot}!")
        
        points = method(self._game_dice)

        self._score_sheet.write_points(
            self._current_players_turn,
            slot,
            points)

        self._start_next_players_turn()


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
        if self._round <= 13:
            self._round += 1
            self._player_sequens_turns = iter(player for player in self._players)
            self._current_players_turn = next(self._player_sequens_turns)
            self._current_players_roll_count = 0
        else:
            self._end_game()


def draw_faces_horizontal(faces:list[Face]) -> str:
    f = [face.get_face() for face in faces]
    face_string = ''
    for row in range(len(f[0])):
        for die in f:
            face_string += die[row] + ' '

        face_string += '\n'
    # Needs to be made generic
    face_string += " ## 1 ##   ## 2 ##   ## 3 ##   ## 4 ##   ## 5 ##  \n"
    return face_string


def main():
    p1 = Player("Sebastian")
    p2 = Player("Kalle")
    yatzy = Yatzy([p1,p2])
    yatzy.start_game()
    yatzy.roll_all_dice()
    while True:
        dices_side_up = yatzy.get_dices_side_up()
        print(draw_faces_horizontal([side.face for side in dices_side_up]))
        current_player = yatzy.get_current_players_turn()
        print(f"Det är {current_player.name} tur att spela!")
        slots = yatzy.get_current_players_unscored_slots()
        for slot in slots:
            print(slot.name)
        val = input("Q or what??")
        if val == "q":break
        if val == "": 
            yatzy.roll_all_dice()
        else:
            re_roll = [int(n) for n in val.split()]
            yatzy.roll_a_subset_of_dice(re_roll)


if __name__ == "__main__":
    main()