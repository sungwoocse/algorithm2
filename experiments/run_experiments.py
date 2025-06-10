import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.tsp_parser import load_tsp_instances
from algorithms.mstapproximation import solve_mst_approx
from algorithms.heldkarp import solve_held_karp
from algorithms.proposedalgorithm import solve_enhanced_algorithm

def run_tsp_experiments():
    print("CSE331 Assignment #2 - TSP Algorithm Experiments")
    print("=" * 60)
    
    # Load instances
    instances = load_tsp_instances()
    
    # Experiment configurations
    experiment_configs = [
        {
            'name': 'test15',
            'algorithms': ['mst', 'held_karp', 'proposed'],  # All algorithms for validation
            'description': '15 cities - Optimal solution verification'
        },
        {
            'name': 'a280', 
            'algorithms': ['mst', 'proposed'],  # Skip Held-Karp due to size
            'description': '280 cities - MST vs Enhanced B&B comparison'
        },
        {
            'name': 'xql662',
            'algorithms': ['mst', 'proposed'],  # Large dataset
            'description': '662 cities - Large-scale performance evaluation'
        },
        {
            'name': 'kz9976',
            'algorithms': ['mst', 'proposed'],  # MST and Proposed feasible
            'description': '9976 cities - MST vs Proposed scalability comparison'
        }
        # mona-lisa100K: Separated into test_monalisa.py for dedicated testing
    ]
    
    # Algorithm mapping
    algorithm_funcs = {
        'mst': solve_mst_approx,
        'held_karp': solve_held_karp,
        'proposed': solve_enhanced_algorithm
    }
    
    results = {}
    
    for config in experiment_configs:
        dataset_name = config['name']
        if dataset_name not in instances:
            print(f"Dataset {dataset_name} not found, skipping...")
            continue
            
        instance = instances[dataset_name]
        print(f"\n📊 Testing {instance.name}: {config['description']}")
        print(f"   Dimension: {instance.dimension} cities")
        
        results[dataset_name] = {}
        
        for algo_name in config['algorithms']:
            print(f"\n🔬 Running {algo_name.upper()} algorithm...")
            
            start_time = time.time()
            try:
                tour, cost = algorithm_funcs[algo_name](instance)
                runtime = time.time() - start_time
                
                if tour and cost != float('inf'):
                    results[dataset_name][algo_name] = {
                        'tour': tour,
                        'cost': cost,
                        'runtime': runtime,
                        'status': 'completed'
                    }
                    print(f"   ✅ {algo_name}: cost={cost:.2f}, time={runtime:.3f}s")
                else:
                    results[dataset_name][algo_name] = {
                        'tour': [],
                        'cost': float('inf'),
                        'runtime': runtime,
                        'status': 'failed/omitted'
                    }
                    print(f"   ❌ {algo_name}: Failed or omitted due to resource constraints")
                    
            except Exception as e:
                runtime = time.time() - start_time
                results[dataset_name][algo_name] = {
                    'tour': [],
                    'cost': float('inf'),
                    'runtime': runtime,
                    'status': f'error: {str(e)}'
                }
                print(f"   ❌ {algo_name}: Error - {str(e)}")
    
    # Summary
    print("\n📋 EXPERIMENT SUMMARY")
    print("=" * 60)
    
    # Save results to file
    import datetime
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"experiment_results_{timestamp}.txt"
    
    summary_lines = []
    summary_lines.append("CSE331 Assignment #2 - TSP Algorithm Experiments")
    summary_lines.append("=" * 60)
    summary_lines.append(f"Execution Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    summary_lines.append("")
    summary_lines.append("EXPERIMENT SUMMARY")
    summary_lines.append("=" * 60)
    
    for dataset_name, dataset_results in results.items():
        line = f"\n{dataset_name.upper()}:"
        print(line)
        summary_lines.append(line)
        
        for algo_name, result in dataset_results.items():
            if result['status'] == 'completed':
                line = f"  {algo_name:12}: cost={result['cost']:8.2f}, time={result['runtime']:6.3f}s"
                print(line)
                summary_lines.append(line)
            else:
                line = f"  {algo_name:12}: {result['status']}"
                print(line)
                summary_lines.append(line)
    
    # Write to file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write('\n'.join(summary_lines))
    
    print(f"\n📄 Results saved to: {filename}")
    
    return results

if __name__ == "__main__":
    run_tsp_experiments() 