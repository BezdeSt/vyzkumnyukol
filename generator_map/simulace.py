import datetime
import csv

class LoggerSimulace:
    def __init__(self, scenar_nazev, poznamka=None):
        self.scenar_nazev = scenar_nazev
        self.poznamka = poznamka
        self.cas_startu = datetime.datetime.now()
        self.log_prubehu = {}  # Kolo: {jednotka_id: {'typ', 'zivoty', 'vlastnik'}}
        self.log_poskozeni = {} # Kolo: {typ_jednotky: {'zpusobene': celkem, 'utrzene': celkem, 'utok': [], 'realne': []}}
        self.log_smrti = {}      # Kolo: [typ_jednotky]
        self.vysledky_simulaci = []

    def log_stav_kola(self, kolo, jednotky):
        stav_kola = {}
        for jednotka_id, jednotka_instance in jednotky.items():
            stav_kola[jednotka_id] = {
                'typ': jednotka_instance.typ,
                'zivoty': jednotka_instance.zivoty,
                'vlastnik': jednotka_instance.vlastnik.jmeno if jednotka_instance.vlastnik else None
            }
        self.log_prubehu[kolo] = stav_kola

    def uloz_vysledek_simulace(self, vitezny_hrac, pocet_kol, jednotky):
        vysledek = {
            'scenar': self.scenar_nazev,
            'vitez': vitezny_hrac.jmeno if vitezny_hrac else 'remiza',
            'pocet_kol': pocet_kol
        }
        zpusobene_celkem = {}
        utrzene_celkem = {}
        for jednotka_id, jednotka_instance in jednotky.items():
            typ = jednotka_instance.typ
            zpusobene_celkem[typ] = zpusobene_celkem.get(typ, 0) + jednotka_instance.celkem_zpusobene_poskozeni
            utrzene_celkem[typ] = utrzene_celkem.get(typ, 0) + jednotka_instance.celkem_prijate_poskozeni
            prefix = f"{typ.lower().replace('ě', 'e').replace('š', 's').replace('č', 'c').replace('ř', 'r').replace('ž', 'z').replace('ý', 'y')}"
            vysledek[f'{prefix}_zpusobene'] = jednotka_instance.celkem_zpusobene_poskozeni
            vysledek[f'{prefix}_prijate'] = jednotka_instance.celkem_prijate_poskozeni

        vysledek.update({f'celkem_zpusobene_{typ.lower()}': damage for typ, damage in zpusobene_celkem.items()})
        vysledek.update({f'celkem_utrzene_{typ.lower()}': damage for typ, damage in utrzene_celkem.items()})

        self.vysledky_simulaci.append(vysledek)

    def uloz_vysledky_do_souboru(self, nazev_souboru='vysledky_simulaci.csv'):
        with open(nazev_souboru, 'w', newline='') as csvfile:
            fieldnames = self.vysledky_simulaci[0].keys() if self.vysledky_simulaci else []
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for vysledek in self.vysledky_simulaci:
                writer.writerow(vysledek)

        print(f"Výsledky simulací pro scénář '{self.scenar_nazev}' uloženy do souboru: {nazev_souboru}")

    def vypis_vysledky(self):
        print(f"=== Výsledky souhrnné simulace pro scénář: {self.scenar_nazev} ===")
        print(f"Začátek simulace: {self.cas_startu.strftime('%Y-%m-%d %H:%M:%S')}")
        if self.poznamka:
            print(f"Poznámka: {self.poznamka}")
        print(f"Počet simulací: {len(self.vysledky_simulaci)}")

        if self.vysledky_simulaci:
            for vysledek in self.vysledky_simulaci:
                print("\n--- Výsledek simulace ---")
                print(f"Vítěz: {vysledek.get('vitez', 'N/A')}")
                print(f"Počet kol: {vysledek.get('pocet_kol', 'N/A')}")
                # Můžete zde přidat výpis dalších statistik z 'vysledek' slovníku
                # Například:
                # for k, v in vysledek.items():
                #     if k not in ['scenar', 'vitez', 'pocet_kol']:
                #         print(f"{k}: {v}")
        else:
            print("Žádné výsledky simulace nebyly zaznamenány.")

    def vypis_prubeh(self):
        print(f"\n=== Průběh simulace pro scénář: {self.scenar_nazev} ===")
        for kolo in sorted(self.log_prubehu.keys()):
            print(f"\n--- Kolo {kolo} ---")
            if kolo in self.log_prubehu:
                print("Stav jednotek:")
                for jednotka_id, info in self.log_prubehu[kolo].items():
                    print(f"  {info['typ']} (vlastník: {info['vlastnik']}) - Životy: {info['zivoty']}")
            if kolo in self.log_poskozeni:
                print("Způsobené a utržené poškození:")
                for typ, poskozeni in self.log_poskozeni[kolo].items():
                    print(f"  {typ}: Způsobené={poskozeni['zpusobene']}, Utržené={poskozeni['utrzene']}, Útoky={poskozeni['utok']}, Reálné={poskozeni['realne']}")
            if kolo in self.log_smrti:
                print("Smrti:")
                for smrt in self.log_smrti[kolo]:
                    print(f"  Jednotka typu {smrt} zemřela")
        print("\n=== Konec průběhu ===")

    def log_utok(self, kolo, utocnik, napadeny, utok, realne_poskozeni):
        utocnik_typ = utocnik.typ
        if kolo not in self.log_poskozeni:
            self.log_poskozeni[kolo] = {}
        if utocnik_typ not in self.log_poskozeni[kolo]:
            self.log_poskozeni[kolo][utocnik_typ] = {'zpusobene': 0, 'utrzene': 0, 'utok': [], 'realne': []}
        self.log_poskozeni[kolo][utocnik_typ]['zpusobene'] += realne_poskozeni
        self.log_poskozeni[kolo][utocnik_typ]['utok'].append(utok)
        self.log_poskozeni[kolo][utocnik_typ]['realne'].append(realne_poskozeni)

        napadnuty_typ = napadeny.typ
        if napadnuty_typ not in self.log_poskozeni[kolo]:
            self.log_poskozeni[kolo][napadnuty_typ] = {'zpusobene': 0, 'utrzene': 0, 'utok': [], 'realne': []}
        self.log_poskozeni[kolo][napadnuty_typ]['utrzene'] += realne_poskozeni

    def log_smrt_jednotky(self, kolo, jednotka_typ):
        if kolo not in self.log_smrti:
            self.log_smrti[kolo] = []
        self.log_smrti[kolo].append(jednotka_typ)