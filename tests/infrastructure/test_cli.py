import os
import sys
import pytest
from unittest.mock import patch, MagicMock
from main import main

def test_main_cli_help():
    with patch("sys.argv", ["main.py", "--help"]):
        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code == 0

def test_main_cli_file(tmp_path):
    fasta_file = tmp_path / "test.fasta"
    fasta_file.write_text(">seq1\nATGC\n")
    
    output_dir = tmp_path / "results"
    
    with patch("sys.argv", ["main.py", str(fasta_file), "--output_dir", str(output_dir)]):
        main()
    
    assert os.path.exists(output_dir)
    assert os.path.exists(output_dir / "test_gc.csv")
    assert os.path.exists(output_dir / "test_gc_analysis.png")

def test_main_cli_not_found():
    with patch("sys.argv", ["main.py", "nonexistent.fasta"]):
        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code == 1
