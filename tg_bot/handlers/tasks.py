
from utils.logger import logger
from tg_bot.bot import bot
from telebot.types import Message
from utils.mini_utils import run_in_thread
from telebot import types
from config import NOTIFY_CHAT_ID, ADMIN_ID, TELEGRAM_THREADS_ID
from tg_bot.senders import send_notify, send_markdown

callback2fa = {}

@logger(
    txtfile="tgnotifybot.txt",
    print_log=True,
    raise_exc=False,
    only_exc=True,
    time_log=True,
)
def callback2fa_pop(key):
    try:
        callback2fa.pop(key)
    except:
        pass

@logger(
    txtfile="tgnotifybot.txt",
    print_log=True,
    raise_exc=False,
    only_exc=True,
    time_log=True,
)
def create_buttons():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("Сделано", callback_data=f"task|Сделано"),
        types.InlineKeyboardButton("Не сделано", callback_data=f"task|Не сделано"),
        types.InlineKeyboardButton("Не успел", callback_data=f"task|Не успел"),
        types.InlineKeyboardButton("Уже не нужно", callback_data=f"task|Уже не нужно"),
        types.InlineKeyboardButton("Удалить", callback_data=f"task|Удалить"),
    )
    return keyboard


@bot.message_handler(
    content_types=['text','photo','video','sticker','document','audio','voice','video_note','location','contact', 'animation', "poll"],
    func=lambda message: message.chat.id==NOTIFY_CHAT_ID and message.from_user.id == ADMIN_ID and message.message_thread_id == TELEGRAM_THREADS_ID["task"] ,
)
@logger(
    txtfile="tgnotifybot.txt",
    print_log=True,
    raise_exc=False,
    only_exc=True,
    time_log=True,
)
def handler_tasks(message: Message):
    run_in_thread(bot.delete_message, NOTIFY_CHAT_ID, message.id)
    text = message.text
    time = "Не указан"
    if '|' in text:
        text, time = map(str, text.split("|"))
    task_text = (f"`Задача`: {text}\n\n"
                 f"`Срок`: {time}")
    send_markdown( thread="task",text=task_text, reply_markup=create_buttons())



@bot.callback_query_handler(
        func=lambda call: call.data.startswith('task|')
        )
@logger(
    txtfile="tgnotifybot.txt",
    print_log=True,
    raise_exc=False,
    only_exc=True,
    time_log=True,
)
def callback_task(call:types.CallbackQuery):
    if call.message.from_user.id == ADMIN_ID:
        bot.answer_callback_query(call.id, text=f"Ты кто такой")
        data=[{
            "user_id": call.message.from_user.id,
            "username": call.message.from_user.username,
            "first_name": call.message.from_user.first_name,
        },{
            "chat_id": call.message.chat.id,
            "chat_name": call.message.chat.title,
            "thread_id": call.message.message_thread_id,
            "message_id": call.message.message_id,
        },{
            "callback_query": call.data,
            "call_id": call.id,
        }]
        send_markdown(thread="guest", text=data  , parse_like_json=True)
        return
    split=call.data.split('|')
    ans = split[1] or ""
    if ans != (callback2fa.get(call.message.id)):
        callback2fa[call.message.id] = ans
        bot.answer_callback_query(call.id, text=f"Нажмите еще раз на {ans} в течении 5 секунд")
        run_in_thread(callback2fa_pop, call.message.id, time_sleep=5)
        return
    run_in_thread(bot.delete_message, NOTIFY_CHAT_ID, call.message.id)
    if ans!="Удалить":
        text = ({"Сделано": "🟢",
                 "Не сделано": "🔴",
                 "Не успел": "🟡",
                 "Уже не нужно": "⚫️"}[ans] +
                call.message.text + f"\n\n`Результат`: {ans}")
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        keyboard.add(types.InlineKeyboardButton("Удалить", callback_data=f"task|Удалить"))
        send_markdown(thread="task_result", text=text,reply_markup=keyboard)




