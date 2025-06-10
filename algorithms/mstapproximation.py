# MST 2-approximation for TSP

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Tuple
import time
from utils.tsp_parser import TSPInstance
from utils.evaluator import calculate_tour_cost



def solve_mst_prim(tsp_instance: TSPInstance) -> Tuple[List[int], float]:
    num_cities = tsp_instance.dimension
    
    if num_cities < 3:
        raise ValueError("Too few cities")
    
    is_visited = []
    for i in range(num_cities):
        is_visited.append(False)
    
    min_cost = []
    for i in range(num_cities):
        min_cost.append(999999)
    
    parent_node = []
    for i in range(num_cities):
        parent_node.append(-1)
    
    min_cost[0] = 0
    tree_edges = []
    
    for step in range(num_cities):
        current_min = -1
        for node in range(num_cities):
            if is_visited[node] == False:
                if current_min == -1 or min_cost[node] < min_cost[current_min]:
                    current_min = node
        
        is_visited[current_min] = True
        if parent_node[current_min] != -1:
            edge = (parent_node[current_min], current_min)
            tree_edges.append(edge)
        
        for neighbor in range(num_cities):
            if is_visited[neighbor] == False:
                distance = 0
                if tsp_instance.large_instance:
                    distance = tsp_instance.get_distance(current_min, neighbor)
                else:
                    distance = tsp_instance.distance_matrix[current_min][neighbor]
                if distance < min_cost[neighbor]:
                    min_cost[neighbor] = distance
                    parent_node[neighbor] = current_min
    
    result_tour, result_cost = build_tour_from_mst(tree_edges, num_cities, tsp_instance)
    return result_tour, result_cost

def solve_mst_kruskal(tsp_instance: TSPInstance) -> Tuple[List[int], float]:
    total_cities = tsp_instance.dimension
    
    if total_cities < 3:
        raise ValueError("Too few cities")
    
    all_edges_list = []
    for city1 in range(total_cities):
        for city2 in range(city1 + 1, total_cities):
            edge_weight = 0
            if tsp_instance.large_instance:
                edge_weight = tsp_instance.get_distance(city1, city2)
            else:
                edge_weight = tsp_instance.distance_matrix[city1][city2]
            new_edge = (edge_weight, city1, city2)
            all_edges_list.append(new_edge)
    
    sorted_edges = []
    for i in range(len(all_edges_list)):
        sorted_edges.append(all_edges_list[i])
    sorted_edges.sort()
    
    node_parent = []
    for i in range(total_cities):
        node_parent.append(i)
    
    def find_root(node):
        if node_parent[node] != node:
            node_parent[node] = find_root(node_parent[node])
        return node_parent[node]
    
    def connect_nodes(node1, node2):
        root1 = find_root(node1)
        root2 = find_root(node2)
        if root1 != root2:
            node_parent[root1] = root2
            return True
        return False
    
    selected_edges = []
    for i in range(len(sorted_edges)):
        weight, node1, node2 = sorted_edges[i]
        if connect_nodes(node1, node2):
            selected_edges.append((node1, node2))
            if len(selected_edges) == total_cities - 1:
                break
    
    final_tour, final_cost = build_tour_from_mst(selected_edges, total_cities, tsp_instance)
    return final_tour, final_cost

def build_tour_from_mst(mst_edges: List[Tuple[int, int]], n: int, tsp_instance: TSPInstance) -> Tuple[List[int], float]:
    adjacency_lists = []
    for city_index in range(n):
        empty_list = []
        adjacency_lists.append(empty_list)
    
    doubled_edges = []
    for edge_idx in range(len(mst_edges)):
        first_city, second_city = mst_edges[edge_idx]
        edge1 = (first_city, second_city)
        edge2 = (second_city, first_city)
        doubled_edges.append(edge1)
        doubled_edges.append(edge2)
    
    for edge_number in range(len(doubled_edges)):
        from_city, to_city = doubled_edges[edge_number]
        adjacency_lists[from_city].append(to_city)
    
    node_stack = [0]
    traversal_path = []
    
    while len(node_stack) > 0:
        current_node = node_stack[len(node_stack)-1]
        if len(adjacency_lists[current_node]) > 0:
            next_city = adjacency_lists[current_node].pop()
            node_stack.append(next_city)
        else:
            visited_node = node_stack.pop()
            traversal_path.append(visited_node)
    
    reversed_path = []
    for path_idx in range(len(traversal_path)-1, -1, -1):
        city = traversal_path[path_idx]
        reversed_path.append(city)
    
    hamiltonian_cycle = []
    city_visited = []
    for city_num in range(n):
        city_visited.append(False)
    
    for path_pos in range(len(reversed_path)):
        current_city = reversed_path[path_pos]
        if city_visited[current_city] == False:
            hamiltonian_cycle.append(current_city)
            city_visited[current_city] = True
    
    for remaining_city in range(n):
        if city_visited[remaining_city] == False:
            hamiltonian_cycle.append(remaining_city)
    
    tour_cost = calculate_tour_cost(hamiltonian_cycle, tsp_instance.distance_matrix, tsp_instance)
    return hamiltonian_cycle, tour_cost

def solve_mst_approx(tsp_instance: TSPInstance) -> Tuple[List[int], float]:
    city_count = tsp_instance.dimension
    if city_count < 500:
        prim_result_tour, prim_result_cost = solve_mst_prim(tsp_instance)
        kruskal_result_tour, kruskal_result_cost = solve_mst_kruskal(tsp_instance)
        
        if prim_result_cost <= kruskal_result_cost:
            best_tour = prim_result_tour
            best_cost = prim_result_cost
            return best_tour, best_cost
        else:
            best_tour = kruskal_result_tour
            best_cost = kruskal_result_cost
            return best_tour, best_cost
    else:
        final_tour, final_cost = solve_mst_prim(tsp_instance)
        return final_tour, final_cost

if __name__ == "__main__":
    from utils.tsp_parser import load_tsp_instances
    
    tsp_data = load_tsp_instances()
    for dataset_name, instance in tsp_data.items():
        if dataset_name in ['test15']:
            print(f"\nTesting {dataset_name}:")
            
            start = time.time()
            prim_tour, prim_cost = solve_mst_prim(instance)
            prim_time = time.time() - start
            
            start = time.time()
            kruskal_tour, kruskal_cost = solve_mst_kruskal(instance)
            kruskal_time = time.time() - start
            
            start = time.time()
            best_tour, best_cost = solve_mst_approx(instance)
            best_time = time.time() - start
            
            print(f"Prim: {prim_cost:.2f} ({prim_time:.3f}s)")
            print(f"Kruskal: {kruskal_cost:.2f} ({kruskal_time:.3f}s)")
            print(f"Best: {best_cost:.2f} ({best_time:.3f}s)") 