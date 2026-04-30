import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tools = [{
    "type": "function",
    "function": {
        "name": "extract_questions",
        "description": "시험 과목 텍스트에서 문제 번호, 문제 내용, 보기를 추출",
        "parameters": {
            "type": "object",
            "properties": {
                "questions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "number": {"type": "integer"},
                            "question": {"type": "string"},
                            "choices": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        },
                        "required": ["number", "question", "choices"]
                    }
                }
            },
            "required": ["questions"]
        }
    }
}]

def subject_to_json(subject_name: str, txt_file_path: str) -> dict:
    with open(txt_file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "시험지 텍스트에서 각 문제의 번호, 문제 내용, 보기를 정확히 추출하세요."},
            {"role": "user", "content": text}
        ],
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "extract_questions"}}
    )

    tool_call = response.choices[0].message.tool_calls
    if not tool_call:
        raise ValueError(f"'{subject_name}' 문제 추출에 실패했습니다.")

    questions = json.loads(tool_call[0].function.arguments)["questions"]
    if not questions:
        raise ValueError(f"'{subject_name}' 문제 추출에 실패했습니다.")

    return {"subject": subject_name, "questions": questions}

if __name__ == "__main__":
    result = subject_to_json(
        "스포츠교육학",
        "output/subjects/스포츠교육학.txt"
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
