# Generated by Django 5.0.1 on 2024-01-19 09:32

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="TelegramUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_id", models.IntegerField(unique=True)),
                ("username", models.CharField(blank=True, max_length=255, null=True)),
                ("first_name", models.CharField(max_length=255)),
                ("last_name", models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
    ]
