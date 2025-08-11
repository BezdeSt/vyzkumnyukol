import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import glob

# --- Konfigurace ---
LOG_DIR = 'sim_logy'
BASE_OUTPUT_DIR = 'agregovane_vystupy'  # Základní výstupní složka
SUMMARY_FILE_NAME = 'souhrn_simulaci.csv'
DETAIL_FILE_PATTERN = '*_detail.csv'  # detailní logy

# Vytvoření základní výstupní složky, pokud neexistuje
os.makedirs(BASE_OUTPUT_DIR, exist_ok=True)

print("--- Spouštím analýzu dat simulací ---")


# --- FUNKCE PRO GENERUJÍCÍ TABULKU ATRIBUTŮ ---
def generate_attribute_summary_table(df_detail_data, output_dir):
    """
    Generuje a ukládá tabulku sumarizující použité atributy pro každou kombinaci
    názvu simulace, ID sady atributů, názvu scénáře a typu entity,
    vytěžené přímo z detailních dat.

    Args:
        df_detail_data (pd.DataFrame): DataFrame s detailními daty simulací (obsahující 'nazev',
                                        'id_atribut_sada', 'scenar_nazev', 'typ' a atributy).
        output_dir (str): Cesta k výstupnímu adresáři.
    """
    print("\n--- Generuji tabulku atributů pro jednotlivé sady ze detailních dat ---")

    static_attributes_candidates = [
        'utok_min', 'utok_max', 'obrana', 'rychlost', 'dosah',
        'crit', 'uhyb', 'max_zivoty', 'cena', 'cena_za_kolo', 'produkce'
    ]

    # Společné sloupce pro seskupení, které definují unikátní sadu atributů
    groupby_cols = ['nazev', 'id_atribut_sada', 'scenar_nazev', 'typ']

    for col in groupby_cols:
        if col not in df_detail_data.columns:
            print(f"Chyba: Sloupec '{col}' není v detailních datech. Nelze vygenerovat tabulku atributů.")
            return

    unique_attribute_sets = df_detail_data.drop_duplicates(subset=groupby_cols).copy()

    actual_static_attributes = [attr for attr in static_attributes_candidates if attr in unique_attribute_sets.columns]

    cols_to_select = groupby_cols + actual_static_attributes

    cols_to_select = [col for col in cols_to_select if col in unique_attribute_sets.columns]

    df_attributes = unique_attribute_sets[cols_to_select].copy()

    df_attributes.rename(columns={
        'nazev': 'Název simulace',
        'id_atribut_sada': 'ID sady atributů',
        'scenar_nazev': 'Název scénáře',
        'typ': 'Typ entity',
        'max_zivoty': 'Maximální životy',
        'utok_min': 'Útok Min',
        'utok_max': 'Útok Max',
        'obrana': 'Obrana',
        'rychlost': 'Rychlost',
        'dosah': 'Dosah',
        'crit': 'Kritická šance (násobitel)',
        'uhyb': 'Úhyb (%)',
        'cena': 'Cena (surovina:množství)',
        'cena_za_kolo': 'Cena za kolo (surovina:množství)',
        'produkce': 'Produkce (surovina:množství)'
    }, inplace=True)

    if not df_attributes.empty:
        output_file = os.path.join(output_dir, 'prehled_atributu_simulaci.csv')
        df_attributes.to_csv(output_file, sep=';', index=False)
        print(f"Tabulka atributů uložena do: {output_file}")
        print(df_attributes.head())
    else:
        print("Nebyly nalezeny žádné atributy k sumarizaci z detailních dat.")


# --- Konec funkcí ---


# --- 1. Načtení dat ---

# Načtení souhrnného logu
try:
    df_summary = pd.read_csv(os.path.join(LOG_DIR, SUMMARY_FILE_NAME), delimiter=',')
    print(f"Načten souhrnný log: {SUMMARY_FILE_NAME}")
    print(f"Počet záznamů v souhrnném logu: {len(df_summary)}")

    # Zajištění správných datových typů pro analýzu
    df_summary['id_simulace'] = df_summary['id_simulace'].astype(str)

    # Zajištění sloupce 'nazev'
    if 'nazev' not in df_summary.columns:
        df_summary['nazev'] = 'Vychozi_nazev_simulace'  # hodnota, pokud sloupec chybí
        print(
            "Varování: Sloupec 'nazev' nebyl nalezen v souhrnném logu. Použit výchozí název 'Vychozi_nazev_simulace'.")

    df_summary['id_atribut_sada'] = df_summary['id_atribut_sada'].astype(str)

    df_summary['pocet_kol'] = pd.to_numeric(df_summary['pocet_kol'], errors='coerce')

except FileNotFoundError:
    print(
        f"Chyba: Souhrnný log '{SUMMARY_FILE_NAME}' nenalezen ve složce '{LOG_DIR}'. Ujistěte se, že simulace proběhly a vygenerovaly logy.")
    exit()
except Exception as e:
    print(f"Chyba při načítání souhrnného logu: {e}. Zkontrolujte formát CSV a oddělovače.")
    exit()

# Načtení a spojení detailních logů
detail_files = glob.glob(os.path.join(LOG_DIR, DETAIL_FILE_PATTERN))
if not detail_files:
    print(
        f"Varování: Žádné detailní logy '{DETAIL_FILE_PATTERN}' nenalezeny ve složce '{LOG_DIR}'. Některé analýzy nebudou možné.")
    df_detail = pd.DataFrame()  # Prázdný DataFrame
else:
    list_df_detail = []
    for f in detail_files:
        try:
            df_temp = pd.read_csv(f, delimiter=',')
            df_temp['id_simulace'] = df_temp['id_simulace'].astype(str)
            df_temp['id_atribut_sada'] = df_temp['id_atribut_sada'].astype(str)
            list_df_detail.append(df_temp)
        except Exception as e:
            print(f"Varování: Nepodařilo se načíst detailní log '{f}': {e}. Zkontrolujte formát CSV a oddělovače.")
    if list_df_detail:
        df_detail = pd.concat(list_df_detail, ignore_index=True)
        print(f"Načteno a spojeno {len(detail_files)} detailních logů.")
        print(f"Celkový počet záznamů v detailním logu: {len(df_detail)}")

        df_detail = pd.merge(df_detail,
                             df_summary[['id_simulace', 'nazev', 'scenar_nazev']],
                             on='id_simulace',
                             how='left')
    else:
        print("Žádné detailní logy nebylo možné úspěšně načíst.")
        df_detail = pd.DataFrame()

# --- Volání nové funkce pro generování tabulky atributů ---
if not df_detail.empty:
    generate_attribute_summary_table(df_detail, BASE_OUTPUT_DIR)
else:
    print("Nelze generovat tabulku atributů, protože detailní data nejsou k dispozici.")

# --- 2. Agregace souhrnných dat (s 'nazev') ---
print("\n--- Agregace souhrnných dat ---")

# Společné seskupovací klíče pro souhrnnné tabulky
summary_groupby_keys = ['nazev', 'id_atribut_sada', 'scenar_nazev']

# Agregace statistik kol
aggregated_rounds = pd.DataFrame()
if 'pocet_kol' in df_summary.columns:
    aggregated_rounds = df_summary.groupby(summary_groupby_keys)['pocet_kol'].agg(
        ['mean', 'median', 'min', 'max', 'std', 'count']
    ).round(2)
    aggregated_rounds.rename(columns={
        'mean': 'Průměr_kol',
        'median': 'Medián_kol',
        'min': 'Min_kol',
        'max': 'Max_kol',
        'std': 'Směrodatná_odchylka_kol',
        'count': 'Počet_simulací'
    }, inplace=True)
    print("\nStatistiky počtu kol dle názvu, sady atributů a scénáře:")
    print(aggregated_rounds.head())

# Agregace vítězných procent
win_percentages = pd.DataFrame()
if 'vitez_simulace' in df_summary.columns:
    win_counts = df_summary.groupby(summary_groupby_keys + ['vitez_simulace']).size().unstack(fill_value=0)
    if not win_counts.empty:
        total_sims_per_group = win_counts.sum(axis=1)
        valid_groups = total_sims_per_group[total_sims_per_group > 0].index
        win_percentages = win_counts.loc[valid_groups].div(total_sims_per_group.loc[valid_groups], axis=0).mul(
            100).round(2)

        expected_winner_cols = ['Hráč 1', 'Hráč 2', 'Nerozhodně', 'Neznámý']
        for col in expected_winner_cols:
            if col not in win_percentages.columns:
                win_percentages[col] = 0.0
        win_percentages = win_percentages[expected_winner_cols]
        win_percentages.rename(columns={
            'Hráč 1': 'Vítěz_Hráč1_%',
            'Hráč 2': 'Vítěz_Hráč2_%',
            'Nerozhodně': 'Nerozhodně_%',
            'Neznámý': 'Neznámý_%'
        }, inplace=True)
        print("\nVítězná procenta dle názvu, sady atributů a scénáře:")
        print(win_percentages.head())

# --- Spojení souhrnných tabulek do jedné ---
final_summary_table = pd.DataFrame()
if not aggregated_rounds.empty and not win_percentages.empty:
    final_summary_table = pd.merge(aggregated_rounds, win_percentages,
                                   left_index=True, right_index=True, how='outer')
elif not aggregated_rounds.empty:
    final_summary_table = aggregated_rounds
elif not win_percentages.empty:
    final_summary_table = win_percentages

if not final_summary_table.empty:
    print("\n--- Finální souhrnná tabulka (agregace kol a vítězství) ---")
    print(final_summary_table.head())
    final_summary_table.to_csv(os.path.join(BASE_OUTPUT_DIR, 'final_summary_table.csv'), sep=';')
else:
    print("\nNelze vytvořit finální souhrnnou tabulku: nedostatek dat z agregace kol nebo vítězství.")

# --- 3. Agregace detailních dat (s 'nazev') ---
print("\n--- Agregace detailních dat jednotek ---")

# Společné seskupovací klíče pro detailní tabulky
detail_groupby_keys = ['nazev', 'id_atribut_sada', 'scenar_nazev', 'typ']

lifespan_stats = pd.DataFrame()
if not df_detail.empty:
    required_lifespan_cols = ['zivoty', 'kolo', 'id', 'typ', 'id_atribut_sada', 'nazev', 'scenar_nazev']
    if all(col in df_detail.columns for col in required_lifespan_cols):
        df_deaths = df_detail[df_detail['zivoty'] == 0].copy()

        if not df_deaths.empty:
            unit_death_rounds = df_deaths.groupby(['id_simulace', 'id']).agg(
                smrt_kolo=('kolo', 'min'),
                typ=('typ', 'first'),
                id_atribut_sada=('id_atribut_sada', 'first'),
                nazev=('nazev', 'first'),
                scenar_nazev=('scenar_nazev', 'first')
            ).reset_index()

            lifespan_stats = unit_death_rounds.groupby(detail_groupby_keys)['smrt_kolo'].agg(
                ['mean', 'median', 'min', 'max', 'std', 'count']
            ).round(2)
            lifespan_stats.rename(columns={
                'mean': 'Průměrná_délka_života_kol',
                'median': 'Medián_délka_života_kol',
                'min': 'Min_délka_života_kol',
                'max': 'Max_délka_života_kol',
                'std': 'Směrodatná_odchylka_délky_života_kol',
                'count': 'Počet_úmrtí'
            }, inplace=True)
            print("\nStatistiky délky života jednotek (kola, kdy zemřely) dle názvu, sady atributů, scénáře a typu:")
            print(lifespan_stats.head())
        else:
            print("\nŽádné záznamy o úmrtích jednotek pro výpočet délky života.")
    else:
        print(
            f"\nDetailní log neobsahuje všechny potřebné sloupce ({', '.join(required_lifespan_cols)}) pro analýzu délky života.")

aggregated_combat = pd.DataFrame()
if not df_detail.empty:
    combat_metrics = [
        'zpusobene_poskozeni_za_kolo',
        'prijate_poskozeni_za_kolo',
        'utoky_za_kolo',
        'protiutoky_za_kolo',
        'kriticke_zasahy_za_kolo',
        'uhyby_za_kolo'
    ]
    required_combat_cols_raw = ['zivoty', 'id_atribut_sada', 'typ', 'nazev', 'scenar_nazev'] + combat_metrics
    if all(col in df_detail.columns for col in required_combat_cols_raw):
        df_active_units = df_detail[df_detail['zivoty'] > 0].copy()

        if not df_active_units.empty:
            for col in combat_metrics:
                df_active_units[col] = pd.to_numeric(df_active_units[col], errors='coerce').fillna(0)

            aggregated_combat = df_active_units.groupby(detail_groupby_keys)[combat_metrics].agg(
                ['mean', 'median', 'min', 'max', 'std']
            ).round(2)

            aggregated_combat.columns = ['_'.join(col).strip() for col in aggregated_combat.columns.values]
            aggregated_combat.columns = [
                col.replace('zpusobene_poskozeni_za_kolo', 'Zpusobene_poskozeni_').replace('prijate_poskozeni_za_kolo',
                                                                                           'Prijate_poskozeni_').replace(
                    'utoky_za_kolo', 'Utoky_')
                .replace('protiutoky_za_kolo', 'Protiutoky_').replace('kriticke_zasahy_za_kolo',
                                                                      'Kriticke_zasahy_').replace('uhyby_za_kolo',
                                                                                                  'Uhyby_')
                for col in aggregated_combat.columns
            ]
            print("\nAgregované bojové statistiky jednotek dle názvu, sady atributů, scénáře a typu:")
            print(aggregated_combat.head())
        else:
            print("\nŽádné aktivní jednotky nalezeny pro agregaci bojových statistik.")
    else:
        print(
            f"\nDetailní log neobsahuje všechny potřebné sloupce ({', '.join(required_combat_cols_raw)}) pro analýzu bojových statistik.")
else:
    print("\nDetailní log není k dispozici nebo je prázdný. Agregace detailních dat přeskočena.")

# --- Spojení detailních tabulek do jedné ---
final_detail_table = pd.DataFrame()
if not lifespan_stats.empty and not aggregated_combat.empty:
    final_detail_table = pd.merge(lifespan_stats, aggregated_combat,
                                  left_index=True, right_index=True, how='outer')
elif not lifespan_stats.empty:
    final_detail_table = lifespan_stats
elif not aggregated_combat.empty:
    final_detail_table = aggregated_combat

if not final_detail_table.empty:
    print("\n--- Finální detailní tabulka (agregace života a bojových statistik jednotek) ---")
    print(final_detail_table.head())
    final_detail_table.to_csv(os.path.join(BASE_OUTPUT_DIR, 'final_detail_table.csv'), sep=';')
else:
    print(
        "\nNelze vytvořit finální detailní tabulku: nedostatek dat z agregace života nebo bojových statistik jednotek.")

# --- 4. Vizualizace (Grafy) ---
print("\n--- Generování grafů (do podsložek dle názvu simulace) ---")

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)

unique_nazvy = df_summary['nazev'].unique()
for current_nazev in unique_nazvy:
    print(f"\n--- Generuji grafy pro název simulace: '{current_nazev}' ---")

    current_output_dir = os.path.join(BASE_OUTPUT_DIR, current_nazev)
    os.makedirs(current_output_dir, exist_ok=True)

    df_summary_for_plot = df_summary[df_summary['nazev'] == current_nazev].copy()
    df_detail_for_plot = df_detail[df_detail['nazev'] == current_nazev].copy()

    unique_sadas_in_nazev = df_summary_for_plot['id_atribut_sada'].unique()
    if len(unique_sadas_in_nazev) == 1:
        sada_suffix = f"_sada_{unique_sadas_in_nazev[0]}"
    elif len(unique_sadas_in_nazev) > 1:
        sada_suffix = "_vsechny_sady"
    else:
        sada_suffix = ""

    summary_plot_data_filtered = pd.DataFrame()
    if current_nazev in final_summary_table.index.get_level_values('nazev'):
        temp_summary_data = final_summary_table.loc[current_nazev].copy()
        if temp_summary_data.index.nlevels > 1:
            summary_plot_data_filtered = temp_summary_data.reset_index()
        else:
            summary_plot_data_filtered = temp_summary_data.reset_index(names=['id_atribut_sada', 'scenar_nazev'])

    # Filter `final_detail_table` for plotting
    detail_plot_data_filtered = pd.DataFrame()
    if current_nazev in final_detail_table.index.get_level_values('nazev'):
        temp_detail_data = final_detail_table.loc[current_nazev].copy()
        if temp_detail_data.index.nlevels > 1:
            detail_plot_data_filtered = temp_detail_data.reset_index()
        else:  # Handle case where only 'nazev' is in index, and id_atribut_sada is not part of index
            detail_plot_data_filtered = temp_detail_data.reset_index(names=['id_atribut_sada', 'scenar_nazev', 'typ'])

    # Graf 1: Vítězná procenta (původní)
    if not summary_plot_data_filtered.empty and 'Vítěz_Hráč1_%' in summary_plot_data_filtered.columns:
        win_percentages_plot_data = summary_plot_data_filtered.melt(
            id_vars=['id_atribut_sada', 'scenar_nazev'],
            value_vars=[col for col in summary_plot_data_filtered.columns if 'Vítěz_' in col or 'Nerozhodně' in col],
            var_name='Výsledek', value_name='Procento'
        )
        win_percentages_plot_data['Procento'] = pd.to_numeric(win_percentages_plot_data['Procento'], errors='coerce')
        win_percentages_plot_data = win_percentages_plot_data.dropna(subset=['Procento'])

        if not win_percentages_plot_data.empty:
            g = sns.catplot(
                data=win_percentages_plot_data,
                x='Výsledek',
                y='Procento',
                col='scenar_nazev',
                row='id_atribut_sada',
                kind='bar',
                height=4, aspect=1.2,
                palette='viridis'
            )
            g.set_axis_labels("Výsledek simulace", "Procento vítězství (%)")
            g.set_titles("Sada atributů: {row_name}, Scénář: {col_name}")
            plt.suptitle(f"Vítězná procenta hráčů a nerozhodné výsledky pro '{current_nazev}'", y=1.02, fontsize=16)
            plt.tight_layout()
            plt.savefig(os.path.join(current_output_dir, f'vitezna_procenta{sada_suffix}.png'))
            plt.close()
            print(f"Graf 'vitezna_procenta{sada_suffix}.png' uložen.")
        else:
            print("Data pro graf vítězných procent jsou prázdná po předzpracování.")
    else:
        print("Nelze vygenerovat graf vítězných procent: data nejsou k dispozici pro tento název simulace.")

    if not summary_plot_data_filtered.empty and 'Vítěz_Hráč1_%' in summary_plot_data_filtered.columns:
        win_percentages_compare_data = summary_plot_data_filtered.melt(
            id_vars=['id_atribut_sada', 'scenar_nazev'],
            value_vars=[col for col in summary_plot_data_filtered.columns if 'Vítěz_' in col or 'Nerozhodně' in col],
            var_name='Výsledek', value_name='Procento'
        )
        win_percentages_compare_data['Procento'] = pd.to_numeric(win_percentages_compare_data['Procento'],
                                                                 errors='coerce')
        win_percentages_compare_data = win_percentages_compare_data.dropna(subset=['Procento'])

        if not win_percentages_compare_data.empty:
            unique_scenarios_for_plot = win_percentages_compare_data['scenar_nazev'].unique()

            for scenario in unique_scenarios_for_plot:
                data_for_scenario = win_percentages_compare_data[
                    win_percentages_compare_data['scenar_nazev'] == scenario]

                if not data_for_scenario.empty:
                    plt.figure(figsize=(12, 7))
                    sns.barplot(
                        data=data_for_scenario,
                        x='id_atribut_sada',
                        y='Procento',
                        hue='Výsledek',
                        palette='coolwarm'
                    )
                    plt.title(f"Srovnání vítězných procent hráčů pro '{current_nazev}'\nScénář: '{scenario}'",
                              fontsize=16)
                    plt.xlabel("ID Sady atributů")
                    plt.ylabel("Procento vítězství (%)")
                    plt.xticks(rotation=45, ha='right')
                    plt.legend(title="Výsledek", bbox_to_anchor=(1.05, 1), loc='upper left')
                    plt.tight_layout()
                    plt.savefig(os.path.join(current_output_dir,
                                             f'vitezna_procenta_srovnani_atributu_{scenario}{sada_suffix}.png'))
                    plt.close()
                    print(f"Graf 'vitezna_procenta_srovnani_atributu_{scenario}{sada_suffix}.png' uložen.")
                else:
                    print(
                        f"Data pro graf srovnání vítězných procent pro scénář '{scenario}' jsou prázdná po předzpracování.")
        else:
            print("Data pro graf srovnání vítězných procent dle sad atributů jsou prázdná po předzpracování (celkem).")
    else:
        print("Nelze vygenerovat graf srovnání vítězných procent: data nejsou k dispozici pro tento název simulace.")

    # Graf 2: Distribuce kol (Box Plot)
    if not df_summary_for_plot.empty and 'pocet_kol' in df_summary_for_plot.columns:
        df_summary_for_plot_dropna = df_summary_for_plot.dropna(subset=['pocet_kol'])
        if not df_summary_for_plot_dropna.empty:
            plt.figure(figsize=(16, 9))
            sns.boxplot(
                data=df_summary_for_plot_dropna,
                x='scenar_nazev',
                y='pocet_kol',
                hue='id_atribut_sada',
                palette='plasma'
            )
            plt.title(f"Distribuce počtu kol simulací pro '{current_nazev}' dle scénáře a sady atributů")
            plt.xlabel("Název scénáře (mapy)")
            plt.ylabel("Počet kol")
            plt.xticks(rotation=30, ha='right')
            plt.legend(title="ID Sady atributů", bbox_to_anchor=(1.05, 1), loc='upper left')  # Legenda mimo graf
            plt.tight_layout()
            plt.savefig(os.path.join(current_output_dir, f'distribuce_kol{sada_suffix}.png'))
            plt.close()
            print(f"Graf 'distribuce_kol{sada_suffix}.png' uložen.")
        else:
            print("Data pro graf distribuce kol jsou prázdná po předzpracování.")
    else:
        print("Nelze vygenerovat graf distribuce kol: data nejsou k dispozici pro tento název simulace.")

    # Graf 3: Průměrné způsobené poškození za kolo
    if not detail_plot_data_filtered.empty and 'Zpusobene_poskozeni__mean' in detail_plot_data_filtered.columns:
        plot_data = detail_plot_data_filtered.pivot_table(
            index=['id_atribut_sada', 'scenar_nazev'],
            columns='typ',
            values='Zpusobene_poskozeni__mean'
        )
        if not plot_data.empty:
            num_x_elements = len(plot_data.index)
            fig_width = max(12, num_x_elements * 0.8)
            plt.figure(figsize=(fig_width, 8))
            plot_data.plot(kind='bar', ax=plt.gca())

            plt.title(f"Průměrné způsobené poškození za kolo na jednotku (Mean) pro '{current_nazev}'")
            plt.xlabel("(ID Sady atributů, Název scénáře)")
            plt.ylabel("Průměrné poškození")
            plt.xticks(rotation=45, ha='right')
            plt.legend(title="Typ jednotky", bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()
            plt.savefig(os.path.join(current_output_dir, f'prumerne_zpusobene_poskozeni{sada_suffix}.png'))
            plt.close()
            print(f"Graf 'prumerne_zpusobene_poskozeni{sada_suffix}.png' uložen.")
        else:
            print("Data pro graf průměrného způsobeného poškození jsou prázdná po pivotování.")
    else:
        print(
            "Nelze vygenerovat graf průměrného způsobeného poškození: data nejsou k dispozici pro tento název simulace.")

    # Graf 4: Průměrné přijaté poškození za kolo
    if not detail_plot_data_filtered.empty and 'Prijate_poskozeni__mean' in detail_plot_data_filtered.columns:
        plot_data = detail_plot_data_filtered.pivot_table(
            index=['id_atribut_sada', 'scenar_nazev'],
            columns='typ',
            values='Prijate_poskozeni__mean'
        )
        if not plot_data.empty:
            num_x_elements = len(plot_data.index)
            fig_width = max(12, num_x_elements * 0.8)
            plt.figure(figsize=(fig_width, 8))
            plot_data.plot(kind='bar', ax=plt.gca())

            plt.title(f"Průměrné přijaté poškození za kolo na jednotku (Mean) pro '{current_nazev}'")
            plt.xlabel("(ID Sady atributů, Název scénáře)")
            plt.ylabel("Průměrné poškození")
            plt.xticks(rotation=45, ha='right')
            plt.legend(title="Typ jednotky", bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()
            plt.savefig(os.path.join(current_output_dir, f'prumerne_prijate_poskozeni{sada_suffix}.png'))
            plt.close()
            print(f"Graf 'prumerne_prijate_poskozeni{sada_suffix}.png' uložen.")
        else:
            print("Data pro graf průměrného přijatého poškození jsou prázdná po pivotování.")
    else:
        print(
            "Nelze vygenerovat graf průměrného přijatého poškození: data nejsou k dispozici pro tento název simulace.")

    # Graf 5: Průměrná délka života jednotek
    if not detail_plot_data_filtered.empty and 'Průměrná_délka_života_kol' in detail_plot_data_filtered.columns:
        plot_data = detail_plot_data_filtered.pivot_table(
            index=['id_atribut_sada', 'scenar_nazev'],
            columns='typ',
            values='Průměrná_délka_života_kol'
        )
        if not plot_data.empty:
            num_x_elements = len(plot_data.index)
            fig_width = max(12, num_x_elements * 0.8)
            plt.figure(figsize=(fig_width, 8))
            plot_data.plot(kind='bar', ax=plt.gca())

            plt.title(f"Průměrná délka života jednotek v kolech pro '{current_nazev}'")
            plt.xlabel("(ID Sady atributů, Název scénáře)")
            plt.ylabel("Průměr kol do smrti")
            plt.xticks(rotation=45, ha='right')
            plt.legend(title="Typ jednotky", bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()
            plt.savefig(os.path.join(current_output_dir, f'prumerna_delka_zivota{sada_suffix}.png'))
            plt.close()
            print(f"Graf 'prumerna_delka_zivota{sada_suffix}.png' uložen.")
        else:
            print("Data pro graf průměrné délky života jsou prázdná po pivotování.")
    else:
        print("Nelze vygenerovat graf průměrné délky života: data nejsou k dispozici pro tento název simulace.")

print(
    "\n--- Analýza dat dokončena. Dvě hlavní tabulky jsou uloženy přímo ve složce 'agregovane_vystupy'. Grafy jsou organizovány v podsložkách dle názvu simulace a obsahují v názvu souboru informaci o sadě atributů. ---")