import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument('-n', '--name', default='Name', type=str,
                    help='Enter name')
parser.add_argument('-s', '--surname', default='Surname', type=str,
                    help='Enter surname')
args = parser.parse_args()


def validate(name=args.name, surname=args.surname):
    """A validation function for input parameters.

    Args:
        name: input name
        surname: input surname
    Returns:
        True or False
    """

    pattern = "^[a-z ,.'-]+$"

    if name and surname:
        if re.findall(pattern, name.lower()) and \
           re.findall(pattern, surname.lower()):
            return True
        else:
            print('Error: input parameters "name" and "surname" are '
                  'incorrect.')
            return False
    else:
        print('Error: enter name and surname.')
        return False


def print_strings(name=args.name, surname=args.surname):
    """Printing input parametrs: name and surname

    Args:
        name: input name
        surname: input surname
    """

    name = name.title()
    surname = surname.title()

    if validate():
        print('name: {} \nsurname: {}'.format(name, surname))


if __name__ == '__main__':
    print_strings()
