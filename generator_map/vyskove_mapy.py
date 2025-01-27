import numpy as np
from scipy.interpolate import griddata


def nahodne_pole(rows, cols, min_value=0, max_value=1):
    """
    Generuje 2D pole náhodných hodnot.

    """
    return np.random.uniform(low=min_value, high=max_value, size=(rows, cols))

rows = 5
cols = 5
min_value = 0
max_value = 1

random_array = nahodne_pole(rows, cols, min_value, max_value)
print(random_array)
