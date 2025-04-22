import datetime

class Logger:
    def __init__(self, spravce_hry, poznamka=None):
        self.spravce_hry = spravce_hry
        self.poznamka = poznamka
        self.cas_startu = datetime.datetime.now()
        self.log_prubehu = []
        self.vysledek = None

    def log_kola(self):
        log_kolo = {'kolo': self.spravce_hry.kolo}

        for hrac in self.spravce_hry.hraci:
            jednotky = {}
            budovy = {}
            for jednotka in self.spravce_hry.jednotky.values():
                if jednotka.vlastnik == hrac:
                    jednotky[jednotka.typ] = jednotky.get(jednotka.typ, 0) + 1
            # NEXT: Bude portřeba upravit, teď jsou budovy uložené jen v seznamu, v plné verzi budou mít pozice, takže budou ve slovníku
            for budova in self.spravce_hry.budovy:
                if budova.vlastnik == hrac:
                    budovy[budova.typ] = budovy.get(budova.typ, 0) + 1
            log_kolo[hrac.jmeno] = {
                'jednotky': jednotky,
                'budovy': budovy,
                'suroviny': hrac.suroviny.copy()
            }

        self.log_prubehu.append(log_kolo)

    def uloz_vysledek(self, vysledek):
        self.vysledek = vysledek

    def vypis_vysledky(self):
        print("=== Výsledky simulace ===")
        print(f"Začátek simulace: {self.cas_startu.strftime('%Y-%m-%d %H:%M:%S')}")
        if self.poznamka:
            print(f"Poznámka: {self.poznamka}")
        print(f"Počet kol: {len(self.log_prubehu)}")
        print(f"Konečný výsledek: {self.vysledek if self.vysledek else 'Neukončeno'}")
        print("=========================")

    def reset(self, nova_poznamka=None):
        self.poznamka = nova_poznamka
        self.cas_startu = datetime.datetime.now()
        self.log_prubehu = []
        self.vysledek = None

    def vypis_zaznam(self, zaznam):
        print(f"\n=== Kolo {zaznam['kolo']} ===")
        for hrac in [k for k in zaznam.keys() if k != 'kolo']:
            print(f"\nHráč: {hrac}")
            celkem_jednotek = sum(zaznam[hrac]['jednotky'].values())
            print(f" Jednotky: (celkem {celkem_jednotek})")
            for typ, pocet in zaznam[hrac]['jednotky'].items():
                print(f"  - {typ}: {pocet}")
            print(" Budovy:")
            for typ, pocet in zaznam[hrac]['budovy'].items():
                print(f"  - {typ}: {pocet}")
            print(" Suroviny:")
            for surovina, hodnota in zaznam[hrac]['suroviny'].items():
                print(f"  - {surovina}: {hodnota}")

    def vypis_prubeh(self):
        print("\n=== Průběh simulace ===")
        for zaznam in self.log_prubehu:
            self.vypis_zaznam(zaznam)
        print("\n=== Konec průběhu ===")