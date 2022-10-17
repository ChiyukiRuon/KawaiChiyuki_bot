import os
import requests
import re
import time
import json

COOKIE = os.getenv('COOKIE')
headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Mobile/15E148 Safari/604.1',
    'cookie': COOKIE
}


# TODO 从pixiv获取随机图片
def get_img_url():
    r = requests.get('https://www.dmoe.cc/random.php?return=json')
    url = json.loads(r.content)['imgurl']

    return url
