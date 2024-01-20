# import logging
# from django.core.management.base import BaseCommand
# from django.db.models import Q
# from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
# from telegram_bot.models import TelegramUser, Question, Answer
#
# logger = logging.getLogger(__name__)
#
#
# class Command(BaseCommand):
#     help = 'Run the Telegram bot'
#
#     def handle(self, *args, **options):
#         updater = Updater(token='6580902004:AAFyYjcAk_lOWJQ3eCPBrNU_D0zJlSWmTMY', use_context=True)
#         dp = updater.dispatcher
#
#         dp.add_handler(MessageHandler(Filters.text & ~Filters.command, self.handle_message))
#
#         updater.start_polling()
#         updater.idle()
#
#     def handle_message(self, update, context):
#         user = update.effective_user
#         chat_id = update.message.chat_id
#         message_text = update.message.text
#
#         # Check the user's current state
#         current_state = TelegramUser.objects.get(user_id=user.id).state
#         print(current_state)
#         if current_state == 'waiting_for_phone':
#             # Process the phone number
#             # Save it to the user model, set the next state, and ask the first question
#             self.process_phone_number(user, message_text)
#             self.ask_question(update, context, chat_id)
#         elif current_state == 'answering_question':
#             # Process the answer
#             self.process_answer(user, message_text, update)
#             self.ask_question(update, context, chat_id)
#         else:
#             # If the user is not in a known state, ask for the phone number
#             self.ask_phone_number(update, context, chat_id)
#
#     def ask_phone_number(self, update, context, chat_id):
#         context.bot.send_message(chat_id, "Please send your phone number.")
#         # Set the user state to waiting_for_phone
#         TelegramUser.objects.filter(user_id=update.effective_user.id).update(state='waiting_for_phone')
#
#     def process_phone_number(self, user, phone_number):
#         # Save the phone number to the user model
#         TelegramUser.objects.filter(user_id=user.id).update(state=None)
#
#     def ask_question(self, update, context, chat_id):
#         # Get the next question
#         question = self.get_next_question(update)
#         if question:
#             context.bot.send_message(chat_id, f"Question: {question.text}")
#             # Set the user state to answering_question
#             TelegramUser.objects.filter(user_id=update.effective_user.id).update(state='answering_question')
#         else:
#             context.bot.send_message(chat_id, "No more questions. Thank you!")
#
#     def get_next_question(self, update):
#         # Implement your logic to get the next question
#         # For example, you can return the next unanswered question for the user
#         # or implement a random selection
#         user_id = update.effective_user.id
#         userr = TelegramUser.objects.filter(user_id=user_id).last()
#         print("USER ID: ", userr.id)
#         questions_user_answered = Answer.objects.filter(user_id=user_id).values_list()
#         print("QUESTIONS USER ANSWERS: ", questions_user_answered)
#         unanswered_questions = Question.objects.filter(~Q(answers__user_id=userr.id))
#
#         print(f"Unanswered Questions: {unanswered_questions}")
#
#         next_question = unanswered_questions.first()
#
#         print(f"Next Question: {next_question}")
#
#         return next_question
#
#     def process_answer(self, user, answer_text, update):
#         # Save the answer to the Answer model
#         question = self.get_next_question(update)
#         userr = TelegramUser.objects.filter(user_id=user.id).last()
#         Answer.objects.create(user=userr, question=question, text=answer_text)
#         # Clear the user state
#         TelegramUser.objects.filter(user_id=user.id).update(state=None)

#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

# """
# First, a few callback functions are defined. Then, those functions are passed to
# the Application and registered at their respective places.
# Then, the bot is started and runs until we press Ctrl-C on the command line.
#
# Usage:
# Example of a bot-user conversation using ConversationHandler.
# Send /start to initiate the conversation.
# Press Ctrl-C on the command line or send a signal to the process to stop the
# bot.
# """
#
# import logging
# from typing import Dict
#
# from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
# from telegram.ext import (
#     Application,
#     CommandHandler,
#     ContextTypes,
#     ConversationHandler,
#     MessageHandler,
#     filters,
# )
#
# # Enable logging
# logging.basicConfig(
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
# )
# # set higher logging level for httpx to avoid all GET and POST requests being logged
# logging.getLogger("httpx").setLevel(logging.WARNING)
#
# logger = logging.getLogger(__name__)
#
# CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)
#
# reply_keyboard = [
#     ["Xa", "Yo'q"],
#     # ["Number of siblings", "Something else..."],
#     # ["Done"],
# ]
# markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
#
#
# def facts_to_str(user_data: Dict[str, str]) -> str:
#     """Helper function for formatting the gathered user info."""
#     facts = [f"{key} - {value}" for key, value in user_data.items()]
#     return "\n".join(facts).join(["\n", "\n"])
#
#
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Start the conversation and ask user for input."""
#     await update.message.reply_text(
#         "Сизда оёқларда кўринадиган веналар борми?",
#         reply_markup=markup,
#     )
#
#     return CHOOSING
#
#
# async def regular_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Ask the user for info about the selected predefined choice."""
#     text = update.message.text
#     print("TTTTTTT: ", text)
#     context.user_data["choice"] = text
#     await update.message.reply_text(f"Your {text.lower()}? Yes, I would love to hear about that!")
#
#     return TYPING_REPLY
#
#
# async def custom_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Ask the user for a description of a custom category."""
#     await update.message.reply_text(
#         'Alright, please send me the category first, for example "Most impressive skill"'
#     )
#
#     return TYPING_CHOICE
#
#
# async def received_information(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Store info provided by user and ask for the next category."""
#     user_data = context.user_data
#     text = update.message.text
#     category = user_data["choice"]
#     print(text)
#     user_data[category] = text
#     del user_data["choice"]
#
#     await update.message.reply_text(
#         "Neat! Just so you know, this is what you already told me:"
#         f"{facts_to_str(user_data)}You can tell me more, or change your opinion"
#         " on something.",
#         reply_markup=markup,
#     )
#
#     return CHOOSING
#
#
# async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Display the gathered info and end the conversation."""
#     user_data = context.user_data
#     if "choice" in user_data:
#         del user_data["choice"]
#
#     await update.message.reply_text(
#         f"I learned these facts about you: {facts_to_str(user_data)}Until next time!",
#         reply_markup=ReplyKeyboardRemove(),
#     )
#
#     user_data.clear()
#     return ConversationHandler.END
#
#
# def main() -> None:
#     """Run the bot."""
#     # Create the Application and pass it your bot's token.
#     application = Application.builder().token("6580902004:AAFyYjcAk_lOWJQ3eCPBrNU_D0zJlSWmTMY").build()
#
#     # Add conversation handler with the states CHOOSING, TYPING_CHOICE and TYPING_REPLY
#     conv_handler = ConversationHandler(
#         entry_points=[CommandHandler("start", start)],
#         states={
#             CHOOSING: [
#                 MessageHandler(
#                     filters.Regex("^(Xa|Yo'q)$"), regular_choice
#                 ),
#                 MessageHandler(filters.Regex("^Something else...$"), custom_choice),
#             ],
#             TYPING_CHOICE: [
#                 MessageHandler(
#                     filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")), regular_choice
#                 )
#             ],
#             TYPING_REPLY: [
#                 MessageHandler(
#                     filters.TEXT & ~(filters.COMMAND | filters.Regex("^Done$")),
#                     received_information,
#                 )
#             ],
#         },
#         fallbacks=[MessageHandler(filters.Regex("^Done$"), done)],
#     )
#
#     application.add_handler(conv_handler)
#
#     # Run the bot until the user presses Ctrl-C
#     application.run_polling(allowed_updates=Update.ALL_TYPES)
#
#
# if __name__ == "__main__":
#     main()



#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

QUESTION, NEXT_QUESTION, ANSWER, BIO = range(4)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [["Boy", "Girl", "Other"]]

    await update.message.reply_text(
        "Hi! My name is Professor Bot. I will hold a conversation with you. "
        "Send /cancel to stop talking to me.\n\n"
        "Are you a boy or a girl?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Boy or Girl?"
        ),
    )

    return QUESTION


async def question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "I see! Please send me a photo of yourself, "
        "so I know what you look like, or send /skip if you don't want to.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return NEXT_QUESTION


async def next_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the photo and asks for a location."""
    user = update.message.from_user
    photo_file = await update.message.photo[-1].get_file()
    await photo_file.download_to_drive("user_photo.jpg")
    logger.info("Photo of %s: %s", user.first_name, "user_photo.jpg")
    await update.message.reply_text(
        "Gorgeous! Now, send me your location please, or send /skip if you don't want to."
    )

    return ANSWER


async def skip_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the photo and asks for a location."""
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    await update.message.reply_text(
        "I bet you look great! Now, send me your location please, or send /skip."
    )

    return ANSWER


async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the location and asks for some info about the user."""
    user = update.message.from_user
    user_location = update.message.location
    logger.info(
        "Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude
    )
    await update.message.reply_text(
        "Maybe I can visit you sometime! At last, tell me something about yourself."
    )

    return BIO


async def skip_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Skips the location and asks for info about the user."""
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    await update.message.reply_text(
        "You seem a bit paranoid! At last, tell me something about yourself."
    )

    return BIO


async def bio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the info about the user and ends the conversation."""
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text("Thank you! I hope we can talk again some day.")

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("6580902004:AAFyYjcAk_lOWJQ3eCPBrNU_D0zJlSWmTMY").build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            QUESTION: [MessageHandler(filters.Regex("^(Boy|Girl|Other)$"), question)],
            NEXT_QUESTION: [MessageHandler(filters.PHOTO, next_question)],
            ANSWER: [
                MessageHandler(filters.LOCATION, answer),
            ],
            BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, bio)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()