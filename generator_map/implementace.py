class Jednotka:
    def __init__(self, pozice=(0, 0), rychlost=0, dosah=1, utok=1, obrana=1, zivoty=10, tym=True):
        self.pozice = pozice
        self.rychlost = rychlost
        self.dosah = dosah
        self.utok = utok
        self.obrana = obrana
        self.zivoty = zivoty
        self.tym = tym  # True pro tým 1, False pro tým 2

    # -------------------------------------------------------------------------------------------------------
    # POHYB
    # -------------------------------------------------------------------------------------------------------
    def vypocet_moznych_pohybu(self, mrizka):
        """
        Vypočítá možné pohyby jednotky s ohledem na terén a omezením vzdálenosti.

        Args:
            mrizka (list[list]): 2D mřížka s terény (V, P, L, H).

        Returns: Seznam možných pozic pro pohyb.
        """

        x, y = self.pozice
        mozne_pohyby = []
        navstivene = {self.pozice}
        fronta = [(self.pozice, self.rychlost)]

        while fronta:
            aktualni_pozice, zbyvajici_vzdalenost = fronta.pop(0)
            x, y = aktualni_pozice

            mozne_pohyby.append(aktualni_pozice)

            if zbyvajici_vzdalenost <= 0:
                continue

            sousedni_pohyby = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

            for nova_x, nova_y in sousedni_pohyby:
                if 0 <= nova_x < len(mrizka[0]) and 0 <= nova_y < len(mrizka) and (nova_x, nova_y) not in navstivene:
                    teren = mrizka[nova_y][nova_x]
                    if teren == 'V':
                        continue

                    navstivene.add((nova_x, nova_y))
                    if teren == 'P':
                        fronta.append(((nova_x, nova_y), zbyvajici_vzdalenost - 1))
                    elif teren == 'L':
                        fronta.append(((nova_x, nova_y), zbyvajici_vzdalenost - 2))
                    elif teren == 'H':
                        fronta.append(((nova_x, nova_y), 0))

        return mozne_pohyby

    # Funkce pouze pro testování
    def pozice_na_matici(self, mozne_pohyby, sirka, vyska):
        """
        Převede seznam pozic na matici 1 a 0.

        Args:
            mozne_pohyby: Seznam povolených pozic.
            sirka: Šířka mřížky.
            vyska: Výška mřížky.

        Returns: Matice 1 a 0.
        """

        matice = [[0 for _ in range(sirka)] for _ in range(vyska)]
        for x, y in mozne_pohyby:
            matice[y][x] = 1
        return matice

    def proved_pohyb(self, cil, mozne_pohyby):
        """
        Provádí pohyb jednotky na cíl.

        Args:
            cil: Cílová pozice.
            mozne_pohyby: Seznam možných pozic.

        Returns: Nová pozice nebo původní pozice.
        """

        if cil in mozne_pohyby:
            jednotky.pop(self.pozice)  # Odstranit starou pozici
            self.pozice = cil
            jednotky[self.pozice] = self  # Přidat novou pozici

    # -------------------------------------------------------------------------------------------------------
    # BOJ
    # -------------------------------------------------------------------------------------------------------

    def najdi_cile_v_dosahu(self, mrizka, jednotky):
        """
        Najde cíle v dosahu útoku, pouze nepřátelské jednotky.

        Args:
            mrizka: 2D mřížka.
            jednotky: Slovník s instancemi Jednotka.

        Returns: Seznam cílů v dosahu.
        """

        x, y = self.pozice
        cile = []

        for dx in range(-self.dosah, self.dosah + 1):
            for dy in range(-self.dosah, self.dosah + 1):
                if abs(dx) + abs(dy) <= self.dosah and (dx != 0 or dy != 0):
                    cil_x, cil_y = x + dx, y + dy

                    if 0 <= cil_x < len(mrizka[0]) and 0 <= cil_y < len(mrizka) and (cil_x, cil_y) in jednotky:
                        cilova_jednotka = jednotky[(cil_x, cil_y)] # Nalezená jednotka
                        if cilova_jednotka.tym != self.tym:  # Kontrola týmu jednotky
                            cile.append(cilova_jednotka)

        return cile

    def proved_utok(self, napadeny):
        """
        Provádí útok na napadeného.

        Args: napadeny: Instance Jednotka napadeného.
        """

        poskozeni = self.utok - napadeny.obrana
        if poskozeni > 0:
            napadeny.zivoty -= poskozeni

    def proved_protiutok(self, utocnik):
        """
        Provádí protiútok, pokud je v dosahu.

        Args: utocnik: Instance Jednotka útočníka.
        """

        if self.zivoty > 0 and abs(utocnik.pozice[0] - self.pozice[0]) + abs(utocnik.pozice[1] - self.pozice[1]) <= self.dosah:
            poskozeni = self.utok - utocnik.obrana
            if poskozeni > 0:
                utocnik.zivoty -= poskozeni

    def vyhodnot_souboj(self, napadeny, jednotky):
        """
        Vyhodnocuje souboj s protiútokem a odstraňuje mrtvé jednotky.

        Args:
            napadeny: Instance Jednotka napadeného.
            jednotky: Slovník s instancemi Jednotka.
        """

        self.proved_utok(napadeny)
        if napadeny.zivoty <= 0:
            # Odstranění napadeného ze slovníku jednotky
            jednotky.pop(napadeny.pozice)
        else:
            napadeny.proved_protiutok(self)
            if self.zivoty <= 0:
                # Odstranění útočníka ze slovníku jednotky
                jednotky.pop(self.pozice)

    # -------------------------------------------------------------------------------------------------------
    # EKONOMIKA
    # -------------------------------------------------------------------------------------------------------



mrizka = [
    ['H', 'H', 'P', 'P', 'P'],
    ['L', 'P', 'L', 'H', 'P'],
    ['P', 'P', 'P', 'P', 'P'],
    ['P', 'H', 'L', 'V', 'P'],
    ['P', 'P', 'P', 'P', 'P'],
]

jednotka1 = Jednotka(pozice=(0, 0), rychlost=3, dosah=3, utok=8, obrana=1, zivoty=10, tym=True)
jednotka2 = Jednotka(pozice=(0, 2), rychlost=1, dosah=5, utok=1, obrana=2, zivoty=10, tym=False)

jednotky = {jednotka1.pozice: jednotka1, jednotka2.pozice: jednotka2}

def pohyb():
    mozne_pohyby = jednotka1.vypocet_moznych_pohybu(mrizka)
    print("Možné pohyby:", mozne_pohyby)

    vyska = len(mrizka)
    sirka = len(mrizka[0])

    matice_pohybu = jednotka1.pozice_na_matici(mozne_pohyby, sirka, vyska)

    for radek in matice_pohybu:
        print(radek)

    jednotka1.proved_pohyb((1, 0), mozne_pohyby)
    print("Nová pozice jednotky 1:", jednotka1.pozice)

def boj():
    cile = jednotka1.najdi_cile_v_dosahu(mrizka, jednotky)
    print("Cíle v dosahu:")
    for cilova_jednotka in cile:
        print(f"  Pozice: {cilova_jednotka.pozice}")

        print(f"  Jednotka1 životy: {jednotka1.zivoty}")
        print(f"  Jednotka2 životy: {cilova_jednotka.zivoty}")
        jednotka1.vyhodnot_souboj(jednotka2, jednotky)
        print("--------")
        print(f"  Jednotka1 životy: {jednotka1.zivoty}")
        print(f"  Jednotka2 životy: {cilova_jednotka.zivoty}")
# TODO: Taky porovnat funkce
# TODO: Funkce vyhodnoť souboj neřeší zda je napadený v dosahu

pohyb()
print("=====================")
boj()