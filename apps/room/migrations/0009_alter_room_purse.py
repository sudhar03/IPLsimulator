# Generated by Django 4.2 on 2025-07-12 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0008_alter_room_purse_alter_teamstate_purse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='purse',
            field=models.BigIntegerField(default=100000000000),
        ),
    ]
