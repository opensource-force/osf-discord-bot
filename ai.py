from huggingface_hub import login
from langchain_community.llms import HuggingFaceHub
from langchain_text_splitters import TokenTextSplitter
from transformers import pipeline
import os
from dotenv import load_dotenv

load_dotenv()

HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
os.environ['HUGGINGFACEHUB_API_TOKEN'] = HUGGINGFACE_API_TOKEN
login(HUGGINGFACE_API_TOKEN)

# Initialize HuggingFaceHub instances
gemma7b = HuggingFaceHub(repo_id='google/gemma-1.1-7b-it')
text_summarizer = HuggingFaceHub(repo_id='Falconsai/text_summarization')

def gemma7b_response(input_text, context):
    """
    Generate response using Gemma7b model.
    """
    template = f"""
    ###context:{context},
    ###instruction:Please provide your response based solely on the information provided in the context and provide the complete answer, If the answer is not in the context please respond with "I am not aware about it" and avoid responding with anything else if its not there,
    ###length: short
    ###question:{input_text},
    ###answer:
"""
    response = gemma7b(template,temperature=0.3,max_new_token=1000)
    return response

def text_summarize(input_text):
    """
    Summarize input text using text summarization model.
    """
    response = text_summarizer(str(input_text))
    return response

def predict_context(input_text):
    """
    Predict if the user is asking a question from database or policy
    """
    response = context_db(input_text)
    
    return response

