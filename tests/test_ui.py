import pytest
from unittest.mock import patch
from streamlit.testing.v1 import AppTest
import io
import pandas as pd
from app.ui.app import display_home_page

def mock_csv_file():
    data = {
        'Date': ['2023-01-01', '2023-01-02', '2023-01-03'],
        'Description': ['Grocery', 'Rent', 'Salary'],
        'Withdrawals': [100.00, 1000.00, 0.00],
        'Deposits': [0.00, 0.00, 3000.00]
    }
    df = pd.DataFrame(data)
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)
    return csv_buffer

def test_display_home_page():
    with patch('streamlit.title') as mock_title:
        display_home_page()
        mock_title.assert_called_once_with("💰 Personalized Budgeting Assistant")

def test_home_page():
    at = AppTest.from_file("app/ui/app.py")
    at.run()
    assert "💰 Personalized Budgeting Assistant" in at.get("title")[0].value


