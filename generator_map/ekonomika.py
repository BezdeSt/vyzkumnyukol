import jednotka
import budova

# TODO: Časem asi zabalit do hra.py

def ziskani_surovin(hraci):
    for hrac in hraci:
        hrac.zisk_z_budov()

def verbovani(jednotky, typ, pozice, vlastnik):
    """
    Verbování nové jednotky určitého typu.

    Args:
        jednotky: Slovník aktuálních jednotek na mapě.
        typ: Název typu jednotky ('bojovnik', 'lucisnik', ...).
        pozice: Pozice, kde má být jednotka vytvořena.
        vlastnik: Instance hráče, který jednotku verbuje.

    Returns:
        Nová jednotka nebo None, pokud hráč nemá dost surovin.
    """
    if pozice in jednotky:
        print("Pozice je obsazená, jednotku není možné naverbovat.")
        return None

    # TODO: Základna je udělaná jako jednotka pouze v prototypu
    if typ == 'zakladna':
        for jedn in vlastnik.jednotky:
            if jedn.typ == 'zakladna':
                print(f"{vlastnik.jmeno} už má základnu, nelze vytvořit další.")
                return None

    # Předdefinované šablony jednotek
    sablony = {
        'bojovnik': {
            'typ': 'bojovnik',
            'rychlost': 3,
            'dosah': 1,
            'utok': 5,
            'obrana': 3,
            'zivoty': 15,
            'cena': {'jidlo': 10, 'drevo': 2, 'kamen': 0},
            'cena_za_kolo': {'jidlo': 2}
        },
        'lucisnik': {
            'typ': 'lucisnik',
            'rychlost': 2,
            'dosah': 5,
            'utok': 5,
            'obrana': 1,
            'zivoty': 8,
            'cena': {'jidlo': 10, 'drevo': 10, 'kamen': 0},
            'cena_za_kolo': {'jidlo': 2}
        },
        'testovaci': {
            'typ': 'testovaci',
            'rychlost': 2,
            'dosah': 2,
            'utok': 2,
            'obrana': 2,
            'zivoty': 10,
            'cena': {'jidlo': 0, 'drevo': 0, 'kamen': 0},
            'cena_za_kolo': {'jidlo': 2}
        },
        'zakladna': {
            'typ': 'zakladna',
            'rychlost': 0,
            'dosah': 0,
            'utok': 0,
            'obrana': 5,
            'zivoty': 50,
            'cena': {'jidlo': 0, 'drevo': 0, 'kamen': 0},
            'cena_za_kolo': {'jidlo': 0}
        }
    }

    if typ not in sablony:
        print(f"Neznámý typ jednotky: {typ}")
        return None

    sablona = sablony[typ]

    # Pokusíme se zaplatit cenu
    if not vlastnik.odecti_suroviny(sablona['cena']):
        print(f"{vlastnik.jmeno} nemá dost surovin na verbování jednotky typu {typ}.")
        return None

    # Vytvoření jednotky
    nova = jednotka.Jednotka(
        typ = sablona['typ'],
        pozice=pozice,
        rychlost=sablona['rychlost'],
        dosah=sablona['dosah'],
        utok=sablona['utok'],
        obrana=sablona['obrana'],
        zivoty=sablona['zivoty'],
        cena=sablona['cena'],
        cena_za_kolo=sablona['cena_za_kolo'],
        vlastnik=vlastnik
    )

    jednotky[pozice] = nova
    print(f"{vlastnik.jmeno} verboval jednotku typu {typ} na pozici {pozice}.")
    return nova

# TODO: V plné verzi tady bude muset být kontrola, že se pozicie nepřekrývají
def stavba_budovy(budovy, typ, pozice, vlastnik):
    """
    Stavba nové budovy určitého typu.

    Args:
        budovy: Seznam všech budov na mapě.
        typ: Název typu budovy ('domek', 'sberna', ...).
        pozice: Pozice, kde má být budova postavena.
        vlastnik: Instance hráče, který budovu staví.

    Returns:
        Nová budova nebo None, pokud hráč nemá dost surovin.
    """

    sablony = {
        'domek': {
            'typ': 'domek',
            'zivoty': 10,
            'obrana': 1,
            'cena': {'drevo': 5},
            'produkce': {'jidlo': 1}
        },
    }

    if typ not in sablony:
        print(f"Neznámý typ budovy: {typ}")
        return None

    sablona = sablony[typ]

    # Zaplacení ceny
    if not vlastnik.odecti_suroviny(sablona['cena']):
        print(f"{vlastnik.jmeno} nemá dost surovin na stavbu budovy typu {typ}.")
        return None

    # Vytvoření budovy
    nova = budova.Budova(
        typ=sablona['typ'],
        pozice=pozice,
        vlastnik=vlastnik,
        zivoty=sablona['zivoty'],
        obrana=sablona['obrana'],
        produkce=sablona['produkce'],
        cena=sablona['cena'],
    )

    print(f"{vlastnik.jmeno} postavil budovu typu {typ} na pozici {pozice}.")
    budovy.append(nova)
    return nova
