import pytest
import os
from src.infrastructure.parallel.dispatcher import process_fasta_parallel

def test_process_fasta_parallel_returns_correct_stats(tmp_path):
    """
    TDD RED Phase: Test if we can process a fasta using multiprocessing.
    Creates a temporary Multi-FASTA file and asserts correctness.
    """
    fasta_file = tmp_path / "mock_multi.fasta"
    # Create 4 sequences to distribute among cores
    content = ">seq1\nATGC\n>seq2\nGCGC\n>seq3\nATAT\n>seq4\nGGCC\n"
    fasta_file.write_text(content)
    
    # We expect `process_fasta_parallel` to return dictionaries mapping sequence IDs
    # to their respective metrics.
    results, all_islands, all_windows = process_fasta_parallel(
        str(fasta_file), 
        window=0, 
        step=0, 
        cpg=False, 
        max_workers=2
    )
    
    assert "seq1" in results
    assert results["seq1"] == 50.0
    assert results["seq2"] == 100.0
    assert results["seq3"] == 0.0
    assert results["seq4"] == 100.0
