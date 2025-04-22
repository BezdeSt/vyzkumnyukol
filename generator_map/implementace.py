import jednotka
import hrac
import budova
import hra
import vyskove_mapy

mapa = vyskove_mapy.cislo_na_policko(vyskove_mapy.perlin_noise_pole(50, 50, scale=10))
vyskove_mapy.zobraz_mapu(mapa)

def test_ai():
    Hra = hra.SpravceHry(hraci=[], mrizka=mapa, jednotky={}, budovy=[])
    Hra.inicializace_hry()

    hrac1 = Hra.hraci[0]
    hrac2 = Hra.hraci[1]
    hrac1.pridej_suroviny({'drevo': 10})
    hrac2.pridej_suroviny({'drevo': 10})
    Hra.verbovani('testovaci', hrac1, Hra)
    Hra.verbovani('testovaci', hrac2, Hra)
    print('===')

    while Hra.stav_hry:
        Hra.proved_tah()
        print('-')
        if Hra.kolo > 1000:
            break

    print("--- Po tazích ---")
    for h in Hra.hraci:
        print(f"{h.jmeno}: suroviny: {h.suroviny}, jednotky: {[(j.typ, j.pozice, j.zivoty) for j in h.jednotky]}")
        print(f"  budovy:  {[(b.typ, b.zivoty) for b in h.budovy]}")

    # Stav pole na konci hry
    print('Stav pole na konci hry:')
    matice = [[0 for _ in range(len(Hra.mrizka[0]))] for _ in range(len(Hra.mrizka))]
    for y in range(len(Hra.mrizka)):
        for x in range(len(Hra.mrizka[0])):
            if (x, y) in Hra.jednotky:
                matice[y][x] = 1

    for radek in matice:
        print(radek)

    print("XXXXXXXXXXXXXXXXXXXX")
    Hra.simulace.vypis_prubeh()

    Hra.simulace.vypis_vysledky()

def test_ai_pohyb():
    Hra = hra.SpravceHry(hraci=[], mrizka=mapa, jednotky={}, budovy=[])
    Hra.inicializace_hry()
    hrac1 = Hra.hraci[0]
    hrac2 = Hra.hraci[1]

    hrac1.pridej_suroviny({'jidlo': 10, 'drevo': 2})
    Hra.verbovani('bojovnik', hrac1, Hra)
    print('===')

    while Hra.stav_hry:
        Hra.proved_tah()
        if Hra.kolo > 2:
            break

    print("--- Po tazích ---")
    for h in Hra.hraci:
        print(f"{h.jmeno}: suroviny: {h.suroviny}, jednotky: {[(j.typ, j.pozice, j.zivoty) for j in h.jednotky]}")
        print(f"  budovy:  {[(b.typ, b.zivoty) for b in h.budovy]}")

    # Stav pole na konci hry
    print('Stav pole na konci hry:')
    matice = [[0 for _ in range(len(Hra.mrizka[0]))] for _ in range(len(Hra.mrizka))]
    for y in range(len(Hra.mrizka)):
        for x in range(len(Hra.mrizka[0])):
            if (x, y) in Hra.jednotky:
                matice[y][x] = 1

    for radek in matice:
        print(radek)


    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

    Hra.simulace.vypis_vysledky()

    Hra.simulace.vypis_prubeh()

#test_ai_pohyb()
test_ai()