# Generated by Django 3.2.4 on 2021-06-13 18:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mythought', '0006_notification'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='conversationmessage',
            options={'ordering': ['created_at']},
        ),
    ]
