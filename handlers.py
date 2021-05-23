from bot import bot
from models import Users
from models import Sources
from models import Subscription
from database import db
from config import Configuration
from telebot import types

@bot.message_handler(commands=['start'])
def start_message(message):
    print(f"------------\n\tStart \n\tchat id: {message.chat.id}\n------------")
    bot.send_message(message.chat.id, 'Привет, ты написал мне /start')
    user = Users(db.get_connection())
    user.create(message.chat.id)


@bot.message_handler(commands=['add'])
def add_source(message):
    if not str(message.chat.id) in Configuration.admins:
        return

    try:
        name, url = message.text.split()[1:]
    except Exception as e:
        print(e)
        return

    source = Sources(db.get_connection())
    source.create(name, url)

    bot.send_message(message.chat.id, f"new sources ({name} - {url}) added success.")


@bot.message_handler(commands=['getSources'])
def get_source(message):
    if not str(message.chat.id) in Configuration.admins:
        return

    callback = ''
    source = Sources(db.get_connection())
    all_sorces = source.get_all()
    for source_name in all_sorces:
        callback += f"{source_name[0]}) {source_name[1]}\n"

    bot.send_message(message.chat.id, callback)


@bot.message_handler(commands=['getScore'])
def get_score(message):
    if not str(message.chat.id) in Configuration.admins:
        return

    user = Users(db.get_connection())
    user_count = len(user.get_all())
    bot.send_message(message.chat.id, f"Всего пользователей: {user_count}")


@bot.message_handler(commands=['removeSources'])
def remove_source(message):
    if not str(message.chat.id) in Configuration.admins:
        return

    source_id = message.text.split()[1]

    source = Sources(db.get_connection())
    id_, name, url, context = source.get(source_id=source_id)
    source.delete()

    bot.send_message(message.chat.id, f"Источник {id_}:{name} был удалён!\n"
                                      f"Если вы хотите его вернуть введите:\n"
                                      f"\"/add {name} {url}\"")


@bot.message_handler(commands=['mySources'])
def my_sources(message):
    source = Sources(db.get_connection())
    sources = source.get_all()
    sub = Subscription(db.get_connection())

    user = Users(db.get_connection())
    user.get_user(tg_id=message.chat.id)
    subs = sub.get_users_subs(user.user_id)

    source_names = dict()
    # sub_names = list()
    msg = 'ваши подписки:\n'

    for s in sources:
        source_names.update({s[0]: s[1]})

    print(source_names)

    for s in subs:
        id_, s_id, u_id, date = s
        msg += f"\t* {source_names[s_id]}\n"

    bot.send_message(message.chat.id, msg)


@bot.message_handler(func=lambda message: message.text == "новости")
@bot.message_handler(commands=['news'])
def start(m):
    keyboard = types.InlineKeyboardMarkup()  #Клавиатура

    source = Sources(db.get_connection())
    all_sources = source.get_all()
    sources_names = list()
    for source in all_sources:
        sources_names.append([source[1], {source[0]}])

    for res in sources_names:
        keyboard.add(types.InlineKeyboardButton(text=res[0], callback_data=res[1]))

    question = 'Выберите новостные порталы:'
    bot.send_message(m.from_user.id, text=question, reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == "test")
@bot.message_handler(commands=['test'])
def start(m):
    keyboard = types.InlineKeyboardMarkup()  #Клавиатура

    source = Sources(db.get_connection())
    all_sources = source.get_all()
    sources_names = list()
    for source in all_sources:
        sources_names.append([source[1] + " test", f"add:{source[0]}"])

    for res in sources_names:
        keyboard.add(types.InlineKeyboardButton(text=res[0], callback_data=res[1]))

    question = 'Выберите новостные порталы:'
    bot.send_message(m.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    def add_sub(tg_id, sub_id):
        user = Users(db.get_connection())
        subscription = Subscription(db.get_connection())
        source = Sources(db.get_connection())

        user.get_user(tg_id=tg_id)
        subscription.create(user.user_id, sub_id)
        source.get(source_id=sub_id)

        bot.send_message(tg_id, f'Подписка на "{source.name}" оформлена.')

        print("add tg_id: ", tg_id)
        print("add sub_id: ", sub_id)

    def del_sub(u_id, sub_id):
        print("del u_id: ", u_id)
        print("del sub_id: ", sub_id)
    if not ":" in call.data:
        return
    code, value = call.data.split(":")

    handler_list = {
        'add': add_sub,
        'del': del_sub
    }

    handler_list[code](call.message.chat.id, value)


    print(call.data)
    # bot.clear_step_handler(call.message)
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
