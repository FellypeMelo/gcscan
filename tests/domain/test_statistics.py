import pytest
from src.domain.statistics import calculate_descriptive_stats

def test_calculate_descriptive_stats():
    """Verify stats calculation."""
    data = [40.0, 60.0]
    stats = calculate_descriptive_stats(data)
    assert stats["mean"] == 50.0
    assert stats["median"] == 50.0
    assert stats["count"] == 2
    assert stats["min"] == 40.0
    assert stats["max"] == 60.0

def test_calculate_descriptive_stats_empty():
    """Empty data should return empty dict or default values."""
    assert calculate_descriptive_stats([]) == {}
