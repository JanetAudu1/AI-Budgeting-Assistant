import os
import openai
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TextIteratorStreamer
from threading import Thread
import queue

def handle_huggingface_model(prompt, model_name):
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
        
        output = model.generate(**inputs, max_new_tokens=500, do_sample=True, top_k=50, top_p=0.95)
        
        return tokenizer.decode(output[0], skip_special_tokens=True)
            
    except Exception as e:
        raise RuntimeError(f"Error processing {model_name}: {str(e)}")

def handle_gpt4(prompt):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful budgeting assistant."},
            {"role": "user", "content": prompt}
        ],
        stream=True
    )
    for chunk in response:
        if chunk.choices[0].delta.get('content'):
            yield chunk.choices[0].delta.content
