import os
import datetime
import pytz

from telegram import InlineKeyboardButton, InputMediaPhoto
from telegram import InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

import bangumi
import crazyKFC
import getPixivImage
import yiyan

TOKEN = os.getenv("TOKEN")


# 打招呼
def start(update, context):
    # 获取必要信息
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    if request_filter(chat_info.id):
        return

    # 输出接受消息的日志
    message_log(chat_info, received)

    try:
        # 发送消息
        dispatcher.bot.sendPhoto(
            chat_id=chat_id,
            photo=open('./res/images/welcome.png', 'rb'),
            caption='来辣！'
        )

        # 输出发送消息成功的日志
        message_log(chat_info, received, True)
    except Exception as e:
        # 发送消息失败
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='发送信息时出现错误{}'.format(e)
        )

        # 输出发送消息失败的日志
        message_log(chat_info, received, False, e)


# 一言二次元语录
def yan(update, context):
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    if request_filter(chat_info.id):
        return

    message_log(chat_info, received)

    try:
        update.message.reply_text('收到消息，正在处理中')
    except Exception as e:
        message_log(chat_info, received, False, e)

    yan_info = yiyan.hitokoto()    # 获取到的一言信息
    if yan_info.get('content') is None:
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='获取一言时出错'
        )

        message_log(chat_info, received, False, '获取一言失败')
    else:
        try:
            dispatcher.bot.sendMessage(
                chat_id=chat_id,
                text='"<b>{}</b>"\n出处：{}'.format(yan_info.get('content'), yan_info.get('source')),
                parse_mode='HTML'
            )

            message_log(chat_info, received, True)
        except Exception as e:
            dispatcher.bot.sendMessage(
                chat_id=chat_id,
                text='发送信息时出错：{}'.format(e)
            )

            message_log(chat_info, received, False, e)


# 新番时间表
def bangumi_calendar(update, context):
    bangumi_str = ''
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    if request_filter(chat_info.id):
        return

    message_log(chat_info, received)

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
        message_log(chat_info, received, False, e)

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

            message_log(chat_info, received, True)
        except Exception as e:
            message_log(chat_info, received, False, e)
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

            message_log(chat_info, received, True)
        except Exception as e:
            dispatcher.bot.sendMessage(
                chat_id=chat_id,
                text='发送消息时出现错误{}'.format(e)
            )

            message_log(chat_info, received, False, e)


# 疯狂星期四文案
def crazy_kfc(update, context):
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    if request_filter(chat_info.id):
        return

    message_log(chat_info, received)

    try:
        update.message.reply_text('收到消息，正在处理中')
    except Exception as e:
        log_output('"crazy_kfc":发送消息时遇到错误{}'.format(e))

    try:
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text=crazyKFC.crazy_kfc()
        )

        message_log(chat_info, received, True)
    except Exception as e:
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='发送消息时出现错误{}'.format(e)
        )

        message_log(chat_info, received, False, e)

# 随机Pixiv图片
def sese(update, context):
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    if request_filter(chat_info.id):
        return

    message_log(chat_info, received)

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

            message_log(chat_info, received, True)
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

            message_log(chat_info, received, True)
        else:   # 发生错误
            dispatcher.bot.sendMessage(
                chat_id=chat_id,
                text='获取图片时发生错误：{}'.format(pic_info.get('message')),
            )

            message_log(chat_info, received, False, pic_info.get('message'))
    except Exception as e:
        if pic_info.get('message') is None:
            dispatcher.bot.sendMessage(
                chat_id=chat_id,
                text='发送图片时出现错误：{}\n如果要查看未成功发送的图片，可以尝试查看来源页面'.format(e),
                parse_mode='HTML',
                reply_markup=markup
            )

            message_log(chat_info, received, False, e)
        else:
            dispatcher.bot.sendMessage(
                chat_id=chat_id,
                text='获取图片时发生错误：{}'.format(pic_info.get('message')),
            )

            message_log(chat_info, received, False, pic_info.get('message'))


# Pixiv日榜
def day_rank(update, context):
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    if request_filter(chat_info.id):
        return

    message_log(chat_info, received)

    try:
        update.message.reply_text('收到消息，正在处理中')
    except Exception as e:
        log_output('"day_rank":发送消息时遇到错误{}'.format(e))

    message = update.message.text.split(' ')

    if len(message) > 1:

        page = int(message[1])

        if 1 <= page <= 30:
            page = page
        elif -30 <= page <= -1:
            page = page + 31
        else:
            update.message.reply_text('输入的数字超出了限制，请输入1~30或-30~-1间的整数')
            log_output('输入的数字超出了限制,返回警告')
            return

        send_photos(chat_id, 'day', page - 1)

    else:

        send_photos(chat_id, 'day', 0)


# Pixiv周榜
def week_rank(update, context):
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    if request_filter(chat_info.id):
        return

    message_log(chat_info, received)

    try:
        update.message.reply_text('收到消息，正在处理中')
    except Exception as e:
        message_log(chat_info, received, False, e)

    message = update.message.text.split(' ')

    if len(message) > 1:

        page = int(message[1])

        if 1 <= page <= 30:
            page = page
        elif -30 <= page <= -1:
            page = page + 31
        else:
            update.message.reply_text('输入的数字超出了限制，请输入1~30或-30~-1间的整数')
            log_output('输入的数字超出了限制,返回警告')
            return

        send_photos(chat_id, 'week', page - 1)

    else:

        send_photos(chat_id, 'week', 0)


# Pixiv月榜
def month_rank(update, context):
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    if request_filter(chat_info.id):
        return

    message_log(chat_info, received)

    try:
        update.message.reply_text('收到消息，正在处理中')
    except Exception as e:
        message_log(chat_info, received, False, e)

    message = update.message.text.split(' ')

    if len(message) > 1:

        page = int(message[1])

        if 1 <= page <= 30:
            page = page
        elif -30 <= page <= -1:
            page = page + 31
        else:
            update.message.reply_text('输入的数字超出了限制，请输入1~30或-30~-1间的整数')
            log_output('输入的数字超出了限制,返回警告')
            return

        send_photos(chat_id, 'month', page - 1)

    else:

        send_photos(chat_id, 'month', 0)


# Pixiv R18日榜
def day_rank_r18(update, context):
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    if request_filter(chat_info.id):
        return

    message_log(chat_info, received)

    try:
        update.message.reply_text('收到消息，正在处理中')
    except Exception as e:
        message_log(chat_info, received, False, e)

    message = update.message.text.split(' ')

    if len(message) > 1:

        page = int(message[1])

        if 1 <= page <= 30:
            page = page
        elif -30 <= page <= -1:
            page = page + 31
        else:
            update.message.reply_text('输入的数字超出了限制，请输入1~30或-30~-1间的整数')
            log_output('输入的数字超出了限制,返回警告')
            return

        send_photos(chat_id, 'day_r18', page - 1)

    else:

        send_photos(chat_id, 'day_r18', 0)


# Pixiv R18周榜
def week_rank_r18(update, context):
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    if request_filter(chat_info.id):
        return

    message_log(chat_info, received)

    try:
        update.message.reply_text('收到消息，正在处理中')
    except Exception as e:
        message_log(chat_info, received, False, e)

    message = update.message.text.split(' ')

    if len(message) > 1:

        page = int(message[1])

        if 1 <= page <= 30:
            page = page
        elif -30 <= page <= -1:
            page = page + 31
        else:
            update.message.reply_text('输入的数字超出了限制，请输入1~30或-30~-1间的整数')
            log_output('输入的数字超出了限制,返回警告')
            return

        send_photos(chat_id, 'week_r18', page - 1)

    else:

        send_photos(chat_id, 'week_r18', 0)


# Pixiv R18G排行榜
def rank_r18g(update, context):
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    if request_filter(chat_info.id):
        return

    message_log(chat_info, received)

    try:
        update.message.reply_text('收到消息，正在处理中')
    except Exception as e:
        message_log(chat_info, received, False, e)

    message = update.message.text.split(' ')

    if len(message) > 1:

        page = int(message[1])

        if 1 <= page <= 30:
            page = page
        elif -30 <= page <= -1:
            page = page + 31
        else:
            update.message.reply_text('输入的数字超出了限制，请输入1~30或-30~-1间的整数')
            log_output('输入的数字超出了限制,返回警告')
            return

        send_photos(chat_id, 'week_r18g', page - 1)

    else:

        send_photos(chat_id, 'week_r18g', 0)


# 获取帮助
def help(update, context):
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    if request_filter(chat_info.id):
        return

    message_log(chat_info, received)

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

        message_log(chat_info, received, True)
    except Exception as e:
        message_log(chat_info, received, False, e)


# 关于
def about(update, context):
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    if request_filter(chat_info.id):
        return

    message_log(chat_info, received)

    try:
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='<b>KawaiChiyuki_bot</b>\n'
                 '项目地址：<a href="https://github.com/ChiyukiRuon/KawaiChiyuki_bot">Github</a>\n'
                 '第三方API：<a href="https://api.obfs.dev/docs">HibiAPI</a>,<a href="https://hitokoto.cn/">一言</a>,<a href="https://bangumi.github.io/api/#/">Bangumi API</a>\n'
                 'Powered by <a href="https://chiyukiruon.top">千雪琉音</a> @ <a href="tg://user?id=5325866562">ChiyukiRuon</a>',
            parse_mode='HTML'
        )

        message_log(chat_info, received, True)
    except Exception as e:
        message_log(chat_info, received, False, e)


def query_mgt(update, context):
    """点击消息按钮的处理函数

    :param update:
    :param context:
    :return:
    """
    query = update.callback_query
    query.answer()
    query_data = query.data

    log_output('内联按钮返回值：{}'.format(query_data))

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
        elif query_data.split('?')[0] == 'prev' or query_data.split('?')[0] == 'next':
            currt_page = int(query_data.split('?')[2])
            rank_type = query_data.split('?')[1]

            if query_data.split('?')[0] == 'prev':
                page = currt_page - 1
            else:
                page = currt_page + 1

            if page < 0 or page >= 30:page = (page + 30) % 30

            image_list = getPixivImage.pixiv_rank(rank_type)

            try:
                if image_list[page].get('num') > 1:
                    query.edit_message_media(
                        media=InputMediaPhoto(
                            media=image_list[page].get('url'),
                            caption='以及{}张图片\n排行榜类型：{}\n标题：{}\n作者：{}'.format(
                                image_list[page].get('num') - 1,
                                rank_type,
                                image_list[page].get('title'),
                                image_list[page].get('username'))
                        ),
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('上一个', None, 'prev?{}?{}'.format(rank_type, page)),
                                                            InlineKeyboardButton('下一个', None, 'next?{}?{}'.format(rank_type, page))],
                                                            [InlineKeyboardButton('查看来源页面', 'https://www.pixiv.net/artworks/{}'.format(image_list[page].get('pid')))]])
                    )
                else:
                    query.edit_message_media(
                        media=InputMediaPhoto(
                            media=image_list[page].get('url'),
                            caption='排行榜类型：{}\n标题：{}\n作者：{}'.format(
                                rank_type,
                                image_list[page].get('title'),
                                image_list[page].get('username'))
                        ),
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('上一个', None, 'prev?{}?{}'.format(rank_type, page)),
                                                            InlineKeyboardButton('下一个', None, 'next?{}?{}'.format(rank_type, page))],
                                                            [InlineKeyboardButton('查看来源页面', 'https://www.pixiv.net/artworks/{}'.format(image_list[page].get('pid')))]])
                    )
            except Exception as e:
                query.edit_message_caption(
                    caption='排行榜类型：{}\n加载第{}张图片时发生了错误\n错误原因：{}\n如果要查看未成功更新的图片，可以尝试查看来源页面'.format(rank_type, page + 1, e),
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton('上一个', None, 'prev?{}?{}'.format(rank_type, page)),
                          InlineKeyboardButton('下一个', None, 'next?{}?{}'.format(rank_type, page))],
                         [InlineKeyboardButton('查看来源页面', 'https://www.pixiv.net/artworks/{}'.format(
                             image_list[page].get('pid')))]])
                )

                log_output('更新图片时出现错误：{}'.format(e))

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
        log_output('更新消息时出现错误：{}'.format(e))


def send_photos(chat_id, rank_type, page):
    image_list = getPixivImage.pixiv_rank(rank_type)

    if image_list[0].get('message') is None:

        markup = InlineKeyboardMarkup([[InlineKeyboardButton('上一个', None, 'prev?{}?{}'.format(rank_type, page)),
                                        InlineKeyboardButton('下一个', None, 'next?{}?{}'.format(rank_type, page))],
                                       [InlineKeyboardButton('查看来源页面', 'https://www.pixiv.net/artworks/{}'.format(image_list[page].get('pid')))]
                                       ])

        try:
            if image_list[page].get('num') > 1:
                dispatcher.bot.sendPhoto(
                    chat_id=chat_id,
                    photo=image_list[page].get('url'),
                    caption='以及{}张图片\n排行榜类型：{}\n标题：{}\n作者：{}'.format(
                        image_list[page].get('num') - 1,
                        rank_type,
                        image_list[page].get('title'),
                        image_list[page].get('username')),
                    reply_markup=markup
                )
            else:
                dispatcher.bot.sendPhoto(
                    chat_id=chat_id,
                    photo=image_list[page].get('url'),
                    caption='排行榜类型：{}\n标题：{}\n作者：{}'.format(
                        rank_type,
                        image_list[page].get('title'),
                        image_list[page].get('username')),
                    reply_markup=markup
                )
        except Exception as e:
            dispatcher.bot.sendPhoto(
                chat_id=chat_id,
                photo=open('./res/images/bang.jpg', 'rb'),
                caption='排行榜类型：{}\n在发送图片时发生错误\n错误信息：{}\n如果要查看未成功发送的图片，可以尝试查看来源页面'.format(rank_type, e),
                reply_markup=markup
            )

            log_output('"send_photos":在发送第{}张图片时发生错误,错误信息：{}'.format(page + 1, e))

    else:

        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='获取图片信息失败\n错误信息：{}'.format(image_list[0].get('message'))
        )

        log_output('"send_photos":获取图片信息失败{}'.format(image_list[0].get('message')))


def get_time():
    """获取当前(GMT+8:00)时间

    :return: ‘%Y-%m-%d %H:%M:%S’
    """
    tz = pytz.timezone('Asia/Shanghai')
    now_time = datetime.datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')

    return now_time


def message_log(*args):
    """接收/发送消息日志

    用于提示消息的接收与发送

    :param args: chat_info 信息发送时携带的信息
    :param args: received 收到的指令内容
    :param args: send_state 可选的，消息发送状态
    :param args: err_info 可选的，错误信息。只有在拥有消息发送状态时才有效
    :return: None
    """
    try:
        chat_info = args[0]
        received = args[1]

        command = received.split(' ')[0].split('@')[0].split('/')[1]
        if len(args) == 2:
            # receive_message
            if chat_info.username is None:
                msg_src = chat_info.title

                log_info = '"{}":收到来自群组<{}>的消息<{}>'.format(command, msg_src, received)
            else:
                msg_src = '{} {}(id:{})'.format(chat_info.first_name, chat_info.last_name, chat_info.id)

                log_info = '"{}":收到来自用户<{}>的消息'.format(command, msg_src, received)
        elif 3 <= len(args) <= 4:
            # send_message
            send_state = args[2]
            if send_state:
                if chat_info.username is None:
                    msg_src = chat_info.title

                    log_info = '"{}":成功向群组<{}>发送消息消息'.format(command, msg_src)
                else:
                    msg_src = '{} {}(id:{})'.format(chat_info.first_name, chat_info.last_name, chat_info.id)

                    log_info = '"{}":成功向用户<{}>发送消息'.format(command, msg_src)
            else:
                err_info = args[3]
                if chat_info.username is None:
                    msg_src = chat_info.title

                    log_info = '"{}":向群组<{}>发送消息时出现错误{}'.format(command, msg_src, err_info)
                else:
                    msg_src = '{} {}(id:{})'.format(chat_info.first_name, chat_info.last_name, chat_info.id)

                    log_info = '"{}":向用户<{}>发送消息时出现错误{}'.format(command, msg_src, err_info)
        else:
            # error
            log_info = '"message_log":传入参数数量错误'
    except Exception as e:
        log_info = '"message_log":传入参数错误{}'.format(e)

    log_output(log_info)


def log_output(log_info):
    """日志输出

    在‘log’文件夹下对应日期的文件中写入日志以及在控制台中输出日志

    :param log_info:日志内容
    :return: 带有时间的日志信息
    """
    if not os.path.exists('./logs'): os.mkdir('./logs')

    now_time = get_time().split(' ')[0]

    log_file = open('./logs/{}.txt'.format(now_time), 'a+', encoding='UTF-8')
    log_file.write('[{}]{}\n'.format(get_time(), log_info))
    log_file.close()

    print('[{}]{}'.format(get_time(), log_info))


def cache_mgt(cache_title, cache_content):
    """缓存管理

    清除过期缓存，写入缓存

    :param cache_title: 缓存标题
    :param cache_content: 缓存内容
    :return: None
    """
    if not os.path.exists('./caches'): os.mkdir('./caches')     # 检查缓存目录是否存在，不存在则创建

    now_time = get_time().split(' ')[0]

    # 检查并清除过期缓存
    for file in os.listdir('./caches'):
        new_time = datetime.datetime.now(pytz.timezone('Asia/Shanghai'))
        file_time = os.path.splitext(file)[0].split('+')[0]
        delta = datetime.timedelta(days=7)  # TODO 自定义缓存留存日期

        if file_time <= (new_time - delta).strftime('%Y-%m-%d'):
            log_output('"cache_mgt":清理过期缓存')
            try:
                os.remove('./caches/{}'.format(file))

                log_output('"cache_mgt":删除文件{}成功'.format(file))
            except Exception as e:
                log_output('"cache_mgt":删除文件{}时出现错误{}'.format(file, e))


    # 写入缓存
    cache_file = open('./caches/{}+{}.txt'.format(now_time, cache_title), 'a+', encoding='UTF-8')

    try:
        str_cache_content = ''

        for char in str(cache_content):
            if char == '"':
                str_cache_content += '\''
            elif char == '\'':
                str_cache_content += '"'
            else:
                str_cache_content += char

        cache_file.write(str_cache_content)

        log_output('"cache_mgt":成功写入缓存')
    except Exception as e:
        if os.path.exists('./caches/{}+{}.txt'.format(now_time, cache_title)): os.remove('./caches/{}+{}.txt'.format(now_time, cache_title))

        log_output('"cache_mgt":写入缓存时出现错误{}，删除缓存文件'.format(e))

    cache_file.close()


# 请求过滤
last_command_time = {}
def request_filter(user_id):
    """ 拦截同一用户短时间内的多次请求

    :param user_id: Telegram用户ID
    :return: True-拦截，False-放行
    """
    # 获取当前时间戳
    now = datetime.datetime.now()

    # 如果用户上一次发送命令的时间距离现在不到60秒，拦截该命令
    if user_id in last_command_time and now - last_command_time[user_id] < datetime.timedelta(seconds=60):
        log_output('"request_filter":拦截用户<{}>的请求'.format(user_id))

        return True

    # 更新用户上一次发送命令的时间
    last_command_time[user_id] = now

    log_output('"request_filter":已放行用户<{}>的请求'.format(user_id))

    return False


if __name__ == '__main__':
    updater = Updater(token=TOKEN, request_kwargs={
        'proxy_url': 'socks5h://127.0.0.1:11223/'
    })

    dispatcher = updater.dispatcher
    log_output('-----------------初始化成功-----------------')

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("yan", yan))
    dispatcher.add_handler(CommandHandler("bangumi", bangumi_calendar))
    dispatcher.add_handler(CommandHandler("crazy_kfc", crazy_kfc))
    dispatcher.add_handler(CommandHandler("sese", sese))
    dispatcher.add_handler(CommandHandler("day_rank", day_rank))
    dispatcher.add_handler(CommandHandler("week_rank", week_rank))
    dispatcher.add_handler(CommandHandler("month_rank", month_rank))
    dispatcher.add_handler(CommandHandler("day_rank_r18", day_rank_r18))
    dispatcher.add_handler(CommandHandler("week_rank_r18", week_rank_r18))
    dispatcher.add_handler(CommandHandler("rank_r18g", rank_r18g))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("about", about))
    dispatcher.add_handler(CallbackQueryHandler(query_mgt))

    updater.start_polling()
    updater.idle()
