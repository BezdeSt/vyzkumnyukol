import numpy as np
from scipy.interpolate import griddata

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


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
                mapa[i][j] = "V" # Voda
            elif grid[i][j] < 0.5:
                mapa[i][j] = "P" # Pláně
            elif grid[i][j] < 0.75:
                mapa[i][j] = "L" # Les
            else: mapa[i][j] = "H" # Hory
    return mapa

def zobraz_mapu(mapa):
    """
    Barevně vykreslí terénní mapu.
    """
    # Definice barev pro jednotlivé typy terénu
    barvy = {
        "V": "#1f77b4",  # Modrá - Voda
        "P": "#58d162",  # Světle zelená - Pláně
        "L": "#0c3b10",  # Zelená - Les
        "H": "#4a4a48",  # Šedá - Hory
    }

    # Převedení mapy na numerickou matici s indexy (0 = "V", 1 = "P", ...)
    text_to_index = {"V": 0, "P": 1, "L": 2, "H": 3}
    index_map = np.vectorize(text_to_index.get)(mapa)

    # Vytvoření barevné mapy
    cmap = ListedColormap(barvy.values())

    # Vykreslení mřížky
    plt.figure(figsize=(8, 8))
    plt.imshow(index_map, cmap=cmap, interpolation='nearest')

    plt.show()


def gradientni_pole(rows, cols, gradient_scale=1):
    """
    Vytvoří výškovou mapu pomocí gradientového šumu.

    """
    # Hrubá mřížka gradientů
    grad_rows = rows // gradient_scale
    grad_cols = cols // gradient_scale

    # Náhodné gradienty na hrubé mřížce
    gradients_x = np.random.uniform(-1, 1, (grad_rows, grad_cols))
    gradients_y = np.random.uniform(-1, 1, (grad_rows, grad_cols))


    # Jemná mřížka pro výsledné hodnoty
    terrain = np.zeros((rows, cols))

    # Výpočet výšek na jemné mřížce
    for y in range(rows):
        for x in range(cols):
            # Určení čtyř sousedních gradientů na hrubé mřížce
            x0 = x // gradient_scale
            y0 = y // gradient_scale
            x1 = min(x0 + 1, grad_cols - 1)
            y1 = min(y0 + 1, grad_rows - 1)

            # Relativní pozice uvnitř buňky
            dx = (x % gradient_scale) / gradient_scale
            dy = (y % gradient_scale) / gradient_scale

            # Výpočet příspěvků z gradientů
            h00 = gradients_x[y0, x0] * dx + gradients_y[y0, x0] * dy
            h01 = gradients_x[y0, x1] * (1 - dx) + gradients_y[y0, x1] * dy
            h10 = gradients_x[y1, x0] * dx + gradients_y[y1, x0] * (1 - dy)
            h11 = gradients_x[y1, x1] * (1 - dx) + gradients_y[y1, x1] * (1 - dy)

            # Interpolace výšek
            height_x0 = h00 * (1 - dx) + h01 * dx
            height_x1 = h10 * (1 - dx) + h11 * dx
            terrain[y, x] = height_x0 * (1 - dy) + height_x1 * dy

    return terrain

# Příklad použití
big_rows = 50
big_cols = 50
small_rows = 5
small_cols = 5
min_value = 0
max_value = 1

# random_grid = nahodne_pole(big_rows, big_cols, min_value, max_value)
# random_tile = cislo_na_policko(random_grid)
# print(random_tile)
# zobraz_mapu(random_tile)
# print('--------------------------------------------------')
# interpolated_grid = interpolovane_pole(big_rows, big_cols, small_rows, small_cols, min_value, max_value)
# interpolated_tile = cislo_na_policko(interpolated_grid)
# print(interpolated_tile)
# zobraz_mapu(interpolated_tile)

gradient_terrain = gradient_based_terrain(big_rows, big_cols, gradient_scale=10)
print(gradient_terrain)
zobraz_mapu(cislo_na_policko(gradient_terrain))


