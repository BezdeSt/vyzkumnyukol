import hra
import vyskove_mapy

#mapa = vyskove_mapy.cislo_na_policko(vyskove_mapy.perlin_noise_pole(50, 50, scale=10))
#vyskove_mapy.zobraz_mapu(mapa)

mapa_flat = [
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
]
#pozice=(0, 0)
#pozice=(7, 7)

mapa_non_flat = [
    ['P', 'P', 'P', 'H', 'H', 'P', 'P', 'P'],
    ['P', 'P', 'P', 'H', 'H', 'P', 'P', 'P'],
    ['P', 'P', 'P', 'H', 'H', 'P', 'P', 'P'],
    ['P', 'P', 'P', 'H', 'H', 'P', 'P', 'P'],
]

mapa_line = [
    ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
]
#pozice=(0, 0)
#pozice=(14, 0)

def jednaVSjedna():
    nazev_scenare = "Válečník vs. Lučištník; Flat"
    Hra = hra.SpravceHry(hraci=[], mrizka=mapa_line, jednotky={}, budovy=[], Simulace=nazev_scenare)
    Hra.inicializace_scenare("Hráč Válečník", "Hráč Lučíštník")
    hrac1 = Hra.hraci[0]
    hrac2 = Hra.hraci[1]

    hrac1.pridej_suroviny({'jidlo': 9999, 'drevo': 9999, 'kamen': 9999})
    hrac2.pridej_suroviny({'jidlo': 9999, 'drevo': 9999, 'kamen': 9999})
    # Umístíme jednotky blízko sebe, aby došlo k souboji
    Hra.verbovani('valecnik', hrac1, Hra, pozice=(0, 0))
    Hra.verbovani('lucisnik', hrac2, Hra, pozice=(14, 0))
    print('===')

    while Hra.stav_hry:
        Hra.proved_tah()
        if Hra.kolo > 1000:  # Omezíme počet kol pro testování
            break

    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    Hra.simulace.vypis_prubeh() # Používáme správný název instance loggeru

    Hra.simulace.vypis_vysledky() # Používáme správný název instance loggeru

jednaVSjedna()