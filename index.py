from openai import OpenAI
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

res = client.responses.create(
    model="gpt-4o",
    instructions="You are a helpful assistant.",
    input="2022년 월드컵 우승 팀은 어디야?"
)

print(res.output_text)
