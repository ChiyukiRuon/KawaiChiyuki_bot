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
    now_time = Functions.get_time()
    chat_id = update.message.chat_id
    try:
        dispatcher.bot.sendPhoto(
            chat_id=chat_id,
            photo=open('./res/images/welcome.png', 'rb'),
            caption='来辣！'
        )
    except Exception as e:
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='发送信息时出现错误{}'.format(e)
        )
        print('[{}]"yan":发送信息失败{}'.format(now_time, e))


def yan(update, context):
    now_time = Functions.get_time()
    chat_id = update.message.chat_id
    yan_info = Yiyan.hitokoto()
    if yan_info.get('content') is None:
        print('[{}]"yan":获取一言失败'.format(now_time))
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='获取一言时出错'
        )
    else:
        try:
            dispatcher.bot.sendMessage(
                chat_id=chat_id,
                text='"<b>{}</b>"\n出处：{}'.format(yan_info.get('content'), yan_info.get('source')),
                parse_mode='HTML'
            )
            print('[{}]"yan":发送信息成功'.format(now_time))
        except Exception as e:
            dispatcher.bot.sendMessage(
                chat_id=chat_id,
                text='发送信息时出错：{}'.format(e)
            )
            print('[{}]"yan":发送信息失败{}'.format(now_time, e))


def bangumi(update, context):
    bangumi_str = ''
    now_time = Functions.get_time()
    chat_id = update.message.chat_id
    message = update.message.text.split(' ')
    if len(message) > 1:
        bangumi_info = Bangumi.bangumi(int(message[1]))
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
            print('[{}]"bangumi":发送消息成功'.format(now_time))
        except Exception as e:
            print('[{}]"bangumi":发送消息时出现错误：{}'.format(now_time, e))
    else:
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
            print('[{}]"bangumi":发送消息成功'.format(now_time))
        except Exception as e:
            print('[{}]"bangumi":发送消息时出现错误：{}'.format(now_time, e))
            dispatcher.bot.sendMessage(
                chat_id=chat_id,
                text='发送消息时出现错误{}'.format(e)
            )


def sese(update, context):
    now_time = Functions.get_time()
    chat_id = update.message.chat_id
    pic_info = GetPixivImage.random_pic()
    print('[{}]"sese":获取到图片信息：{}'.format(now_time, pic_info))
    try:
        if pic_info.get('num') != 1:
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
            print('[{}]"sese":成功发送信息'.format(now_time))
        elif pic_info.get('num') == 1:
            dispatcher.bot.sendPhoto(
                chat_id=chat_id,
                photo=pic_info.get('url'),
                caption='标题：{}\n作者：{}\n<a href="https://www.pixiv.net/artworks/{}">原图链接</a>'.format(
                    pic_info.get('title'),
                    pic_info.get('username'),
                    pic_info.get('pid')),
                parse_mode='HTML'
            )
            print('[{}]"sese":成功发送信息'.format(now_time))
        else:
            dispatcher.bot.sendMessage(
                chat_id=chat_id,
                text='获取图片时发生错误：{}'.format(pic_info.get('message'))
            )
            print('[{}]"sese":发送信息失败'.format(now_time))
    except Exception as e:
        print('[{}]"sese":{}'.format(now_time, e))
        if pic_info.get('message') is None:
            dispatcher.bot.sendMessage(
                chat_id=chat_id,
                text='发送图片时出现错误：{}'.format(e),
                parse_mode='HTML'
            )
        else:
            dispatcher.bot.sendMessage(
                chat_id=chat_id,
                text='获取图片时发生错误：{}'.format(pic_info.get('message'))
            )
        print('[{}]"sese":发送信息失败'.format(now_time))


def day_rank(update, context):
    now_time = Functions.get_time()
    chat_id = update.message.chat_id
    images_info = GetPixivImage.pixiv_rank('day')
    if images_info[0].get('message') is None:
        message = update.message.text.split(' ')
        page = 0
        if len(message) > 1:
            page = int(message[1])
            if page < 0:
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
        print('[{}]"day_rank":发送信息成功'.format(now_time))
    else:
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='获取图片时发生错误：{}'.format(images_info[0].get('message'))
        )
        print('[{}]"day_rank":发送信息失败'.format(now_time))


def week_rank(update, context):
    now_time = Functions.get_time()
    chat_id = update.message.chat_id
    images_info = GetPixivImage.pixiv_rank('week')
    if images_info[0].get('message') is None:
        message = update.message.text.split(' ')
        page = 0
        if len(message) > 1:
            page = int(message[1])
            if page < 0:
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
        print('[{}]"week_rank":发送信息成功'.format(now_time))
    else:
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='获取图片时发生错误：{}'.format(images_info[0].get('message'))
        )
        print('[{}]"week_rank":发送信息失败'.format(now_time))


def month_rank(update, context):
    now_time = Functions.get_time()
    chat_id = update.message.chat_id
    images_info = GetPixivImage.pixiv_rank('month')
    if images_info[0].get('message') is None:
        message = update.message.text.split(' ')
        page = 0
        if len(message) > 1:
            page = int(message[1])
            if page < 0:
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
        print('[{}]"month_rank":发送信息成功'.format(now_time))
    else:
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='获取图片时发生错误：{}'.format(images_info[0].get('message'))
        )
        print('[{}]"month_rank":发送信息失败'.format(now_time))


def day_rank_r18(update, context):
    now_time = Functions.get_time()
    chat_id = update.message.chat_id
    images_info = GetPixivImage.pixiv_rank('day_r18')
    if images_info[0].get('message') is None:
        message = update.message.text.split(' ')
        page = 0
        if len(message) > 1:
            page = int(message[1])
            if page < 0:
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
        print('[{}]"day_rank_r18":发送信息成功'.format(now_time))
    else:
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='获取图片时发生错误：{}'.format(images_info[0].get('message'))
        )
        print('[{}]"day_rank_r18":发送信息失败'.format(now_time))


def week_rank_r18(update, context):
    now_time = Functions.get_time()
    chat_id = update.message.chat_id
    images_info = GetPixivImage.pixiv_rank('week_r18')
    if images_info[0].get('message') is None:
        message = update.message.text.split(' ')
        page = 0
        if len(message) > 1:
            page = int(message[1])
            if page < 0:
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
        print('[{}]"week_rank_r18":发送信息成功'.format(now_time))
    else:
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='获取图片时发生错误：{}'.format(images_info[0].get('message'))
        )
        print('[{}]"week_rank_r18":发送信息失败'.format(now_time))


def rank_r18g(update, context):
    now_time = Functions.get_time()
    chat_id = update.message.chat_id
    images_info = GetPixivImage.pixiv_rank('week_r18g')
    if images_info[0].get('message') is None:
        message = update.message.text.split(' ')
        page = 0
        if len(message) > 1:
            page = int(message[1])
            if page < 0:
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
        print('[{}]"rank_r18":发送信息成功'.format(now_time))
    else:
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='获取图片时发生错误：{}'.format(images_info[0].get('message'))
        )
        print('[{}]"rank_r18":发送信息失败'.format(now_time))


# 发送帮助
def help(update, context):
    now_time = Functions.get_time()
    chat_id = update.message.chat_id
    dispatcher.bot.sendMessage(
        chat_id=chat_id,
        text='在获取Pixiv排行榜的指令后加上页数获取更多图片（每页5张图，共6页），不填默认发送前五张图片\n例：<code>/day_rank 2</code>\n获取日榜第5-10名的图片',
        parse_mode='HTML'
    )


# 关于
def about(update, context):
    now_time = Functions.get_time()
    chat_id = update.message.chat_id
    dispatcher.bot.sendMessage(
        chat_id=chat_id,
        text='Powered by <a href="https://chiyukiruon.top">千雪琉音</a> @ <a href="tg://user?id=5325866562">ChiyukiRuon</a>',
        parse_mode='HTML'
    )


def send_photos(chat_id, image_list, page):
    now_time = Functions.get_time()
    try:
        for key in range(len(image_list)):
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
