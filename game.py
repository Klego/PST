from characters import *
from enemies import *





def resurrect(num_players):

    character = search_player(num_players)
    if character.get_alive() == True:
        return False
    else:
        character.set_alive()
        character.set_max_health()
