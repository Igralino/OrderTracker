# coding: utf-8
from __future__ import unicode_literals

import json
import logging

from flask import request

from business_client.views import get_st
from . import alice_dialogs

logging.basicConfig(level=logging.DEBUG)


@alice_dialogs.route("/", methods=['POST'])
def main():
    # Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )


# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        res['response']['text'] = 'Привет! Я бот, который помогает отследить посылки. Попробуем?'
        res['response']['buttons'] = [
            {'title': "Отследить", 'hide': True}, {'title': "Помощь", 'hide': True}
        ]
        return
    # Обрабатываем ответ пользователя.
    if req['request']['command'].lower() == 'помощь':
        res['response']['text'] = 'Для того, чтобы отследить посылку, укажите её номер, в формате ******-******.'
        return

    # Обрабатываем ответ пользователя.
    if req['request']['command'].lower() in [
        'отследить',
        'трек',
        'где',
        'скоро',
    ]:
        res['response']['text'] = 'Укажите номер посылки:'
        return

    # Обрабатываем ответ пользователя.
    number = req['request']['command']
    print(number)
    if len(number) == 13:
        if number[6] == '-':
            res['response']['text'] = get_st(req['request']['command'])
            return

    # Если он ввел не то, выдаем стандартный ответ:
    res['response']['text'] = 'Напишите, что вы хотите сделать?'
    res['response']['buttons'] = [
        {'title': "Отследить", 'hide': True}, {'title': "Помощь", 'hide': True}
    ]
