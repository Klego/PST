import os
import sys
import argparse
NUM_MAX_STAGES = 10
NUM_MAX_PLAYERS = 10

class InvalidInputError(Exception):
    pass


class RetryCountExceededError(Exception):
    pass


def sanitize_inputs(message="", valid_input=[], valid_cast=str, num_retries=-1):
    cont_retries = 0
    while cont_retries < num_retries or num_retries < 0:
        try:
            raw = valid_cast(input(message))
            if raw in valid_input:
                return raw
            else:
                raise InvalidInputError("You have inputted a wrong option.\n")
        except ValueError:
            sys.exit(print("ValueError Exception. Quitting program...\n"))
        except InvalidInputError:
            cont_retries += 1
            continue
        except KeyboardInterrupt:
            print("The user terminated the program. Quitting...\n")
            sys.exit(0)
    raise RetryCountExceededError("RetryCountExceededError: count exceeded in function 'sanitize_inputs")


def clear_screen():
    os.system('clear')

def arguments_parser():
    try:
        exit = False
        parser = argparse.ArgumentParser()
        parser.add_argument('-p', '--players', type=int, default=1)
        parser.add_argument('-s', '--stages', type=int, default=1)
        args = parser.parse_args()
        if not 0 < args.players <= 4:
            print("The number of players must be between 1 and 4. Finishing program")
            exit = True
        else:
            num_players = args.players
        if not 0 < args.stages <= 10:
            print("The number of stages must be between 1 and 10. Finishing program")
            exit = True
        else:
            num_stages = args.stages
        if exit:
            sys.exit(0)
        else:
            return num_players, num_stages
    except ValueError:
        print("You must input only integers. Finishing program")




