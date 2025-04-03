import requests
import time

TOKEN = '8149809185:AAHTkLEtiv11ELn40aSrM70-D2ZShjTTYYw'
URL = f'https://api.telegram.org/bot{TOKEN}/'

def get_updates(offset=None):
    print("Отримуємо оновлення...")
    params = {'offset': offset, 'timeout': 30}
    response = requests.get(URL + 'getUpdates', params=params)
    updates = response.json()
    print(f"Оновлення отримано: {updates}") 
    return updates

def get_last_chat_info(update):
    try:
        chat_id = update['message']['chat']['id']
        text = update['message']['text']
        username = update['message']['from'].get('username', 'Невідомий користувач')  
        return chat_id, text, username
    except KeyError:
        return None, None, None

def send_message(chat_id, text):
    print(f"Відправляємо повідомлення в чат {chat_id}...")
    params = {'chat_id': chat_id, 'text': text}
    response = requests.get(URL + 'sendMessage', params=params)
    print(f"Відповідь від Telegram: {response.json()}")

def main():
    print("Бот запущений...")
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if 'result' in updates and len(updates['result']) > 0:
            for update in updates['result']:
                last_update_id = update['update_id'] + 1
                chat_id, text, username = get_last_chat_info(update)
                if chat_id and text:
                    response_text = f'@{username} надіслав повідомлення: {text}'
                    send_message(chat_id, response_text)
        time.sleep(2)  

if __name__ == '__main__':
    main()
