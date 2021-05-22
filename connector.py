import psycopg2
from datetime import datetime


class Database(object):
    connection: None

    def __init__(self, **kwargs):
        self.connection = psycopg2.connect(**kwargs)

    def get_connection(self):
        return self.connection


class Table(object):
    table: None
    connection: None
    last_response: None

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

    def create_condition(self, condition):
        out = ''
        for item in condition.items():
            key, val = item
            out += f"AND {key} = '{val}'"

        return " WHERE " + out[4:]

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
        query = f"SELECT * FROM {self.table} {self.create_condition(condition)}"

        self.do_query(query, get_result=True)
        return self.last_response

    def update(self, condition, data):
        set_values = ''

        for item in data.items():
            key, val = item
            set_values += f"{key} = '{val}', "

        set_values = set_values[:-2]

        query = f"UPDATE {self.table} SET {set_values} {self.create_condition(condition)}"

        print(query)

        self.do_query(query)

    def delete(self, condition):
        query = f"DELETE FROM {self.table} {self.prepare_condition( condition)}"
        self.do_query(query)


class Users(Table):
    user_id = None
    tg_id = None
    join_date = None
    table = 'public.users'

    def create(self, tg_id):
        data = {
            "join_date": datetime.now(),
            "tg_id": tg_id
        }
        self.insert_into(data)

        self.get_user(tg_id=tg_id)

    def get_user(self, user_id=None, tg_id=None):
        if not user_id and not tg_id:
            return list()

        condition = dict()
        if user_id:
            condition.update({'id': user_id})
        if tg_id:
            condition.update({'tg_id': tg_id})
        try:
            user = self.select(condition)[0]
            self.user_id, self.join_date, self.tg_id = user
            return user
        except IndexError:
            return list()


class Sources(Table):
    source_id = None
    name = None
    url = None
    table = 'public.sources'

    def create(self, name, url):
        data = {
            "name": name,
            "url": url
        }
        self.insert_into(data)

        self.get(url=url)

    def get(self, source_id=None, url=None, name=None):
        condition = {}
        if source_id:
            condition.update({'id': source_id})
        if url:
            condition.update({'url': url})
        if name:
            condition.update({'name': name})

        try:
            source = self.select(condition)[0]
            self.source_id, self.name, self.url = source
            return source
        except IndexError:
            return ()

    def set_url(self, url, name=None):
        if not self.id:
            raise Exception("no source selected!")
        condition = ('id', self.id)
        data = {'url': url}
        if name:
            data.update({'name': name})
        self.update(condition, data)


class Subscription(Table):
    sub_id = None
    source_id = None
    user_id = None
    date = None

    table = 'public.subscription'

    def create(self, user_id, source_id):
        data = {
            "user_id": user_id,
            "source_id": source_id,
            "date": datetime.now()
        }

        self.insert_into(data)
        # self.get(url=url)