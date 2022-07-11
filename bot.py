from collections.abc import Iterable, Iterator
from sys import version
import telebot
import os
import sqlite3
from typing import TypeVar
import marshal
import atexit

bot = telebot.TeleBot(os.environ["TG_TOKEN"])



T = TypeVar('T')

try:
  with open('db', 'rb') as f:
    db = marshal.load(f)
except (FileNotFoundError, EOFError):
  db = {}

@atexit.register
def save_db():
  with open('db', 'wb') as f:
    marshal.dump(db, f, 4)


@bot.message_handler(commands=['stats'])
def stats(msg):
  #bot.reply_to(msg, create_stats())
  bot.send_message(msg.chat.id, '\n'.join(
    f'{username} - {tirsks}' for username, tirsks in sorted(db.values(), key=lambda x: x[1])
  ))


@bot.message_handler(func=lambda msg: isinstance(msg.text, str) and 'tirsk' in msg.text)
def record(msg):
  db[msg.from_user.id] = (
    msg.from_user.username,
    db.get(msg.from_user.id, ('', 0))[1] + 1
  )


def run():
  bot.infinity_polling()


if __name__ == "__main__":
  run()
