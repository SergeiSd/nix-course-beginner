import argparse
import csv
import os
import psycopg2

from typing import List, Union, Tuple


def check_path(path: str) -> Union[str, None]:

    required_files: List[str] = ['cart_products.csv',
                                 'carts.csv',
                                 'categories.csv',
                                 'order_statuses.csv',
                                 'orders.csv',
                                 'products.csv',
                                 'users.csv']

    if not os.path.exists(path):
        print('Error: next path: {} is not exists.'.format(path))
        raise argparse.ArgumentTypeError

    if path[-1] != '/':
        fixed_path = list(path)
        fixed_path.append('/')
        path = ''.join(fixed_path)

    files = os.listdir(path)

    if sorted(required_files) == sorted(files):
        return path
    else:
        print("""Error: next path: {} is not contain \
              required files.""".format(path))
        raise argparse.ArgumentTypeError


parser = argparse.ArgumentParser()
parser.add_argument('--data_path',
                    default='/home/sergei/nix-projects/SQL/data',
                    type=check_path, help='')
args = parser.parse_args()


def connect_to_db() -> Tuple[psycopg2.extensions.connection,
                             psycopg2.extensions.cursor]:
    """ A function for connet to DB.
    """

    try:
        conn = psycopg2.connect(dbname='nix_db',
                                user='postgres',
                                password='Slyadnev78Fw',
                                host='localhost',
                                port="5432")
        cursor = conn.cursor()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return (cursor, conn)

def load_data_to_db(path: str,
                    curs: psycopg2.extensions.cursor,
                    conn: psycopg2.extensions.connection):

    db_tables: List[str] = ['Cart_product',
                            'Carts',
                            'Categories',
                            'Order',
                            'Order_status',
                            'Products',
                            'Users']

    required_files: List[str] = ['cart_products.csv',
                                 'carts.csv',
                                 'categories.csv',
                                 'order_statuses.csv',
                                 'orders.csv',
                                 'products.csv',
                                 'users.csv']
    '''
    for file, table in zip(required_files, db_tables):
        file = path + file
        with open(file, 'r') as f:
            cursor.copy_from(f, table, sep=',')
    conn.commit()
    '''

    insert_query = """INSERT INTO "users"
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    file = '/home/sergei/nix-projects/SQL/data/sql_input_files/users.csv'

    with open(file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            curs.execute(insert_query, row)
    conn.commit()


if __name__ == "__main__":

    cursor, connection = connect_to_db()

    load_data_to_db(args.data_path, cursor, connection)
