# Generated by Django 4.1.2 on 2023-04-24 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server_api', '0008_alter_participant_party_alter_participant_player_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='party',
            name='url_image',
            field=models.CharField(max_length=500, null=True),
        ),
    ]