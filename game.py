from characters import Bookworm, Worker, Procrastinator, Whatsapper
from enemies import PartialExam, FinalExam, TheoreticalClass, Teacher
from utils import sanitize_inputs, clear_screen, arguments_parser
from random import randint
import sys


# Function that shows the menu and return the characters playing
def game_init_menu(num_players):
    selected_characters = []
    index = 1
    player_index = 1
    available_characters = [Bookworm, Worker, Whatsapper, Procrastinator]
    clear_screen()
    print("***********\tAVAILABLE CHARACTERS\t***********")
    for character in available_characters:
        p = character()
        print(str(index) + ".- " + "The " + str(p))
        index += 1
    print("********************************************************\n")
    while player_index <= num_players:
        option_menu = sanitize_inputs(message="Player " + str(player_index) + ". Please, choose a character(1-4): ",
                                      valid_input=[1, 2, 3, 4], valid_cast=int)
        player = available_characters[option_menu - 1]

        selected_characters.append(player())
        player_index += 1

    index = 1
    for character in selected_characters:
        print(str(index) + ".- " + str(character))
        index += 1
    return selected_characters


# Function that initiates the game with the required arguments and call the game init_menu
def game_init():
    num_players, num_stages = arguments_parser()
    characters_playing = game_init_menu(num_players)
    return characters_playing, num_stages

# -- Functions for character skills --


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
        real_damage = character.deal_damage(target, (character.damage_roll() + character.get_dmg()) * 1.5)
        character.set_cooldown()
        return real_damage
    else:
        return 0


def aoe_dmg_skill(enemies, character, level):
    real_damage = 0
    if character.get_skill_uses() == 1 and character.get_cooldown() == 0:
        for target in enemies:
            real_damage = character.deal_damage(target, (character.damage_roll() + character.get_dmg() + level))
        character.skill_uses_depleted()
        character.set_cooldown()
        return real_damage
    else:
        return 0


def heal_skill(character_target, character):
    heal_after = character_target.get_health() + 2 * character.get_dmg()
    if character.get_cooldown() == 0:
        if character_target.get_health() < character_target.get_max_health():
            if heal_after < character_target.get_max_health():
                character_target.set_health(heal_after)
            else:
                character_target.set_max_health()

            character.set_cooldown()
            return True
    else:
        return 0

# Function that returns if all characters are alive (used in resurrection function)
def all_characters_alive(characters_playing):
    i = 0
    alive = 0
    while i <= len(characters_playing) - 1:
        if characters_playing[i].get_alive() == alive:
            alive += 1
        i += 1
    if alive == len(characters_playing):
        return 1
    else:
        return 0

# Function that returns if all characters are dead (used in game function)
def all_characters_dead(characters_playing):
    i = 0
    dead = 0
    while i <= len(characters_playing) - 1:
        if characters_playing[i].get_alive() == False:
            dead += 1
        i += 1
    if dead == len(characters_playing):
        return 1
    else:
        return 0

# Function used that return a boolean list of characters dead o alive (used in valid_option functions)
def who_alive(characters_playing):
    alive = []
    for a in characters_playing:
        if a.get_alive == True:
            alive.append(True)
        else:
            alive.append(False)
    return alive

# Function that returns the choices available for character resurrection (in characters_turn function)
def valid_option_resurrection(characters_playing):
    valid_option = []
    dead_characters = who_alive(characters_playing)
    index_dead = 0
    while index_dead <= len(dead_characters) - 1:
        if not dead_characters[index_dead]:
            valid_option.append(index_dead + 1)
        index_dead += 1
    return valid_option

# Function that returns the available choices for character healing (used in chatacter_turn function)
def valid_option_healing(characters_playing):
    valid_option = []
    index_heal = 0
    while index_heal <= len(characters_playing) - 1:
        if characters_playing[index_heal].get_alive():
            if characters_playing[index_heal].get_health() < characters_playing[index_heal].get_max_health():
                valid_option.append(index_heal + 1)
        index_heal += 1
    return valid_option

# Function that check skills errors and print message. Also, use the skill of the character if possible.
# (Used in character_turn function)
def use_skill(character, enemies, stage, characters_playing, character_target=None):
    if character.__class__.__name__ == "Bookworm":
        all_alive = all_characters_alive(characters_playing)
        if all_alive == 0:
            resurrection = resurrect_skill(character_target, character)
            if resurrection == 0:
                print("The player you choose is already alive. The skill won't be used")
            elif resurrection == 1:
                print("The skill is currently in cooldown for" + str(character.get_cooldown()) + " rounds")
            else:
                print("The " + character_target.get_name() + " has been revived.")
        else:
            print("All players are alive, so the skill won't be used.")

    elif character.__class__.__name__ == "Worker":
        enemy = enemies[randint(0, len(enemies) - 1)]
        amp_dmg = amp_dmg_skill(enemy, character)
        if amp_dmg == 0:
            print("The skill is currently in cooldown for" + str(character.get_cooldown()) + " rounds")
        else:
            print("The skill has been used." + "The " + character.get_name() + " attacked " + enemy.get_name() + " with"
                  + str(amp_dmg) + "dmg. The " + enemy.get_name() + " has " + str(enemy.get_health()) + "hp left.")

    elif character.__class__.__name__ == "Procrastinator":
        aoe_dmg = aoe_dmg_skill(enemies, character, stage)
        if aoe_dmg == 0:
            print("The skill is currently in cooldown for" + str(character.get_cooldown()) + " rounds" + "with " +
                  str(character.get_skill_uses()) + " available uses.")
        else:
            print("The skill has been used." + "The " + character.get_name() + " attacked " + "all enemies with"
                  + str(aoe_dmg) + "dmg.\n")
            for e in enemies:
                print("The " + e.get_name() + " has " + str(e.get_health()) + "hp left.\n")

    elif character.__class__.__name__ == "Whatsapper":
        heal = heal_skill(character_target, character)
        if heal == 0:
            print("The skill is currently in cooldown for" + str(character.get_cooldown()) + " rounds")
        else:
            print("The " + character_target.get_name() + " has been healed.")

# Function that returns the enemies in each stage (Used in enemies_turn function)
def enemies_stage(stage):
    enemies_playing = []
    enemies_available = [PartialExam(), TheoreticalClass(stage), Teacher(), FinalExam()]
    while len(enemies_playing) < 3:
        if 1 <= stage < 3:
            random = randint(0, 2)
        else:
            random = randint(0, 3)
        enemy = enemies_available[random]
        if enemy not in enemies_playing:
            enemies_playing.append(enemy)
    return enemies_playing

# Function that prints the enemies (used in enemies_turn function)
def print_enemies(stage, enemies_playing):
    print("************************")
    print("*\tSTAGE " + str(stage) + "\t\t" + "*")
    print("************************")
    print("----  CURRENT MONSTERS  ----")
    print("++++++++++++++++++++++++++++++++++++++")
    for enemy in enemies_playing:
        print(str(enemy))
    print("++++++++++++++++++++++++++++++++++++++\n")

# Function that controls characters playing actions (used in game function)
def characters_turn(characters_playing, enemies_playing, stage):
    player_number = 1
    print("------------------------")
    print("-\tPLAYERS TURN\t-")
    print("------------------------\n")
    for character in characters_playing:
        if character.get_alive() == True:
            message = character.get_name() + " (Player " + str(player_number) + "). What are you going to do?: "
            option = sanitize_inputs(message, valid_input=['a', 's'])
            if option == "a":
                if len(enemies_playing) != 0:
                    target = enemies_playing[randint(0, len(enemies_playing) - 1)]
                    real_damage = character.attack(target)
                    print(
                        "The " + character.get_name() + "(Player " + str(player_number) + ") did " + str(real_damage) +
                        " dmg to " + target.get_name() + ". " + target.get_name() + " has " + str(target.get_health()) +
                        " hp left.")
                else:
                    break
            if option == "s":
                if character.__class__.__name__ == "Bookworm":
                    index = 0
                    print("****************************************************\n")
                    while index <= len(characters_playing) - 1:
                        if not characters_playing[index].get_alive():
                            print(str(index + 1) + ".- " + "The " + str(characters_playing[index]))
                        index += 1
                    print("****************************************************")
                    message = "Who do you want to revive?: "
                    valid_option = valid_option_resurrection(characters_playing)
                    character_target = sanitize_inputs(message, valid_option, valid_cast=int)
                    print("****************************************************")
                    use_skill(character, enemies_playing, stage, characters_playing, character_target)
                elif character.__class__.__name__ == "Worker":
                    if len(enemies_playing) != 0:
                        use_skill(character, enemies_playing, stage, characters_playing)
                    else:
                        break
                elif character.__class__.__name__ == "Procrastinator":
                    if len(enemies_playing) != 0:
                        use_skill(character, enemies_playing, stage, characters_playing)
                    else:
                        break
                elif character.__class__.__name__ == "Whatsapper":
                    i_c = 0
                    print("****************************************************")
                    while i_c <= len(characters_playing) - 1:
                        if characters_playing[i_c].get_alive() == True:
                            if characters_playing[i_c].get_health() < characters_playing[i_c].get_max_health():
                                print(str(i_c + 1) + ".- " + "The " + str(characters_playing[i_c]))
                        i_c += 1
                    print("****************************************************")
                    message = "Who do you want to heal?: "
                    valid_option = valid_option_healing(characters_playing)
                    character_target = sanitize_inputs(message, valid_option, valid_cast=int)
                    print("****************************************************")
                    use_skill(character, enemies_playing, stage, characters_playing, character_target)
            player_number += 1

# Function that controls enemies turn (used in game function)
def enemies_turn(enemies_playing, characters_playing):
    targets_alive = []
    print("------------------------")
    print("-\tMONSTERS TURN\t-")
    print("------------------------\n")
    for enemy in enemies_playing:
        if enemy.get_alive() == True:
            for character in characters_playing:
                if character.get_alive() == True:
                    targets_alive.append(character)
                    target = targets_alive[randint(0, len(targets_alive) - 1)]
                    dmg = enemy.attack(target)
                    print("The " + enemy.get_name() + " did " + str(dmg) +
                          " dmg to " + target.get_name() + ". " + target.get_name() + " has " + str(
                        target.get_health()) + " hp left.")
                else:
                    break

# Function that check which enemies are dead an pop from the list (Used in game function)
def check_enemies_pop(enemies_playing):
    i = 0
    if len(enemies_playing) != 0:
        while i <= len(enemies_playing) - 1:
            if enemies_playing[i].get_alive() == False:
                enemies_playing.pop(i)
            i += 1
        return len(enemies_playing)
    else:
        return 0

# Function that check the cooldowns of every skill in all characters alive. (Used in game function)
def check_cooldown(characters_playing):
    for character in characters_playing:
        if character.get_alive() == True:
            if character.get_cooldown() != 0:
                if character.__class__.__name__ == "Procrastinator":
                    character.update_passive_skill()
                character.update_cooldown()

# Function that check if the character is alive at the end of a stage and heals it (Used in game function)
def heal_after_stage(characters_playing):
    for character in characters_playing:
        if character.get_alive():
            character.heal_after_turn()

# Function that reset the characters cooldowns at the end of the stage (used in game function)
def reset_cooldown(characters_playing):
    for character in characters_playing:
        if character.__class__.__name__ == "Procrastinator":
            character.reset_passive_skill()
            character.reset_skill_uses()
        character.reset_cooldown()

# Main function of the game that controls the turns and the stages of the game
def game():
    try:
        current_stage = 1
        num_enemies = 4
        all_dead = 0
        characters_playing, stages = game_init()
        while all_dead == 0 and current_stage <= stages:
            enemies_playing = enemies_stage(current_stage)
            print_enemies(current_stage, enemies_playing)
            while all_dead == 0 and len(enemies_playing) != 0:
                characters_turn(characters_playing, enemies_playing, current_stage)
                all_dead = all_characters_dead(characters_playing)
                if all_dead == 1:
                    break
                enemies_turn(enemies_playing, characters_playing)
                all_dead = all_characters_dead(characters_playing)
                num_enemies = check_enemies_pop(enemies_playing)
                if num_enemies == 0 or all_dead == 1:
                    break
                check_cooldown(characters_playing)

            current_stage += 1
            if all_dead == 1:
                break
            reset_cooldown(characters_playing)
            heal_after_stage(characters_playing)

        if all_dead == 1:
            print("All characters have been defeated. Try again.")
        elif current_stage > stages:
            print("All the stages have been cleared. You won the game!")
        sys.exit(0)
    except KeyboardInterrupt:
        print("The user terminated the program. Quitting...\n")
        sys.exit(0)
