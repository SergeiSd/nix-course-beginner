import argparse
import os
import psycopg2

from typing import List, Union, Dict


def check_path(path: str) -> Union[str, None]:

    required_files: List[str] = ['cart_products.csv',
                                 'carts.csv',
                                 'categories.csv',
                                 'order_statuses.csv',
                                 'orders.csv',
                                 'products.csv',
                                 'users.csv']

    if not os.path.exists(path):
        error_messege = f'next path: {path} is not exists.'
        raise argparse.ArgumentTypeError(error_messege)

    files_in_dir = os.listdir(path)

    if sorted(required_files) == sorted(files_in_dir):
        return path
    else:
        error_messege = f'next path: {path} is not contain required files.'
        raise argparse.ArgumentTypeError(error_messege)


parser = argparse.ArgumentParser()
parser.add_argument('--data_path', type=check_path,
                    default='data/sql_input_files',
                    help='Path of data files.')
parser.add_argument('--db_name', type=str,
                    help='Name of database.')
parser.add_argument('--user', type=str,
                    help='User for connect to database.')
parser.add_argument('--db_password', type=str,
                    help='Password for connect to database.')
parser.add_argument('--db_host', type=str,
                    help='Host for connect to database.')
parser.add_argument('--db_port', type=str,
                    help='Port for connect to database.')
args = parser.parse_args()


def create_connection(db_name, db_user, db_password,
                      db_host, db_port) -> psycopg2.extensions.connection:
    """ A function for creating a connection to the database.
    """
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        print("Connection to PostgreSQL DB successful.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    return connection


def check_if_exists_tables(connection: psycopg2.extensions.connection,
                           db_tables: List[str]) -> Dict[str, bool]:
    """A function to check the existence of all required tables.

    Parametes
    ---------

        - db_tables: `List[str]`

        List of database tables.

    Returns
    -------
        class: `Dict[str, bool]`

        Dictionary, where the `key` is a name of table, and the `value`
        is whether it exists in the database.
    """

    cursor = connection.cursor()
    checking_tables: Dict = dict.fromkeys(db_tables)
    select_query = """select exists(select * from information_schema.tables
                       where table_name = %s)"""

    for table in db_tables:
        cursor.execute(select_query, (table, ))
        checking_tables[table] = cursor.fetchone()[0]

    return checking_tables


def check_if_table_is_empty(connection: psycopg2.extensions.connection,
                            table: str) -> bool:
    select_query = """select * from %s"""
    with connection.cursor() as cursor:
        cursor.execute(select_query, (table, ))
        return cursor.fetchone()


def insert_data_to_db(connection: psycopg2.extensions.connection,
                      table: str, file: str) -> None:

    with connection.cursor() as cursor:
        with open(file, 'r') as f:
            try:
                cursor.copy_from(f, table, sep=',')
                print(f'Data from {f} loaded successfully.')
            except Exception as e:
                print(e)

    connection.commit()


if __name__ == "__main__":

    db_tables: List[str] = ['users',
                            'carts',
                            'categories',
                            'products',
                            'cart_product',
                            'order_status',
                            'order']

    required_files: List[str] = ['users.csv',
                                 'carts.csv',
                                 'categories.csv',
                                 'products.csv',
                                 'cart_products.csv',
                                 'order_statuses.csv',
                                 'orders.csv']

    connection = create_connection(
        args.db_name, args.user, args.db_password,
        args.db_host, args.db_port
    )

    checking_tables = check_if_exists_tables(
        connection,
        db_tables
    )

    if all([value for key, value in checking_tables.items()]):
        print('All tables exist.')
    else:
        for table, exist in checking_tables.items():
            if not exist:
                print(f'Error: table |{table}| does not exist.')

    for table, file in zip(db_tables, required_files):
        #print(check_if_table_is_empty(connection, table))
        insert_data_to_db(connection, table, file)
