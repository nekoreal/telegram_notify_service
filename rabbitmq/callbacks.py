import json

from config import TELEGRAM_THREADS_ID
from tg_bot.senders import send_notify
from utils.JSONformatter import json_format
from utils.logger import logger
from utils.mini_utils import get_geolocation


@logger(
    txtfile="tgnotifybot.txt",
    print_log=True,
    raise_exc=False,
    only_exc=True,
    time_log=True,
)
def tg_notify_callback(
        ch,
        method,
        properties,
        body
):
    data:dict = json.loads(body.decode())
    thread:str|None =  data["type"] or None
    try:
        if thread=='request':
            data['data'].append(get_geolocation(data['data'][1]['ip']))
    except:
        pass
    send_notify(text=json_format(data),thread=thread)
    ch.basic_ack(delivery_tag=method.delivery_tag)