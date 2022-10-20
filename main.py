import json
import os

import time
import traceback

import requests
from telegram.ext import Updater, CommandHandler

import GetPixivImage

TOKEN = os.getenv("TOKEN")


# 打招呼
def start(update, context):
    chat_id = update.message.chat_id
    dispatcher.bot.sendPhoto(
        chat_id=chat_id,
        photo=open('./res/images/welcome.png', 'rb'),
        caption='来辣！'
    )


# TODO 从Pixiv获取一张随机图片
def sese(update, context):
    chat_id = update.message.chat_id
    dispatcher.bot.sendPhoto(
        chat_id=chat_id,
        photo=GetPixivImage.random_pic()
    )


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


def month_rank(update, context):
    chat_id = update.message.chat_id
    images_info = GetPixivImage.pixiv_rank('month')
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


def day_rank_r18(update, context):
    chat_id = update.message.chat_id
    images_info = GetPixivImage.pixiv_rank('day_r18')
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


def week_rank_r18(update, context):
    chat_id = update.message.chat_id
    images_info = GetPixivImage.pixiv_rank('week_r18')
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


def rank_r18g(update, context):
    chat_id = update.message.chat_id
    images_info = GetPixivImage.pixiv_rank('week_r18g')
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
                t = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                traceback.print_exc()
                print('ERROR {}:在发送第 <b>{}</b> 张图片时发生错误\n错误信息：{}'.format(t, key + 1, e))
                dispatcher.bot.sendMessage(
                    chat_id=chat_id,
                    text='在发送第 <b>{}</b> 张图片时发生错误\n错误信息：{}'.format(key + 1, e),
                    parse_mode='HTML'
                )
        elif key > (page + 1)*5 - 1:
            break


if __name__ == '__main__':
    updater = Updater(token=TOKEN)

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
