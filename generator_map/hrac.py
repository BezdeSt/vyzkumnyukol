class Hrac:
    def __init__(self, jmeno):
        """
        Inicializuje nového hráče se zadaným jménem.

        Args:
            jmeno: Řetězec představující jméno hráče.
        """
        self.jmeno = jmeno
        self.suroviny = {
            "jidlo": 0,
            "drevo": 0,
            "kamen": 0,
        }
        self.jednotky = []  # Seznam instancí jednotek patřících hráči
        self.budovy = []    # Seznam instancí budov patřících hráči
        self.stavitelske_body = 0  # Počet dostupných stavebních bodů (volitelné použití)

    # -------------------------------------------------------------------------------------------------------
    # SUROVINY
    # -------------------------------------------------------------------------------------------------------
    def pridej_suroviny(self, nove_suroviny):
        """
        Přičte zadané suroviny k aktuálním zásobám hráče.

        Args:
            nove_suroviny: Slovník s typem suroviny jako klíčem a množstvím jako hodnotou.
        """
        for typ, mnozstvi in nove_suroviny.items():
            if typ in self.suroviny:
                self.suroviny[typ] += mnozstvi
            else:
                self.suroviny[typ] = mnozstvi

    def odecti_suroviny(self, suroviny: dict) -> bool:
        """
        Pokusí se odečíst zadané množství surovin ze zásob hráče.

        Args:
            suroviny: Slovník s typem suroviny jako klíčem a množstvím jako hodnotou.

        Returns:
            True, pokud má hráč dostatek surovin a odečtení proběhne; jinak False.
        """
        for typ, mnozstvi in suroviny.items():
            if self.suroviny.get(typ, 0) < mnozstvi:
                return False  # Nedostatek surovin
        for typ, mnozstvi in suroviny.items():
            self.suroviny[typ] -= mnozstvi
        return True

    # -------------------------------------------------------------------------------------------------------
    # EKONOMIKA
    # -------------------------------------------------------------------------------------------------------
    def zpracuj_nedostatek_jidla(self, jednotky_na_poli, potrebne_jidlo=1, ztrata_zivotu=1):
        """
        Zpracuje následky nedostatku jídla. Pokud hráč nemá dostatek jídla,
        všechny jednotky ztratí životy. Jednotky, které zemřou, budou odstraněny.

        Args:
            jednotky_na_poli: Slovník všech jednotek na mapě (pozice: jednotka).
            potrebne_jidlo: Počet jednotek jídla potřebných k přežití (výchozí: 1).
            ztrata_zivotu: Počet životů, které jednotky ztratí při hladu (výchozí: 1).
        """
        if self.suroviny.get("jidlo", 0) < potrebne_jidlo:
            print(f"{self.jmeno} nemá dostatek jídla! Každá jednotka ztratí {ztrata_zivotu} život.")
            for jednotka in list(self.jednotky):  # list() kvůli bezpečnému mazání
                jednotka.zivoty -= ztrata_zivotu
                if jednotka.zivoty <= 0:
                    print(f"Jednotka na pozici {jednotka.pozice} zemřela hladem!")
                    jednotky_na_poli.pop(jednotka.pozice, None)
                    self.jednotky.remove(jednotka)
        else:
            self.suroviny["jidlo"] -= potrebne_jidlo

    def zisk_z_budov(self):
        souhrn = {}
        for budova in self.budovy:
            produkce = budova.generuj_suroviny()
            for typ, mnozstvi in produkce.items():
                souhrn[typ] = souhrn.get(typ, 0) + mnozstvi
        self.pridej_suroviny(souhrn)
        print(f"{self.jmeno} získal: {souhrn}")

    def zpracuj_udrzbu(self, jednotky):
        """
        Vypočítá celkovou údržbu všech jednotek hráče. Pokud hráč nemá dostatek
        surovin k údržbě, všechny jednotky ztratí 1 život.

        Pokud není dostatek surovin, odečítají se na nulu.
        """
        #TODO: Zvážit jestli by suroviny neměli jít do mínusu?
        celkova_udrzba = {}
        for jednotka in self.jednotky:
            for surovina, mnozstvi in jednotka.cena_za_kolo.items():
                celkova_udrzba[surovina] = celkova_udrzba.get(surovina, 0) + mnozstvi

        nedostatek = False
        for surovina, mnozstvi in celkova_udrzba.items():
            aktualni = self.suroviny.get(surovina, 0)
            if aktualni < mnozstvi:
                nedostatek = True
            self.suroviny[surovina] = max(0, aktualni - mnozstvi)

        if nedostatek:
            print(f"{self.jmeno} nemá dost surovin na údržbu! Všechny jednotky ztrácí životy.")
            for jednotka in self.jednotky:
                jednotka.zivoty -= 1  # Lze upravit podle pravidel
                if jednotka.zivoty <= 0:
                    jednotka.zemri(jednotky)

        return celkova_udrzba