#!/urs/bin/python3
# oppgave en (classes)


class kjoretoy:
    navn = ""
    variant = "bil"
    farge = ""
    verdi = 100.000

    def besrkivelse(self):
        beskrivelse_str = " %s er en %s %s verdt kr %.2f." % (self.navn, self.farge, self.variant, self.verdi)
        print (beskrivelse_str)

bil1 = kjoretoy()
bil1.farge = "rød"
bil1.variant = "cab"
bil1.navn = "bil nummer 1"
bil1.verdi = 800000.00

bil2 = kjoretoy()
bil2.farge = "blå"
bil2.variant = "van"
bil2.navn = "bil nummer 2"
bil2.verdi = 300000.00


(bil1.besrkivelse())
(bil2.besrkivelse())


