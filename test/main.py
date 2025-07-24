import requests
import time


API_URL = 'https://api.telegram.org/bot'
API_CAT_URL = 'https://api.thecatapi.com/v1/images/search'
BOT_TOKEN = '7289036480:AAH45BfxRMWbVc7HJ_hFep2biA8f3eNL5vY'
ERROR_TEXT = 'Сосал?'
MAX_COUNTER = 100

offset = -2
counter = 0
chat_id: int

while counter < MAX_COUNTER:

    print('attempt =', counter)  #Чтобы видеть в консоли, что код живет

    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()

    if updates['result']:
        for result in updates['result']:

            cat = requests.get(API_CAT_URL)

            offset = result['update_id']
            chat_id = result['message']['from']['id']

            if cat.status_code == 200:
                cat_link = cat.json()[0]['url']
                requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={cat_link}')
            else:
                requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={ERROR_TEXT}')

    time.sleep(1)
    counter += 1