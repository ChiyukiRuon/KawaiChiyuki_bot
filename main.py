import os

from telegram.ext import Updater, CommandHandler

import PixivImage

TOKEN = os.getenv("TOKEN")


# 打招呼
def start(update, context):
    chat_id = update.message.chat_id
    dispatcher.bot.sendPhoto(
        chat_id=chat_id,
        photo=open('./res/images/welcome.png', 'rb'),
        caption='来辣！'
    )


# 发送Pixiv日榜前五的图片
def daily_rank(update, context):
    chat_id = update.message.chat_id
    images_info = PixivImage.daily_rank()
    for key in range(len(images_info)):
        if key > 4:
            break
        dispatcher.bot.sendPhoto(
            chat_id=chat_id,
            photo=images_info[key].get('url'),
            caption='标题：{}\n作者：{}\n<a href="https://www.pixiv.net/artworks/{}">原图链接</a>'.format(
                images_info[key].get('title'), images_info[key].get('username'), images_info[key].get('pid')),
            parse_mode='HTML'
        )


# 发送Pixiv R18周榜前五的图片
def weekly_rank_r18(update, context):
    chat_id = update.message.chat_id
    images_info = PixivImage.weekly_rank_r18()
    for key in range(len(images_info)):
        if key > 4:
            break
        dispatcher.bot.sendPhoto(
            chat_id=chat_id,
            photo=images_info[key].get('url'),
            caption='标题：{}\n作者：{}\n<a href="https://www.pixiv.net/artworks/{}">原图链接</a>'.format(
                images_info[key].get('title'), images_info[key].get('username'), images_info[key].get('pid')),
            parse_mode='HTML'
        )


# 发送帮助
def help(update, context):
    chat_id = update.message.chat_id
    dispatcher.bot.sendMessage(
        chat_id=chat_id,
        text='发送“/daily_rank”来获取Pixiv日榜的前五张图片\n发送“/weekly_rank_r18”来获取Pixiv R18周榜的前五张图片',
    )


# 关于
def about(update, context):
    chat_id = update.message.chat_id
    dispatcher.bot.sendMessage(
        chat_id=chat_id,
        text='Powered by <a href="https://chiyukiruon.top">千雪琉音</a> @ <a href="tg://user?id=5325866562">ChiyukiRuon</a>',
        parse_mode='HTML'
    )


if __name__ == '__main__':
    updater = Updater(token=TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("daily_rank", daily_rank))
    dispatcher.add_handler(CommandHandler("weekly_rank_r18", weekly_rank_r18))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("about", about))

    updater.start_polling()
    updater.idle()
