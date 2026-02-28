import pytest
from src.domain.analysis import (
    calculate_gc_percentage,
    calculate_sliding_window,
    detect_cpg_islands
)
from src.domain.models import CpGIsland

def test_calculate_gc_percentage_basic():
    """Verify GC percentage for a simple sequence."""
    assert calculate_gc_percentage("ATGC") == 50.0
    assert calculate_gc_percentage("GCGC") == 100.0
    assert calculate_gc_percentage("ATAT") == 0.0

def test_calculate_gc_percentage_empty():
    """Empty sequence should return 0.0."""
    assert calculate_gc_percentage("") == 0.0

def test_calculate_sliding_window_basic():
    """Verify sliding window results."""
    results = calculate_sliding_window("ATGCATGC", 4, 4)
    assert results == [50.0, 50.0]

def test_calculate_sliding_window_overlap():
    """Test sliding window GC calculation with overlapping windows."""
    sequence = "ATGCATGC"
    results = calculate_sliding_window(sequence, 4, 2)
    assert results == [50.0, 50.0, 50.0]

def test_calculate_sliding_window_uneven():
    """Test sliding window GC calculation where sequence length is not a multiple of step."""
    sequence = "ATGCATGCA"
    results = calculate_sliding_window(sequence, 4, 4)
    assert results == [50.0, 50.0]

def test_detect_cpg_islands_synthetic():
    """Verify CpG detection logic with a known island sequence."""
    island_seq = "CGCG" * 100 # 400bp, 100% GC
    sequence = ("A" * 400) + island_seq + ("A" * 400)
    
    found = detect_cpg_islands(sequence)
    assert len(found) == 1
    isl = found[0]
    assert isinstance(isl, CpGIsland)
    assert isl.start == 400
    assert isl.end == 800
    assert isl.gc_percent == 100.0
    assert isl.oe_ratio > 0.6

def test_detect_cpg_islands_multiple():
    """Test detection of multiple CpG islands."""
    island1 = "CGCGCGCGCG" * 25 # 250bp
    gap = "ATATATATAT" * 20 # 200bp
    island2 = "GCGCGCGCGC" * 30 # 300bp
    sequence = island1 + gap + island2
    
    results = detect_cpg_islands(sequence)
    assert len(results) == 2
    assert results[0].start == 0
    assert results[0].end == 250
    assert results[1].start == 450
    assert results[1].end == 750
