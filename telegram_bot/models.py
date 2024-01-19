from django.db import models

# Create your models here.


class TelegramUser(models.Model):
    user_id = models.IntegerField(unique=True)
    username = models.CharField(max_length=255, null=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)  # Add this field

    def __str__(self):
        return f"{self.username} - {self.user_id}"


class Question(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text


class Answer(models.Model):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()

    def __str__(self):
        return f"{self.user} - {self.question.text}"