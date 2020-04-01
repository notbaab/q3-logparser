# holds the kill info about the given player
WORLDNAME = '<world>'
WORLDID = "1022"


class Kill():
    def __init__(self, killer, victum, kill_method, kill_method_name):
        self.killer = killer
        self.victum = victum
        self.kill_method = kill_method
        self.kill_method_name = kill_method_name


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

    def add_kill(self, other_player, method_id, method_name):
        kill = Kill(self.player, other_player, method_id, method_name)
        self.total_kills += 1
        self.score += 1
        self.__add_death_or_kill(other_player, self.kill_by_player, kill)

    def add_score(self, score):
        self.score = score

    def add_death(self, other_player, method_id, method_name):
        kill = Kill(other_player, self.player, method_id, method_name)
        self.deaths += 1
        if other_player.id == WORLDID:
            self.score -= 1
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

        stat += "Deaths\n"
        for deaths in self.death_by_player.values():
            total = len(deaths)
            killer = deaths[0].killer
            line = "{} {}\n".format(killer.name, total)
            stat += line
        return stat


class Game():
    def __init__(self, map_name):
        # hash of players that have been fully connected
        self.players = {}
        # list of players that disconnected
        self.disconnected_player_stat_table = []
        # add the world since it can kill anyone
        self.stat_table = {}
        self.done_reason = None
        self.map_name = map_name
        self.done = False
        self.add_player_connecting(Player(WORLDNAME, WORLDID, False))

    def add_player_connecting(self, player):
        # This can happen when a player disconnects and then reconnects. How
        # should we handle this?. Should we count them as new
        # players?
        self.players[player.id] = player
        self.stat_table[player.id] = StatTable(player)

    def get_leader(self):
        leader = None
        leader_score = 0
        for table in self.stat_table.values():
            if table.score > leader_score:
                leader = table.player
                leader_score = table.score
        return leader

    def add_final_score(self, player_id, score):
        self.stat_table[player_id].score = score

    def player_disconnected(self, player_id):
        # Is it the games responsibility to not do this when it's done? I'm not
        # sure
        if self.done:
            return

        t = self.stat_table[player_id]
        self.disconnected_player_stat_table.append(t)
        del self.players[player_id]
        del self.stat_table[player_id]

    def add_kill(self, killer_id, victum_id, method, method_name):
        killer = self.players[killer_id]
        victum = self.players[victum_id]
        self.stat_table[killer.id].add_kill(victum, method, method_name)
        self.stat_table[victum.id].add_death(killer, method, method_name)

    def print_summary(self):
        for table in self.stat_table.values():
            print(table.player.name + " " + str(table.score) + " kills " +
                  str(table.total_kills))

        for table in self.disconnected_player_stat_table:
            print("|X|" + table.player.name + " " + str(table.score) + " kills " +
                  str(table.total_kills))

    def __str__(self):
        out = ""
        for table in self.stat_table.values():
            out += str(table)
        return out


class Player():
    def __init__(self, name, id, is_bot):
        self.name = name
        self.id = id
        self.is_bot = is_bot
