import pytest
import os
from app.services.recommender import call_llm_api

# Check for required API keys
if "HUGGINGFACE_TOKEN" not in os.environ:
    pytest.skip("Skipping tests: HUGGINGFACE_TOKEN not set")

@pytest.mark.parametrize("model_name", ["distilgpt2", "gpt2"])
def test_llm_api(model_name):
    prompt = "Define budgeting in one sentence."
    print(f"\nTesting {model_name}...")
    response = call_llm_api(prompt, model_name, timeout=120)  # Increased timeout
    print(f"{model_name} response: {response}")
    if "Error" in response:
        pytest.fail(f"Error occurred for {model_name}: {response}")
    assert isinstance(response, str)
    assert len(response) > 0

@pytest.mark.skipif("OPENAI_API_KEY" not in os.environ, reason="OPENAI_API_KEY not set")
def test_gpt4_api():
    prompt = "Define budgeting in one sentence."
    response = call_llm_api(prompt, "GPT-4", timeout=60)
    print(f"GPT-4 response: {response}")
    if "Error" in response:
        pytest.fail(f"Error occurred for GPT-4: {response}")
    assert isinstance(response, str)
    assert len(response) > 0

def test_unsupported_model():
    prompt = "This should fail."
    response = call_llm_api(prompt, "UnsupportedModel", timeout=30)
    assert "Error" in response
