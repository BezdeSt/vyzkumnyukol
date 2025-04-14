# TODO: Základna kde se budou objevovat nové jednotky
#  (bude potřeba řešit navigování jednotek k nějakému cíli (boj/útok na základu))
# TODO: Začít řešit AI
#   (základní herní akce, rozhodování jaká se provede)
#   Primitivní varianta:
#   * zkontroluje suroviny
#   * pokud může, naverbuje jednotku
#   * pokusí se jednotku náhodně pohnout / zaútočit
#   * jinak nic nedělá
# TODO: Ukládání výsledků hry/kola
import hrac
import ekonomika
from implementace import mrizka


class SpravceHry:
    """
    Spravuje průběh hry, včetně sledování kol, hráčů a vyhodnocení jejich tahů.
    """

    def __init__(self, hraci, mrizka, jednotky, budovy):
        """
        Inicializuje správce hry.

        Args:
            hraci: Seznam hráčů účastnících se hry.
            mrizka: Herní mapa jako 2D seznam terénních typů.
            jednotky: Slovník všech jednotek na mapě (pozice: instance jednotky).
            budovy: Seznam všech budov na mapě.
        """
        self.hraci = hraci
        self.mrizka = mrizka
        self.jednotky = jednotky
        self.budovy = budovy
        self.aktualni_hrac_index = 0
        self.kolo = 1

    def aktualni_hrac(self):
        """
        Vrátí hráče, který je aktuálně na tahu.

        Returns:
            Instance třídy Hrac reprezentující aktuálního hráče.
        """
        return self.hraci[self.aktualni_hrac_index]

    def dalsi_hrac(self):
        """
        Posune tah na dalšího hráče. Pokud byli na tahu všichni, zvýší číslo kola.
        """
        self.aktualni_hrac_index = (self.aktualni_hrac_index + 1) % len(self.hraci)
        if self.aktualni_hrac_index == 0:
            self.kolo += 1
            print("-------")

    def proved_tah(self):
        """
        Provede celý tah aktuálního hráče, včetně údržby, generování surovin a případné AI akce.
        """
        hrac = self.aktualni_hrac()
        print(f"Kolo {self.kolo}, tah hráče: {hrac.jmeno}")

        # Vyhodnocení údržby jednotek (může způsobit ztrátu životů)
        hrac.zpracuj_udrzbu(self.jednotky)

        # Generování surovin ze všech budov vlastněných hráčem
        for budova in hrac.budovy:
            zisk = budova.generuj_suroviny()
            hrac.pridej_suroviny(zisk)

        # Zde by probíhala simulace akcí hráče nebo AI
        # (např. náhodné akce, skripty, apod.)
        print(hrac.suroviny)
        # Ukončení tahu a posun na dalšího hráče
        self.dalsi_hrac()

    def inicializace_hry(self):
        hrac1 = hrac.Hrac(jmeno="Modrý")
        hrac2 = hrac.Hrac(jmeno="Červený")
        ekonomika.verbovani(jednotky=self.jednotky, typ='zakladna',vlastnik=hrac1,pozice=(1,1))
        pocet_radku = len(self.mrizka)
        pocet_sloupcu = len(self.mrizka[0])
        ekonomika.verbovani(jednotky=self.jednotky, typ='zakladna', vlastnik=hrac1, pozice=(pocet_radku-2, pocet_sloupcu-2))
