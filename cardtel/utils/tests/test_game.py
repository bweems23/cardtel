from django.test import TestCase

from cardtel.models import (
    Game,
    Player,
    User,
)
from cardtel.utils.gameplay import (
    add_player_to_game,
    create_game,
    initialize_game,
    increment_current_turn,
    update_user_scores,
    remove_player_from_game,
)

class TestGame(TestCase):
    def setUp(self):
        self.game = create_game()
        self.user = User.objects.create(username='rmarincola')

    def test_create_game(self):
        game = create_game()
        assert game.tables.count() == 1

    def test_add_player_to_game(self):
        game = self.game
        user = self.user
        player = add_player_to_game(game, user)
        game = Game.objects.get(id=game.id)
        assert game.players.count() == 1
        assert player.play_order == 0

        other_user = User.objects.create(username='bweems')
        player = add_player_to_game(game, other_user)
        game = Game.objects.get(id=game.id)
        assert game.players.count() == 2
        assert player.play_order == 1

    def test_initialize_game(self):
        game = self.game
        user = self.user
        player = add_player_to_game(game, user)
        game = initialize_game(game)
        assert game.current_turn == player

        other_user = User.objects.create(username='bweems')
        other_user.score = 20
        other_user.save()
        other_player = add_player_to_game(game, other_user)
        game = initialize_game(game)
        assert game.current_turn == player        

    def test_increment_current_turn(self):
        game = self.game
        user = self.user
        player = add_player_to_game(game, user)
        other_user = User.objects.create(username='bweems')
        other_player = add_player_to_game(game, other_user)
        game = initialize_game(game)
        game = increment_current_turn(game)
        assert game.current_turn == other_player
        assert other_player.play_order == 1

    def test_update_user_scores(self):
        game = self.game
        user = self.user
        player = add_player_to_game(game, user)
        other_user = User.objects.create(username='bweems')
        other_player = add_player_to_game(game, other_user)
        player.score = 5
        player.save()
        other_player.score = 7
        other_player.save()

        game = update_user_scores(game)
        player = Player.objects.get(id=player.id)
        assert player.score == 5
        other_player = Player.objects.get(id=other_player.id)
        assert other_player.score == 7

    def test_remove_player_from_game(self):
        game = self.game
        user = self.user
        player = add_player_to_game(game, user)
        remove_player_from_game(game, user)
        game = Game.objects.get(id=game.id)
        assert game.players.count() == 0

