from cardtel.models import (
    Game,
    Table,
)


def create_game():
    table = Table.objects.create()
    return Game.objects.create(table=table)

def add_player_to_game(game, user):
    play_order = Player.objects.filter(group=group).order_by('-play_order').first() + 1
    return Player.objects.create(game=game, user=user, play_order=play_order)

def initialize_game(game):
    # Set current turn to the player with the lowest overall score
    game.current_turn = game.players.order_by('user__score').first()
    game.save(update_fields=['current_turn'])

def increment_current_turn(game):
    players = game.players.count()
    new_play_order = (game.current_turn.play_order + 1) % num_players
    game.current_turn = game.players.filter(play_order=new_play_order).first()
    game.save(update_fields=['current_turn'])

def remove_player_from_game(game, user):
    player = Player.objects.filter(game=game, user=user).first()
    player.delete()

def update_user_scores(game):
    players = game.players.all()
    for player in players:
        user = player.user
        user.score = user.score + player.score
        user.save(update_fields=['score'])


