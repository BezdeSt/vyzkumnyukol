import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt


class DataProcessor:
    def __init__(self, soubor_csv):
        self.soubor_csv = soubor_csv
        self.df_raw = self.nacti_data()

        if self.df_raw.empty:
            print("Chyba: Raw DataFrame je prázdný. Zkontrolujte soubor a kódování.")
            return

        self.simulace_list = self.rozdel_na_simulace()

    def nacti_data(self):
        """Načte data z CSV souboru s pokusem o různé kódování."""
        encoding_options = ['utf-8', 'cp1250', 'latin-1']
        for encoding in encoding_options:
            try:
                df = pd.read_csv(self.soubor_csv, encoding=encoding)
                if 'vlastnik' in df.columns and df['vlastnik'].astype(str).str.contains('Hráč|Hrac', na=False).any():
                    return df
            except UnicodeDecodeError:
                pass  # Ignoruj chyby kódování a zkus další
            except Exception:
                pass  # Ignoruj ostatní chyby a zkus další

        print(
            f"Nedaří se načíst soubor '{self.soubor_csv}' s žádným běžným kódováním. Zkontrolujte prosím kódování souboru.")
        return pd.DataFrame()

    def rozdel_na_simulace(self):
        """
        Rozdělí DataFrame na seznam menších DataFrames,
        kde každý reprezentuje jednu kompletní simulaci.
        Detekuje začátky simulací podle poklesu čísla kola.
        """
        if self.df_raw.empty:
            return []

        self.df_raw['kolo'] = pd.to_numeric(self.df_raw['kolo'], errors='coerce')
        self.df_raw.dropna(subset=['kolo'], inplace=True)

        kolo_shifted = self.df_raw['kolo'].shift(1).fillna(np.inf)

        simulace_starts_indices = self.df_raw[self.df_raw['kolo'] < kolo_shifted].index.tolist()

        if 0 not in simulace_starts_indices:
            simulace_starts_indices.insert(0, 0)

        simulace_starts_indices = sorted(list(set(simulace_starts_indices)))

        simulace_list = []
        for i in range(len(simulace_starts_indices)):
            start_index = simulace_starts_indices[i]
            end_index = simulace_starts_indices[i + 1] if i + 1 < len(simulace_starts_indices) else len(self.df_raw)

            current_sim_df = self.df_raw.iloc[start_index:end_index].copy()
            simulace_list.append(current_sim_df)

        return simulace_list

    def agreguj_jednotlivou_simulaci(self, df_simulace):
        """
        Agreguje klíčové metriky pro jednu kompletní simulaci.
        """
        if df_simulace.empty:
            return None

        vitez = None
        unikatni_vitezove = df_simulace['vitez'].dropna().unique()
        if len(unikatni_vitezove) > 0:
            vitez = str(unikatni_vitezove[0])

        pocet_kol = int(df_simulace['kolo'].max()) if not df_simulace['kolo'].empty else 0

        agregovane_vysledky_simulace = {}
        df_simulace['typ_jednotky'] = df_simulace['typ_jednotky'].astype(str)
        df_simulace['vlastnik'] = df_simulace['vlastnik'].astype(str)

        jednotky_a_vlastnici = df_simulace[['typ_jednotky', 'vlastnik']].drop_duplicates().values

        for typ_jednotky, vlastnik in jednotky_a_vlastnici:
            df_jednotka_simulace = df_simulace[
                (df_simulace['typ_jednotky'] == typ_jednotky) & (df_simulace['vlastnik'] == vlastnik)]

            if df_jednotka_simulace.empty:
                continue

            df_jednotka_simulace_po_kole_0 = df_jednotka_simulace[df_jednotka_simulace['kolo'] > 0]

            celkove_zpusobene_poskozeni = df_jednotka_simulace_po_kole_0['realne_zpusobene_poskozeni_kolo'].sum().item()
            celkove_utrzene_poskozeni = df_jednotka_simulace_po_kole_0['utrzene_poskozeni_kolo'].sum().item()

            celkovy_pocet_utoku = df_jednotka_simulace_po_kole_0[
                'pocet_utoku_kolo'].sum().item() if 'pocet_utoku_kolo' in df_jednotka_simulace_po_kole_0.columns else 0
            celkovy_pocet_protiutoku = df_jednotka_simulace_po_kole_0[
                'pocet_protiutoku_kolo'].sum().item() if 'pocet_protiutoku_kolo' in df_jednotka_simulace_po_kole_0.columns else 0

            efektivni_pocet_kol_pro_prumery = df_jednotka_simulace_po_kole_0['kolo'].nunique()

            prumerne_zpusobene_za_kolo = (
                    celkove_zpusobene_poskozeni / efektivni_pocet_kol_pro_prumery) if efektivni_pocet_kol_pro_prumery > 0 else 0.0
            prumerne_utrzene_za_kolo = (
                    celkove_utrzene_poskozeni / efektivni_pocet_kol_pro_prumery) if efektivni_pocet_kol_pro_prumery > 0 else 0.0

            prumerny_pocet_utoku_za_kolo = (
                    celkovy_pocet_utoku / efektivni_pocet_kol_pro_prumery) if efektivni_pocet_kol_pro_prumery > 0 else 0.0
            prumerny_pocet_protiutoku_za_kolo = (
                    celkovy_pocet_protiutoku / efektivni_pocet_kol_pro_prumery) if efektivni_pocet_kol_pro_prumery > 0 else 0.0

            last_state = df_jednotka_simulace.iloc[-1]

            zive_jednotky_na_konci = last_state['zive_jednotky'].item()
            celkove_zivoty_na_konci = last_state['celkove_zivoty'].item()

            initial_units_series = df_jednotka_simulace[df_jednotka_simulace['kolo'] == 0]['zive_jednotky']
            initial_units_count = initial_units_series.iloc[0].item() if not initial_units_series.empty else 0

            mira_preziti = (zive_jednotky_na_konci / initial_units_count) * 100.0 if initial_units_count > 0 else 0.0

            unit_data = {
                'vlastnik': vlastnik,
                'celkove_zpusobene_poskozeni_simulace': celkove_zpusobene_poskozeni,
                'celkove_utrzene_poskozeni_simulace': celkove_utrzene_poskozeni,
                'prumerne_zpusobene_za_kolo_simulace': prumerne_zpusobene_za_kolo,
                'prumerne_utrzene_za_kolo_simulace': prumerne_utrzene_za_kolo,
                'zive_jednotky_na_konci': zive_jednotky_na_konci,
                'celkove_zivoty_na_konci': celkove_zivoty_na_konci,
                'mira_preziti': mira_preziti
            }

            # Přidání počtů útoků/protiútoků, pokud existují ve sloupcích
            if 'pocet_utoku_kolo' in df_jednotka_simulace_po_kole_0.columns:
                unit_data['celkovy_pocet_utoku_simulace'] = celkovy_pocet_utoku
                unit_data['prumerny_pocet_utoku_za_kolo_simulace'] = prumerny_pocet_utoku_za_kolo
            if 'pocet_protiutoku_kolo' in df_jednotka_simulace_po_kole_0.columns:
                unit_data['celkovy_pocet_protiutoku_simulace'] = celkovy_pocet_protiutoku
                unit_data['prumerny_pocet_protiutoku_za_kolo_simulace'] = prumerny_pocet_protiutoku_za_kolo

            agregovane_vysledky_simulace[typ_jednotky] = unit_data

        return {
            'vitez': vitez,
            'pocet_kol': pocet_kol,
            'jednotky_data': agregovane_vysledky_simulace
        }

    def zpracuj_vsechny_simulace(self):
        agregovane_vsechny_simulace = []
        for df_simulace in self.simulace_list:
            res = self.agreguj_jednotlivou_simulaci(df_simulace)
            if res:
                agregovane_vsechny_simulace.append(res)
        return agregovane_vsechny_simulace

    def agreguj_vsechny_simulace_dohromady(self, vysledky_jednotlivych_simulaci):
        """
        Provede celkovou agregaci výsledků napříč všemi simulacemi.
        """
        celkove_vysledky = {}
        pocet_simulaci = len(vysledky_jednotlivych_simulaci)

        # Počítání vítězství
        vitezove_counts = {}
        for sim_res in vysledky_jednotlivych_simulaci:
            vitez = sim_res['vitez']
            if vitez:
                vitezove_counts[vitez] = vitezove_counts.get(vitez, 0) + 1
            else:
                vitezove_counts['Remíza/Žádný vítěz'] = vitezove_counts.get('Remíza/Žádný vítěz', 0) + 1

        celkove_vysledky['vitezove_counts'] = vitezove_counts

        # Agregace statistik jednotek napříč simulacemi
        agregace_jednotek = {}

        for sim_res in vysledky_jednotlivych_simulaci:
            for typ_jednotky, data in sim_res['jednotky_data'].items():
                vlastnik = data['vlastnik']
                klic = f"{typ_jednotky} ({vlastnik})"

                if klic not in agregace_jednotek:
                    agregace_jednotek[klic] = {
                        'celkove_zpusobene_poskozeni_simulace': [],
                        'celkove_utrzene_poskozeni_simulace': [],
                        'prumerne_zpusobene_za_kolo_simulace': [],
                        'prumerne_utrzene_za_kolo_simulace': [],
                        'celkovy_pocet_utoku_simulace': [],
                        'celkovy_pocet_protiutoku_simulace': [],
                        'prumerny_pocet_utoku_za_kolo_simulace': [],
                        'prumerny_pocet_protiutoku_za_kolo_simulace': [],
                        'zive_jednotky_na_konci': [],
                        'mira_preziti': [],
                        'pocet_her': 0
                    }

                agregace_jednotek[klic]['celkove_zpusobene_poskozeni_simulace'].append(
                    data['celkove_zpusobene_poskozeni_simulace'])
                agregace_jednotek[klic]['celkove_utrzene_poskozeni_simulace'].append(
                    data['celkove_utrzene_poskozeni_simulace'])
                agregace_jednotek[klic]['prumerne_zpusobene_za_kolo_simulace'].append(
                    data['prumerne_zpusobene_za_kolo_simulace'])
                agregace_jednotek[klic]['prumerne_utrzene_za_kolo_simulace'].append(
                    data['prumerne_utrzene_za_kolo_simulace'])

                # Plnění seznamů daty s kontrolou existence klíče
                if 'celkovy_pocet_utoku_simulace' in data:
                    agregace_jednotek[klic]['celkovy_pocet_utoku_simulace'].append(
                        data['celkovy_pocet_utoku_simulace'])
                if 'celkovy_pocet_protiutoku_simulace' in data:
                    agregace_jednotek[klic]['celkovy_pocet_protiutoku_simulace'].append(
                        data['celkovy_pocet_protiutoku_simulace'])
                if 'prumerny_pocet_utoku_za_kolo_simulace' in data:
                    agregace_jednotek[klic]['prumerny_pocet_utoku_za_kolo_simulace'].append(
                        data['prumerny_pocet_utoku_za_kolo_simulace'])
                if 'prumerny_pocet_protiutoku_za_kolo_simulace' in data:
                    agregace_jednotek[klic]['prumerny_pocet_protiutoku_za_kolo_simulace'].append(
                        data['prumerny_pocet_protiutoku_za_kolo_simulace'])

                agregace_jednotek[klic]['zive_jednotky_na_konci'].append(data['zive_jednotky_na_konci'])
                agregace_jednotek[klic]['mira_preziti'].append(data['mira_preziti'])
                agregace_jednotek[klic]['pocet_her'] += 1

        final_agregace_jednotek = {}
        for klic, data_list in agregace_jednotek.items():
            final_agregace_jednotek[klic] = {
                'pocet_odehranych_simulaci': data_list['pocet_her'],
                'prumer_celkoveho_zpusobeneho_poskozeni_za_simulaci': np.mean(
                    data_list['celkove_zpusobene_poskozeni_simulace']),
                'prumer_celkoveho_utrzeneho_poskozeni_za_simulaci': np.mean(
                    data_list['celkove_utrzene_poskozeni_simulace']),
                'prumer_zpusobeneho_za_kolo': np.mean(data_list['prumerne_zpusobene_za_kolo_simulace']),
                'prumer_utrzeneho_za_kolo': np.mean(data_list['prumerne_utrzene_za_kolo_simulace']),
                # Výpočet průměrů útoků/protiútoků s kontrolou prázdných seznamů
                'prumer_celkoveho_poctu_utoku_za_simulaci': np.mean(data_list['celkovy_pocet_utoku_simulace']) if
                data_list['celkovy_pocet_utoku_simulace'] else 0,
                'prumer_celkoveho_poctu_protiutoku_za_simulaci': np.mean(
                    data_list['celkovy_pocet_protiutoku_simulace']) if data_list[
                    'celkovy_pocet_protiutoku_simulace'] else 0,
                'prumer_poctu_utoku_za_kolo': np.mean(data_list['prumerny_pocet_utoku_za_kolo_simulace']) if data_list[
                    'prumerny_pocet_utoku_za_kolo_simulace'] else 0,
                'prumer_poctu_protiutoku_za_kolo': np.mean(data_list['prumerny_pocet_protiutoku_za_kolo_simulace']) if
                data_list['prumerny_pocet_protiutoku_za_kolo_simulace'] else 0,
                'prumer_zivych_jednotek_na_konci': np.mean(data_list['zive_jednotky_na_konci']),
                'prumerna_mira_preziti': np.mean(data_list['mira_preziti'])
            }

        celkove_vysledky['agregace_jednotek'] = final_agregace_jednotek
        celkove_vysledky['celkovy_pocet_simulaci'] = pocet_simulaci

        return celkove_vysledky

    def vizualizuj_zivoty_prubeh(self, cislo_simulace):
        """
        Vizualizuje vývoj celkových životů jednotek v průběhu kol pro danou simulaci.
        Args:
            cislo_simulace (int): Pořadové číslo simulace (od 1).
        """
        if not (1 <= cislo_simulace <= len(self.simulace_list)):
            print(
                f"Chyba: Simulace číslo {cislo_simulace} neexistuje. Dostupné simulace: 1 až {len(self.simulace_list)}.")
            return

        df_simulace = self.simulace_list[cislo_simulace - 1]  # Převod na 0-index

        plt.figure(figsize=(10, 6))

        # Získání unikátních jednotek a jejich vlastníků v této simulaci
        jednotky_a_vlastnici = df_simulace[['typ_jednotky', 'vlastnik']].drop_duplicates()

        for index, row in jednotky_a_vlastnici.iterrows():
            typ_jednotky = row['typ_jednotky']
            vlastnik = row['vlastnik']

            df_jednotka = df_simulace[(df_simulace['typ_jednotky'] == typ_jednotky) &
                                      (df_simulace['vlastnik'] == vlastnik)].copy()

            plt.plot(df_jednotka['kolo'], df_jednotka['celkove_zivoty'], marker='o',
                     label=f'{typ_jednotky} ({vlastnik})')

        plt.title(f'Vývoj celkových životů v simulaci č. {cislo_simulace}')
        plt.xlabel('Kolo')
        plt.ylabel('Celkové životy')
        plt.grid(True)
        plt.legend()
        plt.xticks(df_simulace['kolo'].unique())  # Zajistí, že ticky na X-ose budou odpovídat kolům
        plt.ylim(bottom=0)  # Zajištění, že Y-osa začíná od 0
        plt.tight_layout()
        plt.show()

    def vizualizuj_poskozeni_prubeh(self, cislo_simulace):
        """
        Vizualizuje způsobené poškození za kolo pro danou simulaci jako bargraf.
        Args:
            cislo_simulace (int): Pořadové číslo simulace (od 1).
        """
        if not (1 <= cislo_simulace <= len(self.simulace_list)):
            print(
                f"Chyba: Simulace číslo {cislo_simulace} neexistuje. Dostupné simulace: 1 až {len(self.simulace_list)}.")
            return

        df_simulace = self.simulace_list[cislo_simulace - 1]  # Převod na 0-index

        plt.figure(figsize=(12, 7))

        jednotky_a_vlastnici = df_simulace[['typ_jednotky', 'vlastnik']].drop_duplicates()

        # Pro správné zobrazení sloupcového grafu (s oddělenými sloupci pro způsobené)
        df_plot = df_simulace[df_simulace['kolo'] > 0].copy()

        # Získání unikátních kol pro nastavení X-os
        kola = df_plot['kolo'].unique()
        # Nastavení šířky sloupce (pouze pro způsobené poškození, takže stačí jeden offset)
        width = 0.5

        # Nový způsob získání barevné mapy a normalizátoru
        cmap = plt.colormaps['Dark2']  # Získáme barevnou mapu
        # Normalizátor pro mapování indexů jednotek na barvy
        norm = plt.Normalize(vmin=0, vmax=len(jednotky_a_vlastnici) - 1)

        # Vytvoření seznamu pro legendu
        labels = []
        bars_list = []

        # Iterujeme přes kola
        for k_idx, kolo_val in enumerate(kola):
            # Pro každé kolo iterujeme přes jednotky
            for j_idx, (typ_jednotky, vlastnik) in enumerate(jednotky_a_vlastnici.values):
                df_jednotka_kolo = df_plot[(df_plot['kolo'] == kolo_val) &
                                           (df_plot['typ_jednotky'] == typ_jednotky) &
                                           (df_plot['vlastnik'] == vlastnik)]

                # Získání hodnoty poškození, nebo 0 pokud pro dané kolo a jednotku není žádné poškození
                poskozeni_val = df_jednotka_kolo[
                    'realne_zpusobene_poskozeni_kolo'].sum() if not df_jednotka_kolo.empty else 0

                # Vypočítáme pozici sloupce na X-ose
                # Základní pozice je index kola (k_idx), a k tomu přidáme offset pro každou jednotku
                x_pos = k_idx + (j_idx - len(jednotky_a_vlastnici) / 2 + 0.5) * width

                bar = plt.bar(x_pos, poskozeni_val, width,
                              label=f'{typ_jednotky} ({vlastnik})' if kolo_val == kola[0] else "",  # Label jen jednou
                              color=cmap(norm(j_idx)))  # Použijeme cmap a norm pro konzistentní barvy jednotek

                # Ukládáme reference k barům a jejich labely pro legendu
                if kolo_val == kola[0]:  # Přidáme label jen jednou pro každou jednotku
                    bars_list.append(bar)
                    labels.append(f'{typ_jednotky} ({vlastnik})')

        plt.title(f'Způsobené poškození za kolo v simulaci č. {cislo_simulace}')
        plt.xlabel('Kolo')
        plt.ylabel('Způsobené poškození')
        plt.xticks(np.arange(len(kola)), [int(k) for k in kola])  # Nastaví popisky X-os pro kola
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.legend(bars_list, labels, bbox_to_anchor=(1.05, 1),
                   loc='upper left')  # Legendu vytváříme z uložených labelů a barů
        plt.ylim(bottom=0)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    # --- Zde vlož skutečnou cestu k tvému CSV souboru ---
    soubor_dat = 'Válečník_vs_Lučištník--Linie_prubeh_simulaci.csv'  # Předpokládá se, že soubor je ve stejné složce
    # --- Konec nastavení cesty ---

    processor = DataProcessor(soubor_dat)
    vysledky_jednotlivych_simulaci = processor.zpracuj_vsechny_simulace()

    if vysledky_jednotlivych_simulaci:
        # --- Dílčí výsledky pro každou simulaci ---
        print("\n--- Dílčí agregované výsledky jednotlivých simulací: ---")
        for i, sim_data in enumerate(vysledky_jednotlivych_simulaci):
            print(f"\n--- Simulace číslo {i + 1} ---")
            print(f"  Vítěz: {sim_data['vitez']}")
            print(f"  Počet kol: {sim_data['pocet_kol']}")
            for unit_type, data in sim_data['jednotky_data'].items():
                print(f"    Jednotka: {unit_type} ({data['vlastnik']})")
                print(
                    f"      Celkové způsobené poškození (za simulaci): {data['celkove_zpusobene_poskozeni_simulace']}")
                print(f"      Celkové utržené poškození (za simulaci): {data['celkove_utrzene_poskozeni_simulace']}")
                print(
                    f"      Průměrné způsobené za kolo (za simulaci): {data['prumerne_zpusobene_za_kolo_simulace']:.2f}")
                print(f"      Průměrné utržené za kolo (za simulaci): {data['prumerne_utrzene_za_kolo_simulace']:.2f}")
                # Tisk celkových a průměrných počtů útoků/protiútoků za simulaci
                if 'celkovy_pocet_utoku_simulace' in data:
                    print(f"      Celkový počet útoků (za simulaci): {data['celkovy_pocet_utoku_simulace']}")
                if 'celkovy_pocet_protiutoku_simulace' in data:
                    print(f"      Celkový počet protiútoků (za simulaci): {data['celkovy_pocet_protiutoku_simulace']}")
                if 'prumerny_pocet_utoku_za_kolo_simulace' in data:
                    print(
                        f"      Průměrný počet útoků za kolo (za simulaci): {data['prumerny_pocet_utoku_za_kolo_simulace']:.2f}")
                if 'prumerny_pocet_protiutoku_za_kolo_simulace' in data:
                    print(
                        f"      Průměrný počet protiútoků za kolo (za simulaci): {data['prumerny_pocet_protiutoku_za_kolo_simulace']:.2f}")
                print(f"      Živé jednotky na konci: {data['zive_jednotky_na_konci']}")
                print(f"      Celkové životy na konci: {data['celkove_zivoty_na_konci']}")
                print(f"      Míra přežití: {data['mira_preziti']:.2f}%")
        print("\n--- Konec dílčích výsledků ---")

        # --- Celková agregace všech simulací ---
        celkove_agregovane_vysledky = processor.agreguj_vsechny_simulace_dohromady(vysledky_jednotlivych_simulaci)

        print("\n--- Celkové agregované výsledky všech simulací: ---")
        print(f"Celkový počet simulací: {celkove_agregovane_vysledky['celkovy_pocet_simulaci']}")

        print("\n  Počet vítězství:")
        for vitez, count in celkove_agregovane_vysledky['vitezove_counts'].items():
            print(f"    {vitez}: {count}x")

        print("\n  Agregované statistiky jednotek napříč všemi simulacemit:")
        for klic_jednotky, data in celkove_agregovane_vysledky['agregace_jednotek'].items():
            print(f"    Jednotka: {klic_jednotky} (z {data['pocet_odehranych_simulaci']} simulací)")
            print(
                f"      Průměrné celkové způsobené poškození za simulaci: {data['prumer_celkoveho_zpusobeneho_poskozeni_za_simulaci']:.2f}")
            print(
                f"      Průměrné celkové utržené poškození za simulaci: {data['prumer_celkoveho_utrzeneho_poskozeni_za_simulaci']:.2f}")
            print(f"      Průměrné způsobené za kolo: {data['prumer_zpusobeneho_za_kolo']:.2f}")
            print(f"      Průměrné utržené za kolo: {data['prumer_utrzeneho_za_kolo']:.2f}")
            # Tisk průměrných útoků/protiútoků z celkové agregace
            print(
                f"      Průměrný celkový počet útoků za simulaci: {data['prumer_celkoveho_poctu_utoku_za_simulaci']:.2f}")
            print(
                f"      Průměrný celkový počet protiutoků za simulaci: {data['prumer_celkoveho_poctu_protiutoku_za_simulaci']:.2f}")
            print(f"      Průměrný počet útoků za kolo: {data['prumer_poctu_utoku_za_kolo']:.2f}")
            print(f"      Průměrný počet protiútoků za kolo: {data['prumer_poctu_protiutoku_za_kolo']:.2f}")
            print(f"      Průměr živých jednotek na konci: {data['prumer_zivych_jednotek_na_konci']:.2f}")
            print(f"      Průměrná míra přežití: {data['prumerna_mira_preziti']:.2f}%")

    else:
        print("Žádné výsledky simulací k zobrazení. Zkontrolujte vstupní data.")

    # VIZUALIZACE
    # Zkus vizualizovat simulaci číslo 1
    processor.vizualizuj_zivoty_prubeh(1)

    processor.vizualizuj_poskozeni_prubeh(1)