
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Tuple
import time
from utils.tsp_parser import TSPInstance
from utils.evaluator import calculate_tour_cost

def held_karp_simple(tsp_data: TSPInstance) -> Tuple[List[int], float]:
    n = tsp_data.dimension
    dist = tsp_data.distance_matrix
    
    if n > 20:
        return [], float('inf')
    
    dp = {}
    parent = {}
    
    for i in range(1, n):
        mask = (1 << 0) | (1 << i)
        dp[(mask, i)] = dist[0][i]
        parent[(mask, i)] = 0
    
    for subset_size in range(3, n + 1):
        for mask in range(1 << n):
            bits_count = 0
            temp = mask
            while temp > 0:
                if temp & 1:
                    bits_count += 1
                temp >>= 1
            
            if bits_count != subset_size:
                continue
            if not (mask & 1):
                continue
                
            for last in range(1, n):
                if not (mask & (1 << last)):
                    continue
                
                prev_mask = mask ^ (1 << last)
                min_cost = float('inf')
                best_prev = -1
                
                for prev in range(n):
                    if prev == last or not (prev_mask & (1 << prev)):
                        continue
                    if (prev_mask, prev) in dp:
                        cost = dp[(prev_mask, prev)] + dist[prev][last]
                        if cost < min_cost:
                            min_cost = cost
                            best_prev = prev
                
                if best_prev != -1:
                    dp[(mask, last)] = min_cost
                    parent[(mask, last)] = best_prev
    
    final_mask = (1 << n) - 1
    min_cost = float('inf')
    last_city = -1
    
    for i in range(1, n):
        if (final_mask, i) in dp:
            total = dp[(final_mask, i)] + dist[i][0]
            if total < min_cost:
                min_cost = total
                last_city = i
    
    if last_city == -1:
        return [], float('inf')
        
    path = []
    mask = final_mask
    curr = last_city
    
    while mask and curr != -1:
        path.append(curr)
        if (mask, curr) not in parent:
            break
        next_curr = parent[(mask, curr)]
        mask ^= (1 << curr)
        curr = next_curr
    
    if not path or path[-1] != 0:
        path.append(0)
    path.reverse()
    
    final_cost = calculate_tour_cost(path, dist)
    return path, final_cost

def solve_held_karp(tsp_data: TSPInstance, limit: int = 20) -> Tuple[List[int], float]:
    return held_karp_simple(tsp_data)

if __name__ == "__main__":
    from utils.tsp_parser import load_tsp_instances
    
    test_instances = load_tsp_instances("dataset")
    if test_instances and "test15" in test_instances:
        sample_instance = test_instances["test15"]
        
        print(f"Testing Held-Karp on {sample_instance.name} ({sample_instance.dimension} cities)")
        
        start_time = time.time()
        tour, cost = solve_held_karp(sample_instance, limit=20)
        execution_time = time.time() - start_time
        
        if tour:
            print(f"Optimal solution found!")
            print(f"  Cost: {cost:.2f}")
            print(f"  Tour length: {len(tour)}")
            print(f"  Execution time: {execution_time:.3f}s")
            print(f"  Tour: {tour}")
        else:
            print(f"No solution found (too many cities)")
    else:
        print("test15 dataset not found") 