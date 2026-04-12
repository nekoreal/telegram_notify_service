from config import NOTIFY_CHAT_ID, TELEGRAM_THREADS_ID
from utils.mini_utils import get_geolocation
from .bot import bot
from  utils.logger import  logger
from telegram_markdown_converter  import convert_markdown
from telebot.types import InlineKeyboardMarkup


def json_to_text(json_data):
    if isinstance(json_data, dict):
        json_data = [json_data]
    text=""

    for i in json_data:
        if isinstance(i, dict):
            for key in i.keys():
                text+= f"`{key}`: {i[key]}\n"
                if key == "ip":
                    json_data.append(get_geolocation(i["ip"]))
        else:
            text+= f"`{i}`"
        text+="\n"
    return text


@logger(
    txtfile="tgnotifybot.txt",
    print_log=True,
    raise_exc=False,
    only_exc=True,
    time_log=True,
)
def send_notify(text, parse_mode:str|None="MarkdownV2", thread:str|None=None, parse_like_json:bool=False):
    if parse_like_json:
        text = json_to_text(text)
    if parse_mode:
        text = convert_markdown(text)
    bot.send_message(NOTIFY_CHAT_ID, text, parse_mode=parse_mode, message_thread_id=TELEGRAM_THREADS_ID[thread] if thread else None)

def send_markdown(text, thread:str|None=None, reply_markup:InlineKeyboardMarkup|None=None,parse_like_json:bool=False):
    if parse_like_json:
        text = json_to_text(text)
    bot.send_message(NOTIFY_CHAT_ID,
                     convert_markdown(text),
                     parse_mode="MarkdownV2",
                     message_thread_id=TELEGRAM_THREADS_ID[thread] if thread else None,
                     reply_markup=reply_markup
    )






