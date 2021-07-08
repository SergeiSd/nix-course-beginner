import argparse
import csv
import os
import psycopg2

from typing import List, Union, Tuple, Dict


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
parser.add_argument('--data_path', type=check_path,
                    help='Path of data files.')
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


def check_if_exists_tables(curs: psycopg2.extensions.cursor,
                           db_tables: List[str]) -> Dict[str, bool]:
    """A Function to check the existence of all required tables.

    Parametes
    ---------
        - curs: `psycopg2.extensions.cursor`

            Cursor to execute PostgreSQL command in database session.

        - db_tables: `List[str]`

            List of database tables.

    Returns
    -------
        class: `Dict[str, bool]`

            Dictionary, where the `key` is a name of table, and the `value`
            is whether it exists in the database.
    """

    checking_tables: Dict = dict.fromkeys(db_tables)
    execute_query = """select exists(select * from information_schema.tables
                       where table_name=%s)"""

    for table in db_tables:
        curs.execute(execute_query, (table, ))
        checking_tables[table] = curs.fetchone()[0]

    return checking_tables


def load_data_to_db(path: str,
                    curs: psycopg2.extensions.cursor,
                    conn: psycopg2.extensions.connection):
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

    db_tables: List[str] = ['cart_product',
                            'carts',
                            'categories',
                            'order',
                            'order_status',
                            'products',
                            'users']

    required_files: List[str] = ['cart_products.csv',
                                 'carts.csv',
                                 'categories.csv',
                                 'order_statuses.csv',
                                 'orders.csv',
                                 'products.csv',
                                 'users.csv']

    cursor, connection = connect_to_db()

    checking_tables = check_if_exists_tables(cursor, db_tables)

    if all([value for key, value in checking_tables.items()]):
        print('All tables exist.')
    else:
        for table, exist in checking_tables.items():
            if not exist:
                print(f'Error: table |{table}| does not exist.')

    #load_data_to_db(args.data_path, cursor, connection)
