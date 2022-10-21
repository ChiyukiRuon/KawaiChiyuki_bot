import datetime
import os
import traceback
import pytz
from telegram.ext import Updater, CommandHandler

import GetPixivImage

TOKEN = os.getenv("TOKEN")

tz = pytz.timezone('Asia/Shanghai')
now_time = datetime.datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')


# 打招呼
def start(update, context):
    chat_id = update.message.chat_id
    dispatcher.bot.sendPhoto(
        chat_id=chat_id,
        photo=open('./res/images/welcome.png', 'rb'),
        caption='来辣！'
    )


def sese(update, context):
    chat_id = update.message.chat_id
    pic_info = GetPixivImage.random_pic()
    print('{}:"sese"获取到图片信息：{}'.format(now_time, pic_info))
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
            print('{}:"sese"成功发送信息'.format(now_time))
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
            print('{}:"sese"成功发送信息'.format(now_time))
        else:
            dispatcher.bot.sendMessage(
                chat_id=chat_id,
                text='获取图片时发生错误：{}'.format(pic_info.get('message'))
            )
            print('{}:"sese"发送信息失败'.format(now_time))
    except Exception as e:
        print('{}:"sese"{}'.format(now_time, e))
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
        print('{}:"sese"发送信息失败'.format(now_time))


def day_rank(update, context):
    chat_id = update.message.chat_id
    images_info = GetPixivImage.pixiv_rank('day')
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


def week_rank(update, context):
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
    else:
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='获取图片时发生错误：{}'.format(images_info[0].get('message'))
        )


def month_rank(update, context):
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
    else:
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='获取图片时发生错误：{}'.format(images_info[0].get('message'))
        )


def day_rank_r18(update, context):
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
    else:
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='获取图片时发生错误：{}'.format(images_info[0].get('message'))
        )


def week_rank_r18(update, context):
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
    else:
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='获取图片时发生错误：{}'.format(images_info[0].get('message'))
        )


def rank_r18g(update, context):
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
    else:
        dispatcher.bot.sendMessage(
            chat_id=chat_id,
            text='获取图片时发生错误：{}'.format(images_info[0].get('message'))
        )


# 发送帮助
def help(update, context):
    chat_id = update.message.chat_id
    dispatcher.bot.sendMessage(
        chat_id=chat_id,
        text='在获取Pixiv排行榜的指令后加上页数获取更多图片（每页5张图，共6页），不填默认发送前五张图片\n例：<code>/day_rank 2</code>\n获取日榜第5-10名的图片',
        parse_mode='HTML'
    )


# 关于
def about(update, context):
    chat_id = update.message.chat_id
    dispatcher.bot.sendMessage(
        chat_id=chat_id,
        text='Powered by <a href="https://chiyukiruon.top">千雪琉音</a> @ <a href="tg://user?id=5325866562">ChiyukiRuon</a>',
        parse_mode='HTML'
    )


def send_photos(chat_id, image_list, page):
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
                print('{}:"send_photos"在发送第 <b>{}</b> 张图片时发生错误\n错误信息：{}'.format(now_time, key + 1, e))
                dispatcher.bot.sendMessage(
                    chat_id=chat_id,
                    text='在发送第 <b>{}</b> 张图片时发生错误\n错误信息：{}'.format(key + 1, e),
                    parse_mode='HTML'
                )
        elif key > (page + 1)*5 - 1:
            break


if __name__ == '__main__':
    updater = Updater(token=TOKEN, request_kwargs={'proxy_url': 'http://127.0.0.1:11223/'})

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
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
