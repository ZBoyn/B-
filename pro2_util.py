import pandas as pd
import math

def read_waste_data(file_path, type):
    data = pd.read_excel(file_path, sheet_name='Sheet1')
    waste_types = ['cy', 'hs', 'ys', 'qt']
    w_values = data[type].values
    w = {i + 1: w_i for i, w_i in enumerate(w_values)}
    w = {0: 0, **w}
    return w


def calculate_distance(n, coords):
    d = {}
    for i in range(n):
        for j in range(n):
            dx = coords[i][0] - coords[j][0]
            dy = coords[i][1] - coords[j][1]
            d[(i, j)] = 0.0 if i == j else math.hypot(dx, dy)
    return d


if __name__ == "__main__":
    w = read_waste_data('pro2.xlsx')
    print(w)

