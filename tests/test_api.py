from fastapi.testclient import TestClient
from app.api.main import app

client = TestClient(app)

def test_generate_advice():
    user_data = {
        "name": "Janet Audu",
        "age": 30,
        "address": "123 Main St",
        "current_income": 1000,
        "current_savings": 10000,
        "goals": ["Buy a house", "Save for retirement"],
        "timeline_months": 60,
        "bank_statement": [
            {"Date": "2023-05-01", "Description": "Salary", "Deposits": 5000, "Withdrawals": 0, "Category": "Income"},
            {"Date": "2023-05-02", "Description": "Rent", "Deposits": 0, "Withdrawals": 1500, "Category": "Housing"}
        ]
    }

    response = client.post("/api/generate_advice", json=user_data)
    print(f"Response status code: {response.status_code}") 
    print(f"Response content: {response.content}")  
    assert response.status_code == 200
    assert "content-type" in response.headers
    assert response.headers["content-type"] == "text/event-stream; charset=utf-8"
    
    assert response.content