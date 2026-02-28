from typing import List, Dict
import math

def calculate_descriptive_stats(data: List[float]) -> Dict[str, float]:
    """Calcula estatísticas descritivas básicas."""
    if not data: return {}
    
    sorted_data = sorted(data)
    n = len(data)
    
    return {
        "mean": _calculate_mean(data, n),
        "median": _calculate_median(sorted_data, n),
        "std_dev": _calculate_std_dev(data, n),
        "min": sorted_data[0],
        "max": sorted_data[-1],
        "count": float(n)
    }

def _calculate_mean(data: List[float], n: int) -> float:
    """Calcula a média aritmética."""
    return sum(data) / n

def _calculate_median(sorted_data: List[float], n: int) -> float:
    """Calcula a mediana."""
    if n % 2 == 1:
        return sorted_data[n // 2]
    return (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2

def _calculate_std_dev(data: List[float], n: int) -> float:
    """Calcula o desvio padrão populacional."""
    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / n
    return math.sqrt(variance)
