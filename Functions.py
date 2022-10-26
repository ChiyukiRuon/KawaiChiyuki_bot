import datetime

import pytz


def get_time():
    """获取当前(GMT+8:00)时间

    :return: ‘%Y-%m-%d %H:%M:%S’
    """
    tz = pytz.timezone('Asia/Shanghai')
    now_time = datetime.datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

    return now_time
