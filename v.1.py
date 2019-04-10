#!/usr/bin/python3

import random

class Player(object):
	
    def __init__(self, name="spillernavn"):
        self.name = name
        self.energy = 0
        self.hp = 10
        self.points = 0
        self.card = []

    def get_hp(self):
        return self.hp
    def get_energy(self):
        return self.energy
    def get_points(self):
        return self.points

player_one = Player()

print (player_one.get_hp)


class Card(object):

    def __init__(self):
        self.name = None
        self.description = None
        self.cost = None
        self.one_time_use = False
        self.image = None



cards = []
Nuclearpowerplant = Card()
Nuclearpowerplant.name = "Nuclearpowerplant"
Nuclearpowerplant.description = " +2 points +3 heart "
Nuclearpowerplant.cost = 6
Nuclearpowerplant.one_time_use = True
Nuclearpowerplant.image = None

Energydrink = Card()
# Energydrink = 

players = []
for counter in range(4):
    player = Player()
    players.append(player)


class Die(object):
    def __init__(self):
        self.faces = [1, 2, 3, "smash", "heart", "energy"]

    def throw(self):
        random.choice(self, faces)
        return result

# opprett 6 terninger
dice = []
for counter in range(6):
    die = Die()
    dice.append(die)

# for player in players: 