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


def test_stress_large_virtual_fasta_parallel(tmp_path):
    """
    TDD RED Phase: Testes estressantes para grandes arquivos virtuais e concorrência.
    Criamos um FASTA simulado com 50.000 sequências para forçar o I/O concurrente
    e verificar tolerância a quebras e leaks de memória.
    """
    massive_fasta = tmp_path / "massive.fasta"
    
    # Gerando um FASTA de estresse iterativamente para não explodir a RAM do teste
    num_sequences = 10000
    with open(massive_fasta, "w") as f:
        for i in range(num_sequences):
            f.write(f">seq_massive_{i}\n")
            # 100 bases alternadas
            f.write("ATGC" * 25 + "\n")

    results, all_islands, all_windows = process_fasta_parallel(
        str(massive_fasta), 
        window=0, 
        step=0, 
        cpg=False, 
        max_workers=4
    )
    
    # Validação do stress test
    assert len(results) == num_sequences
    # O conteúdo "ATGC" * 25 tem exatamente 50% de GC
    assert abs(results["seq_massive_0"] - 50.0) < 0.1
    assert abs(results[f"seq_massive_{num_sequences-1}"] - 50.0) < 0.1
