"""
Mona Lisa TSP Challenge - Simplified Execution
모나리자 TSP (100K cities) 전용 실험 스크립트 (단순화 버전)

실행: python test_monalisa.py
예상 시간: 2-8시간
"""

import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.tsp_parser import load_tsp_instances
from algorithms.mst_approximation import solve_mst_approx

def run_monalisa_experiment():
    print("🎨 MONA LISA TSP CHALLENGE")
    print("=" * 50)
    print("Dataset: mona-lisa100K (100,000 cities)")
    print("Algorithm: MST 2-approximation")
    print("Expected time: 2-8 hours")
    print("=" * 50)
    
    # Load Mona Lisa dataset
    print("\n📂 Loading Mona Lisa dataset...")
    instances = load_tsp_instances("../dataset")
    
    if 'mona-lisa100K' not in instances:
        print("❌ ERROR: mona-lisa100K.tsp not found!")
        print("   Make sure the file exists in dataset/ directory")
        return
    
    instance = instances['mona-lisa100K']
    print(f"✅ Loaded: {instance.name}")
    print(f"   Cities: {instance.dimension:,}")
    print(f"   Memory mode: Real-time distance calculation")
    
    # Start experiment
    print(f"\n🚀 Starting MST 2-approximation...")
    print("   You can monitor progress or stop with Ctrl+C")
    
    start_time = time.time()
    start_str = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"   Start time: {start_str}")
    
    try:
        # Run MST approximation
        tour, cost = solve_mst_approx(instance)
        
        # Calculate results
        end_time = time.time()
        runtime = end_time - start_time
        end_str = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Display results
        print(f"\n🎉 MONA LISA CHALLENGE COMPLETED!")
        print("=" * 50)
        print(f"Final cost: {cost:,.2f}")
        print(f"Tour length: {len(tour):,} cities")
        print(f"Runtime: {runtime/3600:.2f} hours ({runtime:.1f} seconds)")
        print(f"Start: {start_str}")
        print(f"End: {end_str}")
        
        # Save results
        result_file = "monalisa_results.txt"
        with open(result_file, "w") as f:
            f.write("MONA LISA TSP CHALLENGE RESULTS\n")
            f.write("=" * 40 + "\n")
            f.write(f"Dataset: {instance.name}\n")
            f.write(f"Cities: {instance.dimension:,}\n")
            f.write(f"Algorithm: MST 2-approximation\n")
            f.write(f"Final cost: {cost:,.2f}\n")
            f.write(f"Tour length: {len(tour):,}\n")
            f.write(f"Runtime: {runtime/3600:.2f} hours\n")
            f.write(f"Start: {start_str}\n")
            f.write(f"End: {end_str}\n")
        
        print(f"📄 Results saved to: {result_file}")
        
    except KeyboardInterrupt:
        runtime = time.time() - start_time
        print(f"\n⏹️  Experiment stopped by user after {runtime/60:.1f} minutes")
        
    except Exception as e:
        runtime = time.time() - start_time
        print(f"\n❌ Error: {str(e)}")
        print(f"   Runtime before error: {runtime/60:.1f} minutes")

if __name__ == "__main__":
    run_monalisa_experiment() 