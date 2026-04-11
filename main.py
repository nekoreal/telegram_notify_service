from utils.mini_utils import run_in_thread
from tg_bot import run_telegram_bot
from rabbitmq.rabbitmq import start_consumer


def main():
    run_in_thread(run_telegram_bot)
    run_in_thread(start_consumer)


if __name__ == '__main__':
    main()