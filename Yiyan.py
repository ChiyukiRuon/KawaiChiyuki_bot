import json

import requests

import Functions


def hitokoto():
    """一言二次元语录

    :return: {'content','source'}
    """
    now_time = Functions.get_time()
    url = 'https://international.v1.hitokoto.cn?c=a&c=b&c=c&c=l'
    yan = json.loads(requests.get(url).content)
    if yan.get('hitokoto') is None:
        response = {
            'message': '获取一言失败'
        }
        print('[{}]"hitokoto":获取一言失败'.format(now_time))
    else:
        content = yan.get('hitokoto')
        source = yan.get('from')
        response = {
            'content': content,
            'source': source
        }
        print('[{}]"hitokoto":获取一言成功{}'.format(now_time, response))

    return response
