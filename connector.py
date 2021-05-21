import psycopg2
from datetime import datetime


class Database(object):
    connection: None
    def __init__(self, **kwargs):
        self.connection = psycopg2.connect(**kwargs)

    def get_connection(self):
        return self.connection


class Users(object):
    connection: None
    last_response: None
    user_id: None
    tg_id: None
    join_date: None



    '''
    host = 'localhost'
    database = 'parsers'
    user = 'postgres'
    password = '111111'
    '''
    '''
    CREATE TABLE users (
       id Serial,
       join_date date,
       tg_id varchar(10)
    );
    '''

    table = 'public.users'

    def __init__(self, connection, user_id=None, user_tg_id=None):
        self.connection = connection
        if user_id:
            user = self.select({'id': user_id})

    @staticmethod
    def prepare_condition(condition):
        if not condition:
            return ""

        key, val = condition
        return f" WHERE {key} = '{val}'"

    def do_query(self, query, get_result=False):
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.connection.commit()

        if get_result:
            self.last_response = cursor.fetchall()
        cursor.close()

    def insert_into(self, data):
        values = ''
        keys = ''

        for item in data.items():
            key, val = item

            keys += f"{key}, "
            values += f"'{val}', "

        keys = keys[:-2]
        values = values[:-2]
        query = f'insert into {self.table} ({keys}) values ({values})'
        self.do_query(query)

    def select(self, condition=None):
        query = f"SELECT * FROM {self.table}"

        if condition:
            key, val = condition
            condition = f" WHERE {key} = '{val}'"
            query += condition

        self.do_query(query, get_resurt=True)
        return self.last_response

    def update(self, condition, data):
        set_values = ''

        for item in data.items():
            key, val = item
            set_values += f"{key} = '{val}', "

        set_values = set_values[:-2]
        condition = self.prepare_condition(condition)

        query = f"UPDATE {self.table} SET {set_values} {condition}"

        print(query)

        self.do_query(query)

    def delete(self, condition):
        condition = self.prepare_condition(condition)
        query = f"DELETE FROM {self.table} {condition}"
        self.do_query(query)

    def add(self, u_id):
        data = {
            "join_date": datetime.now(),
            "tg_id": u_id
        }
        self.insert_into(data)
