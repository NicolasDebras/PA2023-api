# Generated by Django 4.1.2 on 2023-06-19 17:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server_api', '0011_friend_who_ask'),
    ]

    operations = [
        migrations.AddField(
            model_name='participant',
            name='tag_player',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='party',
            name='start',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='party',
            name='url_game',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.CreateModel(
            name='Play',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('infoSend', models.CharField(max_length=5000)),
                ('date_creation', models.DateTimeField(auto_now_add=True, null=True)),
                ('party', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fk_game_partie', to='server_api.party')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('party', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='server_api.party')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
