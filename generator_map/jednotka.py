class Jednotka:
    def __init__(self, pozice=(0, 0), rychlost=0, dosah=1, utok=1, obrana=1, zivoty=10, vlastnik=None):
        self.pozice = pozice
        self.rychlost = rychlost
        self.dosah = dosah
        self.utok = utok
        self.obrana = obrana
        self.zivoty = zivoty
        self.vlastnik = vlastnik

        self.vlastnik.jednotky.append(self)

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

    # Funkce pouze pro testování TODO: V nějakém bodě odstranit
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

    def proved_pohyb(self, cil, mozne_pohyby, jednotky):
        """
        Provádí pohyb jednotky na cíl.

        Args:
            cil: Cílová pozice.
            mozne_pohyby: Seznam možných pozic.
            jednotky: slovník všech jednotek na herním poli

        Returns: Nová pozice nebo původní pozice.
        """

        if cil in mozne_pohyby:
            jednotky.pop(self.pozice)
            self.pozice = cil
            jednotky[self.pozice] = self

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
                        if cilova_jednotka.vlastnik != self.vlastnik:  # Kontrola týmu jednotky
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

    def vyhodnot_souboj(self, napadeny, jednotky, mrizka):
        """
        Vyhodnocuje souboj s protiútokem a odstraňuje mrtvé jednotky.

        Args:
            napadeny: Instance Jednotka napadeného.
            jednotky: Slovník s instancemi Jednotka.
        """

        if napadeny in self.najdi_cile_v_dosahu(mrizka, jednotky):
            self.proved_utok(napadeny)
            if napadeny.zivoty <= 0:
                napadeny.zemri(jednotky)
            else:
                napadeny.proved_protiutok(self)
                if self.zivoty <= 0:
                    self.zemri(jednotky)

    def zemri(self, jednotky):
        """Odstraňuje jednotku z herní plochy i ze seznamu hráče."""
        jednotky.pop(self.pozice, None)
        if self in self.vlastnik.jednotky:
            self.vlastnik.jednotky.remove(self)