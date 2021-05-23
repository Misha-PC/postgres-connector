import telebot
from config import Configuration


bot = telebot.AsyncTeleBot(Configuration.TOKEN)
