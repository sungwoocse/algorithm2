import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from typing import List, Tuple
from utils.tsp_parser import TSPInstance
from utils.evaluator import calculate_tour_cost

def get_distance(tsp_instance: TSPInstance, i: int, j: int) -> float:
    if tsp_instance.large_instance:
        return tsp_instance.get_distance(i, j)
    else:
        return tsp_instance.distance_matrix[i][j]

def nearest_neighbor_tour(tsp_instance: TSPInstance, start: int = 0) -> Tuple[List[int], float]:
    n = tsp_instance.dimension
    tour = [start]
    unvisited = set(range(n)) - {start}
    current = start
    
    while unvisited:
        nearest = min(unvisited, key=lambda city: get_distance(tsp_instance, current, city))
        tour.append(nearest)
        unvisited.remove(nearest)
        current = nearest
    
    cost = calculate_tour_cost(tour, tsp_instance.distance_matrix, tsp_instance)
    return tour, cost

def farthest_insertion_tour(tsp_instance: TSPInstance, start: int = 0) -> Tuple[List[int], float]:
    n = tsp_instance.dimension
    if n <= 2:
        return nearest_neighbor_tour(tsp_instance, start)
    
    tour = [start]
    unvisited = set(range(n)) - {start}
    
    farthest = max(unvisited, key=lambda city: get_distance(tsp_instance, start, city))
    tour.append(farthest)
    unvisited.remove(farthest)
    
    while unvisited:
        best_city = max(unvisited, 
                       key=lambda city: min(get_distance(tsp_instance, city, tour_city) 
                                           for tour_city in tour))
        
        best_pos = 0
        best_increase = float('inf')
        
        for i in range(len(tour)):
            j = (i + 1) % len(tour)
            old_cost = get_distance(tsp_instance, tour[i], tour[j])
            new_cost = (get_distance(tsp_instance, tour[i], best_city) + 
                       get_distance(tsp_instance, best_city, tour[j]))
            increase = new_cost - old_cost
            
            if increase < best_increase:
                best_increase = increase
                best_pos = i + 1
        
        tour.insert(best_pos, best_city)
        unvisited.remove(best_city)
    
    cost = calculate_tour_cost(tour, tsp_instance.distance_matrix, tsp_instance)
    return tour, cost

def simple_branch_bound(tsp_instance: TSPInstance, time_limit: int = 10) -> Tuple[List[int], float]:
    n = tsp_instance.dimension
    
    best_tour, best_cost = nearest_neighbor_tour(tsp_instance)
    
    if n > 15:  
        return best_tour, best_cost
    
    start_time = time.time()
    nodes_checked = 0
    
    def bound_calculation(partial_tour: List[int], remaining: set) -> float:
        if len(remaining) <= 1:
            return 0
        
        cities = list(remaining)
        if len(cities) < 2:
            return 0
        
        min_cost = 0
        for i in range(len(cities)):
            min_edge = float('inf')
            for j in range(len(cities)):
                if i != j:
                    dist = get_distance(tsp_instance, cities[i], cities[j])
                    min_edge = min(min_edge, dist)
            min_cost += min_edge
        
        return min_cost * 0.5 
    
    def branch_bound_recursive(current_tour: List[int], remaining: set, current_cost: float):
        nonlocal best_tour, best_cost, nodes_checked
        
        nodes_checked += 1
        if time.time() - start_time > time_limit or nodes_checked > 50000:
            return
        
        if not remaining:
            total_cost = current_cost
            if total_cost < best_cost:
                best_tour = current_tour[:]
                best_cost = total_cost
            return

        bound = current_cost + bound_calculation(current_tour, remaining)
        if bound >= best_cost:
            return
        
        current_city = current_tour[-1]
        for next_city in remaining:
            new_cost = current_cost + get_distance(tsp_instance, current_city, next_city)
            if new_cost < best_cost:
                new_remaining = remaining - {next_city}
                branch_bound_recursive(current_tour + [next_city], new_remaining, new_cost)

    remaining = set(range(1, n))
    branch_bound_recursive([0], remaining, 0)
    
    return best_tour, best_cost

def solve_hybrid_algorithm(tsp_instance: TSPInstance) -> Tuple[List[int], float]:
    n = tsp_instance.dimension
    
    if n <= 12:
        return simple_branch_bound(tsp_instance)
    elif n <= 100:
        nn_tour, nn_cost = nearest_neighbor_tour(tsp_instance)
        fi_tour, fi_cost = farthest_insertion_tour(tsp_instance)
        
        if nn_cost <= fi_cost:
            return nn_tour, nn_cost
        else:
            return fi_tour, fi_cost
    else:
        return nearest_neighbor_tour(tsp_instance)

def solve_enhanced_algorithm(tsp_instance: TSPInstance) -> Tuple[List[int], float]:
    return solve_hybrid_algorithm(tsp_instance)

if __name__ == "__main__":
    from utils.tsp_parser import load_tsp_instances
    
    tsp_data = load_tsp_instances()
    for name, instance in tsp_data.items():
        if name in ['test15']:
            start_time = time.time()
            tour, cost = solve_hybrid_algorithm(instance)
            runtime = time.time() - start_time
            print(f"{name}: {cost:.2f} (time: {runtime:.3f}s)")
            print(f"Tour: {tour[:10]}{'...' if len(tour) > 10 else ''}") 