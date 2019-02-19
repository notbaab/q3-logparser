# holds the kill info about the given player
WORLDID = '<world>'


class Kill():
    def __init__(self, killer, victum, kill_method):
        self.killer = killer
        self.victum = victum
        self.kill_method = kill_method


class StatTable():
    def __init__(self, player):
        self.player = player
        self.total_kills = 0
        # kills minus death by world
        self.score = 0
        self.deaths = 0
        # useful to maintain both tables even though one can derive the other
        self.kill_by_player = {}
        self.death_by_player = {}

    def __add_death_or_kill(self, other_player, table, kill):
        if other_player.id not in table:
            table[other_player.id] = []
        table[other_player.id].append(kill)

    def add_kill(self, other_player, method):
        kill = Kill(self.player, other_player, method)
        self.total_kills += 1
        self.score += 1
        self.__add_death_or_kill(other_player, self.kill_by_player, kill)

    def add_death(self, other_player, method):
        kill = Kill(other_player, self.player, method)
        self.deaths += 1
        if other_player.id == WORLDID:
            self.score -= 1
        self.__add_death_or_kill(other_player, self.death_by_player, kill)

    def add_world_death(self, other_player, method):
        kill = Kill(other_player, self.player, method)
        self.deaths += 1
        self.__add_death_or_kill(other_player, self.death_by_player, kill)

    def __str__(self):
        stat = "{} total Kills {} Score {}\n".format(self.player.name,
                                                     self.total_kills,
                                                     self.score)
        # only iterate over kills
        for kills in self.kill_by_player.values():
            total = len(kills)
            victum = kills[0].victum
            line = "{} {}\n".format(victum.name, total)
            stat += line
        return stat


class Game():
    def __init__(self, map_name):
        self.players = {}
        # add the world since it can kill anyone
        self.stat_table = {}
        self.map_name = map_name
        self.add_player(Player(WORLDID, False))

    def add_player(self, player):
        self.players[player.id] = player
        self.stat_table[player.id] = StatTable(player)

    def add_kill(self, killer_id, victum_id, method):
        killer = self.players[killer_id]
        victum = self.players[victum_id]
        self.stat_table[killer.id].add_kill(victum, method)
        self.stat_table[victum.id].add_death(killer, method)

    def print_summary(self):
        for table in self.stat_table.values():
            print(table.player.name + " " + str(table.score))
        print()

    def __str__(self):
        out = ""
        for table in self.stat_table.values():
            out += str(table)
        return out


class Player():
    def __init__(self, name, is_bot):
        self.name = name
        self.id = name
        self.is_bot = is_bot
