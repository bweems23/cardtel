import random

from cardtel.models import (
    Game,
    Player,
    Table,
)


def create_game():
    """
    Make a game, and initialize the game's table
    """
    game = Game.objects.create()
    table = Table.objects.create(game=game)
    return game

def add_player_to_game(game, user):
    """
    Add a new player to a game. When the player is added, give them
    a 0-indexed play order based on the order they joined the game.
    """
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
    """
    Set current turn to the player with the lowest overall score
    """
    game.current_turn = game.players.order_by('user__score').first()
    game.save(update_fields=['current_turn'])
    return game

def increment_current_turn(game):
    """
    Each player has a play order. Increment the play order by one and then
    find the player with that ordering. If that player is folded for the
    round, then go to the next one (until you find someone who hasn't folded)
    """
    players = game.players
    num_players = players.count()
    next_play_order = (game.current_turn.play_order + 1) % num_players
    next_player = players.filter(play_order=next_play_order).first()
    while next_player.has_folded:
        next_play_order = (next_play_order + 1) % num_players
        next_player = players.filter(play_order=next_play_order).first()
    game.current_turn = next_player
    game.save(update_fields=['current_turn'])
    return game

def remove_player_from_game(game, user):
    """
    Remove player from a game
    """
    player = game.players.filter(user=user).first()
    player.delete()

def update_user_scores(game):
    """
    Get the final player rankings, then assign points accordingly
    """
    players = game.players.all()
    ranking_order = sorted(players, cmp=player_score_comparator)
    assign_final_points_to_players(ranking_order)

def player_score_comparator(player_one, player_two):
    """
    Rank players in order of score. If there is a tie, higher rank
    goes to player who won a point most recently
    return 1 means that player_two wins
    return -1 means that player_one wins
    return 0 means they tie (only happens if neither player won a point)
    """
    if player_one.score < player_two.score:
        # If player 2 has a higher score, they win
        return 1
    if player_one.score > player_two.score:
        # If player 1 has a higher score, they win
        return -1

    player_one_last_point = player_one.points.last()
    player_two_last_point = player_two.points.last()

    if not player_one_last_point and not player_two_last_point:
        # If neither player won a point all game, just choose a
        # winner randomly
        return random.choice([-1, 1])

    if not player_one_last_point:
        # If player 1 never got a point, player 2 wins
        return 1

    if not player_two_last_point:
        # If player 2 never got a point, player 1 wins
        return -1

    # If they've both scored points and are tied, then the one with the
    # most recent point wins
    if player_two_last_point.created_at > player_one_last_point.created_at:
        return 1
    else:
        return -1

def assign_final_points_to_players(ranked_players):
    """
    Given a final ranking of players, assign points to
    the associated user's overall score.

    Point rules: Zero sum game with more points assigned
    if more players.

    Example 1:
    3 player game:
    1st: 1 point
    2nd: 0 points
    3rd: -1 points

    Example 2:
    4 player game:
    1st: 2 points
    2nd: 1 point
    3rd: -1 point
    4th: -2 points
    """
    num_players = len(ranked_players)
    # This is the max number of points any player will get
    # Start here with the highest ranked player, and continue
    # to decrement the number of points as you go down the ranking
    points_awarded = num_players / 2
    # Points are a zero sum game, skip zero if there are an even number
    # of players
    skip_zero = (num_players % 2 == 0)
    for player in ranked_players:
        user = player.user
        user.score = user.score + points_awarded
        user.save(update_fields=['score'])
        points_awarded -= 1
        if skip_zero and points_awarded == 0:
            points_awarded -= 1
