import math
import gurobipy as gp
from gurobipy import GRB
from pro1_util import read_data, calculate_distance
import pandas as pd

# 节点参数
n, coords, _, _, _ = read_data('pro1.xlsx')

def read_waste_data(file_path):
    data = pd.read_excel(file_path, sheet_name='Sheet1')
    waste_types = ['cy', 'hs', 'ys', 'qt']
    w = {k+1: {i+1: data[waste_types[k]][i] for i in range(len(data))} for k in range(4)}
    return w
w = read_waste_data('pro2.xlsx')

# 车辆参数
Q = {1: 8, 2: 6, 3: 3, 4: 10}       # 各类车辆容量上限
C = {1: 2.5, 2: 2, 3: 5, 4: 1.8}    # 各类车辆单位距离成本系数

d, nodes = calculate_distance(n, coords)

model = gp.Model("VRP_multi")
# 设置时间
model.setParam('TimeLimit', 600)  # 设置时间限制为600秒
# 决策变量
x = {}
u = {}

for k in range(1, 5):
    N_k = [i for i in range(1, n+1) if w[k][i] > 0]
    nodes_k = [0] + N_k
    
    for i in nodes_k:
        for j in nodes_k:
            if i != j:
                x[k,i,j] = model.addVar(vtype=GRB.BINARY, name=f"x_{k}_{i}_{j}")
    for i in N_k:
        u[k,i] = model.addVar(lb=0, ub=Q[k], vtype=GRB.CONTINUOUS, name=f"u_{k}_{i}")
        
# 目标函数
model.setObjective(gp.quicksum(C[k] * d[i,j] * x[k,i,j] 
                               for k in range(1,5) 
                               for i in range(0, n+1) for j in range(0, n+1) if i != j and (k,i,j) in x),
                   GRB.MINIMIZE)

for k in range(1, 5):
    N_k = [i for i in range(1, n+1) if w[k][i] > 0]
    nodes_k = [0] + N_k
    for i in N_k:
        model.addConstr(gp.quicksum(x[k,j,i] for j in nodes_k if j != i) == 1, name=f"in_{k}_{i}")
        model.addConstr(gp.quicksum(x[k,i,j] for j in nodes_k if j != i) == 1, name=f"out_{k}_{i}")
    model.addConstr(gp.quicksum(x[k,0,j] for j in N_k) == gp.quicksum(x[k,i,0] for i in N_k), name=f"depot_balance_{k}")
    for i in N_k:
        model.addConstr(u[k,i] >= w[k][i] - Q[k] * (1 - x.get((k,0,i), 0)), name=f"load_{k}_from0_{i}")
        for j in N_k:
            if i != j:
                model.addConstr(u[k,j] >= u[k,i] + w[k][j] - Q[k] * (1 - x[k,i,j]), name=f"load_{k}_{i}_{j}")
model.optimize()

if model.Status == GRB.OPTIMAL:
    print(f"最优总运输成本 = {model.ObjVal}")
    for k in range(1, 5):
        N_k = [i for i in range(1, n+1) if w[k][i] > 0]
        routes_k = []
        for j in N_k:
            if (k,0,j) in x and x[k,0,j].X > 0.5:
                route = [0, j]
                cur = j
                while True:
                    next_node = None
                    # 在第k类路径图中寻找 cur 的后继
                    for m in [0] + N_k:
                        if m != cur and (k,cur,m) in x and x[k,cur,m].X > 0.5:
                            next_node = m
                            break
                    if next_node is None:
                        break
                    route.append(next_node)
                    cur = next_node
                    if next_node == 0:
                        break
                routes_k.append(route)
        print(f"类别{k} 垃圾车辆路线：")
        for r_idx, route in enumerate(routes_k, start=1):
            path_str = " -> ".join(str(node) for node in route)
            print(f"  线路{r_idx}: {path_str}")