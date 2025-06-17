from random import randint
import random

import hrac
import jednotka
import budova
import simulace


class SpravceHry:
    """
    Spravuje průběh hry, včetně sledování kol, hráčů a vyhodnocení jejich tahů.
    """

    def __init__(self, hraci, mrizka, jednotky, budovy, scenar_nazev="None", id_simulace=None):
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
        self.pocitadlo_id = 0

        self.ai_decision_weights = {
            "random_move_chance": 0.2,  # 20% šance na náhodný pohyb
            "target_priority_melee": 1.0,  # Váha pro útok na jednotky pro boj zblízka
            "target_priority_ranged": 1.2,  # Váha pro útok na jednotky s velkým dosahem (vyšší priorita)
            # ... další váhy dle potřeby (např. pro ekonomiku, obranu)...
        }

        self.simulace = simulace.LoggerSimulace(id_simulace, scenar_nazev)

    # Předdefinované šablony jednotek
    JEDNOTKY_SABLONY = {
        'bojovnik': {
            'typ': 'bojovnik',
            'rychlost': 3,
            'dosah': 1,
            'utok_min': 3,
            'utok_max': 5,
            'obrana': 3,
            'zivoty': 10,
            'crit': 1.1,
            'uhyb': 0.05,  # Malá šance na uhnutí
            'cena': {'jidlo': 10, 'drevo': 2, 'kamen': 0},
            'cena_za_kolo': {'jidlo': 2}
        },
        'valecnik': {
            'typ': 'valecnik',
            'rychlost': 3,
            'dosah': 1,
            'utok_min': 6,
            'utok_max': 8,
            'obrana': 4,
            'zivoty': 15,
            'crit': 1.2,
            'uhyb': 0.05,
            'cena': {'jidlo': 60, 'drevo': 30, 'kamen': 0},
            'cena_za_kolo': {'jidlo': 3}
        },
        'rytir': {
            'typ': 'rytir',
            'rychlost': 2,
            'dosah': 1,
            'utok_min': 8,
            'utok_max': 10,
            'obrana': 7,
            'zivoty': 30,
            'crit': 1.3,
            'uhyb': 0.01,  # Nízká šance na uhnutí kvůli těžké zbroji
            'cena': {'jidlo': 120, 'drevo': 50, 'kamen': 30},
            'cena_za_kolo': {'jidlo': 4, 'kamen': 1}
        },
        'berserkr': {
            'typ': 'berserkr',
            'rychlost': 4,
            'dosah': 1,
            'utok_min': 9,
            'utok_max': 12,
            'obrana': 2,
            'zivoty': 20,
            'crit': 2,
            'uhyb': 0.1,  # Vyšší šance na uhnutí díky rychlosti
            'cena': {'jidlo': 70, 'drevo': 40, 'kamen': 0},
            'cena_za_kolo': {'jidlo': 4}
        },
        'lucistnik': {
            'typ': 'lucisnik',
            'rychlost': 3,
            'dosah': 4,
            'utok_min': 6,
            'utok_max': 8,
            'obrana': 3,
            'zivoty': 10,
            'crit': 1.2,
            'uhyb': 0.05,  # Mírná šance na uhnutí
            'cena': {'jidlo': 15, 'drevo': 15, 'kamen': 0},
            'cena_za_kolo': {'jidlo': 2, 'drevo': 1, }
        },
        'ostrostrelec': {
            'typ': 'ostrostrelec',
            'rychlost': 2,
            'dosah': 6,
            'utok_min': 8,
            'utok_max': 10,
            'obrana': 1,
            'zivoty': 10,
            'crit': 1.5,
            'uhyb': 0.05,  # Nízká šance na uhnutí, spoléhá na dosah
            'cena': {'jidlo': 80, 'drevo': 60, 'kamen': 40},
            'cena_za_kolo': {'jidlo': 4, 'drevo': 2, }
        },
        'lovec': {
            'typ': 'lovec',
            'rychlost': 5,
            'dosah': 3,
            'utok_min': 5,
            'utok_max': 7,
            'obrana': 2,
            'zivoty': 14,
            'crit': 1.3,
            'uhyb': 0.15,  # Vysoká šance na uhnutí díky rychlosti a obratnosti
            'cena': {'jidlo': 60, 'drevo': 40, 'kamen': 0},
            'cena_za_kolo': {'jidlo': 3, 'drevo': 1, }
        },
        'zakladna': {
            'typ': 'zakladna',
            'rychlost': 0,
            'dosah': 0,
            'utok_min': 0,  # Základna neútočí
            'utok_max': 0,  # Základna neútočí
            'obrana': 0,
            'zivoty': 50,
            'crit': 1.0,  # Základna nemá kritický zásah
            'uhyb': 0.0,  # Základna se nevyhýbá
            'cena': {'jidlo': 0, 'drevo': 0, 'kamen': 0},
            'cena_za_kolo': {'jidlo': 0}
        },
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

            # TODO: Simulace
            self.simulace.log_stav_kola(self.kolo, self.jednotky, self.simulace.id_simulace)
            for jednotka in self.jednotky.values():
                jednotka.reset_round_stats()

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

        #print(f"Clekový zisk: {celkovi_zisk}")
        #print(f"Clekové náklady: {celkove_naklady}")

        # Zde by probíhala simulace akcí hráče nebo AI
        # (např. náhodné akce, skripty, apod.)
        self.ai_tah(hrac, celkovi_zisk, celkove_naklady)

        #print(hrac.suroviny)
        # Ukončení tahu a posun na dalšího hráče


        self.dalsi_hrac()

    def inicializace_scenare(self, hrac1="Modrý", hrac2="Červený"):
        hrac1 = hrac.Hrac(jmeno=hrac1)
        self.hraci.append(hrac1)
        hrac2 = hrac.Hrac(jmeno=hrac2)
        self.hraci.append(hrac2)

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

        self.startovni_domek(hrac1)
        self.startovni_domek(hrac2)

        # Kontrolovat že je herní pole použitelné
        pruchodnost, cena = self.existuje_cesta_mezi_zakladnami((1,1), (pocet_radku-2, pocet_sloupcu-2), self.mrizka)
        if not pruchodnost:
            self.stav_hry = 0
            print("!!! V herním poly neexistuje cesta mezi zakladnami.")
        else:
            print(f'Cena nejkratší cesty je {cena}')

    def startovni_domek(self, hrac):
        hrac.pridej_suroviny({'drevo': 5})
        self.stavba_budovy(self.budovy, 'domek', (0, 0), hrac)


    def vyhodnot_souboj(self, utocnik, napadeny):
        """
        Vyhodnotí souboj mezi dvěma jednotkami včetně protiútoku a odstranění padlých.

        Args:
            utocnik: Útočící jednotka.
            napadeny: Napadená jednotka.
        """
        # zkontrolujeme jestli jsou v dosahu
        print("Probíhá souboj")
        if napadeny in utocnik.najdi_cile_v_dosahu(self.mrizka, self.jednotky):

            utocnik.proved_utok(napadeny, self.mrizka)
            if napadeny.zivoty <= 0:

                # TODO: Simulace
                self.simulace.log_umirajici_jednotku(napadeny)

                napadeny.zemri(self.jednotky)
                self.kontrola_bojeschopnosti(napadeny.vlastnik, utocnik.vlastnik)
                if napadeny.typ == 'zakladna':
                    self.konec(utocnik.vlastnik, napadeny.vlastnik)
            else:
                if abs(utocnik.pozice[0] - napadeny.pozice[0]) + abs(utocnik.pozice[1] - napadeny.pozice[1]) <= napadeny.dosah:
                    napadeny.proved_protiutok(utocnik, self.mrizka)
                if utocnik.zivoty <= 0:
                    # TODO: Simulace
                    self.simulace.log_umirajici_jednotku(utocnik)

                    utocnik.zemri(self.jednotky)
                    self.kontrola_bojeschopnosti(utocnik.vlastnik, napadeny.vlastnik)

    def kontrola_bojeschopnosti(self, poskozeny_hrac, poskozujici_hrac):
        # TODO: Testovat jestli test bojeschopnosti funguje
        if not poskozeny_hrac.jednotky:
            print(f"Hráč {poskozeny_hrac.jmeno} ztratil všechny jednotky!!!!!!!!!!!!!!")
            self.konec(poskozujici_hrac, poskozeny_hrac)

    def konec(self, vitez, porazeny, poznamka = "Vyhrál: "):
        print("KONEC!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

        # TODO: Simulace
        # Zalogujeme poslední stav kola, včetně mrtvých jednotek
        self.simulace.log_stav_kola(self.kolo, self.jednotky, self.simulace.id_simulace)
        # Uložíme celkový výsledek simulace
        self.simulace.uloz_vysledek_simulace(vitez, self.kolo, self.jednotky)

        self.stav_hry = 0

    def verbovani(self, typ, vlastnik, spravce_hry, pozice=None):
        """
        Verbování nové jednotky určitého typu.

        Args:
            typ: Název typu jednotky ('bojovnik', 'lucisnik', ...).
            pozice: Pozice, kde má být jednotka vytvořena.
            vlastnik: Instance hráče, který jednotku verbuje.

        Returns:
            Nová jednotka nebo None, pokud hráč nemá dost surovin.
        """
        # NEXT: Základna je udělaná jako jednotka pouze v prototypu
        if typ == 'zakladna':
            for jedn in vlastnik.jednotky:
                if jedn.typ == 'zakladna':
                    print(f"{vlastnik.jmeno} už má základnu, nelze vytvořit další.")
                    return None

        if pozice == None:
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
            id=self.pocitadlo_id,
            pozice=pozice,
            rychlost=sablona['rychlost'],
            dosah=sablona['dosah'],
            utok_min=sablona['utok_min'],
            utok_max=sablona['utok_max'],
            obrana=sablona['obrana'],
            zivoty=sablona['zivoty'],
            crit=sablona['crit'],
            uhyb=sablona['uhyb'],
            cena=sablona['cena'],
            cena_za_kolo=sablona['cena_za_kolo'],
            vlastnik=vlastnik,
            spravce_hry=spravce_hry,
        )

        self.jednotky[pozice] = nova
        print(f"{vlastnik.jmeno} verboval jednotku typu {typ} na pozici {pozice}.")
        self.pocitadlo_id = self.pocitadlo_id+1
        return nova

    # NEXT: V plné verzi tady bude muset být kontrola, že se pozicie nepřekrývají
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
        #spravce_hry.pohyb_jednotek_ai(hrac)
        spravce_hry.ai_pohyb_a_utok(hrac)

        # Stavba budov a verbování jednotek
        # TODO: Zakomentovávám, protože nebude použito v rámci testování scénářů.

        #spravce_hry.stavba_a_verbovani_ai(hrac, zisk, naklady)


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


    def _vyber_ai_cile(self, utocici_jednotka, ai_weights):
        # TODO: Zkontrolovat
        # TODO: Zkontrolovat
        # TODO: Zkontrolovat
        # IDEA: Už mám funkci na výběr nejslabší jednotky v dosahu, to by celkem dávalo smysl použít
        vazene_cile_list = []
        mozne_cile = utocici_jednotka.najdi_cile_v_dosahu(self.mrizka, self.jednotky)
        for cil in mozne_cile:
            vaha = 0
            if cil.dosah > 1:  # Předpokládáme, že jednotky s dosahem > 1 jsou střelecké
                vaha = ai_weights['target_priority_ranged']
            else:
                vaha = ai_weights['target_priority_melee']

            # Přidat další faktory do váhy, např. nízké životy cíle
            if hasattr(cil, 'zivoty') and hasattr(cil, 'zivoty_max') and cil.zivoty < cil.zivoty_max / 2:
                vaha *= 1.5  # Vyšší priorita pro zraněné cíle

            vazene_cile_list.append((cil, vaha))

        if not vazene_cile_list:
            return None

        # Vyberte cíl na základě vah
        # random.choices vrací seznam, takže vezmeme první prvek
        vybrany_cil = random.choices([c for c, w in vazene_cile_list], weights=[w for c, w in vazene_cile_list], k=1)
        return vybrany_cil[0]

    def nepratele_v_bezprostredni_blizkosit(self, x, y, hrac):
        nepratelske_jednotky = {pozice: j for pozice, j in self.jednotky.items() if j.vlastnik != hrac}

        nepratele_v_bezprostrednim_dosahu = []
        for pozice_nepritele, nepritel in nepratelske_jednotky.items():
            if abs(x - pozice_nepritele[0]) + abs(y - pozice_nepritele[1]) <= 1:
                nepratele_v_bezprostrednim_dosahu.append(nepritel)

        return nepratele_v_bezprostrednim_dosahu



    def ai_pohyb_a_utok(self, hrac):
        for jednotka in hrac.jednotky:

            x, y = jednotka.pozice

            nahodnost = random.random()
            if nahodnost < 0.1:
                self.jednotka_pohyb_nahodny_nebo_k_nepritely(jednotka)
            else:
                cile_v_dosahu = jednotka.najdi_cile_v_dosahu(self.mrizka, self.jednotky)
                if cile_v_dosahu: #IDEA: Nepřátelé v dosahu
                    utok_probehl = False # Kontrola jestli jednotka provedla útok

                    if jednotka.dosah > 1: # IDEA: Střelecká jednotka

                        nepratele_v_bezprostrednim_dosahu = self.nepratele_v_bezprostredni_blizkosit(x,y, hrac)

                        if nepratele_v_bezprostrednim_dosahu:
                            mozne_pohyby = jednotka.vypocet_moznych_pohybu(self.mrizka, self.jednotky)

                            nejblizsi_nepritel_vedle = nepratele_v_bezprostrednim_dosahu[0]

                            nejlepsi_utekova_pozice = None
                            max_vzdalenost_od_nepritele_po_pohybu = -1

                            for nova_pozice in mozne_pohyby:
                                # jednotka z nové pozice dosáhne na nejbližšího nepřítele_vedle
                                vzdalenost_k_nepriteli_z_nove_pozice = abs(
                                    nova_pozice[0] - nejblizsi_nepritel_vedle.pozice[0]) + abs(
                                    nova_pozice[1] - nejblizsi_nepritel_vedle.pozice[1])

                                if jednotka.dosah >= vzdalenost_k_nepriteli_z_nove_pozice:  # Pokud stále dosáhneme
                                    # Pokud je tato nová pozice dál od nepřítele než dosavadní nejlepší
                                    if vzdalenost_k_nepriteli_z_nove_pozice > max_vzdalenost_od_nepritele_po_pohybu:
                                        max_vzdalenost_od_nepritele_po_pohybu = vzdalenost_k_nepriteli_z_nove_pozice
                                        nejlepsi_utekova_pozice = nova_pozice

                            if nejlepsi_utekova_pozice:
                                # Přesuň se na nalezenou únikovou pozici a zaútoč na nejbližšího nepřítele
                                jednotka.proved_pohyb(nejlepsi_utekova_pozice, mozne_pohyby, self.jednotky)
                                print(
                                    f"Jednotka s dlouhým dosahem na pozici {(x, y)} se posunula na {jednotka.pozice} (dál od {nejblizsi_nepritel_vedle.typ} na {nejblizsi_nepritel_vedle.pozice}) a zaútočila.")
                                self.vyhodnot_souboj(jednotka, nejblizsi_nepritel_vedle)
                                utok_probehl = True

                    if not utok_probehl: # IDEA: Boj na blízko
                        vybrany_cil = self._vyber_ai_cile(jednotka, self.ai_decision_weights)
                        if vybrany_cil:
                            self.vyhodnot_souboj(jednotka, vybrany_cil)

                else: # IDEA: Není nepřítel v dosahu
                    mozne_pohyby = jednotka.vypocet_moznych_pohybu(self.mrizka, self.jednotky)

                    # IDEA: Nepřítel je v dosahu po pohybu
                    neni_nepritel_v_dosahu = True
                    for moznost in mozne_pohyby:  # posouvám dočaně jednotku na novou pozici a testuju jestli na někoho dosáhne

                        nepratele_v_dosahu = jednotka.najdi_cile_v_dosahu_z_pozice(moznost, self.mrizka,
                                                                                   self.jednotky)
                        if nepratele_v_dosahu:  # Existuje nepřítel v dosahu
                            neni_nepritel_v_dosahu = False

                            jednotka.proved_pohyb(moznost, mozne_pohyby, self.jednotky)
                            print("K pohybu došlo tady")
                            vybrany_cil = self._vyber_ai_cile(jednotka, self.ai_decision_weights)
                            if vybrany_cil:
                                self.vyhodnot_souboj(jednotka, vybrany_cil)
                                print(f"Jednotka se posunula z pozice {(x, y)} na {jednotka.pozice} a provedla útok.")
                            break

                    # IDEA: V okolí není nepřítel:
                    if neni_nepritel_v_dosahu:
                        self.jednotka_pohyb_nahodny_nebo_k_nepritely(jednotka)

    def jednotka_pohyb_nahodny_nebo_k_nepritely(self, jednotka):
        mozne_pohyby = jednotka.vypocet_moznych_pohybu(self.mrizka, self.jednotky)
        nahodnost = random.random()
        if nahodnost < 0.5:  # Padesát na padesát že půjde náhodně nebo za cílem
            # Náhodný pohyb
            self.nahodny_pohyb(jednotka, mozne_pohyby)
        else:
            # Pohyb směrem k nepřátelské jednotce
            pozice = self.nahodna_jednotka_nepritele_pozice(jednotka)

            cesta = self.pohyb_smerem_na(jednotka, pozice, self.mrizka)
            if cesta:
                jednotka.proved_pohyb(cesta, [cesta], self.jednotky)
                print(f"Jednotka {jednotka.typ} se pohybuje směrem k nepříteli na pozici {cesta}")
            else:
                self.konec(hrac, self.hraci[1] if hrac == self.hraci[0] else
                self.hraci[0], "Něco se nepovedlo při tahu hráče: ")

    def nahodny_pohyb(self, jednotka, mozne_pohyby):
        print(mozne_pohyby)
        random.shuffle(mozne_pohyby)
        print(mozne_pohyby)
        jednotka.proved_pohyb(mozne_pohyby[0], mozne_pohyby, self.jednotky)
        print(f"Jednotka {jednotka.typ} se rozhodla k náhodnému pohybu na pozici: {mozne_pohyby[0]}.")

    def nahodna_jednotka_nepritele_pozice(self, jednotka):
        # TODO: Zkontrolovat, že se vrací správná starna slovníku
        pozice_jednotek = []
        for pozice, j in self.jednotky.items():
            if j.vlastnik != jednotka.vlastnik:
                pozice_jednotek.append(pozice)

        if pozice_jednotek:
            random.shuffle(pozice_jednotek)
            return pozice_jednotek[0]
        else:
            print("Něco se rozflákalo při hledání nepřátel ve velké vzdálenosti.")
            return None


    def stavba_a_verbovani_ai(spravce_hry, hrac, zisk, naklady):
        pocet_pokusu = 0
        while pocet_pokusu < 11 and spravce_hry.stav_hry:
            if naklady.get('jidlo', 0) >= zisk.get('jidlo', 0):
                zisk = spravce_hry.postav_budovu_pro_surovinu(hrac, 'jidlo', zisk)
            elif naklady.get('drevo', 0) >= zisk.get('drevo', 0):
                zisk = spravce_hry.postav_budovu_pro_surovinu(hrac, 'drevo', zisk)
            elif naklady.get('kamen', 0) >= zisk.get('kamen', 0):
                zisk = spravce_hry.postav_budovu_pro_surovinu(hrac, 'kamen', zisk)
            else:
                # IDEA: Dostatek suroin, můžeme budovat nové věci.
                verbovani_nebo_stvba = random.random()
                if verbovani_nebo_stvba < 0.1:
                    # IDEA: Staba náhodné budovy
                    print("Stavba náhodné budovy")
                    budovy = list(spravce_hry.BUDOVY_SABLONY.keys())
                    zisk = spravce_hry.postav_budovu(hrac, budovy, zisk)
                else:
                    print("Verbování jednotky")
                    spravce_hry.naverj_jednotku(hrac, naklady)

            pocet_pokusu += 1
        return zisk

    def postav_budovu_pro_surovinu(spravce_hry, hrac, surovina, zisk):
        print(f"Stavím budovu pro {surovina}")
        budovy = list(spravce_hry.budovy_pro_surovinu(surovina).keys())
        return spravce_hry.postav_budovu(hrac, budovy, zisk)

    def postav_budovu(spravce_hry, hrac, budovy, zisk):
        nahodne_cislo = randint(0, len(budovy) - 1)
        temp_budova = spravce_hry.stavba_budovy(spravce_hry.budovy, budovy[nahodne_cislo], (0, 0), hrac)
        return spravce_hry.aktualizace_zisku(temp_budova, zisk)

    def naverj_jednotku(spravce_hry, hrac, naklady):
        #jednotky = list(spravce_hry.JEDNOTKY_SABLONY.keys())
        jednotky = [j for j in spravce_hry.JEDNOTKY_SABLONY.keys() if j != 'zakladna']
        nahodne_cislo = randint(0, len(jednotky) - 1)
        temp_jednotka = spravce_hry.verbovani(jednotky[nahodne_cislo], hrac, spravce_hry.jednotky)
        return spravce_hry.aktualizace_nakladu(temp_jednotka, naklady)

    def aktualizace_nakladu(spravce_hry, jednotka, naklady):
        """
                Aktualizuje nákladů po naverbování jednotky.
                Args:
                    jednotka: Instance nově naverbované jednotky.
                    naklady: Aktuální náklady za kolo.
                return:
                    Náklady za kolo po naverbování jednotky.
                """
        if jednotka is None:
            print("Jednotku se nepodařilo naverbovat.")
            return naklady
        else:
            for surovina, hodnota in jednotka.cena_za_kolo.items():
                naklady[surovina] = naklady.get(surovina, 0) + hodnota
            return naklady

    def pohyb_smerem_na(spravce_hry, jednotka, cilove_pozice, mrizka):
        """
        Vybírá pozici která ho nejvíce přihližuje základně nepřítele.

        Args:
            jednotka: Jednotka která nemá v dosahu nepřítele.
            cilove_pozice: Pozice ke které se jednotka snaží dostat.
            mrizka: Herní pole.
        return: (x, y) krok který se nejvíce blíží cílové pozici.

        """
        mozne_pozice = jednotka.vypocet_moznych_pohybu(mrizka, spravce_hry.jednotky)
        vzdalenost = float('inf')
        nejlepsi_pozice = None
        for pozice in mozne_pozice:
            vzdalenost_temp = abs(cilove_pozice[0] - pozice[0]) + abs(cilove_pozice[1] - pozice[1])
            if vzdalenost_temp < vzdalenost:
                vzdalenost = vzdalenost_temp
                nejlepsi_pozice = pozice

        return nejlepsi_pozice

    def existuje_cesta_mezi_zakladnami(spravce_hry, start, cil, mrizka):
        """
        Zjistí, jestli existuje cesta mezi dvěma základnami a pokud ano, jak drahá.

        Args:
            start: (x, y) pozice začátku (např. tvoje základna)
            cil: (x, y) cílová pozice (nepřátelská základna)
            mrizka: herní mřížka

        Returns:
            (True/False, cena_cesty) pokud existuje cesta, nebo (False, None)
        """
        # Definice cen podle terénu
        cena_terenu = {
            'P': 1,
            'L': 3,
            'H': 5,
            'W': float('inf')  # nepřístupné
        }

        sirka, vyska = len(mrizka[0]), len(mrizka)
        navstiveno = set()
        fronta = [(0, start)]  # (cena_doposud, pozice)

        while fronta:
            # Najdeme prvek s nejnižší cenou (nejlevnější zatím nalezený bod)
            fronta.sort()  # seřadíme podle ceny
            cena, pozice = fronta.pop(0)  # vezmeme nejlevnější

            if pozice == cil:
                return True, cena  # našli jsme cestu

            if pozice in navstiveno:
                continue
            navstiveno.add(pozice)

            x, y = pozice
            sousedi = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

            for nx, ny in sousedi:
                if 0 <= nx < sirka and 0 <= ny < vyska:
                    typ_terenu = mrizka[ny][nx]
                    cena_pohybu = cena_terenu.get(typ_terenu, float('inf'))

                    if cena_pohybu < float('inf') and (nx, ny) not in navstiveno:
                        fronta.append((cena + cena_pohybu, (nx, ny)))

        return False, None  # žádná cesta neexistuje



