class Budova:
    def __init__(self, typ, pozice, vlastnik, zivoty = 50, obrana = 5, produkce={'drevo': 0}, cena={'drevo': 20}):
        """
        Inicializuje budovu.

        Args:
            typ (str): Typ budovy (např. 'drevorubec', 'dilna', 'sklad', ...).
            pozice (tuple): Souřadnice budovy na mapě.
            vlastnik (Hrac): Instance hráče, který budovu vlastní.
            zivoty (int): Počet životů budovy.
            max_zivoty (int): Maximální počet životů budovy.
            obrana (int): Snižení poškození útoku.
        """
        self.typ = typ
        self.pozice = pozice
        self.vlastnik = vlastnik
        self.zivoty = zivoty
        self.max_zivoty = zivoty
        self.obrana = obrana
        self.produkce = produkce  # slovník {"typ_suroviny": množství}

        self.cena = cena

        self.vlastnik.budovy.append(self)  # Automatická registrace hráči

    def generuj_suroviny(self):
        """
        Vrací suroviny vyprodukované touto budovou za jedno kolo.
        """
        return self.produkce.copy()
