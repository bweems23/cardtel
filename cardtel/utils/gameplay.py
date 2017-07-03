from cardtel.models import (
    Game,
    Table,
)


def create_game():
    table = Table.objects.create()
    return Game.objects.create(table=table)

def add_player_to_game(game, user):
    # TODO set play_order default
    return Player.objects.create(game=game, user=user)

def initialize_game(game):
    players = game.players
    player_with_lowest_score = players.first()
    for player in players:
        if player.user.score < player_with_lowest_score.user.score:
            player_with_lowest_score = player

    game.current_turn = player_with_lowest_score
    game.save()

def remove_player_from_game(game, user):
    player = Player.objects.filter(game=game, user=user).first()
    player.delete()

def update_user_scores(game):
    raise NotImplementedError
