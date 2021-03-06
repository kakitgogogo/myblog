# Generated by Django 2.0.7 on 2018-07-28 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20180727_2245'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-sticky', '-created_time'], 'verbose_name': 'post', 'verbose_name_plural': 'posts'},
        ),
        migrations.AlterField(
            model_name='post',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created time'),
        ),
        migrations.AlterField(
            model_name='post',
            name='modified_time',
            field=models.DateTimeField(auto_now=True, verbose_name='last modified time'),
        ),
    ]
