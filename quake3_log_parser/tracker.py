"""
Works with the lineparsers and the game object class to keep track of stats in
the game object. Every function has the same signature, it just needs the a
game object and the line that maps to the corresponding parser function
"""
from .lineparsers import (parse_player_added, parse_final_score,
                          parse_game_done, parse_player_disconnected,
                          parse_kill, parse_item, LineType)


def track_player_added(game, line):
    player = parse_player_added(line)
    game.add_player_connecting(player)


def track_final_score(game, line):
    player_id, score = parse_final_score(line)
    game.add_final_score(player_id, score)


def track_game_done(game, line):
    reason = parse_game_done(line)
    game.done = True
    game.done_reason = reason


def track_player_disconnected(game, line):
    if game.done:
        # Game finished, don't say the player disconnected
        return
    player_id = parse_player_disconnected(line)
    game.player_disconnected(player_id)


def track_kill(game, line):
    killer, victum, method, method_name = parse_kill(line)
    game.add_kill(killer, victum, method, method_name)


def track_item(game, line):
    parse_item(line)


track_functions = {
    LineType.PLAYER_INFO: track_player_added,
    LineType.SCORE: track_final_score,
    LineType.GAME_DONE: track_game_done,
    LineType.PLAYER_DISCONNECTED: track_player_disconnected,
    LineType.KILL: track_kill,
    LineType.ITEM: track_item,
}
# TODO: Have some subscriber function that allows people to subscribe to
# different messages so we can avoid parsing a line twice
