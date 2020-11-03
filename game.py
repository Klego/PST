from characters import *
from enemies import *

def game_init():
    turns = 0
    characters_playing = []


def resurrect(character):
    if character.get_alive():
        return 0
    else:
        character.set_alive()
        character.set_max_health()
