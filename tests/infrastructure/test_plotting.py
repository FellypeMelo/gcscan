import pytest
from unittest.mock import MagicMock, patch
from src.infrastructure.plotting.adapters import plot_gc_distribution

@patch("src.infrastructure.plotting.adapters.plt.subplots")
@patch("src.infrastructure.plotting.adapters.plt.savefig")
def test_plot_gc_distribution(mock_savefig, mock_subplots):
    mock_fig = MagicMock()
    mock_ax = MagicMock()
    mock_subplots.return_value = (mock_fig, mock_ax)
    
    results = {"s1": 50.0}
    stats = {"mean": 50.0, "std_dev": 0.0, "count": 1}
    plot_gc_distribution(results, stats, "test.png")
    
    mock_savefig.assert_called_once()

def test_plot_gc_distribution_histogram():
    with patch("src.infrastructure.plotting.adapters.plt.subplots") as mock_subplots, \
         patch("src.infrastructure.plotting.adapters.plt.savefig") as mock_savefig:
        mock_fig = MagicMock()
        mock_ax = MagicMock()
        mock_subplots.return_value = (mock_fig, mock_ax)
        mock_ax.hist.return_value = (None, None, None)
        
        results = {f"s{i}": 50.0 for i in range(25)}
        stats = {"mean": 50.0, "std_dev": 0.0, "count": 25}
        plot_gc_distribution(results, stats, "test.png")
        
        assert mock_ax.hist.called
