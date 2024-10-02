import os
import openai
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, TextIteratorStreamer
from threading import Thread
import queue
import logging

logger = logging.getLogger(__name__)

def handle_huggingface_model(prompt, model_name):
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
        
        output = model.generate(**inputs, max_new_tokens=500, do_sample=True, top_k=50, top_p=0.95)
        
        return tokenizer.decode(output[0], skip_special_tokens=True)
            
    except Exception as e:
        raise RuntimeError(f"Error processing {model_name}: {str(e)}")

def handle_gpt4(system_message: str, prompt: str):
    logger.info("Calling GPT-4 API")
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            stream=True
        )
        
        full_response = ""
        for chunk in response:
            if chunk and 'content' in chunk['choices'][0]['delta']:
                content = chunk['choices'][0]['delta']['content']
                full_response += content
                yield content

        logger.info(f"Full GPT-4 response: {full_response}")
        
    except Exception as e:
        logger.exception(f"Error in GPT-4 API call: {str(e)}")
        yield f"Error: {str(e)}"
