import numpy as np
import hygese
import math
import pandas as pd

def calculate_distance_matrix(coords):
    n = len(coords)
    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            dist = math.hypot(coords[i][0] - coords[j][0], coords[i][1] - coords[j][1])
            row.append(round(dist))
        matrix.append(row)
    return matrix

def read_waste_data(file_path, waste_type):
    data = pd.read_excel(file_path, sheet_name='Sheet1')
    w_values = data[waste_type].values
    w = {i + 1: w_i for i, w_i in enumerate(w_values)}
    w = {0: 0, **w}
    return w

def solve_for_center(center_coord, point_infos, waste_file, waste_types, Q_dict, C_dict):
    total_cost = 0
    
    coords = [center_coord] + [info['coords'] for info in point_infos]
    original_indices = [info['original_index'] for info in point_infos]
    distance_matrix = calculate_distance_matrix(coords)

    for w_type in waste_types:
        print(f"\n正在处理垃圾类型：{w_type}，仓库位置：{center_coord}")
        data = dict()
        # print(1)
        w_all = read_waste_data(waste_file, w_type)
        w = [w_all[idx] for idx in original_indices]
        w_sum = sum(w)
        # print(2)
        data['distance_matrix'] = distance_matrix
        data['num_vehicles'] = 1000
        data['depot'] = 0
        data['demands'] = [0] + w
        data['vehicle_capacity'] = Q_dict[w_type]
        data['service_times'] = np.zeros(len(data['demands']))
        # print(3)
        ap = hygese.AlgorithmParameters(timeLimit=2)
        hgs_solver = hygese.Solver(parameters=ap)
        result = hgs_solver.solve_cvrp(data)
        # print(4)
        type_cost = C_dict[w_type] * result.cost
        total_cost += type_cost

        print(f"{w_type} 类型成本 = {C_dict[w_type]} * {result.cost:.2f} = {type_cost:.2f}")
        print(f"路线数量: {result.n_routes}")
        print(f"路线: {result.routes}")
    
    return total_cost