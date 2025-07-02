import random
import csv
import os

import hra
import vyskove_mapy

#mapa = vyskove_mapy.cislo_na_policko(vyskove_mapy.perlin_noise_pole(50, 50, scale=10))
#vyskove_mapy.zobraz_mapu(mapa)

mapa_flat = [
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
]
#pozice=(0, 0)
#pozice=(14, 14)

mapa_non_flat = [
    ['P', 'P','P', 'P', 'L', 'L', 'L', 'H', 'L', 'L', 'L', 'P', 'P', 'P', 'P'],
    ['P', 'P','P', 'P', 'L', 'L', 'L', 'H', 'L', 'L', 'L', 'P', 'P', 'P', 'P'],
    ['P', 'P','P', 'P', 'L', 'L', 'L', 'H', 'L', 'L', 'L', 'P', 'P', 'P', 'P'],
    ['P', 'P','P', 'P', 'L', 'L', 'L', 'H', 'L', 'L', 'L', 'P', 'P', 'P', 'P'],
    ['P', 'P','P', 'P', 'L', 'L', 'L', 'H', 'L', 'L', 'L', 'P', 'P', 'P', 'P'],
    ['P', 'P','P', 'P', 'L', 'L', 'H', 'H', 'H', 'L', 'L', 'P', 'P', 'P', 'P'],
    ['P', 'P','P', 'P', 'L', 'H', 'H', 'H', 'H', 'H', 'L', 'P', 'P', 'P', 'P'],
    ['P', 'P','P', 'P', 'L', 'H', 'H', 'H', 'H', 'H', 'L', 'P', 'P', 'P', 'P'],
    ['P', 'P','P', 'P', 'L', 'H', 'H', 'H', 'H', 'H', 'L', 'P', 'P', 'P', 'P'],
    ['P', 'P','P', 'P', 'L', 'L', 'H', 'H', 'H', 'L', 'L', 'P', 'P', 'P', 'P'],
    ['P', 'P','P', 'P', 'L', 'L', 'L', 'H', 'L', 'L', 'L', 'P', 'P', 'P', 'P'],
    ['P', 'P','P', 'P', 'L', 'L', 'L', 'H', 'L', 'L', 'L', 'P', 'P', 'P', 'P'],
    ['P', 'P','P', 'P', 'L', 'L', 'L', 'H', 'L', 'L', 'L', 'P', 'P', 'P', 'P'],
    ['P', 'P','P', 'P', 'L', 'L', 'L', 'H', 'L', 'L', 'L', 'P', 'P', 'P', 'P'],
    ['P', 'P','P', 'P', 'L', 'L', 'L', 'H', 'L', 'L', 'L', 'P', 'P', 'P', 'P'],

]

#pozice=(0, 0)
#pozice=(14, 0)
duel = "Válečník_vs_Lučištník"
cislo_pokusu = "zaklad2"

def obsahuje_text_v_sloupci(cesta_k_csv, nazev_sloupce, hledany_text):
    """
    Zkontroluje, zda se v daném sloupci nachází hledaný text.

    :param cesta_k_csv: cesta k CSV souboru
    :param nazev_sloupce: název sloupce, ve kterém hledáme
    :param hledany_text: hledaný řetězec
    :return: True, pokud se text nachází, jinak False
    """
    if not os.path.exists(cesta_k_csv):
        print(f"Soubor '{cesta_k_csv}' neexistuje.")
        return False
    with open(cesta_k_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row.get(nazev_sloupce) == hledany_text:
                return True
    return False

global_sim_id_counter = 0

def jednaVSjedna():
    global global_sim_id_counter # Abychom mohli modifikovat globální proměnnou
    nazev_scenare = duel
    mapa_scenare = [mapa_flat, mapa_non_flat]
    mapa_scenare_nazev = ["rovina", "hora"]
    for mapa_id in range(len(mapa_scenare)):
        for i in range(1000):
            global_sim_id_counter += 1 # Inkrementujeme ID pro každou simulaci
            current_sim_id = global_sim_id_counter
            random.seed(current_sim_id)

            # Předáme id_simulace do SpravceHry
            Hra = hra.SpravceHry(
                hraci=[],
                mrizka=mapa_scenare[mapa_id],
                jednotky={},
                budovy=[],
                soubor_nazev=duel,  # Původní scenar_nazev, nyní pro název souboru
                scenar_nazev=mapa_scenare_nazev[mapa_id],  # Nový scenar_nazev pro sloupec (název mapy)
                id_simulace=current_sim_id,
                id_atribut_sada=cislo_pokusu  # Předání ID sady atributů
            )
            Hra.inicializace_scenare("Hráč 1", "Hráč 2")
            hrac1 = Hra.hraci[0]
            hrac2 = Hra.hraci[1]

            hrac1.pridej_suroviny({'jidlo': 9999, 'drevo': 9999, 'kamen': 9999})
            hrac2.pridej_suroviny({'jidlo': 9999, 'drevo': 9999, 'kamen': 9999})
            Hra.verbovani('valecnik', hrac1, Hra, pozice=(0, 0))
            Hra.verbovani('lucistnik', hrac2, Hra, pozice=(14, 14))
            print('===')
            Hra.simulace.log_stav_kola(0, Hra.jednotky, Hra.simulace.id_simulace) # Nulté kolo

            while Hra.stav_hry:
                Hra.proved_tah()
                print('-')
                for jednotka in Hra.jednotky.values():
                    print(f"{jednotka.typ} má {jednotka.zivoty} životů")
                print('-')
                if Hra.kolo > 100:
                    break

            for jednotka in Hra.jednotky.values():
                print(f"{jednotka.typ} má {jednotka.zivoty} životů")


if not obsahuje_text_v_sloupci('sim_logy/souhrn_simulaci.csv','id_atribut_sada',cislo_pokusu):
    jednaVSjedna()
else:
    print("Opakovaná název sady.")