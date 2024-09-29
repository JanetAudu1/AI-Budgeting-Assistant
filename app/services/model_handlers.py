from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import openai
import os
import torch

def handle_huggingface_model(prompt, model_name):
    try:
        print(f"Loading tokenizer for {model_name}...")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        print(f"Loading model for {model_name}...")
        model = AutoModelForCausalLM.from_pretrained(model_name)
        
        print(f"Creating pipeline for {model_name}...")
        generator = pipeline("text-generation", model=model, tokenizer=tokenizer, device=-1)  # Force CPU usage
        
        print(f"Generating response for {model_name}...")
        response = generator(prompt, max_length=100, num_return_sequences=1)[0]['generated_text']
        
        return response.strip()
    except Exception as e:
        raise RuntimeError(f"Error processing {model_name}: {str(e)}")

def handle_gpt4(prompt):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message['content'].strip()
