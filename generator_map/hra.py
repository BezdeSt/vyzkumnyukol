# TODO: (bude potřeba řešit navigování jednotek k nějakému cíli (boj/útok na základu))
# TODO: Začít řešit AI
#   (základní herní akce, rozhodování jaká se provede)
#   Primitivní varianta:
#   * zkontroluje suroviny
#   * pokud může, naverbuje jednotku
#   * pokusí se jednotku náhodně pohnout / zaútočit
#   * jinak nic nedělá
# TODO: Ukládání výsledků hry/kola
from random import randint
import random

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
        self.jednotky = jednotky # {(pozice): Jednotka}
        self.budovy = budovy
        self.aktualni_hrac_index = 0
        self.kolo = 1
        self.stav_hry = 1 # 1 Hra probíhá; 0 Hra byla ukončena

    # Předdefinované šablony jednotek
    JEDNOTKY_SABLONY = {
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
            'rychlost': 5,
            'dosah': 1,
            'utok': 15,
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

    BUDOVY_SABLONY = {
        'farma': {
            'typ': 'farma',
            'zivoty': 10,
            'obrana': 1,
            'cena': {'drevo': 5},
            'produkce': {'jidlo': 2}
        },
        'pila': {
            'typ': 'pila',
            'zivoty': 10,
            'obrana': 1,
            'cena': {'drevo': 5},
            'produkce': {'drevo': 2}
        },
        'dul': {
            'typ': 'dul',
            'zivoty': 10,
            'obrana': 1,
            'cena': {'drevo': 5},
            'produkce': {'kamen': 2}
        },

    }

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

        # Generování surovin ze všech budov vlastněných hráčem
        celkovi_zisk = {'jidlo': 0, 'drevo': 0, 'kamen': 0}
        for budova in hrac.budovy:
            zisk = budova.generuj_suroviny()

            for surovina, mnozstvi in zisk.items():
                celkovi_zisk[surovina] = celkovi_zisk.get(surovina, 0) + mnozstvi

            hrac.pridej_suroviny(zisk)

        # Vyhodnocení údržby jednotek (může způsobit ztrátu životů)
        celkove_naklady = hrac.zpracuj_udrzbu(self.jednotky)

        print(f"Clekový zisk: {celkovi_zisk}")
        print(f"Clekové náklady: {celkove_naklady}")

        # Zde by probíhala simulace akcí hráče nebo AI
        # (např. náhodné akce, skripty, apod.)
        self.ai_tah(hrac, celkovi_zisk, celkove_naklady)

        print(hrac.suroviny)
        # Ukončení tahu a posun na dalšího hráče
        self.dalsi_hrac()

    def inicializace_hry(self):
        hrac1 = hrac.Hrac(jmeno="Modrý")
        self.hraci.append(hrac1)
        hrac2 = hrac.Hrac(jmeno="Červený")
        self.hraci.append(hrac2)

        self.verbovani(typ='zakladna',vlastnik=hrac1,
                            pozice=(1,1), spravce_hry=self)
        pocet_radku = len(self.mrizka)
        pocet_sloupcu = len(self.mrizka[0])
        self.verbovani(typ='zakladna', vlastnik=hrac2,
                            pozice=(pocet_radku-2, pocet_sloupcu-2), spravce_hry=self)

        hrac1.pridej_suroviny({'drevo': 5})
        hrac2.pridej_suroviny({'drevo': 5})
        self.stavba_budovy(self.budovy, 'domek', (0,0), hrac1)
        self.stavba_budovy(self.budovy, 'domek', (0,0), hrac2)


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
        self.stav_hry = 0

    def verbovani(self, typ, vlastnik, spravce_hry, pozice=None):
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
        # TODO: Základna je udělaná jako jednotka pouze v prototypu
        if typ == 'zakladna':
            for jedn in vlastnik.jednotky:
                if jedn.typ == 'zakladna':
                    print(f"{vlastnik.jmeno} už má základnu, nelze vytvořit další.")
                    return None

        if not vlastnik.jednotky == []:
            pozice_zakladna = vlastnik.jednotky[0].pozice
            smery = [(-1, 0), (0, -1), (1, 0), (0, 1)]
            prvni_pokus = smery[randint(0, 3)]
            vybrana_pozice = (pozice_zakladna[0] + prvni_pokus[0], pozice_zakladna[1] + prvni_pokus[1])

            if vybrana_pozice in self.jednotky:
                nalezeno = False
                for smer in smery:
                    nova_pozice = (pozice_zakladna[0] + smer[0], pozice_zakladna[1] + smer[1])
                    if nova_pozice not in self.jednotky:
                        vybrana_pozice = nova_pozice
                        nalezeno = True
                        break
                if not nalezeno:
                    print("Není místo pro naverbování jednotky.")
                    return None
            pozice = vybrana_pozice
        else:
            if pozice in self.jednotky:
                print("Tady nemůžeš postavi Základnu.")
                return None

        if typ not in self.JEDNOTKY_SABLONY:
            print(f"Neznámý typ jednotky: {typ}")
            return None

        sablona = self.JEDNOTKY_SABLONY[typ]

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
            vlastnik=vlastnik,
            spravce_hry=spravce_hry,
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
        if typ not in self.BUDOVY_SABLONY:
            print(f"Neznámý typ budovy: {typ}")
            return None

        sablona = self.BUDOVY_SABLONY[typ]

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

    def ai_tah(spravce_hry, hrac, zisk, naklady):
        """Provede tah AI hráče.

        AI nejprve zkontroluje jednotky:
            - Pokud jednotka sousedí s nepřátelskou jednotkou, zaútočí na ni.
            - Pokud má základna dostatek surovin, verbuje jednotky.

        Poté zkontroluje budovy:
            - Pokud má dost surovin, staví budovy na volných polích u základny.

        Args:
            spravce_hry (SpravceHry): Instance správce hry.
            hrac (Hrac): AI hráč.
        """
        # Tah jednotek
        spravce_hry.pohyb_jednotek_ai(hrac)

        # Stavba budov a verbování jednotek
        spravce_hry.stavba_a_verbovani_ai(hrac, zisk, naklady)


    def nejslabsi_z_nepratel_v_dosahu(spravce_hry, nepratele):
        min_zivoty = 1000
        nejslabsi = None
        for nepritel in nepratele:
            if nepritel.zivoty < min_zivoty:
                min_zivoty = nepritel.zivoty
                nejslabsi = nepritel
        return nejslabsi

    def budovy_pro_surovinu(self, surovina):
        """
        Vrací budovy které generují danou surovinu.
        Args:
            surovina: Typ suroviny
        return:
             Budovy generující danou surovinu.
        """
        return {nazev: data for nazev, data in self.BUDOVY_SABLONY.items() if surovina in data['produkce']}

    def aktualizace_zisku(spravce_hry, budova, zisk):
        """
        Aktualizuje zisk po postavení nové budvy.
        Args:
            budova: Instance nově postavené budovy.
            zisk: Aktuální zisk za kolo.
        return:
            Zisk za kolo po postavení nové budovy.
        """
        if budova is None:
            print("Budova se nepostavila.")
            return zisk
        else:
            for surovina, hodnota in budova.produkce.items():
                zisk[surovina] = zisk.get(surovina, 0) + hodnota
            return zisk

    def pohyb_jednotek_ai(spravce_hry, hrac):
        for jednotka in hrac.jednotky:
            x, y = jednotka.pozice

            # Všechny nepřátelské jednotky (pro každou jednotku znovu protože můžou umřít)
            nepratelske_jednotky = protivnici = {pozice: j for pozice, j in spravce_hry.jednotky.items() if j.vlastnik != hrac}

            # Hledání sousedních nepřátel
            nepratele_v_dosahu = jednotka.najdi_cile_v_dosahu(spravce_hry.mrizka, nepratelske_jednotky)
            if nepratele_v_dosahu: # IDEA: Existuje nepřítel v dosahu
                nejslabsi = spravce_hry.nejslabsi_z_nepratel_v_dosahu(nepratele_v_dosahu)
                print(f"Jednotka na pozici {jednotka.pozice} provedla útok na nepřítele vedle sebe bez nutnosti pohybu.")
                spravce_hry.vyhodnot_souboj(jednotka, nejslabsi)
            else:  # IDEA: Nepřítel není v dosahu bez pohybu.
                mozne_pohyby = jednotka.vypocet_moznych_pohybu(spravce_hry.mrizka, spravce_hry.jednotky)

                #print(f"Možné pohyby jednotky hráče {hrac.jmeno} z pozice {jednotka.pozice} jsou:")
                #for radek in jednotka.pozice_na_matici(mozne_pohyby, len(spravce_hry.mrizka[0]), len(spravce_hry.mrizka)):
                #    print(radek)

                # IDEA: Nepřítel je v dosahu po pohybu
                neni_nepritel_v_dosahu = True
                for moznost in mozne_pohyby: # posouvám dočaně jednotku na novou pozici a testuju jestli na někoho dosáhne

                    nepratele_v_dosahu = jednotka.najdi_cile_v_dosahu_z_pozice(moznost, spravce_hry.mrizka,
                                                                               nepratelske_jednotky)
                    if nepratele_v_dosahu:  # Existuje nepřítel v dosahu
                        neni_nepritel_v_dosahu = False
                        nejslabsi = spravce_hry.nejslabsi_z_nepratel_v_dosahu(nepratele_v_dosahu)
                        jednotka.proved_pohyb(moznost, mozne_pohyby, spravce_hry.jednotky)
                        print(f"Jednotka se posunula z pozice {(x,y)} na {jednotka.pozice} a provedla útok.")
                        spravce_hry.vyhodnot_souboj(jednotka, nejslabsi)
                        break

                # IDEA: V okolí není nepřítel, posunout se k základně nepřítele
                if neni_nepritel_v_dosahu:
                    jednotka.proved_pohyb((x,y), (x,y), spravce_hry.jednotky)
                    print(f"Jednotka na {jednotka.pozice} by se měla začít pohybovat k základně nepřítele.")
                    continue
                    # TODO: Nějaký A* k pohybu směrem k nepřátelské základně.

    def stavba_a_verbovani_ai(spravce_hry, hrac, zisk, naklady):
        pocet_pokusu = 0
        while pocet_pokusu < 11:
            if naklady.get('jidlo', 0) >= zisk.get('jidlo', 0):
                zisk = spravce_hry.postav_budovu(hrac, 'jidlo', zisk)
            elif naklady.get('drevo', 0) >= zisk.get('drevo', 0):
                zisk = spravce_hry.postav_budovu(hrac, 'drevo', zisk)
            elif naklady.get('kamen', 0) >= zisk.get('kamen', 0):
                zisk = spravce_hry.postav_budovu(hrac, 'kamen', zisk)
            else:
                print("Verbování jednotky")
                break
            pocet_pokusu += 1
        return zisk

    def postav_budovu(spravce_hry, hrac, surovina, zisk):
        print(f"Stavím budovu pro {surovina}")
        budovy = list(spravce_hry.budovy_pro_surovinu(surovina).keys())
        nahodne_cislo = randint(0, len(budovy) - 1)
        temp_budova = spravce_hry.stavba_budovy(spravce_hry.budovy, budovy[nahodne_cislo], (0, 0), hrac)
        return spravce_hry.aktualizace_zisku(temp_budova, zisk)
