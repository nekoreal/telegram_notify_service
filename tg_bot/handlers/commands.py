
from utils.logger import logger
from tg_bot.bot import bot
from telebot.types import Message
from utils.mini_utils import run_in_thread
from telebot import types

"""@logger(
    txtfile="tgnotifybot.txt",
    print_log=True,
    raise_exc=False,
    only_exc=True,
    time_log=True,
)
@bot.message_handler()
def handler_msgs(message: Message):
    print(message.from_user.id, message.chat.id, message.message_thread_id,message.text)"""