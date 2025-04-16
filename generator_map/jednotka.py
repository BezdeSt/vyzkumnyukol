class Jednotka:
    def __init__(self, typ=None, pozice=(0, 0), rychlost=0, dosah=1, utok=1, obrana=1, zivoty=10, cena={'jidlo': 10, 'drevo': 5}, cena_za_kolo={'jidlo': 2}, vlastnik=None, spravce_hry=None):
        """
        Inicializuje jednotku s danými parametry a přidá ji do seznamu jednotek vlastníka.

        Args:
            pozice: Počáteční pozice jednotky.
            rychlost: Maximální vzdálenost, kterou může jednotka urazit za tah.
            dosah: Dosah útoku.
            utok: Útočná síla jednotky.
            obrana: Obranná hodnota jednotky.
            zivoty: Počet životů jednotky.
            cena: Cena pro nákup jednotky.
            cena_za_kolo: Cena za kolo (udržovací náklady).
            vlastnik: Instance hráče, kterému jednotka patří.
        """
        self.typ = typ
        self.pozice = pozice
        self.rychlost = rychlost
        self.dosah = dosah
        self.utok = utok
        self.obrana = obrana
        self.zivoty = zivoty
        self.max_zivoty = zivoty
        self.vlastnik = vlastnik

        self.cena = cena
        self.cena_za_kolo = cena_za_kolo
        self.spravce_hry = spravce_hry

        self.vlastnik.jednotky.append(self)
        print(f"Jednotka {self.typ} se připsala k {self.vlastnik.jmeno}. Nachází se na pozici {self.pozice}")

    # -------------------------------------------------------------------------------------------------------
    # POHYB
    # -------------------------------------------------------------------------------------------------------
    def vypocet_moznych_pohybu(self, mrizka, jednotky):
        """
        Vypočítá možné pohyby jednotky na základě terénu a její rychlosti.

        Args:
            mrizka: 2D seznam reprezentující herní mapu (terénní typy).

        Returns:
            Seznam pozic, na které se jednotka může pohybovat.
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
                        continue  # voda je neprostupná

                    # kontrola, jestli tam není jiná jednotka
                    if (nova_x, nova_y) in jednotky:
                        continue  # obsazeno jinou jednotkou

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
        Převede seznam pozic na binární matici (1 = povolený pohyb, 0 = jinak).

        Args:
            mozne_pohyby: Seznam možných pozic.
            sirka: Počet sloupců mřížky.
            vyska: Počet řádků mřížky.

        Returns:
            2D seznam reprezentující binární matici pohybu.
        """
        matice = [[0 for _ in range(sirka)] for _ in range(vyska)]
        for x, y in mozne_pohyby:
            matice[y][x] = 1
        return matice

    def proved_pohyb(self, cil, mozne_pohyby, jednotky):
        """
        Pokusí se přesunout jednotku na cílovou pozici, pokud je legální.

        Args:
            cil: Cílová pozice.
            mozne_pohyby: Seznam možných pozic k pohybu.
            jednotky: Slovník všech jednotek na mapě.

        Returns:
            Nová pozice, pokud pohyb proběhl, jinak zůstává původní pozice.
        """
        if cil in mozne_pohyby:
            jednotky.pop(self.pozice)
            self.pozice = cil
            jednotky[self.pozice] = self


    def najdi_cile_v_dosahu_z_pozice(self, pozice, mrizka, jednotky):
        """
        Najde nepřátelské jednotky v dosahu útoku z dané pozice.

        Args:
            pozice: Pozice, ze které se počítá dosah.
            mrizka: 2D seznam reprezentující herní mapu.
            jednotky: Slovník všech jednotek na mapě.

        Returns:
            Seznam jednotek, které může jednotka z dané pozice napadnout.
        """
        x, y = pozice
        cile = []

        for dx in range(-self.dosah, self.dosah + 1):
            for dy in range(-self.dosah, self.dosah + 1):
                if abs(dx) + abs(dy) <= self.dosah and (dx != 0 or dy != 0):
                    cil_x, cil_y = x + dx, y + dy

                    if 0 <= cil_x < len(mrizka[0]) and 0 <= cil_y < len(mrizka) and (cil_x, cil_y) in jednotky:
                        cilova_jednotka = jednotky[(cil_x, cil_y)]
                        if cilova_jednotka.vlastnik != self.vlastnik:
                            cile.append(cilova_jednotka)

        return cile

    # -------------------------------------------------------------------------------------------------------
    # BOJ
    # -------------------------------------------------------------------------------------------------------

    def najdi_cile_v_dosahu(self, mrizka, jednotky):
        """
        Najde nepřátelské jednotky v dosahu útoku.

        Args:
            mrizka: 2D seznam reprezentující herní mapu.
            jednotky: Slovník všech jednotek na mapě.

        Returns:
            Seznam jednotek, které může aktuální jednotka napadnout.
        """
        x, y = self.pozice
        cile = []

        for dx in range(-self.dosah, self.dosah + 1):
            for dy in range(-self.dosah, self.dosah + 1):
                if abs(dx) + abs(dy) <= self.dosah and (dx != 0 or dy != 0):
                    cil_x, cil_y = x + dx, y + dy

                    if 0 <= cil_x < len(mrizka[0]) and 0 <= cil_y < len(mrizka) and (cil_x, cil_y) in jednotky:
                        cilova_jednotka = jednotky[(cil_x, cil_y)]
                        if cilova_jednotka.vlastnik != self.vlastnik:
                            cile.append(cilova_jednotka)

        return cile

    def proved_utok(self, napadeny):
        """
        Útočí na cílovou jednotku a snižuje jí životy podle síly útoku a obrany cíle.

        Args:
            napadeny: Instance jednotky, která je napadena.
        """
        poskozeni = self.utok - napadeny.obrana
        if poskozeni > 0:
            napadeny.zivoty -= poskozeni

    def proved_protiutok(self, utocnik):
        """
        Provádí protiútok na útočníka, pokud je v dosahu.

        Args:
            utocnik: Instance jednotky, která provedla útok.
        """
        if self.zivoty > 0 and abs(utocnik.pozice[0] - self.pozice[0]) + abs(utocnik.pozice[1] - self.pozice[1]) <= self.dosah:
            poskozeni = self.utok - utocnik.obrana
            if poskozeni > 0:
                utocnik.zivoty -= poskozeni

    def zemri(self, jednotky):
        """
        Odstraní jednotku z herní plochy i ze seznamu hráče.

        Args:
            jednotky: Slovník všech jednotek na mapě.
        """

        jednotky.pop(self.pozice, None)
        if self in self.vlastnik.jednotky:
            self.vlastnik.jednotky.remove(self)
