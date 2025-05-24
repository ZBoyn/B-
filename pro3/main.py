import pandas as pd
from stage2 import solve_for_center
import itertools

def read_location():
    data = pd.read_excel('pro3/location.xlsx')
    x_coords = data['x'].tolist()
    y_coords = data['y'].tolist()
    x_coords += [15, 25, 35, 10, 20]
    y_coords += [15, 25, 15, 25, 30]
    return list(zip(x_coords, y_coords))

def euclidean_distance(p1, p2):
    return round(((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2) ** 0.5)

def assign_points_to_centers(data_points, centers):
    assignments = [[] for _ in range(len(centers))]
    for i, dp in enumerate(data_points):
        min_dist = float('inf')
        idx = -1
        for j, c in enumerate(centers):
            dist = euclidean_distance(dp, c)
            if dist < min_dist:
                min_dist = dist
                idx = j
        assignments[idx].append({"original_index": i + 1, "coords": dp, "distance": min_dist})
    return assignments

# if __name__ == "__main__":
#     all_coords = read_location()
#     data_points = all_coords[1:31]
#     centers = [all_coords[0]] + all_coords[31:]
    
    
#     boolean_selector = [True, False, True, False, True, True]
#     T_cost = [0, 137, 164, 123, 151, 159]
#     centers = [c for i, c in enumerate(centers) if boolean_selector[i]]

#     assignments = assign_points_to_centers(data_points, centers)

#     waste_file = 'pro3/pro2.xlsx'
#     # waste_types = ['cy', 'hs', 'ys', 'qt']
#     waste_types = ['cy', 'hs', '10ys', 'qt']
#     # Q_dict = {'cy': 8, 'hs': 6, 'ys': 3, 'qt': 10}
#     Q_dict = {'cy': 8, 'hs': 6, '10ys':30, 'qt': 10}
#     # C_dict = {'cy': 2.5, 'hs': 2, 'ys': 5, 'qt': 1.8}
#     C_dict = {'cy': 2.5, 'hs': 2, '10ys': 5, 'qt': 1.8}
#     # skip_pairs = [(0, 'ys'), (1, 'ys'), (2, 'ys'), (3, 'ys'), (4, 'ys')]
#     center_index = 0
#     total_all_cost = 0
#     for i, (center, point_infos) in enumerate(zip(centers, assignments)):
#         # if i == 0:
#         #     print(f"\n跳过中心 {i}（坐标 {center}）的调度，仅用于图示")
#         #     continue
#         if i == 0 and boolean_selector[1]:
#             print(f"\n跳过中心 {i}（坐标 {center}）的调度，仅用于图示")
#             total_all_cost += 101.7
#             continue
#         print(f"\n====== 中心 {i}：{center} ======")
#         cost = solve_for_center(center, point_infos, waste_file, waste_types, Q_dict, C_dict)
#         total_all_cost += cost

#     print(f"\n所有中心垃圾运输总成本为: {total_all_cost:.2f}")
    
#     T_cost_sum = sum([T_cost[i] for i, b in enumerate(boolean_selector) if b])
#     print(f"所有中心垃圾运输总成本 + 中心成本 = {total_all_cost:.2f} + {T_cost_sum:.2f} = {total_all_cost + T_cost_sum:.2f}")
    
#     cost_0 = 101.7
#     print(f"考虑0号中心的总成本 = {total_all_cost:.2f} + {T_cost_sum:.2f} + {101.7:.2f}")
    
if __name__ == "__main__":
    all_coords = read_location()
    data_points = all_coords[1:31]
    original_centers = [all_coords[0]] + all_coords[31:]
    
    T_cost = [0, 137, 164, 123, 151, 159]
    waste_file = 'pro3/pro2.xlsx'
    waste_types = ['cy', 'hs', '10ys', 'qt']
    Q_dict = {'cy': 8, 'hs': 6, '10ys': 30, 'qt': 10}
    C_dict = {'cy': 2.5, 'hs': 2, '10ys': 5, 'qt': 1.8}
    
    best_combination = None
    min_total_cost = float('inf')

    # 遍历所有满足条件的布尔组合（第一项为 True，后5项中有3个为True）
    for combo in itertools.combinations(range(1, 6), 3):
        boolean_selector = [True] + [i in combo for i in range(1, 6)]
        
        # 根据布尔选择器过滤中心
        centers = [c for i, c in enumerate(original_centers) if boolean_selector[i]]
        assignments = assign_points_to_centers(data_points, centers)

        total_all_cost = 0
        print(f"\n组合 {boolean_selector}：")
        for i, (center, point_infos) in enumerate(zip(centers, assignments)):
            if i == 0 and boolean_selector[1]:
                print(f"  跳过中心 {i}（坐标 {center}）的调度，仅用于图示")
                total_all_cost += 101.7
                continue
            print(f"  中心 {i}：{center}")
            cost = solve_for_center(center, point_infos, waste_file, waste_types, Q_dict, C_dict)
            total_all_cost += cost

        T_cost_sum = sum([T_cost[i] for i, b in enumerate(boolean_selector) if b])
        total_cost_with_center = total_all_cost + T_cost_sum
        print(f"  总运输成本: {total_all_cost:.2f}, 中心成本: {T_cost_sum:.2f}, 总成本: {total_cost_with_center:.2f}")

        if total_cost_with_center < min_total_cost:
            min_total_cost = total_cost_with_center
            best_combination = boolean_selector[:]

    print(f"\n最优组合为：{best_combination}，最小总成本为：{min_total_cost:.2f}")