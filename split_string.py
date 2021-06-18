"""This module provides the function to split a string of names into
   a list of names."""
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--string', type=str,
                    default='Денис, Олег, Вася, Петя,Дима,Женя',
                    help='String of names. Ex: \'Вася, Петя,Денис, Женя\' ')
args = parser.parse_args()


def split(string: str = args.string) -> list:
    ''' Splitting a string of names into a list of names.
        List items (names) do not contain spaces.

    Args:
        string: string of names.
    Returns:
        list of names.
    '''

    return [x.replace(' ', '') if ' ' in x else x for x in string.split(',')]


if __name__ == '__main__':
    print('List of names:', split())
