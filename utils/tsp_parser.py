"""
TSP File Parser and Distance Calculator
TSP 파일을 파싱하고 거리 행렬을 계산하는 유틸리티
"""

import math
from typing import List, Tuple, Dict, Any

class TSPInstance:
    """TSP 인스턴스를 표현하는 클래스"""
    
    def __init__(self, name: str, coordinates: List[Tuple[float, float]], 
                 distance_matrix, dimension: int, 
                 large_instance: bool = False):
        self.name = name
        self.coordinates = coordinates
        self.distance_matrix = distance_matrix
        self.dimension = dimension
        self.large_instance = large_instance
    
    def get_distance(self, i: int, j: int) -> float:
        """두 도시 간 거리 반환 (대용량 인스턴스 대응)"""
        if self.large_instance:
            # 실시간 계산
            return euclidean_distance(self.coordinates[i], self.coordinates[j])
        else:
            # 미리 계산된 행렬 사용
            return self.distance_matrix[i][j]

def parse_tsp_file(file_path: str) -> TSPInstance:
    """
    TSP 파일을 파싱하여 TSPInstance 객체를 반환
    
    Args:
        file_path: TSP 파일 경로
        
    Returns:
        TSPInstance: 파싱된 TSP 인스턴스
    """
    coordinates = []
    name = ""
    dimension = 0
    edge_weight_type = "EUC_2D"
    
    with open(file_path, 'r') as file:
        reading_coordinates = False
        
        for line in file:
            line = line.strip()
            
            if line.startswith("NAME"):
                name = line.split(":")[1].strip()
            elif line.startswith("DIMENSION"):
                dimension = int(line.split(":")[1].strip())
            elif line.startswith("EDGE_WEIGHT_TYPE"):
                edge_weight_type = line.split(":")[1].strip()
            elif line == "NODE_COORD_SECTION":
                reading_coordinates = True
                continue
            elif line in ["EOF", "DISPLAY_DATA_SECTION", "EDGE_WEIGHT_SECTION"]:
                break
            elif reading_coordinates and line:
                parts = line.split()
                if len(parts) >= 3:
                    # 인덱스, x, y 좌표
                    x, y = float(parts[1]), float(parts[2])
                    coordinates.append((x, y))
    
    if not coordinates:
        raise ValueError(f"Coordinates not found in file: {file_path}")
    
    # 큰 인스턴스 판별 (50,000개 도시 이상)
    is_large = len(coordinates) >= 50000
    
    if is_large:
        print(f"  ⚠️  대용량 인스턴스 감지 (n={len(coordinates)}): 거리 행렬 실시간 계산 모드")
        # 빈 거리 행렬 (메모리 절약)
        distance_matrix = []
    else:
        # 거리 행렬 계산
        distance_matrix = calculate_distance_matrix(coordinates, edge_weight_type)
    
    return TSPInstance(name, coordinates, distance_matrix, len(coordinates), is_large)

def calculate_distance_matrix(coordinates: List[Tuple[float, float]], 
                            edge_weight_type: str = "EUC_2D"):
    """
    좌표로부터 거리 행렬을 계산 (순수 Python 리스트 사용)
    
    Args:
        coordinates: (x, y) 좌표 리스트
        edge_weight_type: 거리 계산 방법
        
    Returns:
        List[List[float]]: 거리 행렬
    """
    n = len(coordinates)
    distance_matrix = [[0.0 for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(i + 1, n):
            if edge_weight_type == "EUC_2D":
                dist = euclidean_distance(coordinates[i], coordinates[j])
            elif edge_weight_type == "MAN_2D":
                dist = manhattan_distance(coordinates[i], coordinates[j])
            else:
                # 기본적으로 유클리드 거리 사용
                dist = euclidean_distance(coordinates[i], coordinates[j])
            
            distance_matrix[i][j] = dist
            distance_matrix[j][i] = dist
    
    return distance_matrix

def euclidean_distance(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """유클리드 거리 계산"""
    x1, y1 = coord1
    x2, y2 = coord2
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def manhattan_distance(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
    """맨하탄 거리 계산"""
    x1, y1 = coord1
    x2, y2 = coord2
    return abs(x1 - x2) + abs(y1 - y2)

def load_tsp_instances(dataset_dir: str = "dataset") -> Dict[str, TSPInstance]:
    """
    모든 필수 데이터셋을 로드
    
    Args:
        dataset_dir: 데이터셋 디렉토리 경로
        
    Returns:
        Dict[str, TSPInstance]: 데이터셋 이름을 키로 하는 TSP 인스턴스 딕셔너리
    """
    import os
    
    required_datasets = [
        "test15.tsp",
        "a280.tsp",
        "xql662.tsp", 
        "kz9976.tsp",
        "mona-lisa100K.tsp"
    ]
    
    instances = {}
    
    for dataset_file in required_datasets:
        file_path = os.path.join(dataset_dir, dataset_file)
        if os.path.exists(file_path):
            print(f"Loading {dataset_file}...")
            try:
                instance = parse_tsp_file(file_path)
                instances[dataset_file.replace('.tsp', '')] = instance
                print(f"✅ {dataset_file} 로드 완료: {instance.dimension}개 도시")
            except Exception as e:
                print(f"❌ {dataset_file} 로드 실패: {e}")
        else:
            print(f"❌ 파일을 찾을 수 없습니다: {file_path}")
    
    return instances

if __name__ == "__main__":
    # 테스트 코드
    instances = load_tsp_instances()
    for name, instance in instances.items():
        matrix_info = f"{len(instance.distance_matrix)}x{len(instance.distance_matrix[0])}" if instance.distance_matrix else "실시간 계산"
        print(f"{name}: {instance.dimension}개 도시, 거리 행렬: {matrix_info}") 