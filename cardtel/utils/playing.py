def play_card(player, card):
    raise NotImplementedError

def fold(player):
    raise NotImplementedError

def check_valid_play(player, card):
    raise NotImplementedError

def update_best_hand(table):
    # This will be stored on the Table
    raise NotImplementedError

def finish_game(game):
    raise NotImplementedError

def finish_hand(game):
    raise NotImplementedError

def finish_point(game):
    # We'll want to call clear_table here
    raise NotImplementedError

def clear_table(table):
    raise NotImplementedError
