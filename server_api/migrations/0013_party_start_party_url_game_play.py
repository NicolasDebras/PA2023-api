# Generated by Django 4.1.2 on 2023-06-21 16:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server_api', '0012_message'),
    ]

    operations = [
        migrations.CreateModel(
            name='Play',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('infoSend', models.CharField(max_length=5000)),
                ('date_creation', models.DateTimeField(auto_now_add=True, null=True)),
                ('party', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fk_game_partie', to='server_api.party')),
                ('player', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='player_play', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]