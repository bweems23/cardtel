from django.db import models

class Game(models.Model):

    class Meta:
        db_table = 'game'
        app_label = 'cardtel'

    players = models.ManyToManyField(
        'cardtel.User',
        through='cardtel.Player'
    )
    table = models.ForeignKey(
        'cardtel.Table',
        related_name='game'
    )
    current_turn = models.ForeignKey(
        'cardtel.Player',
        related_name='pending_moves'
    )
    last_to_play_card = models.ForeignKey(
        'cardtel.Player',
        related_name='unanswered_moves',
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    @property
    def is_over(self):
        raise NotImplementedError

    @property
    def hand_is_over(self):
        raise NotImplementedError

    @property
    def point_is_over(self):
        raise NotImplementedError


class Player(models.Model):

    class Meta:
        db_table = 'player'
        app_label = 'cardtel'
        unique_together = ('game', 'user')

    game = models.ForeignKey(
        'cardtel.Game',
        db_index=True,
    )
    user = models.ForeignKey(
        'cardtel.User',
        db_index=True,
    )
    score = models.IntegerField(default=0)
    cards = models.ManyToManyField('cardtel.Card', through='cardtel.PlayerCardLink')
    has_folded = models.BooleanField(default=False)
    play_order = models.IntegerField()


class Card(models.Model):

    class Meta:
        db_table = 'card'
        app_label = 'cardtel'

    suit = models.IntegerField()
    number = models.IntegerField()
    image = models.FileField()

class Table(models.Model):

    class Meta:
        db_table = 'table'
        app_label = 'cardtel'

    cards = models.ManyToManyField('cardtel.Card')
    best_hand_score = models.IntegerField()

class PlayerCardLink(models.Model):

    class Meta:
        db_table = 'player_card_link'
        app_label = 'cardtel'
        unique_together = ('player', 'card')

    player = models.ForeignKey(
        'cardtel.Player',
        db_index=True,
    )
    card = models.ForeignKey(
        'cardtel.Card',
        db_index=True,
    )

class User(models.Model):

    class Meta:
        db_table = 'user'
        app_label = 'cardtel'

    username = models.CharField(max_length=20)
    ## TODO track overall points
