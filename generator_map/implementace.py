def vypocet_moznych_pohybu(pozice, vzdalenost, mrizka):
    """
    Vypočítá možné pohyby z dané pozice s ohledem na terén a omezením vzdálenosti.

    Args:
        pozice: Aktuální pozice (x, y).
        vzdalenost: Maximální povolená vzdálenost pohybu.
        mrizka (list[list]): 2D mřížka s terény (V, P, L, H).

    Returns: Seznam možných pozic pro pohyb.
    """

    x, y = pozice
    mozne_pohyby = []
    navstivene = {pozice}  # Sledování navštívených pozic
    fronta = [(pozice, vzdalenost)]  # Fronta pro prohledávání

    while fronta:
        aktualni_pozice, zbyvajici_vzdalenost = fronta.pop(0)
        x, y = aktualni_pozice

        mozne_pohyby.append(aktualni_pozice)

        if zbyvajici_vzdalenost <= 0:
            continue

        sousedni_pohyby = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]

        for nova_x, nova_y in sousedni_pohyby:
            if 0 <= nova_x < len(mrizka[0]) and 0 <= nova_y < len(mrizka) and (nova_x, nova_y) not in navstivene:
                teren = mrizka[nova_y][nova_x]
                if teren == 'V':
                    continue  # Voda je neprůchodná

                navstivene.add((nova_x, nova_y))
                if teren == 'P':
                    fronta.append(((nova_x, nova_y), zbyvajici_vzdalenost - 1))
                elif teren == 'L':
                    fronta.append(((nova_x, nova_y), zbyvajici_vzdalenost - 2))
                elif teren == 'H':
                    fronta.append(((nova_x, nova_y), 0)) # pohyb končí na hoře.

    return mozne_pohyby


def pozice_na_matici(pozice_seznam, sirka, vyska):
    """
    Převede seznam pozic (x, y) na matici 1 a 0.

    Args:
        pozice_seznam: Seznam povolených pozic.
        sirka: Šířka mřížky.
        vyska: Výška mřížky.

    Returns: Matice 1 a 0, kde 1 označuje povolenou pozici.
    """

    matice = [[0 for _ in range(sirka)] for _ in range(vyska)]
    for x, y in pozice_seznam:
        matice[y][x] = 1
    return matice

def proved_pohyb(pozice, cil, mozne_pohyby):
    """
    Provádí pohyb z pozice na cíl, pokud je to možné.

    Args:
        pozice: Aktuální pozice (x, y).
        cil: Cílová pozice (x, y).
        mozne_pohyby: Seznam možných pozic pro pohyb.
        mrizka: 2D mřížka s terény (V, P, L, H).

    Returns: Nová pozice po pohybu nebo původní pozice, pokud je pohyb neplatný.
    """

    x, y = pozice
    cil_x, cil_y = cil

    if cil in mozne_pohyby:
        return cil
    else:
        return pozice

# Příklad použití
mrizka = [
    ['H', 'H', 'P', 'P', 'P'],
    ['L', 'P', 'L', 'H', 'P'],
    ['P', 'P', 'P', 'P', 'P'],
    ['P', 'H', 'L', 'V', 'P'],
    ['P', 'P', 'P', 'P', 'P'],
]

pozice = (0, 0)
vzdalenost = 3
cil = (1, 0)

mozne_pohyby = vypocet_moznych_pohybu(pozice, vzdalenost, mrizka)
print("Možné pohyby:", mozne_pohyby)

# Příklad použití (pokračování z předchozího příkladu)
vyska = len(mrizka)
sirka = len(mrizka[0])

matice_pohybu = pozice_na_matici(mozne_pohyby, sirka, vyska)

# Výpis matice pro vizualizaci
for radek in matice_pohybu:
    print(radek)

nova_pozice = proved_pohyb(pozice, cil, mozne_pohyby)
print("Nová pozice:", nova_pozice)