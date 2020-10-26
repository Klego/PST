from characters import *
from enemies import *
class Game:




    def resurrect(character):
        if character.get_alive() == True:
            return 0
        else:
            character.set_alive()
            character.set_max_health()
