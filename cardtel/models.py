from django.db import models

class Game(models.Model):

    class Meta:
        db_table = 'game'
        app_label = 'cardtel'

    current_turn = models.ForeignKey(
        'cardtel.Player',
        related_name='pending_moves',
        null=True,
    )
    last_to_play_card = models.ForeignKey(
        'cardtel.Player',
        related_name='unanswered_moves',
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    winning_score = models.IntegerField(default=7)

    ## Related Fields
    # players - all players participating in this game
    # tables - All tables associated with a game

    @property
    def is_over(self):
        raise NotImplementedError

    @property
    def hand_is_over(self):
        raise NotImplementedError

    @property
    def point_is_over(self):
        raise NotImplementedError

    def __unicode__(self):
        return "{} players, created at {}".format(self.players.count(), self.created_at)


class Point(models.Model):

    class Meta:
        db_table = 'point'
        app_label = 'cardtel'

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    winner = models.ForeignKey(
        'cardtel.Player',
        related_name='points',
    )
    winning_cards = models.ManyToManyField(
        'cardtel.Card',
        related_name='winning_hands'
    )


class Player(models.Model):

    class Meta:
        db_table = 'player'
        app_label = 'cardtel'
        unique_together = ('game', 'user')

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    game = models.ForeignKey(
        'cardtel.Game',
        db_index=True,
        related_name='players',
    )
    user = models.ForeignKey(
        'cardtel.User',
        db_index=True,
        related_name='players'
    )
    score = models.IntegerField(default=0)
    cards = models.ManyToManyField('cardtel.Card', through='cardtel.PlayerCardLink')
    has_folded = models.BooleanField(default=False)
    play_order = models.IntegerField()

    ## Related Fields
    # points - All pointed in which this player was the winner
    # pending_moves - games where it's this player's turn
    # unanswered_moves - games where this player was the last to play

    def __unicode__(self):
        return self.user.username


class Card(models.Model):

    class Meta:
        db_table = 'card'
        app_label = 'cardtel'

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    suit = models.CharField(max_length=1)
    number = models.CharField(max_length=1)
    image = models.FileField()

    def __unicode__(self):
        return "{} of {}".format(self.number, self.suit)

class Table(models.Model):

    class Meta:
        db_table = 'table'
        app_label = 'cardtel'

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    game = models.ForeignKey(
        'cardtel.Game',
        related_name='tables'
    )

    cards = models.ManyToManyField('cardtel.Card')
    best_hand_score = models.IntegerField(null=True)

    def __unicode__(self):
        return "for game {}".format(self.game.id)

class PlayerCardLink(models.Model):

    class Meta:
        db_table = 'player_card_link'
        app_label = 'cardtel'
        unique_together = ('player', 'card')

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    player = models.ForeignKey(
        'cardtel.Player',
        db_index=True,
    )
    card = models.ForeignKey(
        'cardtel.Card',
        db_index=True,
    )

    def __unicode__(self):
        return "{}, {}".format(self.player, self.card)

class User(models.Model):

    class Meta:
        db_table = 'user'
        app_label = 'cardtel'

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    username = models.CharField(max_length=20)
    score = models.IntegerField(default=0)

    ## Related Fields
    # players - games this user is participating in

    def __unicode__(self):
        return username
