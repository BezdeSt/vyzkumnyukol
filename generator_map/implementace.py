import jednotka
import hrac
#TODO: class Hráč
#TODO: class Budova
#   hradby zatím nebudu řešit
mrizka = [
    ['H', 'H', 'P', 'P', 'P'],
    ['L', 'P', 'L', 'H', 'P'],
    ['P', 'P', 'P', 'P', 'P'],
    ['P', 'H', 'L', 'V', 'P'],
    ['P', 'P', 'P', 'P', 'P'],
]

def nova_jednotka(jednotky, pozice, rychlost, dosah, utok, obrana, zivoty, vlastnik):
    nova_jednotka = jednotka.Jednotka(pozice, rychlost, dosah, utok, obrana, zivoty, vlastnik)
    jednotky[pozice] = nova_jednotka
    return nova_jednotka

# Vytvoření hráčů
hrac1 = hrac.Hrac(jmeno="Modrý")
hrac2 = hrac.Hrac(jmeno="Červený")

# Slovník jednotek na poli (pozice: jednotka)
jednotky = {}

# Vytvoření jednotek a jejich registrace
jednotka1 = nova_jednotka(jednotky, pozice=(0, 0), rychlost=3, dosah=3, utok=12, obrana=1, zivoty=10, vlastnik=hrac1)
jednotka2 = nova_jednotka(jednotky, pozice=(0, 2), rychlost=1, dosah=5, utok=2, obrana=2, zivoty=10, vlastnik=hrac2)

# Zapsání jednotek do mapy
jednotky[jednotka1.pozice] = jednotka1
jednotky[jednotka2.pozice] = jednotka2

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

# Spuštění testů
#pohyb()
print("=====================")
boj()