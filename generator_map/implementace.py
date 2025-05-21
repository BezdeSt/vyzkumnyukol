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
    ['P', 'P','P', 'P', 'L', 'L', 'H', 'H', 'H', 'L', 'L', 'P', 'P', 'P', 'P'],
    ['P', 'P','P', 'P', 'L', 'L', 'H', 'H', 'H', 'L', 'L', 'P', 'P', 'P', 'P'],
    ['P', 'P','P', 'P', 'L', 'L', 'H', 'H', 'H', 'L', 'L', 'P', 'P', 'P', 'P'],
    ['P', 'P','P', 'P', 'L', 'L', 'H', 'H', 'H', 'L', 'L', 'P', 'P', 'P', 'P'],
    ['P', 'P','P', 'P', 'L', 'L', 'H', 'H', 'H', 'L', 'L', 'P', 'P', 'P', 'P'],
    ['P', 'P','P', 'P', 'L', 'L', 'H', 'H', 'H', 'L', 'L', 'P', 'P', 'P', 'P'],
    ['P', 'P','P', 'P', 'L', 'L', 'H', 'H', 'H', 'L', 'L', 'P', 'P', 'P', 'P'],
    ['P', 'P','P', 'P', 'L', 'L', 'H', 'H', 'H', 'L', 'L', 'P', 'P', 'P', 'P'],
    ['P', 'P','P', 'P', 'L', 'L', 'H', 'H', 'H', 'L', 'L', 'P', 'P', 'P', 'P'],
    ['P', 'P','P', 'P', 'L', 'L', 'H', 'H', 'H', 'L', 'L', 'P', 'P', 'P', 'P'],
    ['P', 'P','P', 'P', 'L', 'L', 'H', 'H', 'H', 'L', 'L', 'P', 'P', 'P', 'P'],
    ['P', 'P','P', 'P', 'L', 'L', 'H', 'H', 'H', 'L', 'L', 'P', 'P', 'P', 'P'],
    ['P', 'P','P', 'P', 'L', 'L', 'H', 'H', 'H', 'L', 'L', 'P', 'P', 'P', 'P'],
    ['P', 'P','P', 'P', 'L', 'L', 'H', 'H', 'H', 'L', 'L', 'P', 'P', 'P', 'P'],
    ['P', 'P','P', 'P', 'L', 'L', 'H', 'H', 'H', 'L', 'L', 'P', 'P', 'P', 'P'],

]

mapa_line = [
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
]
#pozice=(0, 0)
#pozice=(14, 0)
duel = "Válečník_vs_Lučištník"

def jednaVSjedna_Linie():
    nazev_scenare = duel+"--Linie"
    for i in range(10):
        Hra = hra.SpravceHry(hraci=[], mrizka=mapa_line, jednotky={}, budovy=[], scenar_nazev=nazev_scenare)
        Hra.inicializace_scenare("Hráč 1", "Hráč 2")
        hrac1 = Hra.hraci[0]
        hrac2 = Hra.hraci[1]

        hrac1.pridej_suroviny({'jidlo': 9999, 'drevo': 9999, 'kamen': 9999})
        hrac2.pridej_suroviny({'jidlo': 9999, 'drevo': 9999, 'kamen': 9999})
        # Umístíme jednotky blízko sebe, aby došlo k souboji
        Hra.verbovani('valecnik', hrac1, Hra, pozice=(0, 0))
        Hra.verbovani('lucisnik', hrac2, Hra, pozice=(14, 0))
        print('===')
        Hra.simulace.log_stav_kola(0, Hra.jednotky)  # Nulté kolo

        while Hra.stav_hry:
            Hra.proved_tah()
            if Hra.kolo > 1000:  # Omezíme počet kol pro testování
                break

        for jednotka in Hra.jednotky.values():
            print(f"{jednotka.typ} má {jednotka.zivoty} životů")

        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        nazev_souboru_pro_prubeh = f"{Hra.simulace.scenar_nazev}_prubeh_simulaci.csv"  # Používáme název scénáře
        Hra.simulace.uloz_prubeh_do_souboru(nazev_souboru_pro_prubeh)


def jednaVSjedna_Flat():
    nazev_scenare = duel+"--Flat"
    for i in range(10):
        Hra = hra.SpravceHry(hraci=[], mrizka=mapa_flat, jednotky={}, budovy=[], scenar_nazev=nazev_scenare)
        Hra.inicializace_scenare("Hráč 1", "Hráč 2")
        hrac1 = Hra.hraci[0]
        hrac2 = Hra.hraci[1]

        hrac1.pridej_suroviny({'jidlo': 9999, 'drevo': 9999, 'kamen': 9999})
        hrac2.pridej_suroviny({'jidlo': 9999, 'drevo': 9999, 'kamen': 9999})
        # Umístíme jednotky blízko sebe, aby došlo k souboji
        Hra.verbovani('valecnik', hrac1, Hra, pozice=(0, 0))
        Hra.verbovani('lucisnik', hrac2, Hra, pozice=(14, 14))
        print('===')
        Hra.simulace.log_stav_kola(0, Hra.jednotky)  # Nulté kolo

        while Hra.stav_hry:
            Hra.proved_tah()
            if Hra.kolo > 1000:  # Omezíme počet kol pro testování
                break

        for jednotka in Hra.jednotky.values():
            print(f"{jednotka.typ} má {jednotka.zivoty} životů")

        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        nazev_souboru_pro_prubeh = f"{Hra.simulace.scenar_nazev}_prubeh_simulaci.csv"  # Používáme název scénáře
        Hra.simulace.uloz_prubeh_do_souboru(nazev_souboru_pro_prubeh)

def jednaVSjedna_NonFlat():
    nazev_scenare = duel+"--NonFlat"
    for i in range(10):
        Hra = hra.SpravceHry(hraci=[], mrizka=mapa_non_flat, jednotky={}, budovy=[], scenar_nazev=nazev_scenare)
        Hra.inicializace_scenare("Hráč 1", "Hráč 2")
        hrac1 = Hra.hraci[0]
        hrac2 = Hra.hraci[1]

        hrac1.pridej_suroviny({'jidlo': 9999, 'drevo': 9999, 'kamen': 9999})
        hrac2.pridej_suroviny({'jidlo': 9999, 'drevo': 9999, 'kamen': 9999})
        # Umístíme jednotky blízko sebe, aby došlo k souboji
        Hra.verbovani('valecnik', hrac1, Hra, pozice=(0, 0))
        Hra.verbovani('lucisnik', hrac2, Hra, pozice=(14, 14))
        print('===')
        Hra.simulace.log_stav_kola(0, Hra.jednotky)  # Nulté kolo

        while Hra.stav_hry:
            Hra.proved_tah()
            if Hra.kolo > 1000:  # Omezíme počet kol pro testování
                break

        for jednotka in Hra.jednotky.values():
            print(f"{jednotka.typ} má {jednotka.zivoty} životů")

        print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
        nazev_souboru_pro_prubeh = f"{Hra.simulace.scenar_nazev}_prubeh_simulaci.csv"  # Používáme název scénáře
        Hra.simulace.uloz_prubeh_do_souboru(nazev_souboru_pro_prubeh)

jednaVSjedna_Linie()

#jednaVSjedna_Flat()

#jednaVSjedna_NonFlat()