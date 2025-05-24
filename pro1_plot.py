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
        
        route_colors = plt.cm.rainbow(np.linspace(0, 1, len(grp)))
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
    _, coords, _, _,_ = read_data('pro1.xlsx')
    
    # routes = [[0, 2, 11, 0], [0 , 3 , 19 , 0], [0 , 4 , 15 , 0],[0 , 5 , 22 , 0],
    #           [0 , 6 , 13 , 0],[0 , 7 , 30 , 0],[0 , 9 , 14 , 0],[0 , 12 , 24 , 27 , 0],[0 , 17 , 8 , 0],
    #           [0 , 20 , 21 , 0],[0 , 23 , 18 , 0],[0 , 25 , 10 , 0],[0 , 26 , 1 , 0],[0 , 28 , 16 , 0],[0, 29, 0]]
    
    routes = [[4, 15], [22, 5], [6, 20], [14, 9], [26, 1], [7, 30], [25, 10], [21, 13], [19, 3], [17, 8], [27, 24, 12], [23, 18], [2, 11], [29], [16, 28]]
    routes = [[0] + route + [0] for route in routes]
    lengths = all_route_lengths(routes, coords)
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
