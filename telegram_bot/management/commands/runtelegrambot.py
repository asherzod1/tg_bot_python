import logging
from django.core.management.base import BaseCommand
from django.db.models import Q
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram_bot.models import TelegramUser, Question, Answer

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Run the Telegram bot'

    def handle(self, *args, **options):
        updater = Updater(token='6580902004:AAFyYjcAk_lOWJQ3eCPBrNU_D0zJlSWmTMY', use_context=True)
        dp = updater.dispatcher

        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, self.handle_message))

        updater.start_polling()
        updater.idle()

    def handle_message(self, update, context):
        user = update.effective_user
        chat_id = update.message.chat_id
        message_text = update.message.text

        # Check the user's current state
        current_state = TelegramUser.objects.get(user_id=user.id).state
        print(current_state)
        if current_state == 'waiting_for_phone':
            # Process the phone number
            # Save it to the user model, set the next state, and ask the first question
            self.process_phone_number(user, message_text)
            self.ask_question(update, context, chat_id)
        elif current_state == 'answering_question':
            # Process the answer
            self.process_answer(user, message_text, update)
            self.ask_question(update, context, chat_id)
        else:
            # If the user is not in a known state, ask for the phone number
            self.ask_phone_number(update, context, chat_id)

    def ask_phone_number(self, update, context, chat_id):
        context.bot.send_message(chat_id, "Please send your phone number.")
        # Set the user state to waiting_for_phone
        TelegramUser.objects.filter(user_id=update.effective_user.id).update(state='waiting_for_phone')

    def process_phone_number(self, user, phone_number):
        # Save the phone number to the user model
        TelegramUser.objects.filter(user_id=user.id).update(state=None)

    def ask_question(self, update, context, chat_id):
        # Get the next question
        question = self.get_next_question(update)
        if question:
            context.bot.send_message(chat_id, f"Question: {question.text}")
            # Set the user state to answering_question
            TelegramUser.objects.filter(user_id=update.effective_user.id).update(state='answering_question')
        else:
            context.bot.send_message(chat_id, "No more questions. Thank you!")

    def get_next_question(self, update):
        # Implement your logic to get the next question
        # For example, you can return the next unanswered question for the user
        # or implement a random selection
        user_id = update.effective_user.id
        userr = TelegramUser.objects.filter(user_id=user_id).last()
        print("USER ID: ", userr.id)
        questions_user_answered = Answer.objects.filter(user_id=user_id).values_list()
        print("QUESTIONS USER ANSWERS: ", questions_user_answered)
        unanswered_questions = Question.objects.filter(~Q(answers__user_id=userr.id))

        print(f"Unanswered Questions: {unanswered_questions}")

        next_question = unanswered_questions.first()

        print(f"Next Question: {next_question}")

        return next_question

    def process_answer(self, user, answer_text, update):
        # Save the answer to the Answer model
        question = self.get_next_question(update)
        userr = TelegramUser.objects.filter(user_id=user.id).last()
        Answer.objects.create(user=userr, question=question, text=answer_text)
        # Clear the user state
        TelegramUser.objects.filter(user_id=user.id).update(state=None)
