# Generated by Django 4.1.2 on 2023-04-05 19:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('server_api', '0004_alter_player_options_alter_player_managers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='player',
            name='commentaire',
        ),
    ]