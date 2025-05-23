from pro1_util import calculate_distance, read_data, route_length
from pro1_plot import visualize_routes, visualize_routes_subplots, lpt_partition, all_route_lengths

def split_routes_by_time(routes, distance_matrix, T_max, depot=0):
    new_routes = []
    
    for route in routes:
        current_route = [depot]
        current_time = 0
        
        for i in range(len(route)):
            from_node = current_route[-1]
            to_node = route[i]
            travel_time = distance_matrix[from_node][to_node]
            
            if current_time + travel_time + distance_matrix[to_node][depot] > T_max:
                # 回仓库
                current_route.append(depot)
                new_routes.append(current_route)
                
                # 新一条路径
                current_route = [depot, to_node]
                current_time = distance_matrix[depot][to_node]
            else:
                current_route.append(to_node)
                current_time += travel_time
        
        # 最后一条补仓库
        current_route.append(depot)
        new_routes.append(current_route)
    
    return new_routes

T_max = 100
routes = [[12, 30, 7, 17, 23, 5, 22], [21, 6, 4, 14, 25, 1], [16, 26, 10, 29, 20, 13], [9, 19, 3, 28, 24], [11, 2, 27, 8, 18, 15]]
n, coords, _, _, distance_matrix = read_data('pro1.xlsx')

updated_routes = split_routes_by_time(routes, distance_matrix, T_max)
for i in range(len(updated_routes)):
    route_length_value = route_length(updated_routes[i], coords)
    print(f"Route {i+1}: {updated_routes[i]}, Length: {route_length_value:.2f}")
