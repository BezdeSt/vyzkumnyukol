import random

import numpy as np
from scipy.interpolate import griddata

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

from noise import pnoise2

from collections import deque
import time
import csv # Import pro práci s CSV

def nahodne_pole(rows, cols, min_value=0, max_value=1):
    """
    Generuje 2D pole náhodných hodnot.

    """
    return np.random.uniform(low=min_value, high=max_value, size=(rows, cols))


def interpolovane_pole(big_rows, big_cols, small_rows, small_cols, min_value=0, max_value=1):
    """
    Vytvoří menší náhodnou mřížku, aplikuje ji na větší mřížku, chybějící hodnoty interpoluje.

    """
    # Vytvoření menší mřížky
    small_grid = nahodne_pole(small_rows, small_cols, min_value, max_value)

    # Indexy pro malou a velkou mřížku
    small_x = np.linspace(0, big_cols - 1, small_cols)
    small_y = np.linspace(0, big_rows - 1, small_rows)
    big_x = np.arange(big_cols)
    big_y = np.arange(big_rows)

    # Vytvoření seznamu souřadnic
    small_points = np.array([(x, y) for y in small_y for x in small_x])
    small_values = small_grid.flatten()
    big_points = np.array([(x, y) for y in big_y for x in big_x])

    # Doplnění hodnot seznamu interpolací
    big_list = griddata(small_points, small_values, big_points, method='cubic')

    # Převedení na mřížku

    big_grid = big_list.reshape(big_rows, big_cols)

    return big_grid


def cislo_na_policko(grid):
    mapa = np.empty_like(grid, dtype='str')

    for i in range(grid.shape[0]):  # Počet řádků
        for j in range(grid.shape[1]):  # Počet sloupců
            if grid[i][j] < 0.25:
                mapa[i][j] = "V"  # Voda
            elif grid[i][j] < 0.5:
                mapa[i][j] = "P"  # Pláně
            elif grid[i][j] < 0.75:
                mapa[i][j] = "L"  # Les
            else:
                mapa[i][j] = "H"  # Hory
    return mapa


def perlin_noise_lib(rows, cols, scale=10):
    """
    Generuje výškovou mapu pomocí Perlinova šumu.
    """

    seed_x = np.random.uniform(0, 1000)
    seed_y = np.random.uniform(0, 1000)

    terrain = np.zeros((rows, cols))
    for y in range(rows):
        for x in range(cols):
            terrain[y, x] = pnoise2((x+seed_x) / scale, (y+seed_y) / scale, octaves=4, persistence=0.5, lacunarity=2.0)

    # Normalizace na rozsah 0-1
    terrain = (terrain - terrain.min()) / (terrain.max() - terrain.min())
    return terrain

# -------------------------------------------------------------------------------

def fade(t):
    """
    Perlinova fade funkce pro hladkou interpolaci.
    """
    return 6*t**5 - 15*t**4 + 10*t**3

def random_gradient_pole(rows, cols):
    """
    Vytvoří 2D mřížku náhodných gradientových vektorů.
    """
    angles = np.random.uniform(0, 2 * np.pi, (rows, cols))
    grad_x = np.cos(angles)  # X komponenty gradientů
    grad_y = np.sin(angles)  # Y komponenty gradientů
    return grad_x, grad_y

def skal_souc_gradient(ix, iy, x, y, grad_x, grad_y):
    """
    Skalární součin mezi gradientem v (ix, iy) a vektorem k bodu (x, y).
    """
    dx = x - ix
    dy = y - iy
    return dx * grad_x[iy, ix] + dy * grad_y[iy, ix]

def perlin_noise_pole(rows, cols, scale=10):
    """
    Vygeneruje 2D Perlinův šum.
    """
    grad_rows, grad_cols = rows // scale + 1, cols // scale + 1
    grad_x, grad_y = random_gradient_pole(grad_rows, grad_cols)

    noise = np.zeros((rows, cols))

    for y in range(rows):
        for x in range(cols):
            # Najde čtyři nejbližší body na gradientové mřížce
            x0, y0 = x // scale, y // scale
            x1, y1 = x0 + 1, y0 + 1

            # Relativní souřadnice uvnitř buňky
            sx = (x % scale) / scale
            sy = (y % scale) / scale

            # Skalární součiny gradientů s vektory k bodu
            n00 = skal_souc_gradient(x0, y0, x / scale, y / scale, grad_x, grad_y)
            n01 = skal_souc_gradient(x0, y1, x / scale, y / scale, grad_x, grad_y)
            n10 = skal_souc_gradient(x1, y0, x / scale, y / scale, grad_x, grad_y)
            n11 = skal_souc_gradient(x1, y1, x / scale, y / scale, grad_x, grad_y)

            # Fade -- hladká interpolace
            u, v = fade(sx), fade(sy)

            # Interpolace mezi čtyřmi hodnotami
            nx0 = (1 - u) * n00 + u * n10
            nx1 = (1 - u) * n01 + u * n11
            noise[y, x] = (1 - v) * nx0 + v * nx1

    # Normalizace hodnot na rozsah 0–1
    noise = (noise - noise.min()) / (noise.max() - noise.min())

    return noise

# -------------------------------------------------------------------------------

def zobraz_mapu(mapa, nazev=""):
    """
    Barevně vykreslí terénní mapu.
    """
    # Definice barev pro jednotlivé typy terénu
    barvy = {
        "V": "#1f77b4",  # Modrá - Voda
        "P": "#58d162",  # Světle zelená - Pláně
        "L": "green",  # Zelená - Les
        "H": "#4a4a48",  # Šedá - Hory
    }

    # Převedení mapy na numerickou matici s indexy
    text_to_index = {"V": 0, "P": 1, "L": 2, "H": 3}
    index_map = np.vectorize(text_to_index.get)(mapa)

    # Vytvoření barevné mapy
    cmap = ListedColormap(barvy.values())

    # Vykreslení mřížky
    plt.figure(figsize=(8, 8))
    plt.imshow(index_map, cmap=cmap, interpolation='nearest')
    plt.title(nazev, fontsize=25)
    plt.axis('off')

    plt.show()

#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
def je_validni_policko(r, c, rows, cols):
    """
    Zkontroluje, zda je políčko uvnitř hranic mapy.
    """
    return 0 <= r < rows and 0 <= c < cols

def je_voda(policko_typ):
    """
    Definuje, které typy políček jsou průchozí.
    Pro jednoduchost, předpokládejme, že voda je neprůchozí, ostatní jsou průchozí.
    """
    return policko_typ != "V"

def najdi_cestu_bfs(mapa, start, end):
    """
    Najde nejkratší cestu mezi dvěma body pomocí BFS (Breadth-First Search).
    Vrací True, pokud je cesta nalezena, jinak False.
    """
    rows, cols = mapa.shape
    queue = deque([(start)])
    visited = set([start])

    while queue:
        r, c = queue.popleft()

        if (r, c) == end:
            return True # Cesta nalezena

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if je_validni_policko(nr, nc, rows, cols) and (nr, nc) not in visited and je_voda(mapa[nr, nc]):
                visited.add((nr, nc))
                queue.append((nr, nc))
    return False # Cesta nenalezena

def nahodna_cesta(pole):
    rows, cols = pole.shape

    x1, y1 = np.random.randint(0, rows), np.random.randint(0, cols)
    while not je_voda(pole[x1, y1]):
        x1, y1 = np.random.randint(0, rows), np.random.randint(0, cols)
    start_point = (x1, y1)

    x2, y2 = np.random.randint(0, rows), np.random.randint(0, cols)
    while not je_voda(pole[x2, y2]) or (x2, y2) == start_point:
        x2, y2 = np.random.randint(0, rows), np.random.randint(0, cols)
    end_point = (x2, y2)

    # Testování průchodnosti
    #print(start_point + end_point)
    return najdi_cestu_bfs(pole, start_point, end_point)

def log(pole, seed, nazev, nazev_souboru="map_log.csv"):
    """
    Spočítá počet políček každého typu, otestuje průchodnost a uloží data do CSV.
    """
    V = 0
    P = 0
    L = 0
    H = 0

    for y in range(pole.shape[0]):
        for x in range(pole.shape[1]):
            if pole[y][x] == "V":
                V += 1
            elif pole[y][x] == "P":
                P += 1
            elif pole[y][x] == "L":
                L += 1
            elif pole[y][x] == "H":
                H += 1

    pruchody = 0
    num_path_tests = 100 # Počet testů průchodnosti
    print(f"Probíhá {num_path_tests} testů průchodnosti...")
    for i in range(num_path_tests):
        if nahodna_cesta(pole):
            pruchody += 1

    celkem = pole.shape[0] * pole.shape[1]

    # Uložit do CSV
    try:
        with open(nazev_souboru, 'a', newline='') as csvfile:
            fieldnames = ['NazevMapy', 'Seed', 'Voda[%]', 'Plane[%]', 'Les[%]', 'Hory[%]', 'UspechyCest[%]']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Pokud soubor neexistuje nebo je prázdný, zapiš hlavičku
            if csvfile.tell() == 0:
                writer.writeheader()

            writer.writerow({
                'NazevMapy': nazev,
                'Seed': seed,
                'Voda[%]': (V/celkem)*100,
                'Plane[%]': (P/celkem)*100,
                'Les[%]': (L/celkem)*100,
                'Hory[%]': (H/celkem)*100,
                'UspechyCest[%]': (pruchody/num_path_tests)*100
            })
        print(f"Data byla úspěšně uložena do '{nazev_souboru}'.")
    except IOError as e:
        print(f"Chyba při zápisu do CSV souboru: {e}")

#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------

def testovani():
    nazev = "Malé_scale"
    for i in range(1000):
        random.seed(i+1)
        np.random.seed(i+1)

        perlin_grid = perlin_noise_pole(big_rows, big_cols, scale=scale)
        log(cislo_na_policko(perlin_grid), i, nazev)

def vizualni_test():
    testovaci_id = [561247, 856641,758789]

    for id in testovaci_id:
        random.seed(id)
        np.random.seed(id)

        perlin_grid = perlin_noise_pole(big_rows, big_cols, scale=scale)
        zobraz_mapu(cislo_na_policko(perlin_grid), id)




big_rows = 50
big_cols = 50
scale = 2

vizualni_test()
#testovani()