from config import NOTIFY_CHAT_ID
from . import bot
from  utils.logger import  logger

@logger(
    txtfile="tgnotifybot.txt",
    print_log=True,
    raise_exc=False,
    only_exc=True,
    time_log=True,
)
def send_notify(text, parse_mode:str="Markdown"):
    bot.send_message(NOTIFY_CHAT_ID, text, parse_mode=parse_mode)

