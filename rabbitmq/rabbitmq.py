import time
from typing import Callable
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
def start_consumer(
        func_callback:Callable
):
    ts=5
    while True:
        send_notify(f"Starting consumer for func `{func_callback.__name__}`")
        try:
            with BlockingConnection(CONNECTION_PARAMS) as connection:
                with connection.channel() as channel:
                    channel.queue_declare(queue='tg_notify')
                    channel.basic_consume(queue='tg_notify',
                                          on_message_callback=func_callback)
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