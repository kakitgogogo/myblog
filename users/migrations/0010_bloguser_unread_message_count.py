# Generated by Django 2.0.7 on 2018-08-10 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20180730_2137'),
    ]

    operations = [
        migrations.AddField(
            model_name='bloguser',
            name='unread_message_count',
            field=models.IntegerField(default=0, verbose_name='number of unread messages'),
        ),
    ]
