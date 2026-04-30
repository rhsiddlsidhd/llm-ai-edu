from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

def summarize_txt(file_path: str):
    clent = OpenAI(api_key=api_key)

    with open(file_path,'r',encoding='utf-8') as f:
        txt = f.read()

    system_prompt = f'''
    
    '''