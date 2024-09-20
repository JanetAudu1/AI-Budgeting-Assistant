import pytest
from app.services.recommender import calculate_savings_rate, prepare_user_context, create_gpt_prompt
from app.core.data_validation import UserData
import pandas as pd

@pytest.fixture
def sample_user_data():
    return UserData(
        name="Jane Doe",
        age=35,
        address="456 Elm St",
        current_income=6000,
        current_savings=15000,
        goals=["Save for a vacation", "Invest in stocks"],
        timeline_months=36,
        bank_statement=pd.DataFrame({
            "Date": ["2023-05-01", "2023-05-02"],
            "Description": ["Salary", "Groceries"],
            "Deposits": [6000, 0],
            "Withdrawals": [0, 500],
            "Category": ["Income", "Food"]
        }),
        priorities=["Increase savings", "Learn about investing"]
    )

def test_calculate_savings_rate():
    assert calculate_savings_rate(5000, 4000) == 20.0
    assert calculate_savings_rate(5000, 5000) == 0.0
    assert calculate_savings_rate(0, 1000) == 0.0

def test_prepare_user_context(sample_user_data):
    context = prepare_user_context(sample_user_data)
    assert context["name"] == "Jane Doe"
    assert context["income"] == 6000
    assert context["expenses"] == 500
    assert context["savings_rate"] == pytest.approx(91.67, 0.01)

def test_create_gpt_prompt(sample_user_data):
    context = prepare_user_context(sample_user_data)
    sources = ["Source1", "Source2"]
    prompt = create_gpt_prompt(context, sources)
    assert "Jane Doe" in prompt
    assert "Source1" in prompt
    assert "Source2" in prompt
    assert "Monthly Income: $6000.00" in prompt
