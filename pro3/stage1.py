import pandas as pd

def read_location():
    data = pd.read_excel('pro3\location.xlsx')
    x_coords = data['x'].values
    y_coords = data['y'].values
    x_coords = x_coords.tolist()
    y_coords = y_coords.tolist()
    x_coords.append(15); y_coords.append(15)
    x_coords.append(25); y_coords.append(25)
    x_coords.append(35); y_coords.append(15)
    x_coords.append(10); y_coords.append(25)
    x_coords.append(20); y_coords.append(30)
    return x_coords, y_coords

def euclidean_distance(point1, point2):
    dist = ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) ** 0.5
    dist = round(dist)
    return dist

x_coords, y_coords = read_location()
S = {}
S[0] = [20, 15, 5, 30]
S[1] = [25, 20, 6, 35]
S[2] = [18, 12, 4, 25]
S[3] = [22, 18, 5, 32]
S[4] = [24, 22, 7, 38]

# 求每个S的总和
total = {}
for key in S:
    total[key] = sum(S[key])


data_points_coords = list(zip(x_coords[1:31], y_coords[1:31]))
center_coords = list(zip(x_coords[31:], y_coords[31:]))
center_coords.insert(0, (x_coords[0], y_coords[0]))
boolean_selector = [True, True, False, False, True, True]
# 统计boolean_selector中为True的个数
num_true = sum(boolean_selector)
center_coords = [coord for i, coord in enumerate(center_coords) if boolean_selector[i]]


assignments = [[] for _ in range(num_true)]
for i, data_point in enumerate(data_points_coords):
        min_dist = float('inf')
        assigned_center_idx = -1
        
        for j, center_point in enumerate(center_coords):
            dist = euclidean_distance(data_point, center_point)
            if dist < min_dist:
                min_dist = dist
                assigned_center_idx = j
        
        if assigned_center_idx != -1:
            assignments[assigned_center_idx].append({"original_index": i + 1, "coords": data_point, "distance": min_dist})


# 根据当前的分配画图
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.figure(figsize=(10, 8))
color = ['blue', 'green', 'orange', 'purple', 'pink']
for i, center in enumerate(center_coords):
    if i == 0:
        plt.scatter(*center, marker='*', s=200, label=f'处理站', color='red')
    else:
        plt.scatter(*center, marker='x', s=150, label=f'中转站 {i} ({center})', color=color[i-1])
    for point_info in assignments[i]:
        plt.scatter(*point_info["coords"], alpha=0.5)
        plt.plot([center[0], point_info["coords"][0]], [center[1], point_info["coords"][1]], 'k--', alpha=0.5)
# 添加图例
plt.legend()
plt.xlabel('X坐标')
plt.ylabel('Y坐标')
plt.show()

def read_w(type):
    data = pd.read_excel('pro3\pro2.xlsx')
    waste_types = ['cy', 'hs', 'ys', 'qt']
    w_values = data[type].values
    w = {i + 1: w_i for i, w_i in enumerate(w_values)}
    w = {0: 0, **w}
    return w

def to_stage2_data(type, center_num):
    distance_matrix = []
    for i, center_assignment_list in enumerate(assignments):
        if i == center_num:
            center_coords = center_assignment_list[0]['coords']
            for point_info in center_assignment_list:
                xi, yi = point_info['coords']
                xj, yj = center_coords
                dist = euclidean_distance((xi, yi), (xj, yj))
                distance_matrix.append(round(dist))
    
                
    coords = {i: (xi, yi) for i, (xi,yi) in enumerate(zip(x_coords, y_coords))}
    Q = {'cy': 8, 'hs': 6, 'ys': 3, 'qt': 10}  # 各类车辆容量上限
    Q = Q[type]
    
    return distance_matrix, w, Q

if __name__ == "__main__":
    print("\nCenters for assignment:")
    w = read_w('hs')
    for i, center in enumerate(center_coords):
        print(f"Center {i}: {center}")
    for i, center_assignment_list in enumerate(assignments):
        sum_w = 0
        print(f"\nPoints assigned to Center {i} {center_coords[i]}:")
        center_assignment_list.sort(key=lambda p: p["original_index"])
        for point_info in center_assignment_list:
            print(f"  - Data Point (Original Index: {point_info['original_index']}): {point_info['coords']}, Distance: {point_info['distance']:.2f}")
            sum_w += w[point_info['original_index']]
        print(f"  Total W for Center {i}: {sum_w}")