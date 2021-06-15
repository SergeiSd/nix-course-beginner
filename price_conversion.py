import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--price', default=42.0, type=float,
                    help='Enter price')
args = parser.parse_args()


def conversion(price=args.price):
    """ A conversion function for price

    Args:
        price: input argument with float type
    Returns:
        conv_price: converted price
    """

    if price % 1 == 0:
        conv_price = int(price)
    else:
        conv_price = round(price, 2)

    return conv_price


if __name__ == '__main__':
    print('converted price: {}'.format(conversion()))
