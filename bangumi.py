import datetime

import requests
import json

import bot


def calendar(*args):    # TODO 将番剧时间表加入缓存
    """番剧日历
    获取当日更新的番剧

    :param args: 可选.1-7代表周一到周日，不填默认为当天信息
    :return: {‘weekday_cn’:[str], 'weekday_jp':[str], 'bangumi':[list], 'num':[int]}
    """
    bangumi_list = []
    time_list = bot.get_time().split('-')
    year = time_list[0]
    month = time_list[1]
    day = time_list[2].split(' ')[0]
    today = datetime.date(int(year), int(month), int(day)).weekday()

    headers = {
        'User-Agent': 'ChiyukiRuon/KawaiChiyuki_bot(https://github.com/ChiyukiRuon/KawaiChiyuki_bot)'
    }
    url = 'https://api.bgm.tv/calendar'
    r = requests.get(url, headers)

    if len(args) == 0:
        content = json.loads(r.content)[today]
        weekday_cn = content.get('weekday').get('cn')
        weekday_jp = content.get('weekday').get('ja')

        for item in range(len(content.get('items'))):

            if content.get('items')[item].get('name_cn') == '':
                bangumi_list.append(content.get('items')[item].get('name'))

            else:
                bangumi_list.append(content.get('items')[item].get('name_cn'))

        response = {
            'weekday_cn': weekday_cn,
            'weekday_jp': weekday_jp,
            'bangumi': bangumi_list,
            'num': len(bangumi_list)
        }

        bot.log_output('"bangumi":获取到番剧信息{}'.format(response))

    elif len(args) == 1:
        content = json.loads(r.content)[args[0] - 1]
        weekday_cn = content.get('weekday').get('cn')
        weekday_jp = content.get('weekday').get('ja')

        for item in range(len(content.get('items'))):

            if content.get('items')[item].get('name_cn') == '':
                bangumi_list.append(content.get('items')[item].get('name'))

            else:
                bangumi_list.append(content.get('items')[item].get('name_cn'))

        response = {
            'weekday_cn': weekday_cn,
            'weekday_jp': weekday_jp,
            'bangumi': bangumi_list,
            'num': len(bangumi_list)
        }

        bot.log_output('"bangumi":获取到番剧信息{}'.format(response))

    else:
        response = {
            'weekday_cn': bot.get_time(),
            'message': '参数输入错误'
        }

        bot.log_output('"bangumi":获取番剧信息时遇到错误{}'.format(response))

    return response
