import pytest
from unittest.mock import patch, MagicMock, mock_open
from Bio.Seq import Seq
import pandas as pd
import app

def test_render_sidebar():
    """Test rendering of sidebar components."""
    with patch("streamlit.sidebar"), \
         patch("streamlit.header"), \
         patch("streamlit.file_uploader") as mock_uploader, \
         patch("streamlit.info"), \
         patch("streamlit.divider"), \
         patch("streamlit.checkbox") as mock_check, \
         patch("streamlit.number_input") as mock_num, \
         patch("streamlit.markdown"):
        
        mock_uploader.return_value = ["file1.fasta"]
        mock_check.side_effect = [True, True] # sw, cpg
        mock_num.side_effect = [100, 50] # win, step
        
        files, do_sw, win, step, do_cpg = app.render_sidebar()
        
        assert files == ["file1.fasta"]
        assert do_sw is True
        assert win == 100
        assert step == 50
        assert do_cpg is True

def test_process_files_success():
    """Test file processing logic with success case."""
    mock_file = MagicMock()
    mock_file.name = "test.fasta"
    mock_file.getbuffer.return_value = b">seq1\nATGCATGC\n"
    
    with patch("streamlit.progress") as mock_prog, \
         patch("builtins.open", mock_open()), \
         patch("app.calculate_gc_content") as mock_gc, \
         patch("app.SeqIO.parse") as mock_parse, \
         patch("os.remove"):
        
        mock_gc.return_value = {"seq1": 50.0}
        mock_record = MagicMock()
        mock_record.id = "seq1"
        mock_record.seq = Seq("ATGCATGC")
        mock_parse.return_value = [mock_record]
        
        res, sw_res, cpg_res = app.process_files([mock_file], True, 4, 4, True)
        
        assert "seq1" in res
        assert "seq1" in sw_res
        assert len(sw_res["seq1"]) == 2
        mock_prog.return_value.progress.assert_called()

def test_process_files_error():
    """Test file processing logic with error case for coverage."""
    mock_file = MagicMock()
    mock_file.name = "error.fasta"
    
    with patch("streamlit.progress"), \
         patch("builtins.open", side_effect=Exception("Disk error")), \
         patch("streamlit.error") as mock_error:
        
        res, sw_res, cpg_res = app.process_files([mock_file], False, 100, 50, False)
        assert res == {}
        mock_error.assert_called()

def test_render_dashboard_comprehensive():
    """Test rendering of dashboard components with all features active."""
    results = {"s1": 50.0}
    sw_results = {"s1": [50.0, 50.0]}
    cpg_results = {"s1": [(0, 10, 50.0, 1.0)]}
    
    with patch("app.calculate_statistics") as mock_stats, \
         patch("streamlit.subheader"), \
         patch("streamlit.columns") as mock_cols, \
         patch("streamlit.divider"), \
         patch("streamlit.tabs") as mock_tabs, \
         patch("app.plt.subplots") as mock_subs, \
         patch("app.plot_bar_chart"), \
         patch("app.plot_histogram"), \
         patch("streamlit.pyplot"), \
         patch("streamlit.dataframe"), \
         patch("streamlit.selectbox") as mock_sel, \
         patch("streamlit.altair_chart"), \
         patch("streamlit.expander") as mock_exp, \
         patch("streamlit.table"), \
         patch("streamlit.download_button"), \
         patch("streamlit.warning"), \
         patch("streamlit.info"):
        
        # 1. Setup stats for Histogram branch (N >= 20)
        mock_stats.return_value = {"count": 25, "mean": 55.0, "std_dev": 5.0, "median": 55.0}
        
        # 2. Setup columns and their methods (slider is called on columns)
        kpi_cols = [MagicMock() for _ in range(4)]
        filter_cols = [MagicMock() for _ in range(2)]
        mock_cols.side_effect = [kpi_cols, filter_cols]
        
        # Mock slider values on filter columns
        filter_cols[0].slider.return_value = 0.0
        filter_cols[1].slider.return_value = 100.0
        
        mock_tabs.return_value = [MagicMock() for _ in range(4)]
        mock_subs.return_value = (MagicMock(), MagicMock())
        mock_sel.return_value = "s1"
        
        # Mock context managers
        mock_exp.return_value.__enter__.return_value = MagicMock()

        # Test render
        app.render_dashboard(results, sw_results, cpg_results, True, 100, 50, True)
        
        # Verify calls
        mock_stats.assert_called()
        mock_subs.assert_called()

def test_render_dashboard_no_results_found():
    """Test dashboard with CpG enabled but none found."""
    results = {"s1": 50.0}
    with patch("app.calculate_statistics") as mock_stats, \
         patch("streamlit.subheader"), \
         patch("streamlit.columns") as mock_cols, \
         patch("streamlit.divider"), \
         patch("streamlit.tabs") as mock_tabs, \
         patch("streamlit.warning"), \
         patch("streamlit.info") as mock_info, \
         patch("app.plt.subplots") as mock_subs, \
         patch("streamlit.pyplot"), \
         patch("streamlit.dataframe"), \
         patch("streamlit.download_button"):

        mock_stats.return_value = {"count": 1, "mean": 50.0, "std_dev": 0.0, "median": 50.0}
        kpi_cols = [MagicMock() for _ in range(4)]
        filter_cols = [MagicMock() for _ in range(2)]
        mock_cols.side_effect = [kpi_cols, filter_cols]
        filter_cols[0].slider.return_value = 0.0
        filter_cols[1].slider.return_value = 100.0
        
        mock_tabs.return_value = [MagicMock() for _ in range(4)]
        mock_subs.return_value = (MagicMock(), MagicMock())
        
        # No CpG results
        app.render_dashboard(results, {}, {}, False, 100, 50, True)
        mock_info.assert_any_call("Nenhuma ilha encontrada.")

def test_main_app_flow():
    """Test main entry point of app with and without files."""
    with patch("streamlit.title"), \
         patch("streamlit.markdown"), \
         patch("app.render_sidebar") as mock_side, \
         patch("app.process_files") as mock_proc, \
         patch("app.render_dashboard") as mock_dash, \
         patch("streamlit.info") as mock_info:
        
        # Case 1: No files
        mock_side.return_value = (None, False, 100, 50, False)
        app.main()
        mock_info.assert_called_with("Aguardando upload de arquivos.")
        
        # Case 2: With files
        mock_side.return_value = (["f1"], False, 100, 50, False)
        mock_proc.return_value = ({"s1": 50.0}, {}, {})
        app.main()
        mock_dash.assert_called_once()
