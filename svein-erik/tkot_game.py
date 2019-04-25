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
#  - Energi gir spilleren ekstra energi. 
#  - Hjerter gir spilleren HP. Maks 20 HP er tillatt.
#  - Smash samles opp, og spilleren kan velge hvilken spiller som skal få damage.
#     - Hvis spilleren har et spesialkort for damage, kan han dele ut damage til alle de andre spillerne på en gang.
#  - I slutten av spillerens tur, kan han velge om han vil kjøpe et spesialkort med energien sin.
#     - Hvis spilleren vil bytte ut alle kortene, betaler han to energi, og så byttes alle spesialkortene ut.
#
# Runde sekvens hvis du er i Tokyo :
# - legg til eventuell kort effekt 
# - Få bonus poeng for at du er i Tokyo, har du stått en runde får du 2 poeng
# - Kast terning
# - velg utfall av terningene
# - Motta eller utfør utfall av terningene
# - Legg til kort effekt
# - Kjøp kort 
# - End turn
#
# Runde sekvens hvis du er utenfor Tokyo
# - legg til eventuell kort effekt
# - kast terning
# - velg utfall av terningene
# - motta eller utfør utfall av terningene
# - legg til kort effekt
# - kjøp kort 
# - hvis du gjorde skade på player i Tokyo kan player i tokyo velge om han skal ut av tokyo eller bli, velger han og forlate tokyo må du plassere deg i Tokyo
# - End turn

# Spillet avsluttes:
#  - Når første spiller har nådd 20 poeng
#    eller
#  - Når det bare er én spiller igjen (de andre har mistet all sin HP)

import os
import random
import time

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
    """
    Denne funksjonen tar imot en liste med Terning-objekter, samt en valgfri bonusterning.
    Deretter kaster den alle terningene og returnerer resultatet fra kastene i en liste.

    """

    result = []

    for die in dice:
        current_die_result = die.throw()
        result.append(current_die_result)

    if bonus_die:
        bonus_die_result = bonus_die.throw()
        result.append(bonus_die_result)

    return result

def clear():
    """
    Denne funksjonen brukes for å tømme skjermen i terminalen.

    """
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def main():
    # Nå må vi gjøre spillet klart.
    antall_spillere = 4

    # Game speed
    speed = 1

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
        clear()
        print("Runde nummer: %s" % round_counter)

        # Hvis dette er den første runden, må vi finne ut av hvilken spiller som skal få lov til å begynne.
        if round_counter == 1:
            best_player = players.copy() # best_player skal til slutt kun inneholde Player-objektet til spilleren som får flest antall smash. Denne spilleren får lov til å begynne.
            
            # Denne while-loopen kjører om igjen helt til det bare er ett spillerobjekt igjen i best_player-listen.
            while len(best_player) != 1:
                best_roll = 0 # Variabel som benyttes for å finne ut av om et kast er bedre eller dårligere enn det de andre spillerne har kastet.

                # surviving_players inneholder spillerobjektene til de tspillerne som il enhver tid har de beste kastene.
                surviving_players = []

                # Denne for-loopen kjører gjennom alle spillerobjektene som fremdeles er med i kampen om å starte spillet
                for player in best_player:
                    clear()

                    # Vent på at spilleren kaster terningene
                    input("{spillernavn}: Trykk enter for å kaste terningene!".format(spillernavn=player.name))

                    throw = throw_dice(dice) # Her bruker vi throw_dice-funksjonen vår, og lagrer resultatet fra kastet i throw-variabelen.
                    print("Du kastet: ")
                    for occurence in throw:
                        print(occurence)

                    number_of_smash = throw.count("smash") # Her teller vi opp antallet smash so ble trillet.

                    # Nå sjekker vi om spilleren har klart å trille flere smash enn de andre spillerne så langt.
                    # Hvis spilleren har trillet flest smash, erstatter vi surviving_players-listen med en ny liste som kun inneholder spilleren som har "rekorden"
                    if number_of_smash > best_roll:
                        surviving_players = [player]
                        best_roll = number_of_smash
                    # Hvis det er en annen spiller som har trillet like mange smash, legger spilleren seg selv til i listen over surviving_players.
                    # Disse må kaste på nytt hvis ikke det er annen spiller som slår begge to.
                    elif number_of_smash == best_roll:
                        surviving_players.append(player)
                    
                    time.sleep(speed)
                
                # Her oppdaterer vi best-player-listen med den eller de spillerne som overlevde kasterunden.
                # Hvis det bare blir værende igjen én spiller i best_player, vil while-loopen vår avslutte, og vi har en vinner.
                best_player = surviving_players.copy()

            clear()
            print("{spillernavn} starter spillet. Antall smash: {best_roll}".format(spillernavn=best_player[0].name, best_roll=best_roll))
            
            # Omrokker på players-listen i henhold til hvem som begynner
            players = players[players.index(best_player[0]):] + players[0:players.index(best_player[0])]
            
            # Skriv ut rekkefølgen på spillerne
            print("Spillernes rekkefølge:")

            for player in players:
                print(player.name)
            
            input("Trykk en tast for å starte spillet.")
            
        else:
            # En vanlig runde av spillet starter.
            print("Starter runde nummer {rundeteller}".format(rundeteller=round_counter))

            # Gå inn i terningkast-loopen. Denne loopen skal kjøre i maks 3 runder.
            # Spilleren skal kunne velge hvilke terningen han vil spare på.
        
        round_counter += 1 # Øk rundetelleren med 1.

        if round_counter == 4:
            game_finished = True # Avslutt spillet


if __name__ == '__main__':
    main()

