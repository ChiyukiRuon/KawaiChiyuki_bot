import datetime
import json
import random

import pytz
import requests

tz = pytz.timezone('Asia/Shanghai')
now_time = datetime.datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')


def pixiv_rank(rank_type):
    """获取Pixiv排行榜图片,总共获取50张

    :param rank_type 排行榜类型

    day: 日榜;

    week: 周榜;

    month: 月榜;

    day_male: 男性向;

    day_female: 女性向;

    [day|week|day_male|day_female]_r18: R18;

    week_original: 原创;

    week_rookie: 新人;

    week_r18g: R18G
    """

    resp_list = []
    url = 'https://api.obfs.dev/api/pixiv/rank?mode={}'.format(rank_type)
    pic_json = json.loads(requests.get(url).content)
    pic_list = pic_json.get('illusts')
    if pic_list is None:
        resp_list = [pic_info(pic_json, 1)]
    else:
        for i in range(len(pic_list)):
            response = pic_info(pic_json, i)

            resp_list.append(response)

    return resp_list


def random_pic():
    tags_url = 'https://api.obfs.dev/api/pixiv/tags'
    search_url = 'https://api.obfs.dev/api/pixiv/search?word='
    user = ['1000', '3000', '5000', '7500', '10000', '30000', '50000']
    tag_list = json.loads(requests.get(tags_url).content).get('trend_tags')
    while True:
        try:
            rand_user = user[random.randint(0, 6)]
            rand_tag = random.randint(0, 39)
            tag = tag_list[rand_tag].get('tag')
            pic_json = json.loads(requests.get(search_url + tag + ' ' + rand_user + 'users入り').content)
            print('{}:"random_pic"tag:{},user:{}'.format(now_time, tag, rand_user))
            rand_pic = random.randint(0, 29)
            response = pic_info(pic_json, rand_pic)
            print('{}:"random_pic"resp:{}'.format(now_time, response))
            if len(response) != 0: break
        except Exception as e:
            print('{}:"random_pic"{}'.format(now_time, e))

    return response


def pic_info(pic_json, key):
    pic_list = pic_json.get('illusts')
    if pic_list is None:
        msg = pic_json.get('error').get('message')
        print('{}:"pic_info"获取图片时发生错误{}'.format(now_time, msg))
        response = {
            'message': msg
        }
    else:
        title = pic_list[key].get('title')
        pid = pic_list[key].get('id')
        username = pic_list[key].get('user').get('name')
        if len(pic_list[key].get('meta_pages')) != 0:
            url = pic_list[key].get('meta_pages')[0].get('image_urls').get('medium')
            num = len(pic_list[key].get('meta_pages'))
        else:
            url = pic_list[key].get('meta_single_page').get('original_image_url')
            num = 1

        response = {
            'pid': pid,
            'title': title,
            'username': username,
            'url': url,
            'num': num
        }

    return response
