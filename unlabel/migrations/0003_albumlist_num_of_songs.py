# Generated by Django 3.2.8 on 2021-10-27 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unlabel', '0002_auto_20211027_2149'),
    ]

    operations = [
        migrations.AddField(
            model_name='albumlist',
            name='num_of_songs',
            field=models.IntegerField(default=0),
        ),
    ]
