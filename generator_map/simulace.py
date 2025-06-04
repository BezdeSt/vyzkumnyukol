import datetime
import csv
import os

class LoggerSimulace:
    def __init__(self, id_simulace, scenar_nazev, poznamka=None):
        self.id_simulace = id_simulace # Nové: nyní jednoduchý int
        self.scenar_nazev = scenar_nazev
        self.poznamka = poznamka
        self.cas_startu = datetime.datetime.now()

        # Logy pro detailní průběh kola za kolem
        self.log_prubehu = {}
        self.log_poskozeni = {}
        self.log_poctu_utoku_protiutoku = {}
        self.log_smrti = {}
        self.vitez_simulace = None

        # Nové: Slovník pro ukládání startovních atributů jednotek
        # Klíč: (typ_jednotky, vlastnik_jmeno)
        self.log_jednotky_metadata = {}

    def log_stav_kola(self, kolo, jednotky):
        """
        Zaznamená aktuální stav všech jednotek na konci daného kola (nebo na začátku pro kolo 0).
        Zahrnuje i jednotky s 0 životy, které právě zemřely, ale byly aktivní v tomto kole.
        """
        relevantni_jednotky_klice = set()

        # Přidej klíče živých jednotek
        for jednotka_id, jednotka_instance in jednotky.items():
            if jednotka_instance and hasattr(jednotka_instance, 'typ') and hasattr(jednotka_instance, 'vlastnik'):
                relevantni_jednotky_klice.add((jednotka_instance.typ,
                                               jednotka_instance.vlastnik.jmeno if jednotka_instance.vlastnik else "Neutral"))

        # Přidej klíče jednotek, které způsobily/utržily poškození v tomto kole
        if kolo in self.log_poskozeni:
            for klic_jednotky in self.log_poskozeni[kolo].keys():
                relevantni_jednotky_klice.add(klic_jednotky)

        # Přidej klíče jednotek, které zemřely v tomto kole
        if kolo in self.log_smrti:
            for smrt_info in self.log_smrti[kolo]:
                relevantni_jednotky_klice.add((smrt_info['typ'], smrt_info['vlastnik']))

        # Přidej klíče jednotek, které útočily nebo protiútovaly v tomto kole
        if kolo in self.log_poctu_utoku_protiutoku:
            for klic_jednotky in self.log_poctu_utoku_protiutoku[kolo].keys():
                relevantni_jednotky_klice.add(klic_jednotky)

        stav_kola_zaznamy = {}

        for typ_jednotky, vlastnik_jmeno in relevantni_jednotky_klice:
            # Nově: Agregujeme životy a počet živých jednotek pro daný typ a vlastníka
            agregovane_zivoty = 0
            agregovane_zive_jednotky_count = 0

            # Projdeme VŠECHNY živé jednotky v aktuálním kole a sečteme je
            for jednotka_id, j_instance in jednotky.items():
                if j_instance.typ == typ_jednotky and (
                j_instance.vlastnik.jmeno if j_instance.vlastnik else "Neutral") == vlastnik_jmeno:
                    agregovane_zivoty += j_instance.zivoty
                    agregovane_zive_jednotky_count += 1

            # Získání dat o poškození pro tuto jednotku v tomto kole
            data_poskozeni = self.log_poskozeni.get(kolo, {}).get((typ_jednotky, vlastnik_jmeno), {
                'zpusobene': 0,
                'realne_zpusobene': 0,
                'utrzene': 0
            })

            # Získání dat o počtu útoků a protiútoků
            utoky_data = self.log_poctu_utoku_protiutoku.get(kolo, {}).get((typ_jednotky, vlastnik_jmeno), {
                'utoky': 0,
                'protiutoky': 0
            })

            stav_kola_zaznamy[(typ_jednotky, vlastnik_jmeno)] = {
                'typ': typ_jednotky,
                'zivoty': agregovane_zivoty,  # Použijeme agregované životy
                'vlastnik': vlastnik_jmeno,
                'zive_jednotky_count': agregovane_zive_jednotky_count,  # Použijeme agregovaný počet živých jednotek
                'zpusobene_poskozeni_kolo': data_poskozeni['zpusobene'],
                'realne_zpusobene_poskozeni_kolo': data_poskozeni['realne_zpusobene'],
                'utrzene_poskozeni_kolo': data_poskozeni['utrzene'],
                'pocet_utoku_kolo': utoky_data['utoky'],
                'pocet_protiutoku_kolo': utoky_data['protiutoky']
            }

        self.log_prubehu[kolo] = stav_kola_zaznamy

    def log_utok(self, kolo, utocnik, napadeny, utok_hodnota, realne_poskozeni_hodnota, je_protiutok=False):
        """
        Zaznamená detail útoku, s informacemi o typu a vlastníkovi útočníka i napadeného.
        Předpokládá, že utok_hodnota a realne_poskozeni_hodnota jsou již vypočítány.
        Přidán parametr 'je_protiutok' pro rozlišení.
        """
        utocnik_typ = utocnik.typ
        utocnik_vlastnik = utocnik.vlastnik.jmeno if utocnik.vlastnik else "Neutral"

        napadnuty_typ = napadeny.typ
        napadnuty_vlastnik = napadeny.vlastnik.jmeno if napadeny.vlastnik else "Neutral"

        if kolo not in self.log_poskozeni:
            self.log_poskozeni[kolo] = {}
        if kolo not in self.log_poctu_utoku_protiutoku:
            self.log_poctu_utoku_protiutoku[kolo] = {}

        # Zaznamenat způsobené poškození pro útočníka
        klic_utocnik = (utocnik_typ, utocnik_vlastnik)
        if klic_utocnik not in self.log_poskozeni[kolo]:
            self.log_poskozeni[kolo][klic_utocnik] = {'zpusobene': 0, 'realne_zpusobene': 0, 'utrzene': 0}
        self.log_poskozeni[kolo][klic_utocnik]['zpusobene'] += utok_hodnota
        self.log_poskozeni[kolo][klic_utocnik]['realne_zpusobene'] += realne_poskozeni_hodnota

        # Zaznamenat utržené poškození pro napadeného
        klic_napadeny = (napadnuty_typ, napadnuty_vlastnik)
        if klic_napadeny not in self.log_poskozeni[kolo]:
            self.log_poskozeni[kolo][klic_napadeny] = {'zpusobene': 0, 'realne_zpusobene': 0, 'utrzene': 0}
        self.log_poskozeni[kolo][klic_napadeny]['utrzene'] += realne_poskozeni_hodnota

        # Nové: Zaznamenání počtu útoků/protiútoků
        if klic_utocnik not in self.log_poctu_utoku_protiutoku[kolo]:
            self.log_poctu_utoku_protiutoku[kolo][klic_utocnik] = {'utoky': 0, 'protiutoky': 0}

        if je_protiutok:
            self.log_poctu_utoku_protiutoku[kolo][klic_utocnik]['protiutoky'] += 1
        else:
            self.log_poctu_utoku_protiutoku[kolo][klic_utocnik]['utoky'] += 1

    def log_smrt_jednotky(self, kolo, jednotka_instance):
        """
        Zaznamená úmrtí jednotky, s informacemi o jejím typu a vlastníkovi.
        Předpokládá, že jednotka_instance je objekt s atributy .typ a .vlastnik.
        """
        if kolo not in self.log_smrti:
            self.log_smrti[kolo] = []
        self.log_smrti[kolo].append({
            'typ': jednotka_instance.typ,
            'vlastnik': jednotka_instance.vlastnik.jmeno if jednotka_instance.vlastnik else "Neutral"
        })

    def log_startovni_atributy_jednotky(self, jednotka_instance):
        """
        Zaznamená startovní atributy jednotky.
        Ukládá se pouze první zaznamenané atributy pro daný typ a vlastníka,
        protože jednotky stejného typu a vlastníka mají v této simulaci stejné počáteční atributy.
        """
        vlastnik_jmeno = jednotka_instance.vlastnik.jmeno if jednotka_instance.vlastnik else "Neutral"
        klic = (jednotka_instance.typ, vlastnik_jmeno)

        if klic not in self.log_jednotky_metadata:
            self.log_jednotky_metadata[klic] = {
                'typ_jednotky': jednotka_instance.typ,
                'vlastnik': vlastnik_jmeno,
                'utok_start': jednotka_instance.utok,
                'obrana_start': jednotka_instance.obrana,
                'zivoty_start': jednotka_instance.max_zivoty,
                'rychlost_start': jednotka_instance.rychlost,
                'dosah_start': jednotka_instance.dosah
            }

    def uloz_vysledek_simulace(self, vitezny_hrac, pocet_kol, jednotky):
        """
        Nastaví vítěze simulace pro použití v uloz_prubeh_do_souboru.
        Tato metoda již neslouží k ukládání do samostatného souboru.
        """
        self.vitez_simulace = vitezny_hrac.jmeno if vitezny_hrac else 'remiza'
        pass

    def uloz_prubeh_do_souboru(self, nazev_souboru='prubeh_simulaci.csv'):
        """
        Zapíše detailní průběh simulace kola za kolem do JEDNOHO CSV souboru.
        Zahrnuje počáteční stav (kolo 0) a výsledek (vítěze) v posledním kole.
        """
        soubor_existuje = os.path.isfile(nazev_souboru)

        pole_hlavice = [
            'id_simulace', 'scenar_nazev', # Nové: ID a název scénáře
            'kolo', 'typ_jednotky', 'vlastnik', 'zive_jednotky', 'celkove_zivoty',
            'zpusobene_poskozeni_kolo', 'realne_zpusobene_poskozeni_kolo',
            'utrzene_poskozeni_kolo', 'pocet_utoku_kolo', 'pocet_protiutoku_kolo', 'vitez'
        ]
        writer_mode = 'a' if soubor_existuje else 'w' # Používáme 'w' pro první zápis, 'a' pro append

        with open(nazev_souboru, writer_mode, newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=pole_hlavice)

            if not soubor_existuje:
                writer.writeheader()

            vsechny_typy_vlastnici = set()
            for kolo_num, kolo_data_agregovana in self.log_prubehu.items():
                for klic in kolo_data_agregovana.keys():
                    vsechny_typy_vlastnici.add(klic)

            posledni_kolo = max(self.log_prubehu.keys(), default=0)

            vsechna_kolo_v_logu = sorted(list(self.log_prubehu.keys()))

            for kolo in vsechna_kolo_v_logu:
                for typ_jednotky, vlastnik in sorted(list(vsechny_typy_vlastnici)):

                    jednotka_data = self.log_prubehu.get(kolo, {}).get((typ_jednotky, vlastnik), {})

                    zive_jednotky = jednotka_data.get('zive_jednotky_count', 0)
                    celkove_zivoty = jednotka_data.get('zivoty', 0)
                    zpusobene_poskozeni_kolo = jednotka_data.get('zpusobene_poskozeni_kolo', 0)
                    realne_zpusobene_poskozeni_kolo = jednotka_data.get('realne_zpusobene_poskozeni_kolo', 0)
                    utrzene_poskozeni_kolo = jednotka_data.get('utrzene_poskozeni_kolo', 0)
                    pocet_utoku_kolo = jednotka_data.get('pocet_utoku_kolo', 0)
                    pocet_protiutoku_kolo = jednotka_data.get('pocet_protiutoku_kolo', 0)

                    aktualni_vitez = ""
                    if kolo == posledni_kolo:
                        aktualni_vitez = self.vitez_simulace

                    writer.writerow({
                        'id_simulace': self.id_simulace, # Zde se přidává ID simulace
                        'scenar_nazev': self.scenar_nazev, # Zde se přidává název scénáře
                        'kolo': kolo,
                        'typ_jednotky': typ_jednotky,
                        'vlastnik': vlastnik,
                        'zive_jednotky': zive_jednotky,
                        'celkove_zivoty': celkove_zivoty,
                        'zpusobene_poskozeni_kolo': zpusobene_poskozeni_kolo,
                        'realne_zpusobene_poskozeni_kolo': realne_zpusobene_poskozeni_kolo,
                        'utrzene_poskozeni_kolo': utrzene_poskozeni_kolo,
                        'pocet_utoku_kolo': pocet_utoku_kolo,
                        'pocet_protiutoku_kolo': pocet_protiutoku_kolo,
                        'vitez': aktualni_vitez
                    })

        print(f"Průběh simulací pro scénář '{self.scenar_nazev}' (ID: {self.id_simulace}) byl přidán do souboru: {nazev_souboru}")

    def uloz_metadata_jednotek_do_souboru(self, nazev_souboru='metadata_jednotek.csv'):
        """
        Uloží startovní atributy všech typů jednotek v této simulaci do samostatného CSV souboru.
        """
        soubor_existuje = os.path.isfile(nazev_souboru)

        pole_hlavice = [
            'id_simulace', 'scenar_nazev',
            'typ_jednotky', 'vlastnik',
            'utok_start', 'obrana_start', 'zivoty_start', 'rychlost_start', 'dosah_start'
        ]
        writer_mode = 'a' if soubor_existuje else 'w' # Používáme 'w' pro první zápis, 'a' pro append


        with open(nazev_souboru, writer_mode, newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=pole_hlavice)

            if not soubor_existuje:
                writer.writeheader()

            for klic, data in self.log_jednotky_metadata.items():
                writer.writerow({
                    'id_simulace': self.id_simulace,
                    'scenar_nazev': self.scenar_nazev,
                    'typ_jednotky': data['typ_jednotky'],
                    'vlastnik': data['vlastnik'],
                    'utok_start': data['utok_start'],
                    'obrana_start': data['obrana_start'],
                    'zivoty_start': data['zivoty_start'],
                    'rychlost_start': data['rychlost_start'],
                    'dosah_start': data['dosah_start']
                })
        print(f"Metadata jednotek pro scénář '{self.scenar_nazev}' (ID: {self.id_simulace}) byla přidána do souboru: {nazev_souboru}")

    def vypis_vysledky(self):
        print(f"=== Výsledky souhrnné simulace pro scénář: {self.scenar_nazev} ===")
        print(f"Začátek simulace: {self.cas_startu.strftime('%Y-%m-%d %H:%M:%S')}")
        if self.poznamka:
            print(f"Poznámka: {self.poznamka}")
        print("Souhrnné výsledky nejsou ukládány do samostatného listu v loggeru.")
        print(f"Vítěz této simulace: {self.vitez_simulace}")

    def vypis_prubeh(self):
        """
        Vypíše detailní průběh simulace na konzoli.
        """
        print(f"\n=== Průběh simulace pro scénář: {self.scenar_nazev} ===")

        vsechna_kolo_v_logu = sorted(list(self.log_prubehu.keys()))

        for kolo in vsechna_kolo_v_logu:
            print(f"\n--- Kolo {kolo} ---")

            if kolo in self.log_prubehu:
                print("Stav jednotek a agregovaná data:")
                for (typ, vlastnik), info_agregovane in self.log_prubehu[kolo].items():
                    print(
                        f"  Typ: {typ}, Vlastník: {vlastnik}, Životy: {info_agregovane['zivoty']},"
                        f" Živé jednotky: {info_agregovane['zive_jednotky_count']},"
                        f" Způsobené: {info_agregovane['zpusobene_poskozeni_kolo']},"
                        f" Utržené: {info_agregovane['utrzene_poskozeni_kolo']},"
                        f" Útoky: {info_agregovane['pocet_utoku_kolo']},"
                        f" Protiútoky: {info_agregovane['pocet_protiutoku_kolo']}"
                    )