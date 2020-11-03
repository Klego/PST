import os
import sys


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
