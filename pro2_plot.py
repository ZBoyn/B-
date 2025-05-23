import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from pro1_util import read_data, all_route_lengths, lpt_partition, build_vehicle_routes
import networkx as nx
plt.rcParams['font.sans-serif'] = ['SimHei']

def visualize_routes(routes, coords, assign=None):
    plt.figure(figsize=(12, 8))
    
    x_coords = [coords[i][0] for i in range(len(coords))]
    y_coords = [coords[i][1] for i in range(len(coords))]
    
    plt.scatter(x_coords[0], y_coords[0], c='red', s=200, marker='*', label='处理站')
    
    plt.scatter(x_coords[1:], y_coords[1:], c='blue', s=50, label='收集点')
    
    for i in range(len(coords)):
        plt.annotate(str(i), (x_coords[i], y_coords[i]), xytext=(5, 5), textcoords='offset points')
    
    if assign is None:
        colors = plt.cm.rainbow(np.linspace(0, 1, len(routes)))
        for route, color in zip(routes, colors):
            route_x = [coords[i][0] for i in route]
            route_y = [coords[i][1] for i in route]
            plt.plot(route_x, route_y, c=color, linewidth=2, alpha=0.7)
    else:
        colors = plt.cm.rainbow(np.linspace(0, 1, len(assign)))
        for j, grp in enumerate(assign):
            for route_idx in grp:
                route = routes[route_idx]
                route_x = [coords[i][0] for i in route]
                route_y = [coords[i][1] for i in route]
                plt.plot(route_x, route_y, c=colors[j], linewidth=2, alpha=0.7, label=f'车{j + 1}' if route_idx == grp[0] else "")
    
    plt.xlabel('X坐标')
    plt.ylabel('Y坐标')
    plt.legend()
    plt.grid(True)
    plt.show()

def visualize_routes_subplots(routes, coords, assign):
    n_vehicles = len(assign)
    fig, axes = plt.subplots(1, n_vehicles, figsize=(6*n_vehicles, 6))
    if n_vehicles == 1:
        axes = [axes]
    
    for ax, (j, grp) in zip(axes, enumerate(assign)):
        x_coords = [coords[i][0] for i in range(len(coords))]
        y_coords = [coords[i][1] for i in range(len(coords))]
        
        ax.scatter(x_coords[0], y_coords[0], c='red', s=200, marker='*', label='处理站')
        ax.scatter(x_coords[1:], y_coords[1:], c='blue', s=50, label='收集点')
        
        for i in range(len(coords)):
            ax.annotate(str(i), (x_coords[i], y_coords[i]), xytext=(5, 5), textcoords='offset points')
        
        # route_colors = plt.cm.rainbow(np.linspace(0, 1, len(grp)))
        # 使用黄色映射
        route_colors = plt.cm.spring(np.linspace(0, 1, len(grp)))
        for route_idx, color in zip(grp, route_colors):
            route = routes[route_idx]
            route_x = [coords[i][0] for i in route]
            route_y = [coords[i][1] for i in route]
            ax.plot(route_x, route_y, c=color, linewidth=2, alpha=0.7, label=f'路线 {route_idx}')
        
        ax.set_title(f'车 {j + 1} 的路线')
        ax.set_xlabel('X坐标')
        ax.set_ylabel('Y坐标')
        ax.grid(True)
        ax.legend()
    
    plt.tight_layout()
    plt.show()

def main():
    _, coords, _, _, _ = read_data('pro1.xlsx')
    
    # cy
    # routes = [[0, 12, 30, 7, 17, 23, 5, 22, 0], [0, 21, 6, 4, 14, 25, 1, 0], [0, 16, 26, 10, 29, 20, 13, 0], [0, 9, 19, 3, 28, 24, 0], [0, 11, 2, 27, 8, 18, 15, 0]]
    # routes = [[12, 30, 7, 17, 23, 5, 22], [21, 6, 4, 14, 25, 1], [16, 26, 10, 29, 20, 13], [9, 19, 3, 28, 24], [11, 2, 27, 8, 18, 15]]
    
    # hs
    # routes = [[0, 21, 6, 13, 20, 29, 10, 5, 23, 17, 7, 30, 3, 28, 12, 24, 8, 27, 18, 2, 11,0], [0,1, 25, 4, 14, 26, 22, 19, 16, 9, 15,0]]
    # routes = [[21, 6, 13, 20, 29, 10, 5, 23, 17, 7, 30, 3, 28, 12, 24, 8, 27, 18, 2, 11], [1, 25, 4, 14, 26, 22, 19, 16, 9, 15]]
    
    # ys
    # routes = [[0, 15, 1, 21, 6, 25, 9, 16, 19, 22, 26, 14, 4, 13, 20, 29, 10, 5, 23, 17, 7, 30, 3, 28, 12, 24, 8, 27, 18, 2, 11, 0]]
    
    # qt 3
    # routes = [[0, 15, 9, 16, 19, 17, 7, 30, 3, 28, 12, 24, 8, 27, 18, 0], [0, 2, 11, 0], [0, 1, 25, 4, 14, 26, 22, 5, 23, 10, 29, 20, 13, 6, 21, 0]]
    routes = [[15, 9, 16, 19, 17, 7, 30, 3, 28, 12, 24, 8, 27, 18], [2, 11], [1, 25, 4, 14, 26, 22, 5, 23, 10, 29, 20, 13, 6, 21]]
    
    
    lengths = all_route_lengths(routes, coords)
    total_length = sum(lengths)
    print(f"总里程: {total_length:.1f}")
    K = 3
    assign, load = lpt_partition(routes, lengths, K)

    print(f"\nLPT 分配结果（{K} 辆车）：")
    for j, grp in enumerate(assign):
        print(f"车{j}: 路线索引 {grp}, 总里程 {load[j]:.1f}")
    
    # 绘制整体路线图
    visualize_routes(routes, coords, assign)
    # 绘制子图
    visualize_routes_subplots(routes, coords, assign)

if __name__ == "__main__":
    main()
