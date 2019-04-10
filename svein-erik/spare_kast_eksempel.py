ekskast = [1, 2, 3, "smash", "heart", "energy"]

terningcounter = 1
for kast in ekskast:
    print("Terning {teller}: {kast}".format(teller=terningcounter, kast=kast))
    terningcounter += 1

svar = input("Hvilke terninger vil du spare på? 1-6, separert med komma")

spareliste = svar.split(",")

sparte_terninger = []
for entry in spareliste:
    terning = ekskast.pop(int(entry))
    sparte_terninger.append(terning)

print("Sparte terninger:")
print(sparte_terninger)
print()
print("Reseterende terninger:")
print(ekskast)