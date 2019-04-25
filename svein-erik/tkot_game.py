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
# - Hvis det er runde en skal første spiller bevege seg inn til Tokyo 
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
    return False
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def main():
    # Nå må vi gjøre spillet klart.
    antall_spillere = 4

    # Game speed
    speed = 0.01

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
    player_in_tokyo = None

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

            #husk og sette tilbake clear()
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
            for player in players:
                if player_in_tokyo == player:
                    input(player.name + ": Du får 2 poeng fordi du er i Tokyo.")
                    player.points += 2
                
                if player.points >= 20:
                    winner = player
                    game_finished = True
                    input(player.name + " vant! Antall poeng: " + str(player.points))
                    break

                throw_count = 0
                keep = []
                current_dice = dice.copy()
                while throw_count < 3 and len(current_dice) > 0:
                    input(player.name + ": Trykk en tast for å kaste terningene.")
                    throw = throw_dice(current_dice)
                    die_counter = 1

                    print("Du kastet: ")
                    for occurence in throw:
                        print("Terning " + str(die_counter) + ": " + str(occurence))
                        die_counter += 1
                
                    throw_count += 1

                    if throw_count == 3:
                        keep += throw
                    else:
                        choice_input = input(player.name + ": Hvilke terninger vil du beholde? Separer tallene med komma.")
                        if len(choice_input) > 0:
                            choices = choice_input.split(",")
                            for choice in choices:
                                keep.append(throw[int(choice)-1])
                        
                            # Fjern terninger fra de resterende terningene
                            current_dice = current_dice[len(choices):]
                
                print("Du har valgt å spare på følgende terninger:")
                for choice in keep:
                    print(choice)
                
                # Tell opp resultatet fra terningkastene:
                number_of_smashes = keep.count("smash")
                number_of_energy = keep.count("energy")
                number_of_hearts = keep.count("heart")
                number_of_one = keep.count(1)
                number_of_two = keep.count(2)
                number_of_three = keep.count(3)

                if player_in_tokyo == player:
                    input(player.name + ": Du står i Tokyo, og hjertene dine ble gjort om til energi. +" + str(number_of_hearts) + " energi")
                    player.energy += number_of_hearts
                else:
                    input(player.name + ": +" + str(number_of_hearts) + " hp")
                    player.hp += number_of_hearts
                    if player.hp > 10:
                        input("Du har maks hp.")
                        player.hp = 10

                input(player.name + ": +" + str(number_of_energy) + " energi")
                player.energy += number_of_energy

                points = 0
                if number_of_one >= 3:
                    points = 1 + (number_of_one - 3)
                
                elif number_of_two >= 3:
                    points = 2 + (number_of_two - 3)
                
                elif number_of_three >= 3:
                    points = 3 + (number_of_three - 3)
                
                if points > 0:
                    input(player.name + ": +" + str(points) + " poeng")
                    player.points += points
                
                if player_in_tokyo == player:
                    print("Du står i Tokyo, og skal derfor gi damage til alle de andre spillerne!")
                    for entry in players:
                        if entry != player:
                            entry.hp -= number_of_smashes
                            input(entry.name + ": " + str(number_of_smashes) + " damage. HP: " + str(entry.hp))
                            if entry.hp <= 0:
                                input(entry.name + ": Du er død, og er ikke med i spillet lengre.")
                                players.remove(entry)

                else:
                    try:
                        player_in_tokyo.hp -= number_of_smashes
                        input(player_in_tokyo.name + ": " + str(number_of_smashes) + " damage. HP: " + str(player_in_tokyo.hp))

                        # Sjekk om spilleren i Tokyo ble slått ut
                        if player_in_tokyo.hp <= 0:
                            input(player_in_tokyo.name + ": Du er nå død, og blir fjernet fra spillet.")
                            players.remove(player_in_tokyo)
                            player_in_tokyo = None
                        
                        elif number_of_smashes > 0:
                            svar = input(player_in_tokyo.name + ": Du står i Tokyo. Vil du gå ut? Svar J for å gå ut")
                            if svar == "J":
                                player_in_tokyo = None

                    except AttributeError:
                        pass

                if not player_in_tokyo:
                    input("Det er ingen spillere i Tokyo lengre, så da må du inn dit, " + player.name + "!")
                    player_in_tokyo = player
                    player.points += 1

                if player.points >= 20:
                    input(player.name + " har nådd 20 poeng. Grattis!")
                    winner = player
                    game_finished = True
                    break
                
                if len(players) == 1:
                    input(players[0].name + " er den eneste gjenværende spilleren! Grattis!")
                    winner = players[0]
                    game_finished = True
                    break

                input("Trykk en tast for å fortsette...")

            # Gå inn i terningkast-loopen. Denne loopen skal kjøre i maks 3 runder.
            # Spilleren skal kunne velge hvilke terningen han vil spare på.
        
        round_counter += 1 # Øk rundetelleren med 1.

if __name__ == '__main__':
    main()

