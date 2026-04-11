import threading
import re
from functools import wraps
from time import sleep
from typing import Callable
import requests

def get_geolocation(ip):
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}')
        data = response.json()
        return {
            'country': data.get('countryCode', ''),
            'city': data.get('city', ''),
            'region': data.get('regionName', '')
        }
    except:
        return {'country': '', 'city': '', 'region': ''}



def sleep_func(time_sleep:int=15) -> Callable:
    def wrapper(func:Callable) -> Callable:
        @wraps(func)
        def inner(*args, **kwargs):
            sleep(time_sleep)
            return func(*args, **kwargs)
        return inner
    return wrapper



def run_in_thread(target_func, *args, time_sleep:int=None, **kwargs):
    """
    Запускает функцию target_func в отдельном потоке.
    Аргументы *args и **kwargs передаются в функцию.
    """
    if time_sleep:
        target_func = sleep_func(time_sleep)(target_func)
    thread = threading.Thread(target=target_func, args=args, kwargs=kwargs)
    thread.start()
    return thread

def escape_markdown(text):
    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', text)