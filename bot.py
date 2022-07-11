import telebot
import os
import marshal
import atexit


def create_db():
  try:
    with open('db', 'rb') as f:
      db = marshal.load(f)
  except (FileNotFoundError, EOFError):
    db = {}

  @atexit.register
  def save_db():
    with open('db', 'wb') as f:
      marshal.dump(db, f, 4)

  return db

def create_bot():
  db = create_db()
  bot = telebot.TeleBot(os.environ["TG_TOKEN"])

  @bot.message_handler(commands=['stats'])
  def stats(msg):
    print('stats', flush=True)
    if len(db) == 0:
      bot.send_message(msg.chat.id, "Kukaan ei oo vielä tirskahtanut!!! :(")
      return
    bot.send_message(msg.chat.id, '\n'.join(
      f'{username} - {tirsks}' for username, tirsks in sorted(db.values(), key=lambda x: x[1])
    ))


  @bot.message_handler(func=lambda msg: isinstance(msg.text, str) and 'tirsk' in msg.text.lower())
  def record(msg):
    print('got msg', flush=True)
    new_tirsks = db.get(msg.from_user.id, ('', 0))[1] + 1
    db[msg.from_user.id] = (
      msg.from_user.username,
      new_tirsks
    )
    bot.reply_to(msg, f"KIINNI JÄIT! Tästä sakotetaan vielä... Olet tirskahtanut nyt {new_tirsks} kertaa")

  return bot

def run():
  print("starting bot", flush=True)
  create_bot().infinity_polling()

def daemonize():
  import daemon.pidfile
  import daemon
  basepath = os.getcwd()
  context = daemon.DaemonContext(
    stdout=open(f'{basepath}/stdout', 'wb+', buffering=0),
    stderr=open(f'{basepath}/stderr', 'wb+', buffering=0),
    working_directory='/u/30/sirenj6/unix/tipahdusbot/',
    pidfile=daemon.pidfile.PIDLockFile(f'{basepath}/tipahtanutbot.pid')
  )
  print('starting daemon')
  with context:
    run()

if __name__ == "__main__":
  run()
