from telethon import TelegramClient
import time
import os
import progressbar
from random import randint
from dotenv import dotenv_values

"""
    В папке app создать файл .env и записать API_ID, API_HASH В виде:
    API_ID=***********
    API_HASH=***********************************
    Данные можно получить с https://my.telegram.org/apps
"""
ENV_VARIABLES = dotenv_values('.env')
API_ID, API_HASH = int(ENV_VARIABLES.get('API_ID')), ENV_VARIABLES.get('API_HASH')

client = TelegramClient('anon', API_ID, API_HASH)


async def main():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")

    print('Рассылка началась')

    dialogs = await client.get_dialogs()
    groups = [dialog.entity for dialog in dialogs if dialog.is_group]
    bar = progressbar.ProgressBar(
        widgets=[progressbar.SimpleProgress()],
        maxval=len(groups),
    ).start()
    i = 0

    message = ''
    with open('message.txt', 'r') as file:
        message = file.read()

    async for dialog in client.iter_dialogs():
        if dialog.is_group:
            try:
                await client.send_message(dialog.id, message)
                print(f'Сообщение отправлено в {dialog.name}')
                i += 1
                bar.update(i)
            except Exception:
                print(f'Не удалось отправить сообщение в {dialog.name}')
            time.sleep(randint(0, 5))
    bar.finish()
    print('Рассылка закончилась')

with client:
    while True:
        client.loop.run_until_complete(main())
        time.sleep(100)
