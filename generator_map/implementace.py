import jednotka
import hrac
import budova
import ekonomika
import hra
mrizka0 = [
    ['H', 'H', 'P', 'P', 'P'],
    ['P', 'P', 'L', 'H', 'P'],
    ['P', 'P', 'P', 'P', 'P'],
    ['P', 'H', 'L', 'V', 'P'],
    ['P', 'P', 'P', 'P', 'P'],
]
mrizka = [
    ['P', 'P', 'P', 'P', 'P'],
    ['P', 'P', 'P', 'P', 'P'],
    ['P', 'P', 'P', 'P', 'P'],
    ['P', 'P', 'P', 'P', 'P'],
    ['P', 'P', 'P', 'P', 'P'],
]
def puvodni():
    # Vytvoření hráčů
    hrac1 = hrac.Hrac(jmeno="Modrý")
    hrac2 = hrac.Hrac(jmeno="Červený")

    # Slovník jednotek na poli (pozice: jednotka)
    jednotky = {}

    # Vytvoření jednotek a jejich registrace
    jednotka1 = ekonomika.verbovani(jednotky, 'testovaci', (0, 0), hrac1)
    jednotka2 = ekonomika.verbovani(jednotky, 'testovaci', (0, 3), hrac2)

    dul = budova.Budova(
        typ="Důl",
        pozice=(2, 3),
        vlastnik=hrac1,
        zivoty=30,
        obrana=2,
        produkce={"kámen": 3}
    )

    # Funkce pro testování pohybu
    def pohyb():
        mozne_pohyby = jednotka1.vypocet_moznych_pohybu(mrizka, jednotky)
        print("Možné pohyby:", mozne_pohyby)

        vyska = len(mrizka)
        sirka = len(mrizka[0])

        matice_pohybu = jednotka1.pozice_na_matici(mozne_pohyby, sirka, vyska)

        for radek in matice_pohybu:
            print(radek)

        jednotka1.proved_pohyb((1, 0), mozne_pohyby, jednotky)
        print("Nová pozice jednotky 1:", jednotka1.pozice)

    # Funkce pro testování boje
    def boj():
        cile = jednotka1.najdi_cile_v_dosahu(mrizka, jednotky)
        print("Cíle v dosahu:")
        for cilova_jednotka in cile:
            print(f"  Pozice: {cilova_jednotka.pozice}")
            print(f"  Jednotka1 životy: {jednotka1.zivoty}")
            print(f"  Jednotka2 životy: {cilova_jednotka.zivoty}")

            jednotka1.vyhodnot_souboj(cilova_jednotka, jednotky, mrizka)

            print("--------")
            print(f"  Jednotka1 životy: {jednotka1.zivoty}")
            print(f"  Jednotka2 životy: {cilova_jednotka.zivoty}")

    def ekonomika_basic():
        souhrn = {}
        for budova in hrac1.budovy:
            produkce = budova.generuj_suroviny()
            for typ, mnozstvi in produkce.items():
                souhrn[typ] = souhrn.get(typ, 0) + mnozstvi
        hrac1.pridej_suroviny(souhrn)
        print(f"{hrac1.jmeno} získal: {souhrn}")
        print(f"{hrac1.jmeno} má: {hrac1.suroviny}")

    def test_verbovani():

        print(hrac2.jednotky)
        ekonomika.verbovani(jednotky, 'lucisnik', (3, 3), hrac2)
        print(hrac2.jednotky)
        print('-----------')
        hrac2.pridej_suroviny({"jidlo": 10, "drevo": 10, "kamen": 0})
        print(hrac2.suroviny)
        print(hrac2.jednotky)
        ekonomika.verbovani(jednotky, 'lucisnik', (3, 3), hrac2)
        print(hrac2.jednotky)
        print(hrac2.suroviny)

    def test_cena_za_kolo():
        hrac1.pridej_suroviny({'jidlo': 1})
        hrac1.zisk_z_budov()
        print(hrac1.jednotky)
        print(hrac1.jednotky[0].zivoty)
        print(hrac1.suroviny)
        hrac1.zpracuj_udrzbu(jednotky)
        print('---')
        print(hrac1.jednotky)
        # print(hrac1.jednotky[0].zivoty)
        print(hrac1.suroviny)

    # TODO: V plné verzi tohle bude taky slovník s pozicema jako jednotky
    budovy = hrac1.budovy + hrac2.budovy
    hra0 = hra.SpravceHry([hrac1, hrac2], mrizka, jednotky, budovy)

    def tah():
        hrac1.pridej_suroviny({'jidlo': 5})
        hrac2.pridej_suroviny({'jidlo': 15})
        for _ in range(10):
            hra0.proved_tah()

    def test_budovy():
        print(budovy)
        print('-')
        print(hrac2.budovy)
        # print(hrac2.suroviny)
        domek = ekonomika.stavba_budovy(budovy, 'domek', (0, 0), hrac2)
        print(hrac2.budovy)
        hrac2.pridej_suroviny({'drevo': 6})
        domek2 = ekonomika.stavba_budovy(budovy, 'domek', (0, 0), hrac2)
        print(hrac2.budovy)
        # print(hrac2.suroviny)
        print('-')
        print(budovy)

    pohyb()
    print("=====================")
    # boj()
    # ekonomika_basic()
    test_verbovani()
    # test_cena_za_kolo()
    # tah()
    # test_budovy()

# Spuštění testů

# TODO: Testovat:
#   Inicializaci hry
#   Ukončení hry zničením základny
def herni_cyklus():
    Hra = hra.SpravceHry(hraci=[],mrizka=mrizka,jednotky={},budovy=[])

    Hra.inicializace_hry()
    hrac1 = Hra.hraci[0]
    hrac2 = Hra.hraci[1]

    print('---')
    Hra.verbovani('testovaci', hrac1, Hra)
    Hra.verbovani('testovaci', hrac1, Hra)
    Hra.verbovani('testovaci', hrac1, Hra)
    Hra.verbovani('testovaci', hrac1, Hra)
    Hra.verbovani('testovaci', hrac1, Hra)
    Hra.verbovani('testovaci', hrac1, Hra)
    print('---')
    Hra.verbovani('testovaci', hrac2, Hra)
    hrac1.jednotky[1].zemri(Hra.jednotky)
    Hra.verbovani('testovaci', hrac1, Hra)

def test_ai():
    Hra = hra.SpravceHry(hraci=[], mrizka=mrizka, jednotky={}, budovy=[])
    Hra.inicializace_hry()

    hrac1 = Hra.hraci[0]
    hrac2 = Hra.hraci[1]
    hrac1.pridej_suroviny({'drevo': 10})
    hrac2.pridej_suroviny({'drevo': 10})
    Hra.verbovani('testovaci', hrac1, Hra)
    mozne_pohyby = hrac1.jednotky[1].vypocet_moznych_pohybu(Hra.mrizka, Hra.jednotky)
    #hrac1.jednotky[1].proved_pohyb((3,4), mozne_pohyby, Hra.jednotky)
    print('===')
    #TODO: Nereaguje když je vedle nepřítel
    while Hra.stav_hry:
        Hra.proved_tah()
        if Hra.kolo > 1:
            break

    print("--- Po tazích ---")
    for h in Hra.hraci:
        print(f"{h.jmeno}: suroviny: {h.suroviny}, jednotky: {[(j.typ, j.pozice, j.zivoty) for j in h.jednotky]}")

    # Stav pole na konci hry
    print('Stav pole na konci hry:')
    matice = [[0 for _ in range(len(Hra.mrizka[0]))] for _ in range(len(Hra.mrizka))]
    for y in range(len(Hra.mrizka)):
        for x in range(len(Hra.mrizka[0])):
            if (x, y) in Hra.jednotky:
                matice[y][x] = 1

    for radek in matice:
        print(radek)
test_ai()
#herni_cyklus()