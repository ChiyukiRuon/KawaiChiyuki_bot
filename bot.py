import os
import traceback
import datetime
import pytz

from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

import bangumi
import getPixivImage
import yiyan

TOKEN = os.getenv("TOKEN")


# 打招呼
def start(update, context):
    # 获取必要信息
    now_time = get_time()
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    # 输出接受消息的日志
    message_log(now_time, chat_info, received)

    try:
        # 发送消息
        dispatcher.bot.sendPhoto(
            chat_id=chat_id,
            photo=open('./res/images/welcome.png', 'rb'),
            caption='来辣！'
        )

        # 输出发送消息成功的日志
        message_log(now_time, chat_info, received, True)
    except Exception as e:
        # 发送消息失败
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='发送信息时出现错误{}'.format(e)
        )

        # 输出发送消息失败的日志
        message_log(now_time, chat_info, received, False, e)


# 一言二次元语录
def yan(update, context):
    now_time = get_time()
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    message_log(now_time, chat_info, received)

    try:
        update.message.reply_text('收到消息，正在处理中')
    except Exception as e:
        message_log(now_time, chat_info, received, False, e)

    yan_info = yiyan.hitokoto()    # 获取到的一言信息
    if yan_info.get('content') is None:
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='获取一言时出错'
        )

        message_log(now_time, chat_info, received, False, '获取一言失败')
    else:
        try:
            dispatcher.bot.sendMessage(
                chat_id=chat_id,
                text='"<b>{}</b>"\n出处：{}'.format(yan_info.get('content'), yan_info.get('source')),
                parse_mode='HTML'
            )

            message_log(now_time, chat_info, received, True)
        except Exception as e:
            dispatcher.bot.sendMessage(
                chat_id=chat_id,
                text='发送信息时出错：{}'.format(e)
            )

            message_log(now_time, chat_info, received, False, e)


# 新番时间表
def bangumi_calendar(update, context):
    bangumi_str = ''
    now_time = get_time()
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    message_log(now_time, chat_info, received)

    markup = InlineKeyboardMarkup([[InlineKeyboardButton('日', None, 7),
                                    InlineKeyboardButton('一', None, 1),
                                    InlineKeyboardButton('二', None, 2),
                                    InlineKeyboardButton('三', None, 3),
                                    InlineKeyboardButton('四', None, 4),
                                    InlineKeyboardButton('五', None, 5),
                                    InlineKeyboardButton('六', None, 6),
                                    ]])

    try:
        update.message.reply_text('收到消息，正在处理中')
    except Exception as e:
        message_log(now_time, chat_info, received, False, e)

    message = update.message.text.split(' ')    # 获取输入数据
    # 判断是否指定了日期
    if len(message) > 1:    # 指定了日期
        bangumi_info = bangumi.calendar(int(message[1]))    # 获取到的番剧更新信息
        # 遍历番剧名数组将其组成一个的字符串方便发送
        for i in range(bangumi_info.get('num')):
            bangumi_str = '{}\n{}'.format(bangumi_str, bangumi_info.get('bangumi')[i])

        try:
            dispatcher.bot.sendMessage(
                chat_id=chat_id,
                text='<b>{}({})</b>共有{}部番剧更新：{}'.format(
                    bangumi_info.get('weekday_cn'),
                    bangumi_info.get('weekday_jp'),
                    bangumi_info.get('num'),
                    bangumi_str),
                parse_mode='HTML',
                reply_markup=markup
            )

            message_log(now_time, chat_info, received, True)
        except Exception as e:
            message_log(now_time, chat_info, received, False, e)
    else:   # 未指定日期
        bangumi_info = bangumi.calendar()
        for i in range(bangumi_info.get('num')):
            bangumi_str = '{}\n{}'.format(bangumi_str, bangumi_info.get('bangumi')[i])

        try:
            dispatcher.bot.sendMessage(
                chat_id=chat_id,
                text='今天是<b>{}({})</b>，共有{}部番剧更新：{}'.format(
                    bangumi_info.get('weekday_cn'),
                    bangumi_info.get('weekday_jp'),
                    bangumi_info.get('num'),
                    bangumi_str),
                parse_mode='HTML',
                reply_markup=markup
            )

            message_log(now_time, chat_info, received, True)
        except Exception as e:
            dispatcher.bot.sendMessage(
                chat_id=chat_id,
                text='发送消息时出现错误{}'.format(e)
            )

            message_log(now_time, chat_info, received, False, e)


# 随机Pixiv图片
def sese(update, context):
    now_time = get_time()
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    message_log(now_time, chat_info, received)

    try:
        update.message.reply_text('收到消息，正在处理中')
    except Exception as e:
        log_output('"sese":发送消息时遇到错误{}'.format(e))

    pic_info = getPixivImage.random_pic()
    log_output('"sese":获取到图片信息：{}'.format(pic_info))

    markup = InlineKeyboardMarkup([[InlineKeyboardButton('查看来源页面','https://www.pixiv.net/artworks/{}'.format(pic_info.get('pid')))]])

    try:
        # 判断投稿内的作品数量，用不同的格式发送
        if pic_info.get('num') != 1:    # 投稿内不止一张作品
            dispatcher.bot.sendPhoto(
                chat_id=chat_id,
                photo=pic_info.get('url'),
                caption='以及{}张图片\n标题：{}\n作者：{}'.format(
                    pic_info.get('num') - 1,
                    pic_info.get('title'),
                    pic_info.get('username')),
                parse_mode='HTML',
                reply_markup=markup
            )

            message_log(now_time, chat_info, received, True)
        elif pic_info.get('num') == 1:  # 投稿内仅一张作品
            dispatcher.bot.sendPhoto(
                chat_id=chat_id,
                photo=pic_info.get('url'),
                caption='标题：{}\n作者：{}'.format(
                    pic_info.get('title'),
                    pic_info.get('username')),
                parse_mode='HTML',
                reply_markup=markup
            )

            message_log(now_time, chat_info, received, True)
        else:   # 发生错误
            dispatcher.bot.sendMessage(
                chat_id=chat_id,
                text='获取图片时发生错误：{}'.format(pic_info.get('message')),
                reply_markup=markup
            )

            message_log(now_time, chat_info, received, False, pic_info.get('message'))
    except Exception as e:
        if pic_info.get('message') is None:
            dispatcher.bot.sendMessage(
                chat_id=chat_id,
                text='发送图片时出现错误：{}'.format(e),
                parse_mode='HTML',
                reply_markup=markup
            )

            message_log(now_time, chat_info, received, False, e)
        else:
            dispatcher.bot.sendMessage(
                chat_id=chat_id,
                text='获取图片时发生错误：{}'.format(pic_info.get('message')),
                reply_markup=markup
            )

            message_log(now_time, chat_info, received, False, pic_info.get('message'))


# Pixiv日榜
def day_rank(update, context):
    now_time = get_time()
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    message_log(now_time, chat_info, received)

    try:
        update.message.reply_text('收到消息，正在处理中')
    except Exception as e:
        log_output('"day_rank":发送消息时遇到错误{}'.format(e))

    images_info = getPixivImage.pixiv_rank('day')
    # 判断是否获取到了图片信息
    if images_info[0].get('message') is None:   # 成功获取图片信息
        message = update.message.text.split(' ')
        page = 0    # 设置默认页数
        # 判断是否指定了页数
        if len(message) > 1:
            page = int(message[1])
            # 判断输入的页数是否合法
            if -6 < page < 0:
                page = (page + 6) % 6
            elif page > 0:
                if page > 6:
                    dispatcher.bot.sendMessage(
                        chat_id=chat_id,
                        text='页数超过限制'
                    )
                    pass
                page -= 1

        send_photos(chat_id, images_info, page)

        message_log(now_time, chat_info, received, True)
    else:   # 获取图片信息失败
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='获取图片时发生错误：{}'.format(images_info[0].get('message'))
        )

        message_log(now_time, chat_info, received, False, images_info[0].get('message'))


# Pixiv周榜
def week_rank(update, context):
    now_time = get_time()
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    message_log(now_time, chat_info, received)

    try:
        update.message.reply_text('收到消息，正在处理中')
    except Exception as e:
        message_log(now_time, chat_info, received, False, e)

    images_info = getPixivImage.pixiv_rank('week')
    if images_info[0].get('message') is None:
        message = update.message.text.split(' ')
        page = 0
        if len(message) > 1:
            page = int(message[1])
            if -6 < page < 0:
                page = (page + 6) % 6
            elif page > 0:
                if page > 6:
                    dispatcher.bot.sendMessage(
                        chat_id=chat_id,
                        text='页数超过限制'
                    )
                    pass
                page -= 1

        send_photos(chat_id, images_info, page)

        message_log(now_time, chat_info, received, True)
    else:
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='获取图片时发生错误：{}'.format(images_info[0].get('message'))
        )

        message_log(now_time, chat_info, received, False, images_info[0].get('message'))


# Pixiv月榜
def month_rank(update, context):
    now_time = get_time()
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    message_log(now_time, chat_info, received)

    try:
        update.message.reply_text('收到消息，正在处理中')
    except Exception as e:
        message_log(now_time, chat_info, received, False, e)

    images_info = getPixivImage.pixiv_rank('month')
    if images_info[0].get('message') is None:
        message = update.message.text.split(' ')
        page = 0
        if len(message) > 1:
            page = int(message[1])
            if -6 < page < 0:
                page = (page + 6) % 6
            elif page > 0:
                if page > 6:
                    dispatcher.bot.sendMessage(
                        chat_id=chat_id,
                        text='页数超过限制'
                    )
                    pass
                page -= 1

        send_photos(chat_id, images_info, page)

        message_log(now_time, chat_info, received, True)
    else:
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='获取图片时发生错误：{}'.format(images_info[0].get('message'))
        )

        message_log(now_time, chat_info, received, False, images_info[0].get('message'))


# Pixiv R18日榜
def day_rank_r18(update, context):
    now_time = get_time()
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    message_log(now_time, chat_info, received)

    try:
        update.message.reply_text('收到消息，正在处理中')
    except Exception as e:
        message_log(now_time, chat_info, received, False, e)

    images_info = getPixivImage.pixiv_rank('day_r18')
    if images_info[0].get('message') is None:
        message = update.message.text.split(' ')
        page = 0
        if len(message) > 1:
            page = int(message[1])
            if -6 < page < 0:
                page = (page + 6) % 6
            elif page > 0:
                if page > 6:
                    dispatcher.bot.sendMessage(
                        chat_id=chat_id,
                        text='页数超过限制'
                    )
                    pass
                page -= 1

        send_photos(chat_id, images_info, page)

        message_log(now_time, chat_info, received, True)
    else:
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='获取图片时发生错误：{}'.format(images_info[0].get('message'))
        )

        message_log(now_time, chat_info, received, False, images_info[0].get('message'))


# Pixiv R18周榜
def week_rank_r18(update, context):
    now_time = get_time()
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    message_log(now_time, chat_info, received)

    try:
        update.message.reply_text('收到消息，正在处理中')
    except Exception as e:
        message_log(now_time, chat_info, received, False, e)

    images_info = getPixivImage.pixiv_rank('week_r18')
    if images_info[0].get('message') is None:
        message = update.message.text.split(' ')
        page = 0
        if len(message) > 1:
            page = int(message[1])
            if -6 < page < 0:
                page = (page + 6) % 6
            elif page > 0:
                if page > 6:
                    dispatcher.bot.sendMessage(
                        chat_id=chat_id,
                        text='页数超过限制'
                    )
                    pass
                page -= 1

        send_photos(chat_id, images_info, page)

        message_log(now_time, chat_info, received, True)
    else:
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='获取图片时发生错误：{}'.format(images_info[0].get('message'))
        )

        message_log(now_time, chat_info, received, False, images_info[0].get('message'))


# Pixiv R18G排行榜
def rank_r18g(update, context):
    now_time = get_time()
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    message_log(now_time, chat_info, received)

    try:
        update.message.reply_text('收到消息，正在处理中')
    except Exception as e:
        message_log(now_time, chat_info, received, False, e)

    images_info = getPixivImage.pixiv_rank('week_r18g')
    if images_info[0].get('message') is None:
        message = update.message.text.split(' ')
        page = 0
        if len(message) > 1:
            page = int(message[1])
            if -6 < page < 0:
                page = (page + 6) % 6
            elif page > 0:
                if page > 6:
                    dispatcher.bot.sendMessage(
                        chat_id=chat_id,
                        text='页数超过限制'
                    )
                    pass
                page -= 1

        send_photos(chat_id, images_info, page)

        message_log(now_time, chat_info, received, True)
    else:
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='获取图片时发生错误：{}'.format(images_info[0].get('message'))
        )

        message_log(now_time, chat_info, received, False, images_info[0].get('message'))


# 获取帮助
def help(update, context):
    now_time = get_time()
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    message_log(now_time, chat_info, received)

    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('Pixiv图片', None, 'pixiv')],
        [InlineKeyboardButton('番剧日程表', None, 'bangumi')],
        [InlineKeyboardButton('一言', None, 'yiyan')],
    ])

    try:
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='点击下方按钮获取对应功能的帮助',
            parse_mode='HTML',
            reply_markup=markup
        )

        message_log(now_time, chat_info, received, True)
    except Exception as e:
        message_log(now_time, chat_info, received, False, e)


# 关于
def about(update, context):
    now_time = get_time()
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    message_log(now_time, chat_info, received)

    try:
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='<b>KawaiChiyuki_bot</b>\n'
                 '项目地址：<a href="https://github.com/ChiyukiRuon/KawaiChiyuki_bot">Github</a>\n'
                 '第三方API：<a href="https://api.obfs.dev/docs">HibiAPI</a>,<a href="https://hitokoto.cn/">一言</a>,<a href="https://bangumi.github.io/api/#/">Bangumi API</a>\n'
                 'Powered by <a href="https://chiyukiruon.top">千雪琉音</a> @ <a href="tg://user?id=5325866562">ChiyukiRuon</a>',
            parse_mode='HTML'
        )

        message_log(now_time, chat_info, received, True)
    except Exception as e:
        message_log(now_time, chat_info, received, False, e)


def query_func(update, context):
    """点击消息按钮的处理函数

    :param update:
    :param context:
    :return:
    """
    query = update.callback_query
    query.answer()
    query_data = query.data

    try:

        if query_data == 'pixiv':
            query.edit_message_text(
                text='<b>Pixiv</b>\n'
                     '<code>/{day|week|month}_rank [page]</code> 获取Pixiv{日|周|月}榜的图片\n'
                     '<code>/{day|week}_rank_r18 [page]</code> 获取Pixiv R18{日|周}榜的图片\n'
                     '<code>/rank_g18g [page]</code> 获取Pixiv R18G排行榜的图片\n'
                     '<code>/sese</code> 随机获取Pixiv的图片',
                parse_mode='HTML',
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('返回', None, 'help')]])
            )

        elif query_data == 'bangumi':
            query.edit_message_text(
                text='<b>Bangumi</b>\n'
                     '<code>/bangumi [weekday]</code> 获取当日更新的番剧，可选参数weekday的范围为1-7，代表周一到周日',
                parse_mode='HTML',
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('返回', None, 'help')]])
            )

        elif query_data == 'yiyan':
            query.edit_message_text(
                text='<b>Yiyan</b>\n'
                     '<code>/yan</code> 一言二次元语录',
                parse_mode='HTML',
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('返回', None, 'help')]])
            )

        elif query_data == 'help':
            query.edit_message_text(
                text='点击下方按钮获取对应功能的帮助',
                parse_mode='HTML',
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('Pixiv图片', None, 'pixiv')],
                                                   [InlineKeyboardButton('番剧日程表', None, 'bangumi')],
                                                   [InlineKeyboardButton('一言', None, 'yiyan')],
                                                   ])
            )

        elif 1<= int(query_data) <= 7:
            bangumi_str = ''
            bangumi_info = bangumi.calendar(int(query_data))

            for i in range(bangumi_info.get('num')):
                bangumi_str = '{}\n{}'.format(bangumi_str, bangumi_info.get('bangumi')[i])

            query.edit_message_text(
                text='<b>{}({})</b>共有{}部番剧更新：{}'.format(
                    bangumi_info.get('weekday_cn'),
                    bangumi_info.get('weekday_jp'),
                    bangumi_info.get('num'),
                    bangumi_str),
                parse_mode='HTML',
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('日', None, 7),
                                    InlineKeyboardButton('一', None, 1),
                                    InlineKeyboardButton('二', None, 2),
                                    InlineKeyboardButton('三', None, 3),
                                    InlineKeyboardButton('四', None, 4),
                                    InlineKeyboardButton('五', None, 5),
                                    InlineKeyboardButton('六', None, 6),
                                    ]])
            )

        log_output('更新消息成功')
    except Exception as e:
        log_output('更新消息时出现错误{}'.format(e))


def send_photos(chat_id, image_list, page):
    now_time = get_time()
    try:
        # 准备遍历获取图片信息
        for key in range(len(image_list)):
            # 控制遍历的范围
            if page*5 <= key < (page + 1)*5:
                try:
                    if image_list[key].get('num') > 1:
                        dispatcher.bot.sendPhoto(
                            chat_id=chat_id,
                            photo=image_list[key].get('url'),
                            caption='以及{}张图片\nNo.{}\n标题：{}\n作者：{}\n<a href="https://www.pixiv.net/artworks/{}">原图链接</a>'.format(
                                image_list[key].get('num') - 1,
                                key + 1,
                                image_list[key].get('title'),
                                image_list[key].get('username'),
                                image_list[key].get('pid')),
                            parse_mode='HTML'
                        )
                    else:
                        dispatcher.bot.sendPhoto(
                            chat_id=chat_id,
                            photo=image_list[key].get('url'),
                            caption='No.{}\n标题：{}\n作者：{}\n<a href="https://www.pixiv.net/artworks/{}">原图链接</a>'.format(
                                key + 1,
                                image_list[key].get('title'),
                                image_list[key].get('username'),
                                image_list[key].get('pid')),
                            parse_mode='HTML'
                        )
                except Exception as e:
                    traceback.print_exc()
                    log_output('"send_photos":在发送第 <b>{}</b> 张图片时发生错误,错误信息：{}'.format(key + 1, e))
                    dispatcher.bot.sendMessage(
                        chat_id=chat_id,
                        text='在发送第 <b>{}</b> 张图片时发生错误\n错误信息：{}'.format(key + 1, e),
                        parse_mode='HTML'
                    )
            elif key > (page + 1)*5 - 1:
                break
    except Exception as e:
        log_output('"send_photos":获取图片时发生错误{}'.format(e))
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='获取图片时发生错误：{}'.format(e)
        )


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
        chat_info = args[1]
        received = args[2]

        command = received.split(' ')[0].split('@')[0].split('/')[1]
        if len(args) == 3:
            # receive_message
            if chat_info.username is None:
                _from = chat_info.title

                log_info = '"{}":收到来自群组<{}>的消息<{}>'.format(command, _from, received)
            else:
                _from = '{} {}(id:{})'.format(chat_info.first_name, chat_info.last_name, chat_info.id)

                log_info = '"{}":收到来自用户<{}>的消息'.format(command, _from, received)
        elif 4 <= len(args) <= 5:
            # send_message
            send_state = args[3]
            if send_state:
                if chat_info.username is None:
                    _from = chat_info.title

                    log_info = '"{}":成功向群组<{}>发送消息消息'.format(command, _from)
                else:
                    _from = '{} {}(id:{})'.format(chat_info.first_name, chat_info.last_name, chat_info.id)

                    log_info = '"{}":成功向用户<{}>发送消息'.format(command, _from)
            else:
                err_info = args[4]
                if chat_info.username is None:
                    _from = chat_info.title

                    log_info = '"{}":向群组<{}>发送消息时出现错误{}'.format(command, _from, err_info)
                else:
                    _from = '{} {}(id:{})'.format(chat_info.first_name, chat_info.last_name, chat_info.id)

                    log_info = '"{}":向用户<{}>发送消息时出现错误{}'.format(command, _from, err_info)
        else:
            # error
            log_info = '"message_log":传入参数错误,数量应为3个或4个'
    except Exception as e:
        log_info = '"message_log":传入参数错误{}'.format(e)

    log_output(log_info)


def log_output(log_info):
    """日志输出

    :param log_info:日志内容
    :return: 在‘log’文件夹下对应日期的文件中写入日志以及在控制台中输出日志
    """
    now_time = get_time().split(' ')[0]

    log_file = open('./logs/{}.txt'.format(now_time), 'a+', encoding='UTF-8')
    log_file.write('[{}]{}\n'.format(get_time(), log_info))
    log_file.close()

    print('[{}]{}'.format(get_time(), log_info))


if __name__ == '__main__':
    updater = Updater(token=TOKEN, request_kwargs={
        'proxy_url': 'socks5h://127.0.0.1:11223/'
    })

    dispatcher = updater.dispatcher
    log_output('-----------------初始化成功-----------------')

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("yan", yan))
    dispatcher.add_handler(CommandHandler("bangumi", bangumi_calendar))
    dispatcher.add_handler(CommandHandler("sese", sese))
    dispatcher.add_handler(CommandHandler("day_rank", day_rank))
    dispatcher.add_handler(CommandHandler("week_rank", week_rank))
    dispatcher.add_handler(CommandHandler("month_rank", month_rank))
    dispatcher.add_handler(CommandHandler("day_rank_r18", day_rank_r18))
    dispatcher.add_handler(CommandHandler("week_rank_r18", week_rank_r18))
    dispatcher.add_handler(CommandHandler("rank_r18g", rank_r18g))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("about", about))
    dispatcher.add_handler(CallbackQueryHandler(query_func))

    updater.start_polling()
    updater.idle()
