import datetime
import csv
import os

class LoggerSimulace:
    def __init__(self, id_simulace, scenar_nazev, poznamka=None):
        self.id_simulace = id_simulace # Nové: nyní jednoduchý int
        self.scenar_nazev = scenar_nazev
        self.poznamka = poznamka
        self.cas_startu = datetime.datetime.now()

        # Log pro detailní průběh kola za kolem (nová struktura)
        # Klíč: kolo (int)
        # Hodnota: slovník, kde klíč je ID jednotky a hodnota je slovník s jejími atributy
        self.log_jednotek_detail_kola = {}

        # Dočasný seznam jednotek, které zemřely v aktuálním kole
        # Klíč: ID jednotky, Hodnota: instance jednotky (s konečným stavem)
        self.nedavno_zemrele_jednotky_kolo = {}

        # Celkové výsledky simulace
        self.vitez_simulace = None
        self.pocet_kol = 0

    def log_umirajici_jednotku(self, jednotka):
        """
        Zaznamená jednotku, která právě zemřela, do dočasného seznamu.
        Tato jednotka bude zalogována v aktuálním kole s 0 životy.
        """
        self.nedavno_zemrele_jednotky_kolo[jednotka.id] = jednotka

    def log_stav_kola(self, kolo, aktivni_jednotky, id_simulace):
        """
        Zaznamená aktuální stav všech jednotek na konci daného kola (nebo na začátku pro kolo 0).
        Zahrnuje aktivní jednotky i ty, které zemřely v tomto kole.
        """
        if kolo not in self.log_jednotek_detail_kola:
            self.log_jednotek_detail_kola[kolo] = {}

        # Kombinace aktivních a právě zemřelých jednotek pro logování
        jednotky_k_logovani = {}
        for jednotka_id, jednotka_instance in aktivni_jednotky.items():
            jednotky_k_logovani[jednotka_id] = jednotka_instance
        for jednotka_id, jednotka_instance in self.nedavno_zemrele_jednotky_kolo.items():
            # Pokud by náhodou mrtvá jednotka byla stále v aktivních,
            # tato verze zaručí, že se zaloguje její finální stav (0 životů)
            jednotky_k_logovani[jednotka_id] = jednotka_instance

        for jednotka_id, jednotka_instance in jednotky_k_logovani.items():
            info = jednotka_instance.ziskej_info()
            info['kolo'] = kolo
            info['id_simulace'] = id_simulace
            self.log_jednotek_detail_kola[kolo][jednotka_instance.id] = info

        # Po zalogování vyprázdníme seznam nedávno zemřelých jednotek
        self.nedavno_zemrele_jednotky_kolo.clear()

    def uloz_logy_do_csv(self):
        """
        Uloží detailní log jednotek do CSV souboru (agregovaně podle scénáře)
        a souhrnné výsledky simulace (přidáním řádku).
        """
        # Vytvoření složky pro logy, pokud neexistuje
        if not os.path.exists('sim_logy'):
            os.makedirs('sim_logy')

        # --- Definujte preferované pořadí sloupců zde ---
        # Tyto sloupce se objeví v CSV v tomto pořadí.
        # Ostatní sloupce budou přidány na konec v abecedním pořadí.
        PREFERRED_FIELD_ORDER = [
            'id_simulace',
            'kolo',
            'id',
            'typ',
            'vlastnik',
            'pozice',
            'zivoty',
            'max_zivoty',
            'utok_min',
            'utok_max',
            'obrana',
            'rychlost',
            'dosah',
            'crit',
            'uhyb',
            'utoky_za_kolo',
            'protiutoky_za_kolo',
            'kriticke_zasahy_za_kolo',
            'uhyby_za_kolo',
            'zpusobene_poskozeni_za_kolo',
            'prijate_poskozeni_za_kolo',
        ]
        # --- Konec definice preferovaného pořadí ---

        detail_csv_path = os.path.join('sim_logy', f'{self.scenar_nazev}.csv')

        # Získání všech unikátních klíčů ze všech dat pro určení všech možných sloupců
        all_possible_fields = set()
        for kolo_data in self.log_jednotek_detail_kola.values():
            for unit_data in kolo_data.values():
                all_possible_fields.update(unit_data.keys())

        # Konstrukce finálního seznamu sloupců
        fieldnames = []
        for field in PREFERRED_FIELD_ORDER:
            if field in all_possible_fields:
                fieldnames.append(field)

        # Přidání zbývajících sloupců, které nebyly v PREFERRED_FIELD_ORDER, v abecedním pořadí
        remaining_fields = sorted(list(all_possible_fields - set(PREFERRED_FIELD_ORDER)))
        fieldnames.extend(remaining_fields)

        if not fieldnames: # Pokud není co logovat
            print("Žádná data jednotek k uložení v detailním logu pro tento scénář.")
        else:
            file_exists = os.path.isfile(detail_csv_path)

            with open(detail_csv_path, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()

                for kolo in sorted(self.log_jednotek_detail_kola.keys()):
                    for unit_id in sorted(self.log_jednotek_detail_kola[kolo].keys()):
                        writer.writerow(self.log_jednotek_detail_kola[kolo][unit_id])
            print(f"Detailní log jednotek simulace (scénář '{self.scenar_nazev}') přidán do: {detail_csv_path}")

        # Souhrnné výsledky simulace zůstávají stejné
        souhrn_csv_path = os.path.join('sim_logy', 'souhrn_simulaci.csv')
        souhrn_fieldnames = ['id_simulace', 'scenar_nazev', 'cas_startu', 'vitez_simulace', 'pocet_kol', 'poznamka']

        file_exists = os.path.isfile(souhrn_csv_path)

        with open(souhrn_csv_path, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=souhrn_fieldnames)
            if not file_exists:
                writer.writeheader()

            writer.writerow({
                'id_simulace': self.id_simulace,
                'scenar_nazev': self.scenar_nazev,
                'cas_startu': self.cas_startu.strftime('%Y-%m-%d %H:%M:%S'),
                'vitez_simulace': self.vitez_simulace.jmeno if self.vitez_simulace else "Neznámý",
                'pocet_kol': self.pocet_kol,
                'poznamka': self.poznamka if self.poznamka else ""
            })
        print(f"Souhrnný výsledek simulace přidán do: {souhrn_csv_path}")

    def uloz_vysledek_simulace(self, vitez, pocet_kol, finalni_stav_jednotek):
        """
        Zaznamená a uloží celkový výsledek simulace.
        """
        self.vitez_simulace = vitez
        self.pocet_kol = pocet_kol
        # Zde můžeme volitelně zpracovat finalni_stav_jednotek, pokud potřebujeme
        # ale pro souhrn to není nezbytně nutné, stačí mít vítěze a počet kol.

        self.uloz_logy_do_csv()  # Uložíme logy po skončení simulace <-- DŮLEŽITÉ: Zavolat zde uložení!

    def vypis_souhrnne_vysledky_simulace(self):
        """
        Vypíše souhrnné výsledky simulace na konzoli.
        """
        print(f"\n=== Souhrnné výsledky simulace pro scénář: {self.scenar_nazev} ===")
        print(f"ID Simulace: {self.id_simulace}")
        print(f"Začátek simulace: {self.cas_startu.strftime('%Y-%m-%d %H:%M:%S')}")
        if self.poznamka:
            print(f"Poznámka: {self.poznamka}")
        print(f"Vítěz této simulace: {self.vitez_simulace.jmeno if self.vitez_simulace else 'Neznámý'}")
        print(f"Celkový počet kol: {self.pocet_kol}")
        print(f"Detailní a souhrnné logy byly uloženy do složky 'sim_logy'.")

    def vypis_prubeh(self):
        """
        Vypíše detailní průběh simulace na konzoli.
        """
        print(f"\n=== Detailní průběh simulace pro scénář: {self.scenar_nazev} ===")

        if not self.log_jednotek_detail_kola:
            print("Žádná data průběhu k zobrazení.")
            return

        vsechna_kolo_v_logu = sorted(self.log_jednotek_detail_kola.keys())

        for kolo in vsechna_kolo_v_logu:
            print(f"\n--- Kolo {kolo} ---")
            if kolo in self.log_jednotek_detail_kola:
                print("Stav jednotek:")
                for jednotka_id, info in self.log_jednotek_detail_kola[kolo].items():
                    stav_radku = (
                        f"  ID: {info['id']}, Typ: {info['typ']}, Vlastník: {info['vlastnik']}, "
                        f"Pozice: {info['pozice']}, Životy: {info['zivoty']}/{info['max_zivoty']}, "
                        f"Útoků: {info['utoky_za_kolo']}, Protiútoků: {info['protiutoky_za_kolo']}, "
                        f"Kritických zásahů: {info['kriticke_zasahy_za_kolo']}, Úhybů: {info['uhyby_za_kolo']}, "
                        f"Způsobené poš.: {info['zpusobene_poskozeni_za_kolo']}, Přijaté poš.: {info['prijate_poskozeni_za_kolo']}"
                    )
                    print(stav_radku)
            else:
                print("  Žádné záznamy pro toto kolo.")