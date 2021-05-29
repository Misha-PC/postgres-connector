from bot.bot import bot
from database.models import Users
from database.models import Sources
from database.models import Subscription
from database.db import db
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
        bot.send_message(message.chat.id, "это админская команда.")
        return

    sp = message.text.split(',')
    print(sp)
    try:
        name, url = sp
    except Exception as e:
        print(e)
        return

    name = name[5:]

    print("name:", name)
    print("url:", url)

    source = Sources(db.get_connection())
    source.create(name, url)

    bot.send_message(message.chat.id, f"new sources ({name} - {url}) added success.")


@bot.message_handler(commands=['rename'])
def rename(message):
    if not str(message.chat.id) in Configuration.admins:
        bot.send_message(message.chat.id, "это админская команда.")
        return

    sp = message.text.split(',')
    print(sp)
    try:
        id_, name = sp
    except Exception as e:
        print(e)
        return

    id_ = int(id_.split()[1])

    print("id:", id_)
    print("name:", name)

    source = Sources(db.get_connection())
    source.update({"id": id_}, {"name": name})

    # bot.send_message(message.chat.id, f"new sources ({name} - {url}) added success.")


@bot.message_handler(commands=['getSources'])
def get_source(message):
    if not str(message.chat.id) in Configuration.admins:
        return

    callback = ''
    source = Sources(db.get_connection())
    all_sources = source.get_all()
    for source_name in all_sources:
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


@bot.message_handler(func=lambda message: message.text == "подписки")
@bot.message_handler(commands=['mySources'])
def my_sources(message):
    source = Sources(db.get_connection())
    sources = source.get_all()
    sub = Subscription(db.get_connection())

    user = Users(db.get_connection())
    user.get_user(tg_id=message.chat.id)
    subs = sub.get_users_subs(user.user_id)

    if not subs:
        bot.send_message(message.chat.id, 'у вас нет активных подписок :(\n'
                                          'Что бы оформить подписку нажмите /sources')
        return

    source_names = dict()
    keyboard = types.InlineKeyboardMarkup()  #Клавиатура

    for s in sources:
        source_names.update({s[0]: s[1]})

    print(source_names)

    for s in subs:
        id_, s_id, u_id, date = s
        keyboard.add(types.InlineKeyboardButton(text=source_names[s_id], callback_data=f'del:{s_id}'))

    question = 'Ваши подписки. Что бы отписаться просто нажмите на ненужные.:'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == "источники")
@bot.message_handler(commands=['sources'])
def start(message):
    keyboard = types.InlineKeyboardMarkup()  #Клавиатура

    source = Sources(db.get_connection())
    all_sources = source.get_all()
    sources_names = list()
    for source in all_sources:
        sources_names.append([source[1], f"add:{source[0]}"])

    for res in sources_names:
        keyboard.add(types.InlineKeyboardButton(text=res[0], callback_data=res[1]))

    question = 'Выберите новостные порталы:'
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    def add_sub(tg_id, source_id):
        user = Users(db.get_connection())
        subscription = Subscription(db.get_connection())
        source = Sources(db.get_connection())

        user.get_user(tg_id=tg_id)
        source.get(source_id=source_id)

        print("add tg_id: ", tg_id)
        print("add sub_id: ", source_id)

        if not subscription.create(user.user_id, source_id):
            bot.send_message(tg_id, f'Вы уже подписаны на "{source.name}".')
            return

        bot.send_message(tg_id, f'Подписка на "{source.name}" оформлена.')
        bot.send_message(tg_id, source.context)

    def del_sub(tg_id, source_id):
        user = Users(db.get_connection())
        subscription = Subscription(db.get_connection())
        source = Sources(db.get_connection())

        user.get_user(tg_id=tg_id)

        subscription.delete({
            'source_id': source_id,
            'user_id': user.user_id
        })

        source.get(source_id=source_id)

        print("del tg_id: ", tg_id)
        print("del sub_id: ", source_id)

        bot.send_message(tg_id, f'Подписка на "{source.name}" отменена.')

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
