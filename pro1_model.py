import math
import gurobipy as gp
from gurobipy import GRB
from pro1_util import read_data, calculate_distance
import json

n, coords, w, Q = read_data('pro1.xlsx')
d, nodes = calculate_distance(n, coords)


model = gp.Model("VRP_single")

# 决策变量
x = {}
for i in nodes:
    for j in nodes:
        if i != j:
            x[i,j] = model.addVar(vtype=GRB.BINARY, name=f"x_{i}_{j}")
            
u = {}
for i in range(1, n+1):
    u[i] = model.addVar(lb=0, ub=Q, vtype=GRB.CONTINUOUS, name=f"u_{i}")
    
# 目标函数
model.setObjective(gp.quicksum(d[i,j] * x[i,j] for i in nodes for j in nodes if i != j), GRB.MINIMIZE)

# 约束条件
# 约束1: 每个收集点只能被访问一次
for i in range(1, n+1):
    model.addConstr(gp.quicksum(x[j,i] for j in nodes if j != i) == 1, name=f"in_{i}")
    model.addConstr(gp.quicksum(x[i,j] for j in nodes if j != i) == 1, name=f"out_{i}")

# 约束2: 处理站出入平衡
model.addConstr(gp.quicksum(x[0,j] for j in range(1, n+1)) == gp.quicksum(x[i,0] for i in range(1, n+1)), name="depot_balance")

# 约束3: 车辆容量限制
for i in range(1, n+1):
    # 第一个节点
    model.addConstr(u[i] >= w[i] - Q * (1 - x[0,i]), name=f"load_from0_{i}")
    for j in range(1, n+1):
        if i != j:
            model.addConstr(u[j] >= u[i] + w[j] - Q * (1 - x[i,j]), name=f"load_cont_{i}_{j}")

model.optimize()

if model.Status == GRB.OPTIMAL:
    print(f"最优总行驶距离 = {model.ObjVal}")
    # 路线
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
    
    # 保存路线数据到json
    with open('routes.json', 'w') as f:
        json.dump(routes, f)
    
else:
    print("No optimal solution found.")
    