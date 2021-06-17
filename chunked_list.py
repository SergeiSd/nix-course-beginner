"""This module provides the function to split a list of integers into parts."""
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--list', nargs='+', default=[1, 2, 3, 4],
                    dest='list', type=int,
                    help='A list of integer elements to split.')
parser.add_argument('-n', default=3, type=int,
                    help='Number of parts to split.')
args = parser.parse_args()


def index(i):
    return int(round(i))


def chunked(lst: list = args.list, n: int = args.n) -> list:
    ''' A function to split a list of integers into n parts.

    Args:
        lst: list of integers.
        n: number of parts to split.
    Returns:
        A chunked list.
    '''

    if len(lst) >= n and n > 0:
        size = len(lst) / n
        return [lst[index(size*i):index(size*(i+1))] for i in range(n)]


if __name__ == '__main__':
    if chunked() is None:
        print("Error: can't split the list.")
    else:
        print(chunked())
