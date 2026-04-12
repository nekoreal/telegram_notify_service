import json

from tg_bot.senders import send_notify
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
    text=""
    data:dict = json.loads(body.decode())
    #type:str = data["type"]
    send_notify(text=data,thread="request", parse_like_json=True)

    ch.basic_ack(delivery_tag=method.delivery_tag)