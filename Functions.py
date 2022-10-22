import datetime

import pytz


def get_time():
    tz = pytz.timezone('Asia/Shanghai')
    now_time = datetime.datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

    return now_time
