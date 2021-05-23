import requests
from models import Sources
from models import Users
from models import Subscription
from time import sleep
from datetime import datetime
from parser import parse
from log import write_log
from config import Configuration
from bot import bot
from database import db


def parser_thread():

    source = Sources(db.get_connection())
    user_table = Users(db.get_connection())

    while True:
        try:
            user_list = user_table.get_all()
            sources = source.get_all()
            for s in sources:
                id_, name, url, context = s
                new_context = parse(url.strip())
                if new_context != context and new_context:
                    source.get(source_id=id_)
                    source.update_context(new_context)
                    for user in user_list:
                        user_id, join, tg_id = user
                        bot.send_message()
                        requests.get(f"https://api.telegram.org/bot{Configuration.TOKEN}/sendMessage?chat_id={tg_id}&text={new_context}")
                    print(f"NEW!! \n{new_context}\n time: {datetime.time( datetime.now())} \n------------------")
            sleep(Configuration.parsing_interval)
        except Exception as e:
            print(e)
            write_log(e)

