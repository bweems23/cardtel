from cardtel.models import (
    Game,
    Player,
    Table,
)


def create_game():
    game = Game.objects.create()
    table = Table.objects.create(game=game)
    return game

def add_player_to_game(game, user):
    players = game.players
    if players.count() == 0:
        return Player.objects.create(game=game, user=user, play_order=0)

    play_order = Player.objects.filter(
        game=game
    ).order_by(
        '-play_order'
    ).values_list(
        'play_order',
        flat=True
    ).first() + 1

    return Player.objects.create(game=game, user=user, play_order=play_order)

def initialize_game(game):
    # Set current turn to the player with the lowest overall score
    players = Player.objects.filter(game=game)
    game.current_turn = players.order_by('user__score').first()
    game.save(update_fields=['current_turn'])
    return game

def increment_current_turn(game):
    players = Player.objects.filter(game=game)
    new_play_order = (game.current_turn.play_order + 1) % players.count()
    game.current_turn = players.filter(play_order=new_play_order).first()
    game.save(update_fields=['current_turn'])
    return game

def remove_player_from_game(game, user):
    player = Player.objects.filter(game=game, user=user).first()
    player.delete()

def update_user_scores(game):
    raise NotImplementedError
    # players = Player.objects.filter(game=game).all()
    # winner = players.order_by('score').first()
    # for player in players:
    #     user = player.user
    #     user.score = user.score + player.score
    #     user.save(update_fields=['score'])


