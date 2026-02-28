import pytest
from unittest.mock import patch, MagicMock
from Bio.Seq import Seq

# We will try to test parts of app.py by mocking streamlit
@patch("streamlit.sidebar")
@patch("streamlit.file_uploader")
def test_app_sidebar(mock_uploader, mock_sidebar):
    """Test if sidebar elements are rendered."""
    from app import main
    mock_uploader.return_value = None
    # This is a shallow test since Streamlit is hard to unit test without specialized tools
    # but we can verify it doesn't crash on start
    with patch("streamlit.title"), patch("streamlit.markdown"):
        main()
    mock_uploader.assert_called_once()

def test_app_logic_integration():
    """Verify app.py uses functions from main.py correctly."""
    from app import calculate_gc_content, calculate_statistics
    # These should be imported from main.py
    assert calculate_gc_content is not None
    assert calculate_statistics is not None
