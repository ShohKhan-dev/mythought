# Generated by Django 3.2.4 on 2022-03-08 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mythought', '0007_alter_conversationmessage_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('message', 'Message'), ('follower', 'Follower'), ('like', 'Like'), ('mention', 'Mention')], max_length=20),
        ),
    ]
