#!/usr/bin/python
# 
# En Python-versjon av The King of Tokyo.
#
# Spillet foregår på følgende måte:
#
# Første runde:
#  - Alle spillerene kaster terningene én gang hver
#  - Den spilleren med flest smash stiller seg i Tokyo og starter spillet.
#
# En vanlig runde:
#  - Spilleren kaster terningen
#  - Energi gir spilleren ekstra energi. Maks 20 energi er tillatt.
#  - Hjerter gir spilleren HP. Maks 20 HP er tillatt.
#  - Smash samles opp, og spilleren kan velge hvilken spiller som skal få damage.
#     - Hvis spilleren har et spesialkort for damage, kan han dele ut damage til alle de andre spillerne på en gang.
#  - I slutten av spillerens tur, kan han velge om han vil kjøpe et spesialkort med energien sin.
#     - Hvis spilleren vil bytte ut alle kortene, betaler han to energi, og så byttes alle spesialkortene ut.
#
# Spillet avsluttes:
#  - Når første spiller har nådd 20 poeng
#    eller
#  - Når det bare er én spiller igjen (de andre har mistet all sin HP)


import random

class Player(object):
    """
    En spiller-klasse som inneholder informasjon som er viktig for spillet:
     - Navnet på spilleren
     - Energinivået
     - HP
     - Poeng
     - "Bonus-kort"

    """

    def __init__(self, name="Spillernavn"):
        self.name = name
        self.energy = 0
        self.hp = 10
        self.points = 0
        self.cards = []

    def get_hp(self):
        return self.hp

    def get_energy(self):
        return self.energy
    
    def get_points(self):
        return self.points

class Die(object):
    """
    En terning-klasse som representerer en terning i TKoT-spillet.
    Denne klassen har også en funksjon som returnerer utfallet av et terningkast.

    """

    def __init__(self):
        self.faces = [1, 2, 3, "smash", "heart", "energy"]
    
    def throw(self):
        result = random.choice(self.faces)

        return result

class Card(object):
    """
    En klasse som representerer et kort i TKoT-spillet.
    Kortene påvirker spillet på ulike måter.

    """

    def __init__(self):
        self.name = None
        self.description = None
        self.cost = None
        self.one_time_use = False
        self.image = None
        self.gives_energy = None
        self.gives_hp = None
        self.deals_attack = None

def throw_dice(dice=[], bonus_die=None):
    result = []

    for die in dice:
        current_die_result = die.throw()
        result.append(current_die_result)

    if bonus_die:
        bonus_die_result = bonus_die.throw()
        result.append(bonus_die_result)

    return result

def main():
    # Nå må vi gjøre spillet klart.
    antall_spillere = 4

    # Opprett spiller-objektene, og lagre dem i "players"-lista
    players = []
    for counter in range(antall_spillere):
        player = Player(name = "Spiller {nummer}".format(nummer=counter+1))
        players.append(player)
    
    # Opprett seks terninger
    dice = []
    for counter in range(6):
        die = Die()
        dice.append(die)

    # Opprett en bonusterning. Denne skal brukes hvis spilleren sitter på et bonuskort som gir han en ekstra terning.
    bonus_die = Die()

    # Lag en variabel som holder styr på om spillet er ferdig eller ikke
    game_finished = False
    
    # winner-variabelen skal oppdateres med navnet til spilleren som til slutt vinner spillet.
    winner = None

    # round_counter forteller hvilken runde vi er i for øyeblikket. Denne må økes for hver runde spillet tar.
    round_counter = 1

    # Spill-loopen vår kjører helt til game_finished settes til True
    while not game_finished:
        print("Runde nummer: %s" % round_counter)

        if round_counter == 1:
            best_player = players.copy()
            best_roll = 0

            while len(best_player) != 1:
                surviving_players = []
                for player in best_player:
                    # Vent på at spilleren kaster terningene
                    input("{spillernavn}: Trykk enter for å kaste terningene!".format(spillernavn=player.name))

                    throw = throw_dice(dice)
                    print("Du kastet: ")
                    for occurence in throw:
                        print(occurence)

                    number_of_smash = throw.count("smash")

                    if number_of_smash > best_roll:
                        surviving_players = [player]
                        best_roll = number_of_smash
                    elif number_of_smash == best_roll:
                        surviving_players.append(player)
                
                best_player = surviving_players.copy()
                best_roll = 0

            print("{spillernavn} starter spillet!".format(spillernavn=best_player[0].name))

            # Omrokker på players-listen i henhold til hvem som begynner
            
        
        else:
            # En vanlig runde av spillet starter.
            print("Starter runde nummer {rundeteller}".format(rundeteller=round_counter))
        
        round_counter += 1 # Øk rundetelleren med 1.

        if round_counter == 50:
            game_finished = True # Avslutt spillet


if __name__ == '__main__':
    main()
