# Generated by Django 3.2.8 on 2021-11-13 06:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('unlabel', '0008_alter_artist_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ArtistList',
        ),
    ]