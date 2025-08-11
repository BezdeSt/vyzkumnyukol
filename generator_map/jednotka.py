import random

CRITICAL_HIT_CHANCE = 0.1

class Jednotka:
    def __init__(self, typ=None, id=0, pozice=(0, 0), rychlost=0, dosah=1, utok_min=1, utok_max=1, obrana=1, zivoty=10, crit = 1.1, uhyb = 0.0, cena={'jidlo': 10, 'drevo': 5}, cena_za_kolo={'jidlo': 2}, vlastnik=None, spravce_hry=None):
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
        self.id = id
        self.typ = typ
        self.pozice = pozice
        self.rychlost = rychlost
        self.dosah = dosah
        #self.utok = utok
        self.utok_min = utok_min
        self.utok_max = utok_max

        self.obrana = obrana
        self.zivoty = zivoty
        self.max_zivoty = zivoty
        self.vlastnik = vlastnik

        self.crit = crit
        self.uhyb = uhyb

        self.cena = cena
        self.cena_za_kolo = cena_za_kolo
        self.spravce_hry = spravce_hry

        self.vlastnik.jednotky.append(self)

        # TODO: Simulace
        # Statistiky za jedno kolo pro logování
        self.zpusobene_poskozeni_za_kolo = 0
        self.prijate_poskozeni_za_kolo = 0
        self.utoky_za_kolo = 0
        self.protiutoky_za_kolo = 0
        self.kriticke_zasahy_za_kolo = 0
        self.uhyby_za_kolo = 0

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
            print(f"Jednotka {self.typ} se pohybuje na pozici {cil}")
            jednotky.pop(self.pozice)
            self.pozice = cil
            jednotky[self.pozice] = self
        else:
            print(f"Cíl {cil}, není v možných pohybech {mozne_pohyby}!")


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


    def modifikace_obrany_terenem(self, mapa):
        modifikace = 0
        if mapa[self.pozice[1]][self.pozice[0]] == 'H':
            modifikace += 2
        return modifikace

    def proved_utok(self, cilova_jednotka, mapa, utok=True):
        """
            Útočí na cílovou jednotku a snižuje jí životy podle síly útoku a obrany cíle
            Args:
            cilova_jednotka: Instance jednotky, která je napadena.
        """
        # TODO: Simulace
        # Kontrola zda se nejedná o protiútok (ten se započítává jinde)
        if utok:
            self.utoky_za_kolo += 1

        # 1. Výpočet základního poškození s náhodnou variabilitou
        poskozeni_ciste = random.randint(self.utok_min, self.utok_max)

        # Poškození redukované obranou cíle
        celkove_poskozeni = max(0, poskozeni_ciste - (cilova_jednotka.obrana + cilova_jednotka.modifikace_obrany_terenem(mapa)))

        # 2. Šance na uhnutí cílové jednotky
        if random.random() < cilova_jednotka.uhyb:
            celkove_poskozeni = 0  # Útok minul
            # TODO: Simulace
            cilova_jednotka.uhyby_za_kolo += 1
            print(f"{cilova_jednotka.typ} uhnula útoku!") # Pro ladění
        else:
            # 3. Kritický zásah
            if random.random() < CRITICAL_HIT_CHANCE:
                # TODO: Simulace
                self.kriticke_zasahy_za_kolo += 1
                print(f"{self.typ} způsobil kritický zásah původní poškození mělo být {celkove_poskozeni}!") # Pro ladění
                celkove_poskozeni = round(self.crit*celkove_poskozeni)

        # Aplikace poškození
        print(f"{self.typ} způsobil poškození: {celkove_poskozeni}!")
        cilova_jednotka.zivoty -= celkove_poskozeni

        # TODO: Simulace
        self.zpusobene_poskozeni_za_kolo += celkove_poskozeni
        cilova_jednotka.prijate_poskozeni_za_kolo += celkove_poskozeni

    def proved_protiutok(self, utocici_jednotka, mapa):
        if self.zivoty > 0 and abs(utocici_jednotka.pozice[0] - self.pozice[0]) + abs(utocici_jednotka.pozice[1] - self.pozice[1]) <= self.dosah:

            # TODO: Simulace
            self.protiutoky_za_kolo += 1
            self.proved_utok(utocici_jednotka, mapa, False)
            # print(f"{self.nazev} provedl protiútok na {utocici_jednotka.nazev}!") # Pro ladění

    def zemri(self, jednotky):
        """
        Odstraní jednotku z herní plochy i ze seznamu hráče.

        Args:
            jednotky: Slovník všech jednotek na mapě.
        """

        jednotky.pop(self.pozice, None)
        if self in self.vlastnik.jednotky:
            self.vlastnik.jednotky.remove(self)

    # TODO: Simulace
    def reset_round_stats(self):
        """Resetuje statistiky jednotky sbírané za jedno kolo."""
        self.zpusobene_poskozeni_za_kolo = 0
        self.prijate_poskozeni_za_kolo = 0
        self.utoky_za_kolo = 0
        self.protiutoky_za_kolo = 0
        self.kriticke_zasahy_za_kolo = 0
        self.uhyby_za_kolo = 0

    def ziskej_info(self):
        """Vrátí slovník s aktuálními informacemi o jednotce, včetně statistik za kolo."""
        return {
            'id': self.id,
            'typ': self.typ,
            'pozice': self.pozice,
            'vlastnik': self.vlastnik.jmeno,
            'zivoty': self.zivoty,
            'max_zivoty': self.max_zivoty,
            'utok_min': self.utok_min,
            'utok_max': self.utok_max,
            'obrana': self.obrana,
            'rychlost': self.rychlost,
            'dosah': self.dosah,
            'crit': self.crit,
            'uhyb': self.uhyb,
            'cena': self.cena,
            'cena_za_kolo': self.cena_za_kolo,

            'zpusobene_poskozeni_za_kolo': self.zpusobene_poskozeni_za_kolo,
            'prijate_poskozeni_za_kolo': self.prijate_poskozeni_za_kolo,
            'utoky_za_kolo': self.utoky_za_kolo,
            'protiutoky_za_kolo': self.protiutoky_za_kolo,
            'kriticke_zasahy_za_kolo': self.kriticke_zasahy_za_kolo,
            'uhyby_za_kolo': self.uhyby_za_kolo,
        }