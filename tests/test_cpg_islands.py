import pytest
from Bio.Seq import Seq
from main import detect_cpg_islands

def test_detect_cpg_islands_positive():
    """Test detection of a clear CpG island."""
    # Synthetic sequence: 100bp low GC, 300bp high GC (CpG island), 100bp low GC
    # CpG island criteria: length > 200, GC > 50%, Obs/Exp > 0.6
    island = "CGCGCGCGCG" * 30 # 300bp, 100% GC, high CpG
    flank_low = "ATATATATAT" * 10 # 100bp, 0% GC
    sequence = Seq(flank_low + island + flank_low)
    
    results = detect_cpg_islands(sequence)
    
    assert len(results) == 1
    start, end, gc_content, obs_exp = results[0]
    assert start == 100
    assert end == 400
    assert gc_content > 50.0
    assert obs_exp > 0.6

def test_detect_cpg_islands_negative_short():
    """Test that short regions are not detected as islands."""
    # 100bp of high GC
    island_short = "CGCGCGCGCG" * 10
    sequence = Seq(island_short)
    
    results = detect_cpg_islands(sequence)
    assert len(results) == 0

def test_detect_cpg_islands_negative_low_gc():
    """Test that low GC regions are not detected as islands."""
    # 300bp of moderate GC (40%) but high length
    region = "ATGCATATAT" * 30 # 10% GC actually, let's make it 40%
    region = "GCATATATAT" * 30 # 20% GC
    sequence = Seq(region)
    
    results = detect_cpg_islands(sequence)
    assert len(results) == 0

def test_detect_cpg_islands_multiple():
    """Test detection of multiple CpG islands."""
    island1 = "CGCGCGCGCG" * 25 # 250bp
    gap = "ATATATATAT" * 20 # 200bp
    island2 = "GCGCGCGCGC" * 30 # 300bp
    sequence = Seq(island1 + gap + island2)
    
    results = detect_cpg_islands(sequence)
    assert len(results) == 2
    assert results[0][0] == 0
    assert results[0][1] == 250
    assert results[1][0] == 450
    assert results[1][1] == 750
