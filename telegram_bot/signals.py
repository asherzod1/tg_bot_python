from django.db.models.signals import post_save
from django.dispatch import receiver
from telegram_bot.models import TelegramUser
from telegram import Update


@receiver(post_save, sender=TelegramUser)
def update_user(sender, instance, **kwargs):
    # Update logic goes here
    pass