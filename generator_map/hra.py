# TODO: Dodělat verbování tak aby se jednotky objevovali okolo základny
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
import jednotka
import budova


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
        ekonomika.verbovani(jednotky=self.jednotky, typ='zakladna',vlastnik=hrac1,
                            pozice=(1,1), spravce_hry=self)
        pocet_radku = len(self.mrizka)
        pocet_sloupcu = len(self.mrizka[0])
        ekonomika.verbovani(jednotky=self.jednotky, typ='zakladna', vlastnik=hrac2,
                            pozice=(pocet_radku-2, pocet_sloupcu-2), spravce_hry=self)

    def vyhodnot_souboj(self, utocnik, napadeny):
        """
        Vyhodnotí souboj mezi dvěma jednotkami včetně protiútoku a odstranění padlých.

        Args:
            utocnik: Útočící jednotka.
            napadeny: Napadená jednotka.
        """
        # zkontrolujeme jestli jsou v dosahu
        if napadeny in utocnik.najdi_cile_v_dosahu(self.mrizka, self.jednotky):
            utocnik.proved_utok(napadeny)
            if napadeny.zivoty <= 0:
                napadeny.zemri(self.jednotky)
                if napadeny.typ == 'zakladna':
                    print(f"{napadeny.vlastnik.jmeno} přišel o základnu! Hra končí.")
                    self.konce(napadeny.vlastnik)
            else:
                napadeny.proved_protiutok(utocnik)
                if utocnik.zivoty <= 0:
                    utocnik.zemri(self.jednotky)

    def konce(self, porazeny):
        #TODO: Uloží informace o výslekdu hry/simulace.
        print(f"{porazeny} prohrál! Hra končí.")
        return

    def verbovani(self, typ, pozice, vlastnik):
        """
        Verbování nové jednotky určitého typu.

        Args:
            jednotky: Slovník aktuálních jednotek na mapě.
            typ: Název typu jednotky ('bojovnik', 'lucisnik', ...).
            pozice: Pozice, kde má být jednotka vytvořena.
            vlastnik: Instance hráče, který jednotku verbuje.

        Returns:
            Nová jednotka nebo None, pokud hráč nemá dost surovin.
        """
        if pozice in self.jednotky:
            print("Pozice je obsazená, jednotku není možné naverbovat.")
            return None

        # TODO: Základna je udělaná jako jednotka pouze v prototypu
        if typ == 'zakladna':
            for jedn in vlastnik.jednotky:
                if jedn.typ == 'zakladna':
                    print(f"{vlastnik.jmeno} už má základnu, nelze vytvořit další.")
                    return None

        # Předdefinované šablony jednotek
        sablony = {
            'bojovnik': {
                'typ': 'bojovnik',
                'rychlost': 3,
                'dosah': 1,
                'utok': 5,
                'obrana': 3,
                'zivoty': 15,
                'cena': {'jidlo': 10, 'drevo': 2, 'kamen': 0},
                'cena_za_kolo': {'jidlo': 2}
            },
            'lucisnik': {
                'typ': 'lucisnik',
                'rychlost': 2,
                'dosah': 5,
                'utok': 5,
                'obrana': 1,
                'zivoty': 8,
                'cena': {'jidlo': 10, 'drevo': 10, 'kamen': 0},
                'cena_za_kolo': {'jidlo': 2}
            },
            'testovaci': {
                'typ': 'testovaci',
                'rychlost': 2,
                'dosah': 2,
                'utok': 2,
                'obrana': 2,
                'zivoty': 10,
                'cena': {'jidlo': 0, 'drevo': 0, 'kamen': 0},
                'cena_za_kolo': {'jidlo': 2}
            },
            'zakladna': {
                'typ': 'zakladna',
                'rychlost': 0,
                'dosah': 0,
                'utok': 0,
                'obrana': 5,
                'zivoty': 50,
                'cena': {'jidlo': 0, 'drevo': 0, 'kamen': 0},
                'cena_za_kolo': {'jidlo': 0}
            }
        }

        if typ not in sablony:
            print(f"Neznámý typ jednotky: {typ}")
            return None

        sablona = sablony[typ]

        # Pokusíme se zaplatit cenu
        if not vlastnik.odecti_suroviny(sablona['cena']):
            print(f"{vlastnik.jmeno} nemá dost surovin na verbování jednotky typu {typ}.")
            return None

        # Vytvoření jednotky
        nova = jednotka.Jednotka(
            typ=sablona['typ'],
            pozice=pozice,
            rychlost=sablona['rychlost'],
            dosah=sablona['dosah'],
            utok=sablona['utok'],
            obrana=sablona['obrana'],
            zivoty=sablona['zivoty'],
            cena=sablona['cena'],
            cena_za_kolo=sablona['cena_za_kolo'],
            vlastnik=vlastnik
        )

        self.jednotky[pozice] = nova
        print(f"{vlastnik.jmeno} verboval jednotku typu {typ} na pozici {pozice}.")
        return nova

    # TODO: V plné verzi tady bude muset být kontrola, že se pozicie nepřekrývají
    def stavba_budovy(self, budovy, typ, pozice, vlastnik):
        """
        Stavba nové budovy určitého typu.

        Args:
            budovy: Seznam všech budov na mapě.
            typ: Název typu budovy ('domek', 'sberna', ...).
            pozice: Pozice, kde má být budova postavena.
            vlastnik: Instance hráče, který budovu staví.

        Returns:
            Nová budova nebo None, pokud hráč nemá dost surovin.
        """

        sablony = {
            'domek': {
                'typ': 'domek',
                'zivoty': 10,
                'obrana': 1,
                'cena': {'drevo': 5},
                'produkce': {'jidlo': 1}
            },
        }

        if typ not in sablony:
            print(f"Neznámý typ budovy: {typ}")
            return None

        sablona = sablony[typ]

        # Zaplacení ceny
        if not vlastnik.odecti_suroviny(sablona['cena']):
            print(f"{vlastnik.jmeno} nemá dost surovin na stavbu budovy typu {typ}.")
            return None

        # Vytvoření budovy
        nova = budova.Budova(
            typ=sablona['typ'],
            pozice=pozice,
            vlastnik=vlastnik,
            zivoty=sablona['zivoty'],
            obrana=sablona['obrana'],
            produkce=sablona['produkce'],
            cena=sablona['cena'],
        )

        print(f"{vlastnik.jmeno} postavil budovu typu {typ} na pozici {pozice}.")
        budovy.append(nova)
        return nova