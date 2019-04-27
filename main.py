from flask import Flask, request
import logging
import json
import random

from math2 import vibor

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
    session_id = req['session']['session_id']

    # если пользователь новый, то просим его представиться.
    if req['session']['new']:
        res['response']['text'] = 'Привет! Назови свое имя!'
        # созда\м словарь в который в будущем положим имя пользователя
        sessionStorage[session_id] = {
            'first_name': None,
            'reiting': [0, 0],
            'dialog': "continue",
            'question': None
        }

        return

    # если пользователь не новый, то попадаем сюда.
    # если поле имени пустое, то это говорит о том,
    # что пользователь ещё не представился.
    if sessionStorage[session_id]['first_name'] is None:
        # в последнем его сообщение ищем имя.
        first_name = get_first_name(req)
        # если не нашли, то сообщаем пользователю что не расслышали.
        if first_name is None:
            res['response']['text'] = \
                'Не расслышала имя. Повтори, пожалуйста!'
        # если нашли, то приветствуем пользователя.

        else:
            sessionStorage[session_id]['first_name'] = first_name
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
    elif sessionStorage[session_id]['dialog'] is "continue":
        if "да" in req['request']['nlu']['tokens']:
            sessionStorage[session_id]['dialog'] = "play"
            sessionStorage[session_id]['question'] = vibor()
            res['response']['text'] = 'Сколько будет ' + sessionStorage[session_id]['question'][0]

        elif "нет" in req['request']['nlu']['tokens']:
            res['response']['text'] = 'пока'
            res['response']['end_session'] = True
        else:
            res['response']['text'] = 'Я не поняла ответа. Так да ли нет?'

    elif sessionStorage[session_id]['dialog'] is "play":
        if get_number(req) == None:
            res['response']['text'] = 'Повтори я не расслышала'

        elif int(get_number(req)) == sessionStorage[session_id]['question'][1]:
            sessionStorage[session_id]['reiting'] = [sessionStorage[session_id]['reiting'][0] + 1,
                                                  sessionStorage[session_id]['reiting'][1] + 1]
            res['response']['text'] = "Абсолютно верно! Твой рейтинг: " + str(sessionStorage[session_id]['reiting'][
                                                                                  0]) + " из " + str(
                sessionStorage[session_id]['reiting'][1]) + ". Хочешь сыграть еще?"
            sessionStorage[session_id]['dialog'] = "continue"
        else:
            sessionStorage[session_id]['reiting'] = [sessionStorage[session_id]['reiting'][0],
                                                  sessionStorage[session_id]['reiting'][1] + 1]
            res['response']['text'] = "Неверно! Правильный ответ: " + str(
                sessionStorage[session_id]['question'][1]) + ". Твой рейтинг: " + str(sessionStorage[session_id]['reiting'][
                                                                                       0]) + " из " + str(
                sessionStorage[session_id]['reiting'][1]) + ". Хочешь сыграть еще?"
            sessionStorage[session_id]['dialog'] = "continue"


def get_first_name(req):
    # перебираем сущности
    for entity in req['request']['nlu']['entities']:
        # находим сущность с типом 'YANDEX.FIO'
        if entity['type'] == 'YANDEX.FIO':
            # Если есть сущность с ключом 'first_name',
            # то возвращаем ее значение.
            # Во всех остальных случаях возвращаем None.
            return entity['value'].get('first_name', None)


def get_number(req):
    for token in req['request']['nlu']['tokens']:

        if token.isdigit():
            return token
    return None


if __name__ == '__main__':
    app.run()
