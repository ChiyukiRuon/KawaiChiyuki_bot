import os
import traceback

from telegram.ext import Updater, CommandHandler

import Bangumi
import Functions
import GetPixivImage
import Yiyan

TOKEN = os.getenv("TOKEN")


# 打招呼
def start(update, context):
    # 获取必要信息
    now_time = Functions.get_time()
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    # 输出接受消息的日志
    Functions.message_log(now_time, chat_info, received)

    try:
        # 发送消息
        dispatcher.bot.sendPhoto(
            chat_id=chat_id,
            photo=open('./res/images/welcome.png', 'rb'),
            caption='来辣！'
        )

        # 输出发送消息成功的日志
        Functions.message_log(now_time, chat_info, received, True)
    except Exception as e:
        # 发送消息失败
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='发送信息时出现错误{}'.format(e)
        )

        # 输出发送消息失败的日志
        Functions.message_log(now_time, chat_info, received, False, e)


# 一言二次元语录
def yan(update, context):
    now_time = Functions.get_time()
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    Functions.message_log(now_time, chat_info, received)

    try:
        update.message.reply_text('收到消息，正在处理中')
    except Exception as e:
        Functions.message_log(now_time, chat_info, received, False, e)

    yan_info = Yiyan.hitokoto()    # 获取到的一言信息
    if yan_info.get('content') is None:
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='获取一言时出错'
        )

        Functions.message_log(now_time, chat_info, received, False, '获取一言失败')
    else:
        try:
            dispatcher.bot.sendMessage(
                chat_id=chat_id,
                text='"<b>{}</b>"\n出处：{}'.format(yan_info.get('content'), yan_info.get('source')),
                parse_mode='HTML'
            )

            Functions.message_log(now_time, chat_info, received, True)
        except Exception as e:
            dispatcher.bot.sendMessage(
                chat_id=chat_id,
                text='发送信息时出错：{}'.format(e)
            )

            Functions.message_log(now_time, chat_info, received, False, e)


# 新番时间表
def bangumi(update, context):
    bangumi_str = ''
    now_time = Functions.get_time()
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    Functions.message_log(now_time, chat_info, received)

    try:
        update.message.reply_text('收到消息，正在处理中')
    except Exception as e:
        Functions.message_log(now_time, chat_info, received, False, e)

    message = update.message.text.split(' ')    # 获取输入数据
    # 判断是否制定了日期
    if len(message) > 1:    # 指定了日期
        bangumi_info = Bangumi.bangumi(int(message[1]))    # 获取到的番剧更新信息
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
                parse_mode='HTML'
            )

            Functions.message_log(now_time, chat_info, received, True)
        except Exception as e:
            Functions.message_log(now_time, chat_info, received, False, e)
    else:   # 未指定日期
        bangumi_info = Bangumi.bangumi()
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
                parse_mode='HTML'
            )

            Functions.message_log(now_time, chat_info, received, True)
        except Exception as e:
            dispatcher.bot.sendMessage(
                chat_id=chat_id,
                text='发送消息时出现错误{}'.format(e)
            )

            Functions.message_log(now_time, chat_info, received, False, e)


# 随机Pixiv图片
def sese(update, context):
    now_time = Functions.get_time()
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    Functions.message_log(now_time, chat_info, received)

    try:
        update.message.reply_text('收到消息，正在处理中')
    except Exception as e:
        print('[{}]"sese":发送消息时遇到错误{}'.format(now_time, e))

    pic_info = GetPixivImage.random_pic()
    print('[{}]"sese":获取到图片信息：{}'.format(now_time, pic_info))

    try:
        # 判断投稿内的作品数量，用不同的格式发送
        if pic_info.get('num') != 1:    # 投稿内不止一张作品
            dispatcher.bot.sendPhoto(
                chat_id=chat_id,
                photo=pic_info.get('url'),
                caption='以及{}张图片\n标题：{}\n作者：{}\n<a href="https://www.pixiv.net/artworks/{}">原图链接</a>'.format(
                    pic_info.get('num') - 1,
                    pic_info.get('title'),
                    pic_info.get('username'),
                    pic_info.get('pid')),
                parse_mode='HTML'
            )

            Functions.message_log(now_time, chat_info, received, True)
        elif pic_info.get('num') == 1:  # 投稿内仅一张作品
            dispatcher.bot.sendPhoto(
                chat_id=chat_id,
                photo=pic_info.get('url'),
                caption='标题：{}\n作者：{}\n<a href="https://www.pixiv.net/artworks/{}">原图链接</a>'.format(
                    pic_info.get('title'),
                    pic_info.get('username'),
                    pic_info.get('pid')),
                parse_mode='HTML'
            )

            Functions.message_log(now_time, chat_info, received, True)
        else:   # 发生错误
            dispatcher.bot.sendMessage(
                chat_id=chat_id,
                text='获取图片时发生错误：{}'.format(pic_info.get('message'))
            )

            Functions.message_log(now_time, chat_info, received, False, pic_info.get('message'))
    except Exception as e:
        if pic_info.get('message') is None:
            dispatcher.bot.sendMessage(
                chat_id=chat_id,
                text='发送图片时出现错误：{}'.format(e),
                parse_mode='HTML'
            )

            Functions.message_log(now_time, chat_info, received, False, e)
        else:
            dispatcher.bot.sendMessage(
                chat_id=chat_id,
                text='获取图片时发生错误：{}'.format(pic_info.get('message'))
            )

            Functions.message_log(now_time, chat_info, received, False, pic_info.get('message'))


# Pixiv日榜
def day_rank(update, context):
    now_time = Functions.get_time()
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    Functions.message_log(now_time, chat_info, received)

    try:
        update.message.reply_text('收到消息，正在处理中')
    except Exception as e:
        print('[{}]"day_rank":发送消息时遇到错误{}'.format(now_time, e))

    images_info = GetPixivImage.pixiv_rank('day')
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

        Functions.message_log(now_time, chat_info, received, True)
    else:   # 获取图片信息失败
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='获取图片时发生错误：{}'.format(images_info[0].get('message'))
        )

        Functions.message_log(now_time, chat_info, received, False, images_info[0].get('message'))


# Pixiv周榜
def week_rank(update, context):
    now_time = Functions.get_time()
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    Functions.message_log(now_time, chat_info, received)

    try:
        update.message.reply_text('收到消息，正在处理中')
    except Exception as e:
        Functions.message_log(now_time, chat_info, received, False, e)

    images_info = GetPixivImage.pixiv_rank('week')
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

        Functions.message_log(now_time, chat_info, received, True)
    else:
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='获取图片时发生错误：{}'.format(images_info[0].get('message'))
        )

        Functions.message_log(now_time, chat_info, received, False, images_info[0].get('message'))


# Pixiv月榜
def month_rank(update, context):
    now_time = Functions.get_time()
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    Functions.message_log(now_time, chat_info, received)

    try:
        update.message.reply_text('收到消息，正在处理中')
    except Exception as e:
        Functions.message_log(now_time, chat_info, received, False, e)

    images_info = GetPixivImage.pixiv_rank('month')
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

        Functions.message_log(now_time, chat_info, received, True)
    else:
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='获取图片时发生错误：{}'.format(images_info[0].get('message'))
        )

        Functions.message_log(now_time, chat_info, received, False, images_info[0].get('message'))


# Pixiv R18日榜
def day_rank_r18(update, context):
    now_time = Functions.get_time()
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    Functions.message_log(now_time, chat_info, received)

    try:
        update.message.reply_text('收到消息，正在处理中')
    except Exception as e:
        Functions.message_log(now_time, chat_info, received, False, e)

    images_info = GetPixivImage.pixiv_rank('day_r18')
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

        Functions.message_log(now_time, chat_info, received, True)
    else:
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='获取图片时发生错误：{}'.format(images_info[0].get('message'))
        )

        Functions.message_log(now_time, chat_info, received, False, images_info[0].get('message'))


# Pixiv R18周榜
def week_rank_r18(update, context):
    now_time = Functions.get_time()
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    Functions.message_log(now_time, chat_info, received)

    try:
        update.message.reply_text('收到消息，正在处理中')
    except Exception as e:
        Functions.message_log(now_time, chat_info, received, False, e)

    images_info = GetPixivImage.pixiv_rank('week_r18')
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

        Functions.message_log(now_time, chat_info, received, True)
    else:
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='获取图片时发生错误：{}'.format(images_info[0].get('message'))
        )

        Functions.message_log(now_time, chat_info, received, False, images_info[0].get('message'))


# Pixiv R18G排行榜
def rank_r18g(update, context):
    now_time = Functions.get_time()
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    Functions.message_log(now_time, chat_info, received)

    try:
        update.message.reply_text('收到消息，正在处理中')
    except Exception as e:
        Functions.message_log(now_time, chat_info, received, False, e)

    images_info = GetPixivImage.pixiv_rank('week_r18g')
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

        Functions.message_log(now_time, chat_info, received, True)
    else:
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='获取图片时发生错误：{}'.format(images_info[0].get('message'))
        )

        Functions.message_log(now_time, chat_info, received, False, images_info[0].get('message'))


# 获取帮助
def help(update, context):
    now_time = Functions.get_time()
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    Functions.message_log(now_time, chat_info, received)

    try:
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='<b>Pixiv</b>\n-<code>/{day|week|month}_rank [page]</code> \n-获取Pixiv{日|周|月}榜的图片\n'
                 '...\n'
                 '<b>Bangumi</b>\n-<code>/bangumi [weekday]</code> \n-weekday的范围为1-7\n'
                 '<b>使用 /about 以获取更多信息</b>',
            parse_mode='HTML'
        )

        Functions.message_log(now_time, chat_info, received, True)
    except Exception as e:
        Functions.message_log(now_time, chat_info, received, False, e)


# 关于
def about(update, context):
    now_time = Functions.get_time()
    chat_id = update.message.chat_id
    received = update.message.text
    chat_info = update.message.chat

    Functions.message_log(now_time, chat_info, received)

    try:
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='项目地址：<a href="https://github.com/ChiyukiRuon/KawaiChiyuki_bot">Github</a>\n'
                 'Powered by <a href="https://chiyukiruon.top">千雪琉音</a> @ <a href="tg://user?id=5325866562">ChiyukiRuon</a>',
            parse_mode='HTML'
        )

        Functions.message_log(now_time, chat_info, received, True)
    except Exception as e:
        Functions.message_log(now_time, chat_info, received, False, e)


def send_photos(chat_id, image_list, page):
    now_time = Functions.get_time()
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
                    print('[{}]"send_photos":在发送第 <b>{}</b> 张图片时发生错误\n错误信息：{}'.format(now_time, key + 1, e))
                    dispatcher.bot.sendMessage(
                        chat_id=chat_id,
                        text='在发送第 <b>{}</b> 张图片时发生错误\n错误信息：{}'.format(key + 1, e),
                        parse_mode='HTML'
                    )
            elif key > (page + 1)*5 - 1:
                break
    except Exception as e:
        print('[{}]"send_photos":获取图片时发生错误{}'.format(now_time, e))
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='获取图片时发生错误：{}'.format(e)
        )


if __name__ == '__main__':
    now_time = Functions.get_time()
    updater = Updater(token=TOKEN, request_kwargs={'proxy_url': 'http://127.0.0.1:11223/'})

    dispatcher = updater.dispatcher
    print('[{}]初始化成功'.format(now_time))

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("yan", yan))
    dispatcher.add_handler(CommandHandler("bangumi", bangumi))
    dispatcher.add_handler(CommandHandler("sese", sese))
    dispatcher.add_handler(CommandHandler("day_rank", day_rank))
    dispatcher.add_handler(CommandHandler("week_rank", week_rank))
    dispatcher.add_handler(CommandHandler("month_rank", month_rank))
    dispatcher.add_handler(CommandHandler("day_rank_r18", day_rank_r18))
    dispatcher.add_handler(CommandHandler("week_rank_r18", week_rank_r18))
    dispatcher.add_handler(CommandHandler("rank_r18g", rank_r18g))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("about", about))

    updater.start_polling()
    updater.idle()
