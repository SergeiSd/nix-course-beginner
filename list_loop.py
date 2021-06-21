from random import randint, choices, random
from string import ascii_letters


def unique_integers(n: int) -> list:
    ''' A function for generating a list of pseudorandom numbers.

    Args:
        n: number of integers.
    Returns:
        list of integers.
    '''

    integers = set()
    while len(integers) < n:
        integer = randint(0, 1000)
        integers.add(integer)

    return list(integers)


def unique_strings(ntokens: int, pool: str = ascii_letters) -> list:
    ''' A function for generating a list of random strings.

    Args:
        pool: letters for string.
        n: number of strings.
    Returns:
        list of strings.
    '''

    strings = set()
    while len(strings) < ntokens:
        token = ''.join(choices(pool, k=randint(5, 15)))
        strings.add(token)

    return list(strings)


if __name__ == '__main__':
    
    # concatenation of two lists
    random_list = unique_integers(200) + unique_strings(200)
    
    # shuffle list
    random_list = sorted(random_list, key=lambda A: random())
    
    # attempts counter
    count = 0

    for x in random_list:
        if x == 777:
            print('Number 777 found!')
            break
        elif count == 100:
            print('Error: achieved 100 attempts.')
            break

        count += 1
