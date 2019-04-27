from flask import Flask, request
import logging
import json
import random

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)

# создаём словарь, где для каждого пользователя мы будем хранить его имя и остальное
sessionStorage = {}


@app.route('/post', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(response, request.json)
    logging.info('Response: %r', response)
    return json.dumps(response)


def handle_dialog(res, req):
    user_id = req['session']['user_id']

    # если пользователь новый, то просим его представиться.
    if req['session']['new']:
        res['response']['text'] = 'Привет! Назови свое имя!'
        # созда\м словарь в который в будущем положим имя пользователя
        sessionStorage[user_id] = {
            'first_name': None,
            'reiting': None,
            'number': None,
            'dialog': "continue"
        }

        return

    # если пользователь не новый, то попадаем сюда.
    # если поле имени пустое, то это говорит о том,
    # что пользователь ещё не представился.
    if sessionStorage[user_id]['first_name'] is None:
        # в последнем его сообщение ищем имя.
        first_name = get_first_name(req)
        # если не нашли, то сообщаем пользователю что не расслышали.
        if first_name is None:
            res['response']['text'] = \
                'Не расслышала имя. Повтори, пожалуйста!'
        # если нашли, то приветствуем пользователя.

        else:
            sessionStorage[user_id]['first_name'] = first_name
            res['response'][
                'text'] = 'Приятно познакомиться, ' + first_name.title() \
                          + '. Я - Алиса. Хочешь позаниматься математикой?'
            # получаем варианты buttons из ключей нашего словаря cities
            res['response']['buttons'] = [
                {
                    'title': "Да",
                    'hide': True
                },

                {
                    'title': "Нет",
                    'hide': True
                }
            ]
    # если мы знакомы с пользователем и он нам что-то написал,
    # и если он отвечает на вопрос хочет ли он играть
    elif sessionStorage[user_id]['dialog'] is "continue":
        if "да" in req['request']['nlu']['tokens']:
            res['response']['text'] = 'понятно'
        elif "нет" in req['request']['nlu']['tokens']:
            req['response']['response']['end_session'] = True
        else:
            res['response']['text'] = 'Я не поняла ответа. Так да ли нет?'


def get_first_name(req):
    # перебираем сущности
    for entity in req['request']['nlu']['entities']:
        # находим сущность с типом 'YANDEX.FIO'
        if entity['type'] == 'YANDEX.FIO':
            # Если есть сущность с ключом 'first_name',
            # то возвращаем ее значение.
            # Во всех остальных случаях возвращаем None.
            return entity['value'].get('first_name', None)


if __name__ == '__main__':
    app.run()
