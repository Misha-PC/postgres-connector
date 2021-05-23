from threading import Thread
import handlers

from parser_thread import parser_thread
from bot_thread import bot_thread

if __name__ == "__main__":
    thread1 = Thread(target=parser_thread)
    thread2 = Thread(target=bot_thread)

    thread1.start()
    thread2.start()
