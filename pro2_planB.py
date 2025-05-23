import numpy as np 
import hygese
from pro1_util import read_data
from pro2_util import read_waste_data,calculate_distance

data = dict()
n, coords, _, _, distance_matrix = read_data('pro1.xlsx')
# waste_types = ['cy', 'hs', 'ys', 'qt']

# Q = {'cy': 8, 'hs': 6, 'ys': 3, 'qt': 10}       # 各类车辆容量上限
# C = {1: 2.5, 2: 2, 3: 5, 4: 1.8}    # 各类车辆单位距离成本系数
w = read_waste_data('pro2.xlsx', 'cy')
Q = 8

data['distance_matrix'] = distance_matrix
data['num_vehicles'] = 1000
data['depot'] = 0
data['demands'] = [w[i] for i in range(len(w))]
total_demand = sum(data['demands'])
data['vehicle_capacity'] = Q  # different from OR-Tools: homogeneous capacity
data['service_times'] = np.zeros(len(data['demands']))

# Solver initialization
ap = hygese.AlgorithmParameters(timeLimit=5)  # seconds
hgs_solver = hygese.Solver(parameters=ap)

# Solve
result = hgs_solver.solve_cvrp(data)
print("cost: ", result.cost)
print("time: ", result.time)
print("num of routes: ", result.n_routes)
print("routes: ", result.routes)
