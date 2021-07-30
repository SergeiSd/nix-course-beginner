import argparse
import os
import psycopg2

from psycopg2 import sql
from psycopg2 import DatabaseError
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from typing import List, NoReturn, Union, Dict, Tuple, Optional


def check_path(path: str) -> Union[str, None]:

    required_files: Tuple[str] = ('cart_products.csv',
                                  'carts.csv',
                                  'categories.csv',
                                  'order_statuses.csv',
                                  'orders.csv',
                                  'products.csv',
                                  'users.csv')

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
                    default='data/sql_input_files/',
                    help='Path of data files.')
parser.add_argument('--db_name', type=str, default='nix_db',
                    help='Database name.')
parser.add_argument('--user', type=str, default='postgres',
                    help='Username to connect to the database.')
parser.add_argument('--db_password', type=str, default='my_password',
                    help='Password to connect to the database.')
parser.add_argument('--db_host', type=str, default='localhost',
                    help='The name of the server or IP address.')
parser.add_argument('--db_port', type=str, default='5432',
                    help='Port for connecting to the database.')
args = parser.parse_args()


def create_connection(db_user: str, db_password: str, db_host: str,
                      db_port: str, db_name: Optional[str] = None):
    """A function to create a connection to a PostgreSQL database instance.
    Parameters:
    ----------
        - db_user: type[`str`]
        Username to connect to the database.
        - db_password: type[`str`]
        Password to connect to the database.
        - db_host: type[`str`]
        The name of the server or IP address that the database is running on.
        - db_port: type[`str`]
        Port for connecting to the database.
        - db_name: type[`str`]
        Database name.
    Returns:
    -------
        type[`psycopg2.extensions.connection`]
        A connection object to a PostgreSQL database instance.
    """

    if db_name is None:
        print('Connection to PostgreSQL...')
    else:
        print(f'Connection to PostgreSQL Database |{db_name}|...')

    connection = None
    try:
        connection = psycopg2.connect(
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
            database=db_name
        )
        if db_name is None:
            print("Connection to PostgreSQL successful.")
        else:
            print(f'Connection to PostgreSQL Database |{db_name}| successful.')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        raise SystemExit
    else:
        return connection


def create_database(db_name: str, connection:
                    psycopg2.extensions.connection) -> Union[bool, None]:
    """Database creation in PostgreSQL.

    Parameters:
    ----------
        - db_name: type[`str`]
        A database name.

        - connection: type[`psycopg2.extensions.connection`]
        A connection object to a PostgreSQL database instance.

    Returns:
    -------
        type[`bool`]: whether the database was created or not.
    """

    cursor: psycopg2.extensions.cursor

    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()

    print('Database creation...')
    try:
        cursor.execute(
            sql.SQL("CREATE DATABASE {}")
               .format(sql.Identifier(db_name))
        )
        print('The database has been created successfully.')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        raise SystemExit
    else:
        connection.commit()
        return True


def create_tables(connection, db_table: str) -> None:
    """A function to create database tables.
    The function creates seven tables: `users`, `carts`, `categories`,
    `order_status`, `products`, `cart_product`, `orders`.

    Parameters:
    ----------

        - connection: `psycopg2.extensions.connection`.
        A connection object to a PostgreSQL database instance.

        - db_table: `str`.
        A database table name.
    """

    create_table_query: str
    cursor: psycopg2.extensions.cursor

    if db_table == 'users':
        print('Creating a table |users|...')

        create_table_query = '''
            CREATE TABLE users (
                    user_id INTEGER NOT NULL PRIMARY KEY
                        GENERATED ALWAYS AS IDENTITY,
                    email VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    first_name VARCHAR(255) NOT NULL,
                    last_name VARCHAR(255) NOT NULL,
                    middle_name VARCHAR(255),
                    is_staff SMALLINT,
                    country VARCHAR(255),
                    city VARCHAR(255),
                    address TEXT
            )
        '''
    elif db_table == 'carts':
        print('Creating a table |carts|...')

        create_table_query = '''
            CREATE TABLE carts (
                cart_id INTEGER NOT NULL PRIMARY KEY
                    GENERATED ALWAYS AS IDENTITY,
                Users_user_id INTEGER NOT NULL,
                subtotal DECIMAL NOT NULL,
                total DECIMAL NOT NULL,
                timestamp TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                FOREIGN KEY (Users_user_id) REFERENCES users (user_id)
            )
        '''
    elif db_table == 'categories':
        print('Creating a table |categories|...')

        create_table_query = '''
            CREATE TABLE categories (
                category_id INTEGER  NOT NULL PRIMARY KEY
                    GENERATED ALWAYS AS IDENTITY,
                category_title VARCHAR(255) NOT NULL,
                category_description TEXT
            )
        '''
    elif db_table == 'order_status':
        print('Creating a table |order_status|...')

        create_table_query = '''
            CREATE TABLE order_status (
                order_status_id INTEGER  NOT NULL PRIMARY KEY
                    GENERATED ALWAYS AS IDENTITY,
                status_name VARCHAR(255) NOT NULL
            )
        '''
    elif db_table == 'products':
        print('Creating a table |products|...')

        create_table_query = '''
            CREATE TABLE products (
                product_id INTEGER NOT NULL PRIMARY KEY
                    GENERATED ALWAYS AS IDENTITY,
                product_title VARCHAR(255) NOT NULL,
                product_description TEXT,
                in_stock INTEGER NOT NULL,
                price REAL NOT NULL,
                slug VARCHAR(45) NOT NULL,
                category_id INTEGER NOT NULL,
                FOREIGN KEY (category_id) REFERENCES categories (category_id)
            )
        '''
    elif db_table == 'cart_product':
        print('Creating a table |cart_product|...')

        create_table_query = '''
            CREATE TABLE cart_product (
                carts_cart_id INTEGER NOT NULL,
                products_product_id INTEGER NOT NULL,
                FOREIGN KEY (carts_cart_id) REFERENCES carts (cart_id),
                FOREIGN KEY (products_product_id) REFERENCES
                    products (product_id)
            )
        '''
    elif db_table == 'orders':
        print('Creating a table |order|...')

        create_table_query = '''
            CREATE TABLE orders (
                order_id INTEGER NOT NULL PRIMARY KEY,
                Carts_cart_id INTEGER NOT NULL,
                Order_status_order_status_id INTEGER NOT NULL,
                shipping_total DECIMAL NOT NULL,
                total DECIMAL NOT NULL,
                created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
                FOREIGN KEY (Carts_cart_id) REFERENCES carts (cart_id),
                FOREIGN KEY (Order_status_order_status_id) REFERENCES
                    order_status (order_status_id)
            )
        '''

    cursor = connection.cursor()
    try:
        cursor.execute(create_table_query)
        print('The table was created successfully.')
    except (Exception, DatabaseError) as error:
        print(error)
    else:
        connection.commit()


def insert_data_to_db(connection: psycopg2.extensions.connection,
                      table: str, file: str, path: str) -> None:
    """ A function for loading data from csv files into database tables.

    Parameters:
    ----------
        - connection: `psycopg2.extensions.connection`.
        A connection object to a PostgreSQL database instance.

        - table: `str`.
        Database table name.

        - file: `str`
        The name of the data file.

        - path: `str`
        Path to data files.
    """

    print('Loading data into database tables...')
    path = path + file
    with connection.cursor() as cursor:
        with open(path, 'r') as f:
            try:
                cursor.copy_from(f, table, sep=',')
                print(f'Data from |{file}| loaded successfully.')
            except Exception as error:
                print(error)

    connection.commit()


if __name__ == "__main__":

    tables_and_files = {
        'users': 'users.csv',
        'carts': 'carts.csv',
        'categories': 'categories.csv',
        'products': 'products.csv',
        'cart_product': 'cart_products.csv',
        'order_status': 'order_statuses.csv',
        'orders': 'orders.csv'
    }

    connection = create_connection(
        args.user,
        args.db_password,
        args.db_host,
        args.db_port
    )

    if create_database(args.db_name, connection):
        connection = create_connection(
            args.user,
            args.db_password,
            args.db_host,
            args.db_port,
            args.db_name
        )
        for table in tables_and_files.keys():
            create_tables(connection, table)

    for table, file in tables_and_files.items():
        insert_data_to_db(connection, table, file, args.data_path)
