import telebot
from config import TELEGRAM_TOKEN
from time import sleep as delay
from utils.logger import logger, make_log

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@logger(
    txtfile="tgnotifybot.txt",
    print_log=True,
    raise_exc=False,
    only_exc=True,
    time_log=True,
)
def run_telegram_bot():
    #import telegram_bot.handlers
    while True:
        try:
            print("Telegram Bot Starting")
            bot.polling(none_stop=True)
        except Exception as e:
            print(e)
            make_log(
                txtfile="tgnotifybot.txt",
                text=f"Telegram bot error: {e}",
                print_log=True,
                time_log=True
            )
            delay(180)