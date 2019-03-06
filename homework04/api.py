from typing import List

import requests
import config
import time

from api_models import Message


def get(url, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос

    :param url: адрес, на который необходимо выполнить запрос
    :param params: параметры запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    delay = 0.5
    response = None
    for i in range(max_retries):
        try:
            response = requests.get(url, params, timeout=delay)
            break
        except requests.exceptions.RequestException:
            delay = min(delay * backoff_factor, timeout)
    return response


def get_friends(user_id, fields):
    """ Returns a list of user IDs or detailed information about a user's friends """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    query = "{domain}/friends.get?access_token={access_token}&user_id={user_id}&fields={fields}&v={api_version}" \
        .format(domain=config.VK_CONFIG.get('domain'), access_token=config.VK_CONFIG.get('access_token'),
                user_id=user_id, fields=fields, api_version=config.VK_CONFIG.get("version"))
    return get(query)


def messages_get_history(user_id: int, offset: int = 0, count: int = 20) -> List[Message]:
    """  Get user messages history

    :param user_id: user ID with which we want to get messages
    :param offset: offset from last message
    :param count: count of messages
    :return: json object with messages
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"

    query_params = {
        'access_token': config.VK_CONFIG['access_token'],
        'user_id': user_id,
        'offset': offset,
        'count': min(count, 200),
        'v': config.VK_CONFIG['version']
    }

    messages = []
    while count > 0:
        response = get(config.VK_CONFIG['domain'] + "/messages.getHistory", query_params)
        if response:
            result = response.json()
            if 'error' in result:
                print(result['error']['error_msg'])
            else:
                for message in result['response']['items']:
                    messages.append(Message(**message))
        count -= min(count, 200)
        query_params['offset'] += 200
        query_params['count'] = min(count, 200)

    return messages

print(get_friends(int(config.VK_CONFIG.get('my_id')), '').text)


