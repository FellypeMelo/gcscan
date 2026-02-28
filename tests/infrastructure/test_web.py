import pytest
from unittest.mock import MagicMock, patch
from src.infrastructure.web.components import render_sidebar, process_uploads, _render_kpis

def test_render_sidebar():
    with patch("src.infrastructure.web.components.st") as mock_st:
        mock_st.sidebar = MagicMock()
        mock_st.file_uploader.return_value = []
        mock_st.checkbox.return_value = False
        
        files, do_sw, w, s, do_cpg = render_sidebar()
        
        assert files == []
        assert do_sw is False
        assert w == 100
        assert s == 50

def test_process_uploads():
    mock_file = MagicMock()
    mock_file.name = "test.fasta"
    mock_file.getvalue.return_value = b">seq1\nATGC\n"
    
    with patch("src.infrastructure.web.components.st") as mock_st:
        results, sw_res, cpg_res = process_uploads([mock_file], False, 100, 50, False)
        
        assert "seq1" in results
        assert results["seq1"] == 50.0

def test_render_kpis():
    stats = {"count": 1, "mean": 50.0, "std_dev": 0.0, "median": 50.0}
    with patch("src.infrastructure.web.components.st") as mock_st:
        mock_st.columns.return_value = [MagicMock() for _ in range(4)]
        _render_kpis(stats)
        assert mock_st.columns.called

def test_render_raw_tab():
    results = {"s1": 50.0}
    with patch("src.infrastructure.web.components.st") as mock_st:
        from src.infrastructure.web.components import _render_raw_tab
        _render_raw_tab(results)
        assert mock_st.download_button.called

def test_render_main_dashboard():
    results = {"s1": 50.0}
    sw_res = {"s1": [50.0]}
    cpg_res = {"s1": []}
    sw_params = {'window': 100, 'step': 50}
    with patch("src.infrastructure.web.components.st") as mock_st:
        def mock_cols(n):
            cols = [MagicMock() for _ in range(n)]
            for c in cols: c.slider.return_value = 50.0
            return cols
        mock_st.columns.side_effect = mock_cols
        mock_st.tabs.return_value = [MagicMock() for _ in range(4)]
        mock_st.selectbox.return_value = "s1"
        from src.infrastructure.web.components import render_main_dashboard
        render_main_dashboard(results, sw_res, cpg_res, sw_params)
        assert mock_st.tabs.called

def test_render_advanced_tab():
    sw_res = {"s1": [50.0]}
    cpg_res = {"s1": [MagicMock(start=0, end=100, gc_percent=50.0, oe_ratio=0.8)]}
    sw_params = {'window': 100, 'step': 50}
    with patch("src.infrastructure.web.components.st") as mock_st:
        mock_st.selectbox.return_value = "s1"
        mock_st.expander.return_value.__enter__.return_value = MagicMock()
        from src.infrastructure.web.components import _render_advanced_tab
        _render_advanced_tab(sw_res, cpg_res, sw_params)
        assert mock_st.altair_chart.called
        assert mock_st.table.called
