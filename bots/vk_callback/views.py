import vk
from flask import request, json

from business_client.views import get_st
from . import vk_callback

# не трогайте мой токен, плз
token = '71327b6ad3c5a2e1aa36fc8d4ddd303fb90e23a016c16f3f53d0168e7f1f11e393947fc76b1bd2d4dd6a2'
confirmation_token = "177201d0"


@vk_callback.route('/')
def hello_world():
    return 'Короче, тут бот для ВК.'


@vk_callback.route('/', methods=['POST'])
def processing():
    data = json.loads(request.data)
    print(data)
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return confirmation_token
    elif data['type'] == 'message_new':
        session = vk.Session()
        api = vk.API(session, v=5.75)
        user_id = data['object']['user_id']
        message_text = data['object']['body']
        message_text = str(message_text).split()
        if len(message_text) == 1:
            if message_text[0].lower() == "привет":
                api.messages.send(access_token=token, user_id=str(user_id), message="Привет")
        if len(message_text) == 2:
            if message_text[0].lower() == "посылка":
                order_id = message_text[1]
                responce_message = get_st(order_id)
                api.messages.send(access_token=token, user_id=str(user_id), message=responce_message)

        return 'ok'
