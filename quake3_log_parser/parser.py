import argparse
import sys
from .lineparsers import *
from .tracker import track_functions
from .datastructures import *


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
        elif linetype == LineType.GAME_SHUTDOWN:
            current_game = None
        else:
            track_functions[linetype](current_game, line)

    for game in games:
        print("=" * 80)
        game.print_summary()

    return games


def parse_str(game_str):
    lines = game_str.split("\n")

    return parse_lines(lines)


def parse_log_file(file):
    with open(file, 'r') as f:
        contents = f.read()
        lines = contents.split("\n")

    return parse_lines(lines)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("log_source", metavar="log-file", default=sys.stdin,
                   nargs="?", type=argparse.FileType("r"),
                   help="Log file to parse")
    args = p.parse_args()
    parse_lines(args.log_source)


if __name__ == '__main__':
    main()
