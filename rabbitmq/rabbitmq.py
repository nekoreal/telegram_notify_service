import time

from pika import ConnectionParameters, BlockingConnection, callback, exceptions
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
    ts=5
    while True:
        send_notify("Starting consumer")
        try:
            with BlockingConnection(CONNECTION_PARAMS) as connection:
                with connection.channel() as channel:
                    channel.queue_declare(queue='tg_notify')
                    channel.basic_consume(queue='tg_notify',
                                          on_message_callback=tg_notify_callback)
                    channel.start_consuming()

        except  exceptions.ConnectionClosedByBroker:
            send_notify("Соединение закрыто брокером. Переподключение...")
            time.sleep(5)
            continue
        except exceptions.AMQPConnectionError as e:
            send_notify(f"Ошибка соединения: {e}. Переподключение через 5 секунд...")
            time.sleep(5)
            continue
        except Exception as e:
            send_notify(f"Неизвестная ошибка: {e}. Перезапуск...")
            time.sleep(ts)
            ts = ts * 2
            continue
        finally:
            try:
                connection.close()
            except:
                pass