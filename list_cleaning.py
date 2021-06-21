"""This module provides the function to clear a list of integers."""
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input_list', nargs='+', default=[1, 2, 3, 4, 5],
                    type=int, help='Enter a list of integers to clear.')
parser.add_argument('--remove_list', nargs='+', default=[1, 3, 4], type=int,
                    help='Enter a list of integers, which must be removed.')
args = parser.parse_args()


def clean(lst1: list = args.input_list, lst2: list = args.remove_list) -> list:
    ''' A function to clear the list of integers.

    Args:
        lst1: a list of integers for cleaning.
        lst2: a list of integers, the values on which you want to clear.
    Returns:
        a cleared list of integers.
    '''

    return list(set(lst1).difference(set(lst2)))


if __name__ == '__main__':
    print('Cleared list: {}'.format(clean()))
