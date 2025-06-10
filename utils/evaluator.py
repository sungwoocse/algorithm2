"""
TSP Algorithm Evaluator
TSP 알고리즘의 성능을 평가하는 유틸리티
"""

import time
from typing import List, Tuple, Dict, Any, Callable
from utils.tsp_parser import TSPInstance

class TSPResult:
    """TSP 알고리즘 실행 결과를 저장하는 클래스"""
    
    def __init__(self, tour: List[int], cost: float, runtime: float, 
                 algorithm_name: str, instance_name: str):
        self.tour = tour
        self.cost = cost
        self.runtime = runtime
        self.algorithm_name = algorithm_name
        self.instance_name = instance_name

def calculate_tour_cost(tour: List[int], distance_matrix = None, 
                       instance: TSPInstance = None) -> float:
    """
    투어의 총 비용을 계산
    
    Args:
        tour: 도시 방문 순서 (0-based index)
        distance_matrix: 거리 행렬 (선택사항)
        instance: TSP 인스턴스 (대용량 인스턴스용)
        
    Returns:
        float: 투어 총 비용
    """
    if not tour:
        return float('inf')
    
    total_cost = 0.0
    n = len(tour)
    
    for i in range(n):
        current_city = tour[i]
        next_city = tour[(i + 1) % n]  # 마지막 도시에서 첫 번째 도시로 돌아감
        
        if instance and instance.large_instance:
            # 대용량 인스턴스: 실시간 계산
            total_cost += instance.get_distance(current_city, next_city)
        elif distance_matrix is not None:
            # 일반 인스턴스: 미리 계산된 행렬 사용
            total_cost += distance_matrix[current_city][next_city]
        else:
            raise ValueError("distance_matrix or instance parameter required")
    
    return total_cost

def is_valid_tour(tour: List[int], n_cities: int) -> bool:
    """
    투어가 유효한지 검증
    
    Args:
        tour: 도시 방문 순서
        n_cities: 총 도시 수
        
    Returns:
        bool: 투어가 유효하면 True
    """
    if len(tour) != n_cities:
        return False
    
    # 모든 도시를 정확히 한 번씩 방문하는지 확인
    return set(tour) == set(range(n_cities))

def evaluate_algorithm(algorithm_func: Callable[[TSPInstance], Tuple[List[int], float]], 
                      instance: TSPInstance, 
                      algorithm_name: str,
                      max_runtime: float = 300.0) -> TSPResult:
    """
    TSP 알고리즘을 실행하고 성능을 평가
    
    Args:
        algorithm_func: TSP 알고리즘 함수
        instance: TSP 인스턴스
        algorithm_name: 알고리즘 이름
        max_runtime: 최대 실행 시간 (초)
        
    Returns:
        TSPResult: 평가 결과
    """
    print(f"🔄 {algorithm_name} 실행 중... ({instance.name})")
    
    start_time = time.time()
    
    try:
        # 시간 제한이 있는 경우 처리 (실제 구현에서는 더 정교한 방법 필요)
        tour, cost = algorithm_func(instance)
        
        end_time = time.time()
        runtime = end_time - start_time
        
        if runtime > max_runtime:
            print(f"⚠️  시간 초과: {runtime:.2f}초 > {max_runtime}초")
        
        # 투어 유효성 검증
        if not is_valid_tour(tour, instance.dimension):
            print(f"❌ 유효하지 않은 투어가 반환됨")
            return TSPResult([], float('inf'), runtime, algorithm_name, instance.name)
        
        # 비용 재계산 (검증)
        calculated_cost = calculate_tour_cost(tour, instance.distance_matrix, instance)
        if abs(calculated_cost - cost) > 1e-6:
            print(f"⚠️  비용 불일치: 반환값={cost:.2f}, 계산값={calculated_cost:.2f}")
            cost = calculated_cost
        
        print(f"✅ {algorithm_name} 완료: 비용={cost:.2f}, 시간={runtime:.2f}초")
        
        return TSPResult(tour, cost, runtime, algorithm_name, instance.name)
        
    except Exception as e:
        end_time = time.time()
        runtime = end_time - start_time
        print(f"❌ {algorithm_name} 실행 실패: {e}")
        return TSPResult([], float('inf'), runtime, algorithm_name, instance.name)

def compare_results(results: List[TSPResult], optimal_costs: Dict[str, float] = None) -> Dict[str, Any]:
    """
    여러 알고리즘 결과를 비교
    
    Args:
        results: TSPResult 리스트
        optimal_costs: 각 인스턴스의 최적해 (있는 경우)
        
    Returns:
        Dict[str, Any]: 비교 결과
    """
    if not results:
        return {}
    
    comparison = {
        'instance_name': results[0].instance_name,
        'algorithms': {},
        'best_cost': float('inf'),
        'best_algorithm': None
    }
    
    # 각 알고리즘 결과 정리
    for result in results:
        comparison['algorithms'][result.algorithm_name] = {
            'cost': result.cost,
            'runtime': result.runtime,
            'tour_length': len(result.tour)
        }
        
        # 최고 성능 업데이트
        if result.cost < comparison['best_cost']:
            comparison['best_cost'] = result.cost
            comparison['best_algorithm'] = result.algorithm_name
    
    # 최적해가 있는 경우 근사 비율 계산
    if optimal_costs and results[0].instance_name in optimal_costs:
        optimal_cost = optimal_costs[results[0].instance_name]
        comparison['optimal_cost'] = optimal_cost
        
        for result in results:
            if result.cost != float('inf'):
                approximation_ratio = result.cost / optimal_cost
                comparison['algorithms'][result.algorithm_name]['approximation_ratio'] = approximation_ratio
    
    return comparison

def print_comparison_table(comparisons: List[Dict[str, Any]]):
    """비교 결과를 표 형태로 출력"""
    
    print("\n" + "="*80)
    print("📊 TSP 알고리즘 성능 비교 결과")
    print("="*80)
    
    for comp in comparisons:
        print(f"\n🗺️  데이터셋: {comp['instance_name']}")
        print("-" * 60)
        
        if 'optimal_cost' in comp:
            print(f"🎯 최적해: {comp['optimal_cost']:.2f}")
        
        print(f"🏆 최고 성능: {comp['best_algorithm']} (비용: {comp['best_cost']:.2f})")
        print()
        
        # 헤더
        header = f"{'알고리즘':<20} {'비용':<15} {'시간(초)':<10}"
        if any('approximation_ratio' in alg_data for alg_data in comp['algorithms'].values()):
            header += f" {'근사비율':<10}"
        print(header)
        print("-" * len(header))
        
        # 각 알고리즘 결과
        for alg_name, alg_data in comp['algorithms'].items():
            line = f"{alg_name:<20} {alg_data['cost']:<15.2f} {alg_data['runtime']:<10.2f}"
            if 'approximation_ratio' in alg_data:
                line += f" {alg_data['approximation_ratio']:<10.3f}"
            print(line)

# 알려진 최적해 (참고용)
KNOWN_OPTIMAL_COSTS = {
    'a280': 2579.0,
    'xql662': 2513.0,
    # kz9976과 mona-lisa100K는 정확한 최적해를 모르므로 생략
}

if __name__ == "__main__":
    # 테스트용 더미 결과
    dummy_results = [
        TSPResult([0, 1, 2, 3], 100.0, 0.5, "Algorithm A", "test"),
        TSPResult([0, 2, 1, 3], 110.0, 0.3, "Algorithm B", "test")
    ]
    
    comparison = compare_results(dummy_results, {'test': 95.0})
    print_comparison_table([comparison]) 