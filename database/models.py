from database.connector import Table
from datetime import datetime


class Users(Table):
    user_id = None
    tg_id = None
    join_date = None
    table = 'public.users'

    def tg_id_to_db_id(self, tg_id):
        db_id = None
        self.get_user(tg_id=tg_id)

        if self.last_response:
            db_id = self.last_response[0][0]
        return db_id

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
    context = None
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

        source = self.select(condition)[0]

        try:
            if len(self.last_response) == 0:
                return ()

            if len(self.last_response) == 1:
                self.source_id, self.name, self.url, self.context = source
                return source
        except Exception as e:
            return
        return

    def set_url(self, url, name=None):
        if not self.source_id:
            raise Exception("no source selected!")
        condition = {'id': self.source_id}
        data = {'url': url}
        if name:
            data.update({'name': name})
        self.update(condition, data)

    def update_context(self, context):
        if not self.source_id:
            raise Exception("no source selected!")
        condition = {'id': self.source_id}
        data = {'context': context}
        self.update(condition, data)

    def delete(self, condition=None):
        if not condition:
            if self.source_id:
                condition = {'id': self.source_id}
            elif self.name:
                condition = {'name': self.name}
            elif self.url:
                condition = {'url': self.url}

        super().delete(condition)


class Subscription(Table):
    sub_id = None
    source_id = None
    user_id = None
    date = None

    table = 'public.subscription'

    def get_users_subs(self, user_id):
        self.select({"user_id": user_id})
        return self.last_response

    def create(self, user_id, source_id):
        data = {
            "user_id": user_id,
            "source_id": source_id,
        }

        if self.select(data):
            return False

        data.update({"date": datetime.now()})
        self.insert_into(data)
        # self.get(url=url)
        return True
