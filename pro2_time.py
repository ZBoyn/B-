import math
import gurobipy as gp
from gurobipy import GRB
from pro1_util import read_data, calculate_distance
from pro2_util import read_waste_data
import json

n, coords, _, _, _ = read_data('pro1.xlsx')
w = read_waste_data('pro2.xlsx', 'cy')
# Q = {'cy': 8, 'hs': 6, 'ys': 3, 'qt': 10}       # 各类车辆容量上限
# C = {1: 2.5, 2: 2, 3: 5, 4: 1.8}    # 各类车辆单位距离成本系数
Q = 8
d, nodes = calculate_distance(n, coords)

vehicle_speed = 40
travel_matrix = {(i,j): dist / vehicle_speed for (i,j), dist in d.items()} 

service_times = [0.0] + [0.5] * n

MAX_ROUTE_TIME = 4

model = gp.Model("VRP_single_with_time_constraint")

x = {}
for i in nodes:
    for j in nodes:
        if i != j:
            x[i,j] = model.addVar(vtype=GRB.BINARY, name=f"x_{i}_{j}")
            
u = {}
for i in range(1, n + 1):
    u[i] = model.addVar(lb=0, ub=Q, vtype=GRB.CONTINUOUS, name=f"u_{i}")

# 时间累积变量
time_elapsed = {}
for i in range(1, n + 1):
    time_elapsed[i] = model.addVar(lb=0, ub=MAX_ROUTE_TIME, vtype=GRB.CONTINUOUS, name=f"time_elapsed_{i}")
    
model.setObjective(gp.quicksum(d[i,j] * x[i,j] for i in nodes for j in nodes if i != j), GRB.MINIMIZE)

for i in range(1, n + 1):
    model.addConstr(gp.quicksum(x[j,i] for j in nodes if j != i) == 1, name=f"in_{i}")
    model.addConstr(gp.quicksum(x[i,j] for j in nodes if j != i) == 1, name=f"out_{i}")

model.addConstr(gp.quicksum(x[0,j] for j in range(1, n + 1)) == gp.quicksum(x[i,0] for i in range(1, n + 1)), name="depot_balance")

for i in range(1, n + 1):
    model.addConstr(u[i] >= w[i] - Q * (1 - x[0,i]), name=f"load_from0_{i}")
    for j in range(1, n + 1):
        if i != j:
            model.addConstr(u[j] >= u[i] + w[j] - Q * (1 - x[i,j]), name=f"load_cont_{i}_{j}")

# 约束 T1: 从仓库到客户点的时间累积
for j_node in range(1, n + 1):
    model.addConstr(time_elapsed[j_node] >= (travel_matrix[0,j_node] + service_times[j_node]) - MAX_ROUTE_TIME * (1 - x[0,j_node]), 
                    name=f"time_acc_from_depot_{j_node}")

# 约束 T2: 客户点之间的时间累积
for i_node in range(1, n + 1):
    for j_node in range(1, n + 1):
        if i_node != j_node:
             model.addConstr(time_elapsed[j_node] >= time_elapsed[i_node] + travel_matrix[i_node,j_node] + service_times[j_node] - MAX_ROUTE_TIME * (1 - x[i_node,j_node]),
                            name=f"time_acc_cust_{i_node}_{j_node}")

# 约束 T3: 最大路径时间限制
for i_node in range(1, n + 1):
    model.addConstr(time_elapsed[i_node] + travel_matrix[i_node,0] <= MAX_ROUTE_TIME + MAX_ROUTE_TIME * (1 - x[i_node,0]), 
                    name=f"max_route_time_from_{i_node}")

model.optimize()

if model.Status == GRB.OPTIMAL:
    print(f"最优总行驶距离 = {model.ObjVal}")
    routes = []
    used = set()
    for j in range(1, n+1):
        if x[0,j].X > 0.5:  
            route = [0, j]
            cur = j
            while True:
                next_node = None
                for k in range(0, n+1):
                    if k != cur and x[cur,k].X > 0.5:
                        next_node = k
                        break
                if next_node is None:
                    break
                route.append(next_node)
                cur = next_node
                if next_node == 0:    
                    break
            routes.append(route)
    
    for r_idx, route in enumerate(routes, start=1):
        path_str = " -> ".join(str(node) for node in route)
        print(f"车辆{r_idx} 路线: {path_str}")

else:
    print("No optimal solution found.")