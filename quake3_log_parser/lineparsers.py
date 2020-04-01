import re
from .datastructures import Player
from enum import Enum

kill_regex = re.compile(r":(.+): (.+) killed (.+) by (\w+)")


class LineType(Enum):
    INIT_GAME = "InitGame:"
    PLAYER_INFO = "ClientUserinfoChanged:"
    # PLAYER_CONNECTED = "ClientBegin:"
    PLAYER_DISCONNECTED = "ClientDisconnect:"
    KILL = "Kill:"
    SCORE = "score:"
    ITEM = "Item:"
    GAME_DONE = "Exit:"
    GAME_SHUTDOWN = "ShutdownGame:"


def get_line_type(line):
    for linetype in LineType:
        if line.startswith(linetype.value):
            return linetype
    # print("nothing found for ", line, end="")
    return None


def parse_start_game(line):
    split_lines = line.split("\\")[1:]
    return dict(zip(split_lines[::2], split_lines[1::2]))


def parse_player_added(line):
    split_lines = line.split(" ")
    # is bot check. Add to the game but mark as bot
    is_bot = "skill" in line
    player_id = split_lines[1]
    player_name = split_lines[2].split("\\")[1]
    player = Player(player_name, player_id, is_bot)
    return player


def parse_player_disconnected(line):
    # returns the player id that is disconnecting
    player_id = line.split(":")[1].strip()
    return player_id


def parse_game_done(line):
    # game is done, get the reason for the end
    reason = line.split(":")[1].strip()
    return reason


def parse_final_score(line):
    parts = line.split(" ")
    score = int(parts[1])
    player_id = parts[7]
    return player_id, score


def parse_kill(line):
    # this one works when the players id doesn't change. unfortunately that
    # isn't a guarantee. Use with the track functions and the game
    # object to correlate with whoever the current holder of that
    # id is
    _, data, human_readable = line.split(":")
    killer, victum, method = data.strip().split()
    method_name = human_readable.split("by")[1].strip()
    return killer, victum, method, method_name


def parse_item(line):
    player_id, item = line.split(":")[1].strip().split()
