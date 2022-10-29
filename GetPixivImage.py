import json
import random

import requests

import Functions


def pixiv_rank(rank_type):
    """获取Pixiv排行榜图片,总共获取50张

    day: 日榜;

    week: 周榜;

    month: 月榜;

    day_male: 男性向;

    day_female: 女性向;

    [day|week|day_male|day_female]_r18: R18;

    week_original: 原创;

    week_rookie: 新人;

    week_r18g: R18G

    :param rank_type: 想要获取的排行榜类型
    :return: [{'pid':[int], 'title':[str], 'username':[str], 'url':[str], 'num':[int]},{},...]
    """
    now_time = Functions.get_time()
    resp_list = []
    url = 'https://api.obfs.dev/api/pixiv/rank?mode={}'.format(rank_type)
    try:
        pic_json = json.loads(requests.get(url).content)
    except Exception as e:
        print('[{}]"pixiv_rank":获取图片信息失败{}'.format(now_time, e))

        resp_list = [
            {
                'message': e
            }
        ]
        return resp_list
    pic_list = pic_json.get('illusts')
    if pic_list is None:
        resp_list = [pic_info(pic_json, 1)]
    else:
        for i in range(len(pic_list)):
            response = pic_info(pic_json, i)

            resp_list.append(response)

    return resp_list


def random_pic():
    """获取随机Pixiv图片

    :return: {'pid':[int] ,'title':[str], 'username':[str], 'url':[str], 'num':[int}}
    """
    now_time = Functions.get_time()
    tags_url = 'https://api.obfs.dev/api/pixiv/tags'
    search_url = 'https://api.obfs.dev/api/pixiv/search?word='
    user = ['1000', '3000', '5000', '7500', '10000', '30000', '50000']  # 搜索时用到的热度关键词
    try:
        tag_list = json.loads(requests.get(tags_url).content).get('trend_tags')    # 获取当前Pixiv的热门tag
    except Exception as e:
        print('[{}]"random_pic":获取图片信息失败{}'.format(now_time, e))

        response = {
            'message': '获取图片信息失败{}'.format(e)
        }

        return response
    while True:
        try:
            rand_user = user[random.randint(0, 6)]  # 随机一个热度标签
            # 随机获取一个热门tag
            rand_tag = random.randint(0, 39)
            tag = tag_list[rand_tag].get('tag')
            # 搜索并拿到json格式的结果
            pic_json = json.loads(requests.get(search_url + tag + ' ' + rand_user + 'users入り').content)

            print('[{}]"random_pic":tag:{},user:{}'.format(now_time, tag, rand_user))

            # 从搜索结果中随机拿出一张图片
            rand_pic = random.randint(0, 29)
            response = pic_info(pic_json, rand_pic)

            print('[{}]"random_pic":resp:{}'.format(now_time, response))

            # 如果成功拿到图片信息就跳出循环，否则重复上述步骤直至成功
            if len(response) != 0:
                break

        except Exception as e:
            print('[{}]"random_pic":{}'.format(now_time, e))

    return response


def pic_info(pic_json, key):
    """获取Pixiv的图片信息

    :param pic_json: Json格式返回的图片信息
    :param key: 获取返回的信息中的第key张图片
    :return: {'pid':[int] ,'title':[str], 'username':[str], 'url':[str], 'num':[int}}
    """
    now_time = Functions.get_time()
    pic_list = pic_json.get('illusts')
    # 判断是否成功获取到排行榜的图片
    if pic_list is None:    # 获取失败
        msg = pic_json.get('error').get('message')
        print('[{}]"pic_info":获取图片时发生错误{}'.format(now_time, msg))
        response = {
            'message': msg
        }
    else:   # 获取成功
        title = pic_list[key].get('title')  # 投稿标题
        pid = pic_list[key].get('id')   # 作品id
        username = pic_list[key].get('user').get('name')    # 画师用户名
        # 判断同一投稿内是否有多张图片
        if len(pic_list[key].get('meta_pages')) != 0:
            url = pic_list[key].get('meta_pages')[0].get('image_urls').get('medium')    # 图片直链
            num = len(pic_list[key].get('meta_pages'))  # 图片数量
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
