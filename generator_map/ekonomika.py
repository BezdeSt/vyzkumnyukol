import jednotka

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

    # Předdefinované šablony jednotek
    sablony = {
        'bojovnik': {
            'rychlost': 3,
            'dosah': 1,
            'utok': 5,
            'obrana': 3,
            'zivoty': 15,
            'cena': {'jidlo': 10, 'drevo': 2, 'kamen': 0},
            'cena_za_kolo': {'jidlo': 2}
        },
        'lucisnik': {
            'rychlost': 2,
            'dosah': 5,
            'utok': 5,
            'obrana': 1,
            'zivoty': 8,
            'cena': {'jidlo': 10, 'drevo': 10, 'kamen': 0},
            'cena_za_kolo': {'jidlo': 2}
        },
        'testovaci': {
            'rychlost': 2,
            'dosah': 2,
            'utok': 2,
            'obrana': 2,
            'zivoty': 10,
            'cena': {'jidlo': 0, 'drevo': 0, 'kamen': 0},
            'cena_za_kolo': {'jidlo': 2}
        },
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


