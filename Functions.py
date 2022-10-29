import datetime

import pytz


def get_time():
    """获取当前(GMT+8:00)时间

    :return: ‘%Y-%m-%d %H:%M:%S’
    """
    tz = pytz.timezone('Asia/Shanghai')
    now_time = datetime.datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

    return now_time


def message_log(*args):
    """接收/发送消息日志

    <now_time>, <chat_info>, <received>, [send_state], [err_info]

    :param args: <now_time>, <chat_info>, <received>, [send_state], [err_info]
    :return: None
    """
    try:
        now_time = args[0]
        chat_info = args[1]
        received = args[2]

        command = received.split(' ')[0].split('@')[0].split('/')[1]
        if len(args) == 3:
            # receive_message
            if chat_info.username is None:
                _from = chat_info.title
                print('[{}]"{}":收到来自群组<{}>的消息<{}>'.format(now_time, command, _from, received))
            else:
                _from = '{} {}(id:{})'.format(chat_info.first_name, chat_info.last_name, chat_info.id)
                print('[{}]"{}":收到来自用户<{}>的消息'.format(now_time, command, _from, received))
        elif 4 <= len(args) <= 5:
            # send_message
            send_state = args[3]
            if send_state:
                if chat_info.username is None:
                    _from = chat_info.title

                    print('[{}]"{}":成功向群组<{}>发送消息消息'.format(now_time, command, _from))
                else:
                    _from = '{} {}(id:{})'.format(chat_info.first_name, chat_info.last_name, chat_info.id)

                    print('[{}]"{}":成功向用户<{}>发送消息'.format(now_time, command, _from))
            else:
                err_info = args[4]
                if chat_info.username is None:
                    _from = chat_info.title

                    print('[{}]"{}":向群组<{}>发送消息时出现错误{}'.format(now_time, command, _from, err_info))
                else:
                    _from = '{} {}(id:{})'.format(chat_info.first_name, chat_info.last_name, chat_info.id)

                    print('[{}]"{}":向用户<{}>发送消息时出现错误{}'.format(now_time, command, _from, err_info))
        else:
            # error
            print('[{}]"message_log":传入参数错误,数量应为3个或4个'.format(get_time()))
    except Exception as e:
        print('[{}]"message_log":传入参数错误{}'.format(get_time(), e))
