import numpy as np
from scipy.interpolate import griddata


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

# Příklad použití
big_rows = 9
big_cols = 9
small_rows = 3
small_cols = 3
min_value = 0
max_value = 1

random_grid = nahodne_pole(big_rows, big_cols, min_value, max_value)
random_tile = cislo_na_policko(random_grid)
print(random_tile)
print('--------------------------------------------------')
interpolated_grid = interpolovane_pole(big_rows, big_cols, small_rows, small_cols, min_value, max_value)
interpolated_tile = cislo_na_policko(interpolated_grid)
print(interpolated_tile)

