class Hrac:
    def __init__(self, jmeno):
        """
        Inicializuje nového hráče se zadaným jménem.
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

    def pridej_suroviny(self, suroviny: dict):
        """
        Přidá zadané množství surovin do zásob hráče.

        Args:
          suroviny: slovník s typem suroviny jako klíčem a množstvím jako hodnotou
        """
        for typ, mnozstvi in suroviny.items():
            self.suroviny[typ] = self.suroviny.get(typ, 0) + mnozstvi

    def odecti_suroviny(self, suroviny: dict) -> bool:
        """
        Pokusí se odečíst zadané množství surovin ze zásob hráče.
        Vrací True, pokud má hráč dostatek surovin a odečtení proběhne, jinak False.

        Args:
          suroviny: slovník s typem suroviny jako klíčem a množstvím jako hodnotou
        """
        for typ, mnozstvi in suroviny.items():
            if self.suroviny.get(typ, 0) < mnozstvi:
                return False  # nedostatek surovin
        for typ, mnozstvi in suroviny.items():
            self.suroviny[typ] -= mnozstvi
        return True

    def pridej_jednotku(self, jednotka):
        """
        Přidá zadanou jednotku do seznamu jednotek hráče.

        Args:
          jednotka: instance třídy Jednotka
        """
        self.jednotky.append(jednotka)

    def pridej_budovu(self, budova):
        """
        Přidá zadanou budovu do seznamu budov hráče.

        Args:
          budova: instance třídy Budova
        """
        self.budovy.append(budova)
