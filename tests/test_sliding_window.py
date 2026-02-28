import pytest
from Bio.Seq import Seq
# This import will fail initially as the function doesn't exist yet
from main import calculate_sliding_window_gc

def test_calculate_sliding_window_gc_basic():
    """Test sliding window GC calculation with basic sequence."""
    sequence = Seq("ATGCATGC") # 50% GC
    window_size = 4
    step_size = 4
    
    # Expected windows: "ATGC" (50%), "ATGC" (50%)
    expected = [50.0, 50.0]
    results = calculate_sliding_window_gc(sequence, window_size, step_size)
    assert results == expected

def test_calculate_sliding_window_gc_overlap():
    """Test sliding window GC calculation with overlapping windows."""
    sequence = Seq("ATGCATGC")
    window_size = 4
    step_size = 2
    
    # Windows: 
    # 1: "ATGC" (0-4) -> 50%
    # 2: "GCAT" (2-6) -> 50%
    # 3: "ATGC" (4-8) -> 50%
    expected = [50.0, 50.0, 50.0]
    results = calculate_sliding_window_gc(sequence, window_size, step_size)
    assert results == expected

def test_calculate_sliding_window_gc_uneven():
    """Test sliding window GC calculation where sequence length is not a multiple of step."""
    sequence = Seq("ATGCATGCA") # length 9
    window_size = 4
    step_size = 4
    
    # Windows:
    # 1: "ATGC" (0-4) -> 50%
    # 2: "ATGC" (4-8) -> 50%
    # "A" at end is ignored if smaller than window_size
    expected = [50.0, 50.0]
    results = calculate_sliding_window_gc(sequence, window_size, step_size)
    assert results == expected

def test_calculate_sliding_window_gc_high_low():
    """Test with regions of high and low GC."""
    sequence = Seq("AAAA"+"GGGG"+"TTTT"+"CCCC")
    window_size = 4
    step_size = 4
    
    expected = [0.0, 100.0, 0.0, 100.0]
    results = calculate_sliding_window_gc(sequence, window_size, step_size)
    assert results == expected
