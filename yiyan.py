import json

import requests

import bot


def hitokoto():
    """一言二次元语录

    :return: {'content':[str], 'source':[str]}
    """
    url = 'https://international.v1.hitokoto.cn?c=a&c=b&c=c&c=l'
    yan = json.loads(requests.get(url).content)

    if yan.get('hitokoto') is None:
        response = {
            'message': '获取一言失败'
        }

        bot.log_output('"hitokoto":获取一言失败')

    else:
        content = yan.get('hitokoto')
        source = yan.get('from')

        response = {
            'content': content,
            'source': source
        }

        bot.log_output('"hitokoto":获取一言成功{}'.format(response))

    return response
