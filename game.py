from characters import Bookworm, Worker, Procrastinator, Whatsapper
from enemies import PartialExam, FinalExam, TheoreticalClass, Teacher
from utils import sanitize_inputs, clear_screen, arguments_parser


def game_init_menu(num_players):
    selected_characters = [num_players]
    index = 1
    player_index = 1
    available_characters = [Bookworm(), Worker(), Whatsapper(), Procrastinator()]
    clear_screen()
    print("***********\tAVAILABLE CHARACTERS\t***********")
    for character in available_characters:
        print(str(index) + ".- " + str(character))
        index += 1
    print("********************************************************\n")
    while player_index <= num_players:
        option_menu = sanitize_inputs(message="Player " + str(player_index) + ". Please, choose a character(1-4): ",
                                      valid_input=[1, 2, 3, 4], valid_cast=int)
        selected_characters.append(available_characters[option_menu-1])
    print("********************************************************\n")
    index = 1
    for character in selected_characters:
        print(str(index) + ".- " + str(character))
        index += 1
    return selected_characters


def game_init():
    num_players, num_stages = arguments_parser()
    characters_playing = game_init_menu(num_players)
    num_turns = 0

def resurrect(character):
    if character.get_alive():
        return 0
    else:
        character.set_alive()
        character.set_max_health()
