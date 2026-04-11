from pika import ConnectionParameters, BlockingConnection, callback
from config import CONNECTION_PARAMS
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
def tg_notify_callback(ch, method, properties, body):
    text=""
    arr = json.loads(body.decode())
    for i in arr:
        for key in i.keys():
            text+= f"`{key}`: {i[key]}\n"
            if key == "ip":
                arr.append(get_geolocation(i["ip"]))
        text+="\n"
    send_notify(text)
    ch.basic_ack(delivery_tag=method.delivery_tag)

@logger(
    txtfile="tgnotifybot.txt",
    print_log=True,
    raise_exc=False,
    only_exc=True,
    time_log=True,
)
def start_consumer():
    with BlockingConnection(CONNECTION_PARAMS) as connection:
        with connection.channel() as channel:
            channel.queue_declare(queue='tg_notify')
            channel.basic_consume(queue='tg_notify',
                                  on_message_callback=tg_notify_callback)
            channel.start_consuming()