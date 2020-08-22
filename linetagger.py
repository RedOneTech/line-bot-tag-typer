endpoint = 'https://line-tag-bot.herokuapp.com/'
token = input('Mohon masukk')

import requests
from pynput.keyboard import Key, Controller
import time

while True:
    r = requests.get(endpoint, params={
        'token' : token
    })

    res = r.json()
    keyboard = Controller()

    index = 1
    for member in res['members']:
        keyboard.type(f"@{member}")
        time.sleep(0.5)
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

        if index % 20 == 0:
            keyboard.press(Key.alt_l)
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            keyboard.release(Key.alt_l)

    if index != 1:
        keyboard.press(Key.alt_l)
        keyboard.press(Key.enter)
        time.sleep(0.5)
        keyboard.release(Key.enter)
        keyboard.release(Key.alt_l)

    time.sleep(5)