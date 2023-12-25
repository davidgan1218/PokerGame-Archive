# Generated by Django 5.0 on 2023-12-25 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poker_game_app', '0005_game_pot_player_bet_alter_game_min_bet'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='river_cards',
        ),
        migrations.AddField(
            model_name='game',
            name='river_card1',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='river_card2',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='river_card3',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='river_card4',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='river_card5',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
