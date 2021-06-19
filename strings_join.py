"""This module provides the function to join a list of strings into string."""
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--list', nargs='+',
                    default=['my_string1', 'my_string2', 'my_string3'],
                    dest='list', type=str, help='List of strings.')
args = parser.parse_args()


def join_strings(lst: list = args.list) -> str:
    """ Concatenation strings of list into a string.

    Args:
        lst: list of strings.
    Returns:
        concatenated string.
    """

    return ','.join([x.strip() for x in lst])


if __name__ == '__main__':
    print(join_strings())
