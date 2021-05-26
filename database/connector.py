import psycopg2


class Database(object):
    connection: None

    def __init__(self, **kwargs):
        self.connection = psycopg2.connect(**kwargs)

    def get_connection(self):
        return self.connection


class Table(object):
    table: None
    connection: None
    last_response = None

    def __init__(self, connection, user_id=None, user_tg_id=None):
        self.connection = connection
        if user_id:
            user = self.select({'id': user_id})

    @staticmethod
    def create_condition(condition=None):
        if not condition:
            return ''

        out = ''
        for item in condition.items():
            key, val = item
            out += f"AND {key} = '{val}'"

        return " WHERE " + out[4:]

    def do_query(self, query, get_result=False):
        # print("do query", query)
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

    def get_all(self):
        self.select()
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

    def delete(self, condition=None):
        query = f"DELETE FROM {self.table} {self.create_condition(condition)}"
        self.do_query(query)

