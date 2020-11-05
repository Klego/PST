from characters import Bookworm, Worker, Procrastinator, Whatsapper
from enemies import PartialExam, FinalExam, TheoreticalClass, Teacher
from utils import sanitize_inputs, clear_screen, arguments_parser
from random import randint


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


def resurrect_skill(character_target, character):
    if character_target.get_alive():
        return 0
    elif character.get_cooldown() != 0:
        return 1
    else:
        character_target.set_alive()
        character_target.set_max_health()
        character.set_cooldown()


def amp_dmg_skill(target, character):
    if character.get_cooldown() == 0:
        character.deal_damage(target, (character.damage_roll() + character.get_dmg()) * 1.5)
        character.set_cooldown()
    else:
        return 0


def aoe_dmg_skill(enemies, character, level):
    if character.get_skill_uses() == 1 and character.get_cooldown() == 0:
        for target in enemies:
            character.deal_damage(target, (character.damage_roll() + character.get_dmg() + level))
        character.skill_uses_depleted()
        character.set_cooldown()
    else:
        return 0

#
def heal_skill(character_target, character):
    heal_after = character_target.get_health() + 2 * character.get_dmg()
    if character_target.get_health() < character_target.get_max_health():
        if heal_after <= character_target.get_max_health():
            character_target.set_health(heal_after)
        else:
            character_target.set_max_health()

        character.set_cooldown()
    else:
        return 0


def all_characters_alive(characters_playing):
    alive = 0
    for c in characters_playing:
        if c.get_alive():
            alive += 1
    if alive == len(characters_playing):
        print("All players are alive, so the skill won't be used.")
        return True


def all_characters_dead(characters_playing):
    dead = 0
    for c in characters_playing:
        if not c.get_alive:
            dead += 1
    if dead == len(characters_playing):
        print("All characters have been defeated. Try Again.")
        return True


def who_alive(characters_playing):
    alive = []
    for a in characters_playing:
        if a.get_alive:
            alive.append(True)
        else:
            alive.append(False)
    return alive


def use_skill(character, enemies, level, characters_playing, character_target):

    if character.__class__.__name__ == "Bookworm":
        if not all_characters_alive(characters_playing):
            if resurrect_skill(character_target, character) == 0:
                print("The player you choose is already alive. The skill won't be used")
            elif resurrect_skill(character_target, character) == 1:
                print("The skill is curently in cooldown for" + str(character.get_cooldown()) + " rounds")

    elif character.__class__.__name__ == "Worker":
        if amp_dmg_skill(enemies[randint(0, len(enemies)-1)], character) == 0:
            print("The skill is curently in cooldown for" + str(character.get_cooldown()) + " rounds")

    elif character.__class__.__name__ == "Procastinator":
        if aoe_dmg_skill(enemies, character, level) == 0:
            print("The skill is curently in cooldown for" + str(character.get_cooldown()) + " rounds" + "with " +
                  str(character.get_skill_uses()) + " available uses.")

    elif character.__class__.__name__ == "Whatsapper":
        if heal_skill(character_target, character) == 0:
            print("The skill is curently in cooldown for" + str(character.get_cooldown()) + " rounds")

