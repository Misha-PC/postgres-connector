import requests
from connector import Database
from connector import Sources
from time import sleep
from datetime import datetime
from parser import parse
from log import write_log

TOKEN = r"527820020:AAGj3qIgb_cmkDWWIIXEC4w-"
USERS = ['337804063']


if __name__ == "__main__":
    db = Database(dbname='parsers', user='postgres', password='111111', host='localhost')
    source = Sources(db.get_connection())

    while True:
        try:
            sources = source.get_all()
            for s in sources:
                id_, name, url, context = s
                new_context = parse(url.strip())
                if new_context != context and new_context:
                    source.get(source_id=id_)
                    source.update_context(new_context)
                    for user in USERS:
                        requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={user}&text={new_context}")
                    print(f"NEW!! \n{new_context}\n time: {datetime.time( datetime.now())} \n------------------")
            sleep(15)
        except Exception as e:
            print(e)
            write_log(e)
