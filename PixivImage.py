import json

import requests


# 获取Pixiv日榜图片
def daily_rank():
    resp_list = []
    r = json.loads(requests.get('https://api.obfs.dev/api/pixiv/rank').content)
    res_list = r.get('illusts')
    for i in range(len(res_list)):
        pid = res_list[i].get('id')
        title = res_list[i].get('title')
        username = res_list[i].get('user').get('name')
        if len(res_list[i].get('meta_pages')) != 0:
            url = res_list[i].get('meta_pages')[0].get('image_urls').get('medium')  # 多张图片只获取第一张
        else:
            url = res_list[i].get('meta_single_page').get('original_image_url')

        response = {
            'pid': pid,
            'title': title,
            'username': username,
            'url': url
        }

        resp_list.append(response)
    # print(resp_list)

    return resp_list


# 获取Pixiv R18周榜前五张图片
def weekly_rank_r18():
    resp_list = []
    r = json.loads(requests.get('https://api.obfs.dev/api/pixiv/rank?mode=week_r18').content)
    res_list = r.get('illusts')
    for i in range(len(res_list)):
        pid = res_list[i].get('id')
        title = res_list[i].get('title')
        username = res_list[i].get('user').get('name')
        if len(res_list[i].get('meta_pages')) != 0:
            url = res_list[i].get('meta_pages')[0].get('image_urls').get('medium')
        else:
            url = res_list[i].get('image_urls').get('medium')

        response = {
            'pid': pid,
            'title': title,
            'username': username,
            'url': url
        }

        resp_list.append(response)

    return resp_list
