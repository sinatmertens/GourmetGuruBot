from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests
import json
import cookbook
import os

last_bot_message = None
last_message_id = None
last_chat_id = None

telegram_bot_key = os.getenv('TELEGRAM_BOT_TOKEN')


def start(update: Update, context: CallbackContext):
    global last_bot_message, last_message_id, last_chat_id
    context.user_data['chat_id'] = update.message.chat_id
    message_text = f"""👋 Willkommen beim Gourmet-Kochbot! Ich bin Ihr persönlicher Küchenassistent, inspiriert von den kulinarischen Kreationen des berühmten Yotam Ottolenghi. Fotografieren Sie einfach die Zutaten, die Sie verwenden wollen, und ich liefere Ihnen einen maßgeschneiderten Rezeptvorschlag und nützliche Küchentipps 🍳🌿"""

    update.message.reply_text(
        message_text
    )


def echo(update: Update, context: CallbackContext) -> None:
    """
    This function would be added to the dispatcher as a handler for messages coming from the Bot API
    """
    global last_bot_message, last_message_id, last_chat_id
    sender_name = update.message['chat']['first_name']

    # Print to console
    print(f'{update.message.from_user.first_name} wrote {update.message.text}')

    if not update.message.photo and last_chat_id:
        corrected_recipe = cookbook.correct_recipe(last_recipe=last_bot_message, correction=update.message.text)
        context.bot.edit_message_text(chat_id=last_chat_id,
                                      message_id=last_message_id,
                                      text=corrected_recipe)

        context.bot.send_message(update.message.chat_id,
                                 f"Kein Problem. Ich habe das Rezept oben an deine Wünsche angepasst. Falls es noch etwas gibt, das du geändert haben möchtest, nur zu!")

    if update.message.photo:

        # Downloading the image from the telegram server
        try:
            photo_id = update.message.photo[1]['file_id']
        except IndexError:
            photo_id = update.message.photo[0]['file_id']

        photo_path = requests.get(
            f"https://api.telegram.org/bot{telegram_bot_key}/getFile?file_id={photo_id}")
        photo_path = photo_path.content.decode('utf-8')
        photo_url = json.loads(photo_path)['result']['file_path']
        photo_url = f"https://api.telegram.org/file/bot{telegram_bot_key}/{photo_url}"
        photo = requests.get(photo_url)
        photo = photo.content

        if photo:
            print(f"Downloaded the picture from {sender_name}")

            context.bot.send_message(update.message.chat_id,
                                     f"Perfekt! Gib mir eine Minute, um dein Rezept zu generieren.")

            analysis, image_url = cookbook.main(photo)
            if image_url:
                photo = requests.get(image_url)
                photo = photo.content
                print(image_url)
                context.bot.send_photo(update.message.chat_id,
                                       photo)

            if analysis:
                sent_message = context.bot.send_message(update.message.chat_id,
                                                        f"{analysis}")
                last_bot_message = analysis
                last_message_id = sent_message.message_id
                last_chat_id = sent_message.chat_id
                context.bot.send_message(update.message.chat_id,
                                         f"🍝 Voila! Klingt das gut, oder gibt es noch etwas, das du gerne ändern würdest?")



def main() -> None:
    updater = Updater(telegram_bot_key, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    # Echo any message that is not a command
    dispatcher.add_handler(MessageHandler(~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()
