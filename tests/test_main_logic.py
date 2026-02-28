import os
import csv
import sys
import pytest
import numpy as np
from unittest.mock import patch, MagicMock, ANY
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from main import (
    calculate_gc_content,
    calculate_statistics,
    save_results_to_csv,
    plot_bar_chart,
    plot_histogram,
    plot_gc_content,
    main
)

def test_calculate_gc_content(tmp_path):
    """Test standard GC content calculation from FASTA file."""
    fasta_content = ">seq1\nATGC\n>seq2\nGCGC\n"
    fasta_file = tmp_path / "test.fasta"
    fasta_file.write_text(fasta_content)
    
    results = calculate_gc_content(str(fasta_file))
    assert results == {"seq1": 50.0, "seq2": 100.0}

def test_calculate_gc_content_error():
    """Test error handling in calculate_gc_content."""
    with patch("main.SeqIO.parse", side_effect=Exception("Read error")):
        with pytest.raises(SystemExit):
            calculate_gc_content("nonexistent.fasta")

def test_calculate_statistics():
    """Test statistics calculation."""
    results = {"s1": 40.0, "s2": 60.0}
    stats = calculate_statistics(results)
    assert stats["mean"] == 50.0
    assert stats["median"] == 50.0
    assert stats["count"] == 2
    assert stats["min"] == 40.0
    assert stats["max"] == 60.0

def test_calculate_statistics_empty():
    """Test statistics with empty results."""
    assert calculate_statistics({}) == {}

def test_save_results_to_csv(tmp_path):
    """Test saving results to CSV."""
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
        row2 = next(reader)
        assert row2 == ["seq2", "75.50"]

def test_save_results_to_csv_error():
    """Test error handling in save_results_to_csv."""
    with patch("builtins.open", side_effect=IOError("Write error")):
        with patch("main.print") as mock_print:
            save_results_to_csv({"s1": 50.0}, "/invalid/path/file.csv")
            mock_print.assert_any_call("Erro ao salvar CSV: Write error")

def test_plot_bar_chart():
    """Test bar chart plotting call."""
    results = {"s1": 50.0}
    ax = MagicMock()
    mock_bar = MagicMock()
    mock_bar.get_height.return_value = 50.0
    mock_bar.get_x.return_value = 0
    mock_bar.get_width.return_value = 0.8
    ax.bar.return_value = [mock_bar]
    plot_bar_chart(results, ax)
    ax.bar.assert_called_once()

def test_plot_histogram():
    """Test histogram plotting call."""
    results = {"s1": 50.0, "s2": 60.0}
    stats = {"mean": 55.0, "std_dev": 5.0}
    ax = MagicMock()
    ax.hist.return_value = (None, None, None)
    plot_histogram(results, ax, stats)
    ax.hist.assert_called_once()
    assert ax.axvline.call_count == 3

@patch("main.plt.subplots")
@patch("main.plt.savefig")
def test_plot_gc_content_bar(mock_savefig, mock_subplots):
    """Test top-level plotting function (bar chart case)."""
    mock_fig = MagicMock()
    mock_ax = MagicMock()
    mock_subplots.return_value = (mock_fig, mock_ax)
    mock_ax.bar.return_value = []
    
    results = {f"s{i}": 50.0 for i in range(10)} # < 20
    plot_gc_content(results, "test.png")
    
    mock_savefig.assert_called_once()

@patch("main.plt.subplots")
@patch("main.plt.savefig")
def test_plot_gc_content_hist(mock_savefig, mock_subplots):
    """Test top-level plotting function (histogram case)."""
    mock_fig = MagicMock()
    mock_ax = MagicMock()
    mock_subplots.return_value = (mock_fig, mock_ax)
    mock_ax.hist.return_value = (None, None, None)
    
    results = {f"s{i}": 50.0 for i in range(25)} # >= 20
    plot_gc_content(results, "test.png")
    
    mock_savefig.assert_called_once()

def test_plot_gc_content_empty():
    """Test plotting with empty results."""
    with patch("main.print") as mock_print:
        plot_gc_content({}, "test.png")
        mock_print.assert_called_with("Nenhum resultado para plotar.")

@patch("main.plt.savefig", side_effect=IOError("Save error"))
@patch("main.plt.subplots")
def test_plot_gc_content_error(mock_subplots, mock_savefig):
    """Test error handling in plot_gc_content."""
    mock_subplots.return_value = (MagicMock(), MagicMock())
    with patch("main.print") as mock_print:
        plot_gc_content({"s1": 50.0}, "test.png")
        mock_print.assert_any_call("Erro ao salvar gráfico: Save error")

@patch("main.calculate_gc_content")
@patch("main.save_results_to_csv")
@patch("main.plot_gc_content")
def test_main_cli(mock_plot, mock_csv, mock_calc, tmp_path):
    """Test main CLI entry point with file."""
    # Create a dummy fasta file
    fasta_file = tmp_path / "test.fasta"
    fasta_file.write_text(">seq1\nATGC\n")
    
    mock_calc.return_value = {"seq1": 50.0}
    
    test_args = ["main.py", str(fasta_file), "--output_dir", str(tmp_path / "results")]
    with patch("sys.argv", test_args):
        main()
    
    mock_calc.assert_called_once()

@patch("main.calculate_gc_content")
@patch("main.save_results_to_csv")
@patch("main.plot_gc_content")
def test_main_cli_new_features(mock_plot, mock_csv, mock_calc, tmp_path):
    """Test main CLI with sliding window and CpG island arguments."""
    fasta_file = tmp_path / "test.fasta"
    fasta_file.write_text(">seq1\nATGCATGC\n")
    
    mock_calc.return_value = {"seq1": 50.0}
    
    test_args = [
        "main.py", str(fasta_file), 
        "--window", "4", 
        "--step", "4",
        "--cpg"
    ]
    
    with patch("sys.argv", test_args):
        main()
    
    mock_calc.assert_called_once_with(ANY, 4, 4, True)

@patch("main.calculate_gc_content")
def test_main_cli_directory(mock_calc, tmp_path):
    """Test main CLI entry point with directory."""
    dir_path = tmp_path / "fastas"
    dir_path.mkdir()
    (dir_path / "test1.fasta").write_text(">s1\nGC\n")
    (dir_path / "test2.fa").write_text(">s2\nAT\n")
    (dir_path / "not_fasta.txt").write_text("dummy")
    
    mock_calc.return_value = {"s": 50.0}
    
    test_args = ["main.py", str(dir_path), "--output_dir", str(tmp_path / "results")]
    with patch("sys.argv", test_args), patch("main.save_results_to_csv"), patch("main.plot_gc_content"):
        main()
    
    assert mock_calc.call_count == 2

def test_main_cli_no_files(tmp_path):
    """Test main CLI when no FASTA files found in directory."""
    dir_path = tmp_path / "empty_dir"
    dir_path.mkdir()
    test_args = ["main.py", str(dir_path)]
    with patch("sys.argv", test_args), pytest.raises(SystemExit) as e:
        main()
    assert e.value.code == 0

def test_main_cli_not_found():
    """Test main CLI with nonexistent input."""
    test_args = ["main.py", "nonexistent.fasta"]
    with patch("sys.argv", test_args), pytest.raises(SystemExit):
        main()

@patch("main.calculate_gc_content", return_value={})
def test_main_cli_empty_fasta(mock_calc, tmp_path):
    """Test main CLI with FASTA file containing no sequences."""
    fasta_file = tmp_path / "empty.fasta"
    fasta_file.write_text("")
    test_args = ["main.py", str(fasta_file)]
    with patch("sys.argv", test_args):
        main()
    mock_calc.assert_called_once()
