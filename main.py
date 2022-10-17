import os
import get_image
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TOKEN = os.getenv("TOKEN")


# 打招呼
def start(update, context):
    chat_id = update.message.chat_id
    dispatcher.bot.sendMessage(chat_id, '来辣！')


def sese(update, context):
    chat_id = update.message.chat_id
    url = get_image.get_img_url()
    dispatcher.bot.sendPhoto(chat_id, url, '手冲一时爽，一只手冲一直爽')
    # dispatcher.bot.sendMessage(chat_id, '手冲一时爽，一只手冲一直爽')


# 发送帮助
def help(update, context):
    chat_id = update.message.chat_id
    update.message.reply_text('开发中...')


# 关于
def about(update, context):
    chat_id = update.message.chat_id
    update.message.reply_text('Powered by <a href="https://chiyukiruon.top">千雪琉音</a> @ <a '
                              'href="tg://user?id=5325866562">ChiyukiRuon</a>', parse_mode='HTML')


# 复读姬
def echo(update, context):
    chat_id = update.message.chat_id
    update.message.reply_text(update.message.text)


# def error(update, context):
#     logger.warning('Update "%s" caused error "%s"', update, context.error)


if __name__ == '__main__':
    updater = Updater(token=TOKEN, request_kwargs={'proxy_url': 'http://127.0.0.1:11223/'})

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(CommandHandler("sese", sese))
    dispatcher.add_handler(CommandHandler("about", about))

    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    # dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()
