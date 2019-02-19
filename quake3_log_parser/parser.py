import argparse
import sys
from .lineparsers import *
from .datastructures import *
from enum import Enum
from pprint import pprint


class LineType(Enum):
    INIT_GAME = "InitGame:"
    PLAYER_INFO = "ClientUserinfoChanged:"
    KILL = "Kill:"
    ITEM = "Item:"
    GAME_DONE = "ShutdownGame:"


# generic parsing functions that take a line and the current game being played
parse_functions = {
    LineType.PLAYER_INFO: parse_player_added,
    LineType.KILL: parse_kill,
    LineType.ITEM: parse_item,
}


def get_line_type(line):
    for linetype in LineType:
        if line.startswith(linetype.value):
            return linetype

    return None


def parse_lines(log_input):
    games = []
    current_game = None

    for line in log_input:
        linetype = get_line_type(line)
        if linetype is None:
            continue

        if linetype == LineType.INIT_GAME:
            game_data = parse_start_game(line)
            current_game = Game(game_data["mapname"])
            games.append(current_game)
        # I'm not sure if we need to detect a game is done
        elif linetype == LineType.GAME_DONE:
            current_game = None
        else:
            parse_functions[linetype](current_game, line)

    for game in games:
        game.print_summary()


def parse_log_file(file):
    with open(file, 'r') as f:
        contents = f.read()
        lines = contents.split("\n")

    parse_lines(lines)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("log_source", metavar="log-file", default=sys.stdin,
                   nargs="?", type=argparse.FileType("r"),
                   help="Log file to parse")
    args = p.parse_args()
    parse_lines(args.log_source)


if __name__ == '__main__':
    main()
