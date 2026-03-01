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

def test_formatter():
    from src.infrastructure.cli.formatter import print_header, print_stats, print_cpg_islands
    from src.domain.models import CpGIsland
    print_header(1)
    print_stats({"count": 1, "mean": 50.0, "std_dev": 0.0})
    print_cpg_islands("s1", [CpGIsland(0, 100, 50.0, 0.8)])
    print_cpg_islands("s1", [])

def test_runner_no_files():
    from src.infrastructure.cli.runner import run_analysis
    args = MagicMock()
    args.input = "nonexistent_dir"
    with patch("os.path.isfile", return_value=False), patch("os.path.isdir", return_value=True), patch("os.listdir", return_value=[]):
        run_analysis(args)


def test_identify_files_invalid_path():
    """_identify_files returns [] when path is neither file nor directory."""
    from src.infrastructure.cli.runner import _identify_files
    with patch("os.path.isfile", return_value=False), patch("os.path.isdir", return_value=False):
        assert _identify_files("invalid_path") == []


def test_process_single_file_parallel(tmp_path):
    """Cover parallel branch of _process_single_file (lines 49-61)."""
    from src.infrastructure.cli.runner import _process_single_file

    fasta_file = tmp_path / "par.fasta"
    fasta_file.write_text(">s1\nATGCATGCATGC\n")

    args = MagicMock()
    args.parallel = True
    args.window = 4
    args.step = 4
    args.cpg = True
    args.workers = 1
    args.output_dir = str(tmp_path / "out")
    os.makedirs(args.output_dir, exist_ok=True)

    _process_single_file(str(fasta_file), args)


def test_process_single_file_sequential_with_window_and_cpg(tmp_path):
    """Cover sequential branch with window and cpg flags (lines 69-75)."""
    from src.infrastructure.cli.runner import _process_single_file

    fasta_file = tmp_path / "seq.fasta"
    fasta_file.write_text(">s1\nATGCATGC\n")

    args = MagicMock()
    args.parallel = False
    args.window = 4
    args.step = 0
    args.cpg = True
    args.output_dir = str(tmp_path / "out")
    os.makedirs(args.output_dir, exist_ok=True)

    _process_single_file(str(fasta_file), args)


def test_formatter_sliding_window_info():
    """Cover formatter.py line 17: print_sliding_window_info."""
    from src.infrastructure.cli.formatter import print_sliding_window_info
    print_sliding_window_info("seq1", 10)
