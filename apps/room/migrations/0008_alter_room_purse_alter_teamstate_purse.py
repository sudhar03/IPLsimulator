# Generated by Django 4.2 on 2025-07-12 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0007_alter_auctionplayer_current_bid_team_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='purse',
            field=models.BigIntegerField(default=10000000000),
        ),
        migrations.AlterField(
            model_name='teamstate',
            name='purse',
            field=models.BigIntegerField(default=0),
        ),
    ]
