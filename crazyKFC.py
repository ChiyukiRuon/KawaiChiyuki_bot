import requests

import bot


def crazy_kfc():
    """
    疯狂星期四文案
    :return: [text]
    """
    url = "https://kfc-crazy-thursday.vercel.app/api/index"
    try:
        content = requests.get(url).text

        bot.log_output('"crazy_kfc":成功获取到内容')
    except Exception as e:
        bot.log_output('“crazy_kfc”:获取内容时出现错误{}'.format(e))

    return content