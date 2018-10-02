import deuces
import gameplay
from django.db import transaction

def play_cards(player, cards):
    '''|player| attempts to play |cards| on the table.'''
    if check_valid_play(player, cards):
        for card in cards:
            play_card(player, card)
    else:
        raise IllegalPlay

@transaction.atomic
def play_card(player, card):
    '''|player| plays |card| on the table.'''
    player.cards.remove(card)
    player.game.table.add(card)

def fold(player):
    '''|player| folds, giving up his ability to play again this point.'''
    player.has_folded = True
    player.save()

def check_valid_play(player, new_cards):
    '''Check if |new_cards| makes the table better during |player|'s turn.'''
    table_deuces_cards = get_deuces_cards(player.game.table.cards.all())
    new_deuces_cards = get_deuces_cards(new_cards)
    all_cards = new_deuces_cards + table_deuces_cards
    current_score = player.game.table.best_hand_score
    updated_score = evaluate_cards(all_cards)

    # Check that every card makes the hand better
    for index in xrange(len(new_deuces_cards)):
        tmp_cards = all_cards[:index] + all_cards[index+1:]
        tmp_score = evaluate_cards(tmp_cards)
        if tmp_score <= updated_score:
            return False

    # Check that the score has been improved
    if updated_score < current_score:
        table.best_hand_score = updated_score
        table.save()
        return True
    else:
        return False

def finish_hand(game):
    '''End a hand in the |game|.'''
    raise NotImplementedError

def finish_point(game):
    '''Finish a point in the |game|'''
    winner = game.last_to_play_card
    winner.score = winner.score + 1
    if game.is_over():
        gameplay.finish_game(game)
    elif game.hand_is_over():
        finish_hand(game)
    game.players.update(has_folded=False)
    winner.save()

def evaluate_cards(cards):
    '''Evaluate the score of a hand of |cards|'''

    raise NotImplementedError

def get_deuces_cards(cards):
    '''Convert |cards| into deuces format'''
    return [deuces.Card.new(card.number + card.suit)
            for card in player.game.table.cards.all()]

class IllegalPlay(Exception):
    '''Raise when a user attempts a play that is not legal.'''
