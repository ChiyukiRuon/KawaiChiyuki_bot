import json
import os

import time
import traceback

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


def day_rank(update, context):
    chat_id = update.message.chat_id
    images_info = GetPixivImage.pixiv_rank('day')
    send_photos(chat_id, images_info)


def week_rank(update, context):
    chat_id = update.message.chat_id
    images_info = GetPixivImage.pixiv_rank('week')
    send_photos(chat_id, images_info)


def month_rank(update, context):
    chat_id = update.message.chat_id
    images_info = GetPixivImage.pixiv_rank('month')
    send_photos(chat_id, images_info)


def day_rank_r18(update, context):
    chat_id = update.message.chat_id
    images_info = GetPixivImage.pixiv_rank('day_r18')
    send_photos(chat_id, images_info)


def week_rank_r18(update, context):
    chat_id = update.message.chat_id
    images_info = GetPixivImage.pixiv_rank('week_r18')
    send_photos(chat_id, images_info)


def rank_r18g(update, context):
    chat_id = update.message.chat_id
    images_info = GetPixivImage.pixiv_rank('week_r18g')
    send_photos(chat_id, images_info)


# 发送帮助
def help(update, context):
    chat_id = update.message.chat_id
    dispatcher.bot.sendPhoto(
        chat_id=chat_id,
        photo=open('./res/images/bang.jpg', 'rb'),
        caption='命令列表里都说的这么明白了还要什么帮助啊!'
    )


# 关于
def about(update, context):
    chat_id = update.message.chat_id
    dispatcher.bot.sendMessage(
        chat_id=chat_id,
        text='Powered by <a href="https://chiyukiruon.top">千雪琉音</a> @ <a href="tg://user?id=5325866562">ChiyukiRuon</a>',
        parse_mode='HTML'
    )


# TODO 在发送五张图片后发送下五张图片
def send_photos(chat_id, image_list):
    for key in range(len(image_list)):
        if key > 4:
            break
        try:
            if image_list[key].get('num') > 1:
                dispatcher.bot.sendPhoto(
                    chat_id=chat_id,
                    photo=image_list[key].get('url'),
                    caption='以及{}张图片\n标题：{}\n作者：{}\n<a href="https://www.pixiv.net/artworks/{}">原图链接</a>'.format(
                        image_list[key].get('num') - 1,
                        image_list[key].get('title'),
                        image_list[key].get('username'),
                        image_list[key].get('pid')),
                    parse_mode='HTML'
                )
            else:
                dispatcher.bot.sendPhoto(
                    chat_id=chat_id,
                    photo=image_list[key].get('url'),
                    caption='标题：{}\n作者：{}\n<a href="https://www.pixiv.net/artworks/{}">原图链接</a>'.format(
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


# def set_status(func_name):
#     with open('./runningStatus.json', 'rb') as f:
#         params = json.load(f)
#         params[func_name]['last_run'] = time.strftime('%Y-%m-%d', time.localtime())


if __name__ == '__main__':
    updater = Updater(token=TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
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
