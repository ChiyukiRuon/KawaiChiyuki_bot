import json
import os
import random

import requests

import bot

api_list = [
    'https://api.obfs.dev/api/pixiv/',
    'https://api.imki.moe/api/pixiv/'
]


def pixiv_rank(*args):
    """获取Pixiv排行榜图片,总共获取30张

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
    :param api_no: 可选，选择API
    :return: [{'pid':[int], 'title':[str], 'username':[str], 'url':[str], 'num':[int]},{},...]
    """
    rank_type = args[0]
    resp_list = []

    bot.clear_cache(7)

    for file in os.listdir('./caches'):
        file_name = os.path.splitext(file)[0].split('+')

        if file_name[0] == bot.get_time().split(' ')[0] and file_name[1] == rank_type:
            bot.log_output('"pixiv_rank":找到{}类型的缓存数据'.format(rank_type))

            with open('./caches/{}'.format(file), 'r', encoding='UTF-8') as f:
                resp_list = json.loads(f.read())
            f.close()

            bot.log_output('"pixiv_rank":从缓存返回的图片数据{}'.format(resp_list))

            return resp_list

        else:
            pass

    api = api_list[0]

    if len(args) > 1 and args[1] < len(api_list): api = api_list[args[1]]

    bot.log_output('"pixiv_rank":使用API-{}进行搜索'.format(api))

    url = '{}rank?mode={}'.format(api, rank_type)
    try:
        pic_json = json.loads(requests.get(url).content)
    except Exception as e:
        bot.log_output('"pixiv_rank":获取图片信息失败{}'.format(e))

        if len(args) == 1:
            bot.log_output('"pixiv_rank":获取图片信息失败，更换API')

            resp_list = pixiv_rank(rank_type, 1)
        else:
            bot.log_output('"pixiv_rank":获取图片信息失败，放弃')

            resp_list = [
                {
                    'message': e
                }
            ]

        return resp_list
    pic_list = pic_json.get('illusts')

    if pic_list is None:

        resp_list = [pic_info(pic_json, 1)]

    elif len(pic_list) == 0:

        if len(args) == 1:
            bot.log_output('"pixiv_rank":获取到的图片信息为空，更换API')

            resp_list = pixiv_rank(rank_type, 1)
        else:
            bot.log_output('"pixiv_rank":获取到的图片信息仍为空，放弃')

            resp_list = [
                {
                    'message': '获取到的图片信息为空'
                }
            ]

        return resp_list

    else:

        for i in range(len(pic_list)):
            response = pic_info(pic_json, i)

            resp_list.append(response)

    bot.log_output('"pixiv_rank":返回的图片数据{}'.format(resp_list))

    bot.write_cache(rank_type, resp_list)

    bot.log_output('"pixiv_rank":写入{}类型的缓存'.format(rank_type))

    return resp_list


def random_pic(*args):
    """获取随机Pixiv图片

    :param api_no: 可选，选择API
    :return {'pid':[int] ,'title':[str], 'username':[str], 'url':[str], 'num':[int}}
    """
    api = api_list[0]
    if len(args) == 1 and args[0] < len(api_list): api = api_list[args[1]]

    bot.log_output('"random_pic":使用API-{}进行搜索'.format(api))

    tags_url = '{}tags'.format(api)
    search_url = '{}search?word='.format(api)
    user = ['1000', '3000', '5000', '7500', '10000', '30000', '50000']  # 搜索时用到的热度关键词
    try:
        tag_list = json.loads(requests.get(tags_url).content).get('trend_tags')    # 获取当前Pixiv的热门tag
    except Exception as e:
        if len(args) == 1:
            bot.log_output('"random_pic":获取图片信息失败{}'.format(e))

            response = {
                'message': '获取图片信息失败{}'.format(e)
            }

            return response
        else:
            bot.log_output('"random_pic":获取图片信息失败{},更换API'.format(e))

            response = random_pic(1)

            return response

    count = 0
    while True:
        count += 1
        try:
            rand_user = user[random.randint(0, 6)]  # 随机一个热度标签
            # 随机获取一个热门tag
            rand_tag = random.randint(0, 39)
            tag = tag_list[rand_tag].get('tag')
            # 搜索并拿到json格式的结果
            pic_json = json.loads(requests.get(search_url + tag + ' ' + rand_user + 'users入り').content)

            bot.log_output('"random_pic":尝试使用tag:{},user:{}获取图片'.format(tag, rand_user))

            # 从搜索结果中随机拿出一张图片
            rand_pic = random.randint(0, 29)
            response = pic_info(pic_json, rand_pic)

            bot.log_output('"random_pic":resp:{}'.format(response))

            # 如果成功拿到图片信息就跳出循环，总计重复6次上述步骤跳出循环
            if len(response) == 0 and count == 3 and len(args) == 0:
                bot.log_output('"random_pic":获取图片信息失败,切换API')
                count = 0

                response = random_pic(1)

                return response
            elif len(response) == 0 and count == 3 and len(args) == 1:
                bot.log_output('"random_pic":获取图片信息失败')
                break
            elif len(response) != 0 and count <= 6:
                return response

        except Exception as e:
            bot.log_output('"random_pic":获取图片信息时发生错误{}，重试{}/6'.format(e, count))

    return response


def pic_info(pic_json, key):
    """获取Pixiv的图片信息

    :param pic_json: Json格式返回的图片信息
    :param key: 获取返回的信息中的第key张图片
    :return: {'pid':[int] ,'title':[str], 'username':[str], 'url':[str], 'num':[int}}
    """
    now_time = bot.get_time()
    pic_list = pic_json.get('illusts')
    # 判断是否成功获取到排行榜的图片
    if pic_list is None:    # 获取失败
        msg = pic_json.get('error').get('message')
        bot.log_output('"pic_info":获取图片时发生错误{}'.format(msg))
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
