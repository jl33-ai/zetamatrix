# Generated by Django 5.0.1 on 2024-01-30 01:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("game", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="gamesession",
            name="is_dailychallenge",
            field=models.BooleanField(default=False),
        ),
    ]
