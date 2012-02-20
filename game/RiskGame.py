'''
Created on 2011-12-28

@author: Jerry
'''
import random
import pickle

class Map:
    def __init__(self, c_map, b_map):
        self.c_map = c_map #maps territories to connected territories
        self.b_map = b_map #maps bonus names to bonus sets
        
    def get_territories(self):
        return self.c_map.keys()

    def get_bonuses(self):
        return self.b_map.keys()
    
class Game:
    def __init__(self, map, players, p_map=None, t_map=None):
        self.map = map 
        self.turn = 0
        self.players = players
        if not p_map or not t_map:
            self.p_map = {} #maps players to territories owned
            self.t_map = {} #maps territories to number of armies present on them
            self.randomize_map(players, 3)
        else:
            self.p_map = p_map
            self.t_map = t_map
        
    def randomize_map(self, players, troops_per_territory):
        new_p_map = {}
        new_t_map = {}
        territories = self.map.get_territories()
        players2 = min(len(territories)/len(players),max ) * players
        for t in territories:
            new_t_map.update({t: troops_per_territory})
            if players2:                
                choice = random.choice(players2)
                players2.remove(choice)
                if choice in new_p_map.keys():
                    new_p_map[choice].append(t)
                else:
                    new_p_map.update({choice: [t]})
            else:
                if "N" in new_t_map.keys():
                    new_p_map["N"].append(t)
                else:
                    new_p_map.update({"N": [t]})
        self.p_map = new_p_map
        self.t_map = new_t_map
        
    def get_dice_roll(self, min, max):
        return random.choice(range(min,max+1))
    
    def get_bonus_for_player(self, player):
        player_territories = self.p_map
        sum = 0
        bonuses = self.map.b_map
        for (bset, value) in bonuses.values():
            if bset <= set(player_territories[player]):
                sum += value
        return sum
    
    def get_territories_for_player(self, player):
        return self.p_map[player]
    
    def get_reinforcements_for_player(self, player):
        reinforcements = max(len(c.get_territories_for_player(player)) / 3 
                             , 3) + c.get_bonus_for_player(player)
        return reinforcements
    def get_attackables_for_player_at_location(self, player, location):
        attackable = []
        if self.t_map[location] > 1:
            connected = set(self.map.c_map[location])
            owned = set(self.p_map[player]) 
            attackable = list(connected - owned)
        return attackable 
         
    def add_reinforcements_at_location(self, location, num_reinforcements):
        self.t_map[location] += num_reinforcements
    
    def get_fortifiables_for_player_at_location(self,player, location):
        fortifiable = []
        if self.t_map[location] > 1:
            connected = set(self.map.c_map[location])
            owned = set(self.p_map[player])
            fortifiable = list(connected & owned)
        return fortifiable
    
    def do_attack_from_location_to_location(self, attacker, defender):
        
        attacker_num = self.t_map[attacker] - 1
        assert(attacker_num > 0)
        defender_num = self.t_map[defender]
        attacker_dice = []
        defender_dice = []
        
        num_attacker_dice = min(3, attacker_num)
        for x in range(num_attacker_dice):
            attacker_dice.append(self.get_dice_roll(1,6))
            
        num_defender_dice = min(2, defender_num)
        for x in range(num_defender_dice):
            defender_dice.append(self.get_dice_roll(1,6))
        
        attacker_dice.sort(reverse = True)
        defender_dice.sort(reverse = True)
        print attacker_dice, defender_dice
        for x in range(min(num_attacker_dice, num_defender_dice)):
            if attacker_dice[x] > defender_dice[x]:
                self.t_map[defender] -= 1
            else:
                self.t_map[attacker] -= 1
                
        if self.t_map[defender] == 0:
            self.t_map[attacker] -= 1
            self.t_map[defender] = 1
            for player in self.p_map:
                if attacker in self.p_map[player]:
                    self.p_map[player].append(defender)
                elif defender in self.p_map[player]:
                    self.p_map[player].remove(defender)
            return True
        return False
    def do_move_armies_from_location_to_location(self, source, destination, num):
        assert(num < self.t_map[source])
        self.t_map[source] -= num
        self.t_map[destination] += num

    def get_t_as_pickle(self):
        return pickle.dumps(self.t_map)
    
    def get_p_as_pickle(self):
        return pickle.dumps(self.p_map)
    
    def increment_turn(self):
        self.turn = (self.turn + 1) % len(self.p_map)
        
    def get_owner_for_location(self, location):
        for p in self.p_map:
            if location in self.p_map[p]:
                return p
        
        
if __name__ == "__main__":
    
    c_map = {"A": ("B", "D"), "B":("A", "C", "D"), "C":("B", "D", "F"), "D":("A","B","C" , "E"), "E":("D"), "F":("C")}
    b_map2 = {"Province of A": (set("A"), 2), "Province of B": (set("B"), 2)}
    players = ["p1", "p2", "p3"]
    b = Map(c_map, b_map2)
    c = Game(b, players)
    print c.get_bonus_for_player('p1')
    #c.t_map = {'A': 3, 'C': 3, 'B': 3, 'E': 3, 'D': 1, 'F': 3}
    #c.p_map = {'p2': ['C', 'F'], 'p3': ['A', 'B'], 'p1': ['E', 'D']}
    print c.p_map
    import os
    clear = lambda: os.system('cls')

    while 1:
        
        player = c.players[c.turn]
        territories = c.get_territories_for_player(player)
        if territories:
            print "Player " + player + ":"
            print "Territories:"
            bonus = c.get_bonus_for_player(player)
            reinforcements = c.get_reinforcements_for_player(player)
            #Reinforcements
            #---------------------------------------------------
            
            for x in range(len(territories)):
                troops = c.t_map[territories[x]]
                print str(x + 1) + ".  " + territories[x] + " with " + str(troops) + " armies."
            while reinforcements > 0:
                print "Reinforce"
                print str(reinforcements) + " armies available"
                print "Choose territory(#) to reinforce:"
                t = int(raw_input())
                print "Number of armies to add:"
                n = int(raw_input())
                reinforcements -= n
                clear()
                c.add_reinforcements_at_location(territories[t-1], n)
                for x in range(len(territories)):
                    troops = c.t_map[territories[x]]
                    print str(x + 1) + ".  " + territories[x] + " with " + str(troops) + " armies."
            #Attacks 
            #--------------------------------------------------
            while t != "e":
                print "Attack"
                clear()
                print "Game State:"
                print "Territory | Number of Armies | Controlled by"
                i = 1
                for j in c.t_map:
                    
                    print str(i) + ".", j, "     ", c.t_map[j],"                   ", c.get_owner_for_location(j)
                    i+=1    
                print "Choose Territory to attack from(enter e to end attacks):"
                for x in range(len(territories)):
                        troops = c.t_map[territories[x]]
                        print str(x + 1) + ".  " + territories[x] + " with " + str(troops) + " armies."
                t = raw_input()
                
                if t != 'e':
                    t = int(t)
                    print "Choose Territory to attack:"
                    enemies = c.get_attackables_for_player_at_location(player, territories[t-1])
                    for x in range(len(enemies)):
                            troops = c.t_map[enemies[x]]
                            print str(x + 1) + ".  " + enemies[x] + " with " + str(troops) + " armies."
                    n = int(raw_input())
                    print territories, t-1, enemies, n-1
                    if c.do_attack_from_location_to_location(territories[t-1], enemies[n-1]):
                        print enemies[n-1] + " captured"
                        print c.t_map
                        print "Choose number of troops to advance to "  + enemies[n-1] + " (0-" + str(c.t_map[territories[t-1]] - 1) + ")"
                        o = int(raw_input())
                        c.do_move_armies_from_location_to_location(territories[t-1], enemies[n-1], o)
            #Fortifcations
            #--------------------------------------------------
            clear()
            source = ''
            
            while source != 'e':
                print "Fortify"
                territories = c.get_territories_for_player(player)
                for x in range(len(territories)):
                    troops = c.t_map[territories[x]]
                    print str(x + 1) + ".  " + territories[x] + " with " + str(troops) + " armies."
                print "Choose territory to move armies from:"
                source = raw_input()
                if source != 'e':
                    source = int(raw_input()) - 1
                    fortifiables = c.get_fortifiables_for_player_at_location(player, territories[source])
                    print "Choose territory to move armies to:"
                    dest = int(raw_input() - 1)
                    c.do_move_armies_from_location_to_location(territories[source], territories[dest])
        c.increment_turn()
                
#if __name__ == "__main__":
#    
#    c_map = {"A": ("B", "D"), "B":("A, C, D"), "C":("D, F"), "D":("A","B","C, E"), "E":("D"), "F":("C")}
#    b_map2 = {"Province of A": (set("A"), 2), "Province of B": (set("B"), 2)}
#    players = ["p1", "p2", "p3"]
#    b = Map(c_map, b_map2)
#    c = Game(b, players)
#    c.t_map = {'A': 3, 'C': 3, 'B': 3, 'E': 3, 'D': 1, 'F': 3}
#    c.p_map = {'p2': ['C', 'F'], 'p3': ['A', 'B'], 'p1': ['E', 'D']}
#    print c.get_territories_for_player("p1")
#    print c.get_territories_for_player("p2")
#    print c.get_territories_for_player("p3")
#    print c.get_fortifiables_for_player_at_location("p3", "A")
#    print c.get_attackables_for_player_at_location("p3", "A")
#    c.do_attack_from_location_to_location("A", "D")
#    print c.t_map
#    print c.p_map
#    print c.get_p_as_pickle()
#    print c.get_t_as_pickle()
#    x = c.get_p_as_pickle()
#    y = pickle.loads(x)
#    print y
#    print len(x)
#    x = raw_input()