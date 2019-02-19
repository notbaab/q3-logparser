from .datastructures import *
import re

kill_regex = re.compile(r":(.+): (.+) killed (.+) by (\w+)")


def parse_start_game(line):
    split_lines = line.split("\\")[1:]
    return dict(zip(split_lines[::2], split_lines[1::2]))


def parse_end_game(game, line):
    return game


def parse_player_added(game, line):
    split_lines = line.split(" ")
    # is bot check. Add to the game but mark as bot
    is_bot = "skill" in line
    # skip bots for now

    player_name = split_lines[2].split("\\")[1]
    # player_id = split_lines[1]
    player = Player(player_name, is_bot)

    game.add_player(player)


def parse_kill(game, line):
    # this one works when the players id doesn't change. unfortunately that
    # isn't a guarantee.
    # killer, killee, method = line.split(":")[1].strip().split()
    _, killer, victum, method = kill_regex.search(line).groups(1)
    game.add_kill(killer, victum, method)


def parse_item(game, line):
    return game