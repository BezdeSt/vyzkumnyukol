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

mapa_line = [
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
]
#pozice=(0, 0)
#pozice=(14, 0)
duel = "Válečník_vs_Lučištník"

global_sim_id_counter = 0

def jednaVSjedna_Linie():
    global global_sim_id_counter # Abychom mohli modifikovat globální proměnnou
    nazev_scenare = duel+"--Linie"
    for i in range(10): # Zachováváme 10 opakování, jak sis přál
        global_sim_id_counter += 1 # Inkrementujeme ID pro každou simulaci
        current_sim_id = global_sim_id_counter

        # Předáme id_simulace do SpravceHry
        Hra = hra.SpravceHry(hraci=[], mrizka=mapa_line, jednotky={}, budovy=[], scenar_nazev=nazev_scenare, id_simulace=current_sim_id)
        Hra.inicializace_scenare("Hráč 1", "Hráč 2")
        hrac1 = Hra.hraci[0]
        hrac2 = Hra.hraci[1]

        hrac1.pridej_suroviny({'jidlo': 9999, 'drevo': 9999, 'kamen': 9999})
        hrac2.pridej_suroviny({'jidlo': 9999, 'drevo': 9999, 'kamen': 9999})
        Hra.verbovani('valecnik', hrac1, Hra, pozice=(0, 0))
        Hra.verbovani('lucisnik', hrac2, Hra, pozice=(14, 0))
        print('===')
        Hra.simulace.log_stav_kola(0, Hra.jednotky) # Nulté kolo

        while Hra.stav_hry:
            Hra.proved_tah()
            if Hra.kolo > 1000:
                break

        for jednotka in Hra.jednotky.values():
            print(f"{jednotka.typ} má {jednotka.zivoty} životů")

        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        # Používáme fixní názvy souborů, aby se data appendovala
        nazev_souboru_prubeh = f"prubeh_simulaci_{nazev_scenare}.csv"
        Hra.simulace.uloz_prubeh_do_souboru(nazev_souboru_prubeh)

        nazev_souboru_metadata = f"metadata_{nazev_scenare}.csv"
        Hra.simulace.uloz_metadata_jednotek_do_souboru(nazev_souboru_metadata)


def jednaVSjedna_Flat():
    global global_sim_id_counter
    nazev_scenare = duel+"--Flat"
    for i in range(10):
        global_sim_id_counter += 1
        current_sim_id = global_sim_id_counter

        Hra = hra.SpravceHry(hraci=[], mrizka=mapa_flat, jednotky={}, budovy=[], scenar_nazev=nazev_scenare, id_simulace=current_sim_id)
        Hra.inicializace_scenare("Hráč 1", "Hráč 2")
        hrac1 = Hra.hraci[0]
        hrac2 = Hra.hraci[1]

        hrac1.pridej_suroviny({'jidlo': 9999, 'drevo': 9999, 'kamen': 9999})
        hrac2.pridej_suroviny({'jidlo': 9999, 'drevo': 9999, 'kamen': 9999})
        Hra.verbovani('valecnik', hrac1, Hra, pozice=(0, 0))
        Hra.verbovani('lucisnik', hrac2, Hra, pozice=(14, 14))
        print('===')
        Hra.simulace.log_stav_kola(0, Hra.jednotky)

        while Hra.stav_hry:
            Hra.proved_tah()
            if Hra.kolo > 1000:
                break

        for jednotka in Hra.jednotky.values():
            print(f"{jednotka.typ} má {jednotka.zivoty} životů")

        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        nazev_souboru_prubeh = f"prubeh_simulaci_{nazev_scenare}.csv"
        Hra.simulace.uloz_prubeh_do_souboru(nazev_souboru_prubeh)

        nazev_souboru_metadata = f"metadata_{nazev_scenare}.csv"
        Hra.simulace.uloz_metadata_jednotek_do_souboru(nazev_souboru_metadata)


def jednaVSjedna_NonFlat():
    global global_sim_id_counter
    nazev_scenare = duel+"--NonFlat"
    for i in range(10):
        global_sim_id_counter += 1
        current_sim_id = global_sim_id_counter

        Hra = hra.SpravceHry(hraci=[], mrizka=mapa_non_flat, jednotky={}, budovy=[], scenar_nazev=nazev_scenare, id_simulace=current_sim_id)
        Hra.inicializace_scenare("Hráč 1", "Hráč 2")
        hrac1 = Hra.hraci[0]
        hrac2 = Hra.hraci[1]

        hrac1.pridej_suroviny({'jidlo': 9999, 'drevo': 9999, 'kamen': 9999})
        hrac2.pridej_suroviny({'jidlo': 9999, 'drevo': 9999, 'kamen': 9999})
        Hra.verbovani('valecnik', hrac1, Hra, pozice=(0, 0))
        Hra.verbovani('lucisnik', hrac2, Hra, pozice=(14, 14))
        print('===')
        Hra.simulace.log_stav_kola(0, Hra.jednotky)

        while Hra.stav_hry:
            Hra.proved_tah()
            if Hra.kolo > 1000:
                break

        for jednotka in Hra.jednotky.values():
            print(f"{jednotka.typ} má {jednotka.zivoty} životů")

        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        nazev_souboru_prubeh = f"prubeh_simulaci_{nazev_scenare}.csv"
        Hra.simulace.uloz_prubeh_do_souboru(nazev_souboru_prubeh)

        nazev_souboru_metadata = f"metadata_{nazev_scenare}.csv"
        Hra.simulace.uloz_metadata_jednotek_do_souboru(nazev_souboru_metadata)

#jednaVSjedna_Linie()

#jednaVSjedna_Flat()

#jednaVSjedna_NonFlat()


def jednaVSjedna():
    global global_sim_id_counter # Abychom mohli modifikovat globální proměnnou
    nazev_scenare = [duel+"--Linie", duel+"--Flat",duel+"--NonFlat"]
    mapa_scenare = [mapa_line, mapa_flat, mapa_non_flat]
    for i in range(3): # Zachováváme 10 opakování, jak sis přál
        global_sim_id_counter += 1 # Inkrementujeme ID pro každou simulaci
        current_sim_id = global_sim_id_counter

        # Předáme id_simulace do SpravceHry
        Hra = hra.SpravceHry(hraci=[], mrizka=mapa_scenare[i], jednotky={}, budovy=[], scenar_nazev=nazev_scenare[i], id_simulace=current_sim_id)
        Hra.inicializace_scenare("Hráč 1", "Hráč 2")
        hrac1 = Hra.hraci[0]
        hrac2 = Hra.hraci[1]

        hrac1.pridej_suroviny({'jidlo': 9999, 'drevo': 9999, 'kamen': 9999})
        hrac2.pridej_suroviny({'jidlo': 9999, 'drevo': 9999, 'kamen': 9999})
        Hra.verbovani('valecnik', hrac1, Hra, pozice=(0, 0))
        if i == 0:
            Hra.verbovani('lucistnik', hrac2, Hra, pozice=(14, 0))
        else:
            Hra.verbovani('lucistnik', hrac2, Hra, pozice=(14, 14))
        print('===')
        Hra.simulace.log_stav_kola(0, Hra.jednotky) # Nulté kolo

        while Hra.stav_hry:
            Hra.proved_tah()
            if Hra.kolo > 1000:
                break

        for jednotka in Hra.jednotky.values():
            print(f"{jednotka.typ} má {jednotka.zivoty} životů")

        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        # Používáme fixní názvy souborů, aby se data appendovala
        nazev_souboru_prubeh = f"prubeh_simulaci_{duel}.csv"
        Hra.simulace.uloz_prubeh_do_souboru(nazev_souboru_prubeh)

        nazev_souboru_metadata = f"metadata_{duel}.csv"
        Hra.simulace.uloz_metadata_jednotek_do_souboru(nazev_souboru_metadata)

jednaVSjedna()