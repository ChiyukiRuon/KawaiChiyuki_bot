import datetime
import os

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

    bot.clear_cache(7)

    for file in os.listdir('./caches'):
        file_name = os.path.splitext(file)[0].split('+')

        if file_name[1] == 'bangumi':
            bot.log_output('"calendar":找到番剧更新表的缓存数据')

            with open('./caches/{}'.format(file), 'r', encoding='UTF-8') as f:
                r = json.loads(f.read())
            f.close()

            bot.log_output('"calendar":从缓存返回的数据{}'.format(r))

        else:
            headers = {
                'User-Agent': 'ChiyukiRuon/KawaiChiyuki_bot(https://github.com/ChiyukiRuon/KawaiChiyuki_bot)'
            }
            url = 'https://api.bgm.tv/calendar'
            try:
                r = requests.get(url, headers).content  # TODO 返回值为Unicode编码，需要转换为UTF-8

                bot.log_output('"calendar":成功获取番剧更新时间')

                # bot.write_cache('bangumi', r)
            except Exception as e:
                bot.log_output('"calendar":获取番剧更新时间时发生错误{}'.format(e))

                response = {
                    'weekday_cn': bot.get_time(),
                    'message': '获取番剧更新时间时发生错误{}'.format(e)
                }

                return response

    if len(args) == 0:
        content = json.loads(r)[today]
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

        bot.log_output('"calendar":获取到番剧信息{}'.format(response))

    elif len(args) == 1:
        content = json.loads(r)[args[0] - 1]
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

        bot.log_output('"calendar":获取到番剧信息{}'.format(response))

    else:
        response = {
            'weekday_cn': bot.get_time(),
            'message': '参数输入错误'
        }

        bot.log_output('"calendar":获取番剧信息时遇到错误{}'.format(response))

    return response
