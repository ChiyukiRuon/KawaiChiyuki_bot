import json

import requests


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
    r = json.loads(requests.get(url).content)
    res_list = r.get('illusts')
    for i in range(len(res_list)):
        pid = res_list[i].get('id')
        title = res_list[i].get('title')
        username = res_list[i].get('user').get('name')
        if len(res_list[i].get('meta_pages')) != 0:
            url = res_list[i].get('meta_pages')[0].get('image_urls').get('medium')  # 多张图片只获取第一张
            num = len(res_list[i].get('meta_pages'))
        else:
            url = res_list[i].get('meta_single_page').get('original_image_url')
            num = 1

        response = {
            'pid': pid,     # 图片ID
            'title': title,     # 图片标题
            'username': username,   # 作者
            'url': url,     # 图片下载链接
            'num': num,     # 图片数量
        }

        resp_list.append(response)

    return resp_list
