import requests
from time import sleep
from datetime import datetime

from database.models import Sources
from database.models import Users
from database.models import Subscription
from database.db import db

from parse.parser import parse
from log.log import write_log
from config import Configuration
from bot import bot


def parser_thread():

    source = Sources(db.get_connection())
    user_table = Users(db.get_connection())
    subscription = Subscription(db.get_connection())

    while True:
        try:
            user_list = user_table.get_all()
            sources = source.get_all()
            for s in sources:
                id_, name, url, context = s

                new_context = parse(url.strip())

                if new_context:
                    new_context = new_context.replace("'", "")

                if new_context != context and new_context:
                    print("new post!\n", new_context)
                    source.get(source_id=id_)
                    source.update_context(new_context)
                    subscription.select({'source_id': id_})
                    print("subscription.last_response:", subscription.last_response)

                    for sub in subscription.last_response:
                        sub_id, source_id, user_id, data = sub
                        user_table.get_user(user_id=user_id)
                        tg_id = user_table.last_response[0][2]
                        url = f"https://api.telegram.org/" \
                              f"bot{Configuration.TOKEN}/" \
                              f"sendMessage?chat_id={tg_id}" \
                              f"&text={new_context}"
                        requests.get(url)

                    for user in user_list:
                        user_id, join, tg_id = user
                        # bot.send_message()

                    print(f"NEW!! \n{new_context}\n time: {datetime.time( datetime.now())} \n------------------")
            sleep(Configuration.parsing_interval)
        except Exception as e:
            print(e)
            write_log(e)

