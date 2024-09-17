from score_sheet import ScoreSheet, ScoreSlotsEnum, Player
## Cirkulär importering av scoreslotsenum
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

    ###
    # Utifrån antalet slots man kan fylla borde det kanske vara 15 rundor.
    ###
    ROUNDS = 13

    def __init__(self, players:list[Player]) -> None:
        self._players = players.copy()
        self._score_sheet = ScoreSheet(players)
        self._game_dices = {dice_id:create_regular_six_sided_dice() for dice_id in range(1,6)}
        self._score_calculator = CalculateScore()
        self._game_started = False


    def roll_counter(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            ###
            ## KAN INTE HITTA NÅGONT _current_players_roll_count
            ##
            if self._current_players_roll_count < 3: 
                resultat = func(self, *args, **kwargs)
                self._current_players_roll_count += 1
            else:
                ###
                ## Ingen info att man har uppnått max roll av 3
                ###
                resultat = None
            # could implemet some logic to signal that player must set_current_players_point!
            return resultat
        return wrapper

    @roll_counter ## Visar inte någon räkning
    def roll_all_dices(self) -> None:
        for dice in self._game_dices.values(): 
            dice.roll()

    @roll_counter ## Visar inte någon räkning
    def roll_a_subset_of_dices(self, dice_ids:list[int]) -> None:
        ## En felhantering om det inte finns någon dice id som man skickat hit.
        for dice_id in dice_ids:
            self._game_dices[dice_id].roll()

    ##
        ## Visar ingenting om man har slut på kasst eller inte efter man rullat. 1 / 3 kast eller liknande ##
    ##

    def get_dices_side_up(self) -> list[Side]:
        return [d.side_up for d in self._game_dices.values()]


    def get_current_players_turn(self) -> Player:
        return self._current_players_turn


    def get_current_players_unscored_slots(self) -> list[ScoreSlotsEnum]:
        return self._score_sheet.get_unscored_slots(self._current_players_turn)


    def set_current_players_score(self, slot:ScoreSlotsEnum) -> None:
        ### Ingen kontroll att en poängslot är upptagen eller inte. Samt att metoden inte returnerar något.
        method = self._score_calculator.get_method_by_ScoreSlotsEnum(slot)

        if not method: 
            raise ValueError(f"Error occured when trying to fetch method for slot:{slot}!")
        
        points = method(self._game_dices)

        self._score_sheet.write_points(
            self._current_players_turn,
            slot,
            points)

        self._start_next_players_turn()


    def start_game(self) -> None:
        assert not self._game_started
        self._game_started = True
        self._round = 0 # Börjar man inte på runda 1?
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
        if self._round <= 13: ### Kör till och med runda 13 alltså 14 rundor mellan 0 och 13.
            self._round += 1
            self._player_sequens_turns = iter(player for player in self._players)
            self._current_players_turn = next(self._player_sequens_turns)
            self._current_players_roll_count = 0
        else:
            self._end_game()


def draw_faces_horizontal(faces:list[Face]) -> str:
    ## Ska man verkligen göra det här separat från rollen? borde inte rollen triggera denna.
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
    p1 = Player("Sebastian")
    p2 = Player("Kalle")
    yatzy = Yatzy([p1,p2])
    yatzy.start_game()
    yatzy.roll_all_dices()
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
            yatzy.roll_all_dices()
        else:
            re_roll = [int(n) for n in val.split()]
            yatzy.roll_a_subset_of_dices(re_roll)


if __name__ == "__main__":
    main()