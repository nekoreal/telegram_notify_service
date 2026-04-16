from utils.JSONformatter import json_format
from utils.logger import logger
from tg_bot.bot import bot
from telebot.types import Message
from utils.mini_utils import run_in_thread
from telebot import types
from config import NOTIFY_CHAT_ID, ADMIN_ID, TELEGRAM_THREADS_ID
from tg_bot.senders import send_notify


@bot.message_handler(
    content_types=['text','photo','video','sticker','document','audio','voice','video_note','location','contact', 'animation', "poll"],
    func=lambda message: message.chat.id!=NOTIFY_CHAT_ID
                         or message.from_user.id != ADMIN_ID
                         or (not((message.message_thread_id or None) in TELEGRAM_THREADS_ID.values() )),
)
@logger(
    txtfile="tgnotifybot.txt",
    print_log=True,
    raise_exc=False,
    only_exc=True,
    time_log=True,
)
def handler_guests(message: Message):
    data = [
    {
        "user_id": message.from_user.id,
        "username": message.from_user.username,
        "first_name": message.from_user.first_name,
    },{
        "chat_id": message.chat.id,
        "chat_name": message.chat.title,
        "chat_type": message.chat.type,
        "message_id": message.message_id,
        "message_thread_id": message.message_thread_id,
    },{
        "text": message.text or message.caption or "Empty",
        "content_type": message.content_type or "Empty",
    }
    ]
    send_notify(text=json_format(data),thread="guest")