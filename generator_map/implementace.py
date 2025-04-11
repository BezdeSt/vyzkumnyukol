import jednotka
import hrac
import budova
import ekonomika
import hra
mrizka = [
    ['H', 'H', 'P', 'P', 'P'],
    ['L', 'P', 'L', 'H', 'P'],
    ['P', 'P', 'P', 'P', 'P'],
    ['P', 'H', 'L', 'V', 'P'],
    ['P', 'P', 'P', 'P', 'P'],
]

# Vytvoření hráčů
hrac1 = hrac.Hrac(jmeno="Modrý")
hrac2 = hrac.Hrac(jmeno="Červený")

# Slovník jednotek na poli (pozice: jednotka)
jednotky = {}

# Vytvoření jednotek a jejich registrace
jednotka1 = ekonomika.verbovani(jednotky, 'testovaci', (0,0), hrac1)
jednotka2 = ekonomika.verbovani(jednotky, 'testovaci', (0,2), hrac2)

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
    mozne_pohyby = jednotka1.vypocet_moznych_pohybu(mrizka)
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
    ekonomika.verbovani(jednotky, 'lucisnik', (3,3), hrac2)
    print(hrac2.jednotky)
    print('-----------')
    hrac2.pridej_suroviny({"jidlo": 10,"drevo": 10,"kamen": 0})
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
hra = hra.SpravceHry([hrac1, hrac2], mrizka, jednotky, budovy)
def tah():
    hrac1.pridej_suroviny({'jidlo': 5})
    hrac2.pridej_suroviny({'jidlo': 15})
    for _ in range(10):
        hra.proved_tah()

def test_budovy():
    print(hrac2.budovy)
    print(hrac2.suroviny)
    domek = ekonomika.stavba_budovy(budovy, 'domek', (0, 0), hrac2)
    print(hrac2.budovy)
    hrac2.pridej_suroviny({'drevo': 6})
    domek2 = ekonomika.stavba_budovy(budovy, 'domek', (0, 0), hrac2)
    print(hrac2.budovy)
    print(hrac2.suroviny)

# Spuštění testů
#pohyb()
print("=====================")
#boj()
#ekonomika_basic()
#test_verbovani()
#test_cena_za_kolo()
#tah()
test_budovy()

