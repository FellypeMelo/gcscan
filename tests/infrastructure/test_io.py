import os
import csv
import pytest
from src.infrastructure.io.fasta import read_fasta
from src.infrastructure.io.exporters import save_results_to_csv

def test_read_fasta(tmp_path):
    fasta_content = ">seq1\nATGC\n>seq2\nGCGC\n"
    fasta_file = tmp_path / "test.fasta"
    fasta_file.write_text(fasta_content)
    
    results = list(read_fasta(str(fasta_file)))
    assert results == [("seq1", "ATGC"), ("seq2", "GCGC")]

def test_save_results_to_csv(tmp_path):
    results = {"seq1": 50.0, "seq2": 75.5}
    output_path = tmp_path / "results.csv"
    save_results_to_csv(results, str(output_path))
    
    assert os.path.exists(output_path)
    with open(output_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == ["Sequence_ID", "GC_Content_Percent"]
        row1 = next(reader)
        assert row1 == ["seq1", "50.00"]


def test_read_fasta_with_blank_lines(tmp_path):
    """Cover fasta.py line 15: blank lines within the FASTA are skipped."""
    content = ">seq1\nATGC\n\n\n>seq2\n\nGCGC\n\n"
    fasta_file = tmp_path / "blanks.fasta"
    fasta_file.write_text(content)

    results = list(read_fasta(str(fasta_file)))
    assert results == [("seq1", "ATGC"), ("seq2", "GCGC")]
