# Generated by Django 4.1.2 on 2023-07-17 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server_api', '0018_party_max_player'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='tag_player',
            field=models.IntegerField(null=True),
        ),
    ]
