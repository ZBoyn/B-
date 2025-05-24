import pandas as pd
import math
import numpy as np

def read_data(file_path):
    data = pd.read_excel(file_path, sheet_name='Sheet1')

    x_coords = data['x'].values
    y_coords = data['y'].values
    w_values = data['w'].values

    n = 30
    coords = {i: (xi, yi) for i, (xi, yi) in enumerate(zip(x_coords, y_coords))}
    w = {i: w_i for i, w_i in enumerate(w_values)}
    w[0] = 0
    
    Q = 5
    
    # 生成距离矩阵
    distance_matrix = []
    for i in range(n + 1):
        row = []
        for j in range(n+ 1):
            xi, yi = coords[i]
            xj, yj = coords[j]
            dist = np.hypot(xi - xj, yi - yj)
            row.append(round(dist))
            # row.append(round(dist, 3))  # 保留三位小数
        distance_matrix.append(row)
        
    return n, coords, w, Q, distance_matrix

def calculate_distance(n, coords):
    nodes = list(range(0, n+1))
    d = {}
    for i in nodes:
        for j in nodes:
            if i != j:
                dx = coords[i][0] - coords[j][0]
                dy = coords[i][1] - coords[j][1]
                d[i,j] = math.hypot(dx, dy)
                # 取整到整数
                d[i,j] = round(d[i,j])
    return d, nodes

def route_length(route, coords):
    dist = 0.0
    for i in range(len(route) - 1):
        x1, y1 = coords[route[i]]
        x2, y2 = coords[route[i+1]]
        dist += np.hypot(x1 - x2, y1 - y2)
    return dist

def all_route_lengths(routes, coords):
    return [route_length(r, coords) for r in routes]

def lpt_partition(routes, lengths, k):
    """Largest-Processing-Time 贪心"""
    assign = [[] for _ in range(k)]
    load   = [0.0] * k          # 每辆车当前总里程

    # 按长度降序遍历路线
    for idx in np.argsort(-np.array(lengths)):
        # 找到当前负载最小的车辆
        j = int(np.argmin(load))
        assign[j].append(idx)
        load[j] += lengths[idx]
    return assign, load

def build_vehicle_routes(assign, routes):
    """根据分配索引，把原 routes 重新组装成按车辆划分的列表。"""
    veh_routes = []
    for group in assign:
        veh_routes.append([routes[i] for i in group])
    return veh_routes

if __name__ == "__main__":
    n, coords, w, Q = read_data('pro1.xlsx')
    print(w)
    # d = calculate_distance(n, coords)
    # print(d)