#result = ["1", "2", "3", "smash", "hjerte", "energi"]
result = ["1", "1", "smash", "smash", "2", "energi"]
reroll = 0 # Hvor mange terninger som skal kastes om igjen.

# Teller hvor mange ganger hvert av terningsansiktene forekommer i listen.
result_count_1 = result.count("1")
result_count_2 = result.count("2")
result_count_3 = result.count("3")
result_count_smash = result.count("smash")
result_count_hjerte = result.count("hjerte")
result_count_energi = result.count("energi")

# Viser hva som er i result-listen
print("Før:")
print(result)

# Mye under her kan byttes ut med en funksjon som bytter ut hvilke lister som blir sjekket basert på hva man skriver inn.
# Hvis et av ansiktene forekommer, spør om de vil beholde terningene
if result_count_1 != 0:
    while True:
        q_1 = input("Vil du beholde alle enere? (j/n) ")
        if q_1 == "j" or "n": # Tillater bare svarene "j" eller "n".
            break
    if q_1 == "n": # Hvis svaret er "n", fjern alle forekomstene av "1" i listen result.
        while result_count_1 > 0: 
            result.remove("1")
            reroll += 1 # Legger til en terning til hvor mange terninger som skal kastes om igjen.
            result_count_1 -= 1

if result_count_2 != 0:
    while True:
        q_2 = input("Vil du beholde alle toere? (j/n) ")
        if q_2 == "j" or "n": # Tillater bare svarene "j" eller "n".
            break
    if q_2 == "n": # Hvis svaret er "n", fjern alle forekomstene av "2" i listen result.
        while result_count_2 > 0:
            result.remove("2")
            reroll += 1 # Legger til en terning til hvor mange terninger som skal kastes om igjen.
            result_count_2 -= 1

if result_count_3 != 0:
    while True:
        q_3 = input("Vil du beholde alle treere? (j/n) ")
        if q_3 == "j" or "n": # Tillater bare svarene "j" eller "n".
            break
    if q_3 == "n": # Hvis svaret er "n", fjern alle forekomstene av "3" i listen result.
        while result_count_3 > 0:
            result.remove("3")
            reroll += 1 # Legger til en terning til hvor mange terninger som skal kastes om igjen.
            result_count_3 -= 1

if result_count_smash != 0:
    while True:
        q_s = input("Vil du beholde alle smash-ene? (j/n) ")
        if q_s == "j" or "n": # Tillater bare svarene "j" eller "n".
            break
    if q_s == "n": # Hvis svaret er "n", fjern alle forekomstene av "smash" i listen result.
        while result_count_smash > 0:
            result.remove("smash")
            reroll += 1 # Legger til en terning til hvor mange terninger som skal kastes om igjen.
            result_count_smash -= 1

if result_count_hjerte != 0:
    while True:
        q_h = input("Vil du beholde alle hjertene? (j/n) ")
        if q_h == "j" or "n": # Tillater bare svarene "j" eller "n".
            break
    if q_h == "n": # Hvis svaret er "n", fjern alle forekomstene av "hjerte" i listen result.
        while result_count_hjerte > 0:
            result.remove("hjerte")
            reroll += 1 # Legger til en terning til hvor mange terninger som skal kastes om igjen.
            result_count_hjerte -= 1

if result_count_energi != 0:
    while True:
        q_e = input("Vil du beholde alle energiene? (j/n) ")
        if q_e == "j" or "n": # Tillater bare svarene "j" eller "n".
            break
    if q_e == "n": # Hvis svaret er "n", fjern alle forekomstene av "energi" i listen result.
        while result_count_energi > 0:
            result.remove("energi")
            reroll += 1 # Legger til en terning til hvor mange terninger som skal kastes om igjen.
            result_count_energi -= 1

# Sier hvor mange terninger som har blitt valgt bort og skal kastes igjen.
print(str(reroll) + " terninger kastes om igjen.")
print(result)