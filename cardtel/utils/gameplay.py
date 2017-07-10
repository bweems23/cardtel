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
    game.current_turn = game.players.order_by('score').first()
    game.save(update_fields=['current_turn'])
    return game

def increment_current_turn(game):
    players = game.players
    new_play_order = (game.current_turn.play_order + 1) % players.count()
    game.current_turn = players.filter(play_order=new_play_order).first()
    game.save(update_fields=['current_turn'])
    return game

def remove_player_from_game(game, user):
    player = game.players.filter(user=user).first()
    player.delete()

def update_user_scores(game):
    players = game.players.order_by('-score').all()
    ranking_order = get_player_rankings(players)
    assign_final_points_to_players(ranking_order)

def resolve_game_tie(players):
    """
    Given players that are tied at the end of a game,
    return them in the order that they should be ranked.
    Ranking is based on who won a point the most recently.
    """
    return sorted(players, key=lambda x: x.points.last().created_at, reverse=True)

def get_player_rankings(players):
    """
    Assumes players are passed through in order of game score (descending).
    Goes through and ranks players in order of score, resolving ties
    as necessary.
    """
    ranking_order = []
    while len(ranking_order) < len(players):
        index = len(ranking_order)
        player = players[index]
        next_player_index = index + 1
        if next_player_index > len(players) - 1:
            next_player = None
        else:
            next_player = players[next_player_index]

        tied_players = set()
        while next_player and player.score == next_player.score:
            tied_players.add(player)
            tied_players.add(next_player)
            next_player_index += 1
            if next_player_index > len(players) - 1:
                break
            player = next_player
            next_player = players[next_player_index]

        if tied_players:
            ranking_order.extend(resolve_game_tie(tied_players))
        else:
            ranking_order.append(player)

    return ranking_order

def assign_final_points_to_players(ranked_players):
    """
    Given a final ranking of players, assign points to
    the associated user's overall score.
    """
    num_players = len(ranked_players)
    points_awarded = num_players / 2
    skip_zero = (num_players % 2 == 0)
    for player in ranked_players:
        user = player.user
        user.score = user.score + points_awarded
        user.save(update_fields=['score'])
        points_awarded -= 1
        if skip_zero and points_awarded == 0:
            points_awarded -= 1
