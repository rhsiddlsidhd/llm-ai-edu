import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tools = [{
    "type": "function",
    "function": {
        "name": "extract_subjects",
        "description": "시험지 목차에서 과목명과 시작 페이지를 추출",
        "parameters": {
            "type": "object",
            "properties": {
                "subjects": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "start_page": {"type": "integer"}
                        },
                        "required": ["name", "start_page"]
                    }
                }
            },
            "required": ["subjects"]
        }
    }
}]

def extract_toc(txt_file_path: str) -> list[dict]:
    with open(txt_file_path, 'r', encoding='utf-8') as f:
        full_text = f.read()

    # 1면 텍스트 추출
    end_idx = full_text.find("1면")
    if end_idx == -1:
        raise ValueError("1면 마커를 찾을 수 없습니다.")
    toc_text = full_text[:end_idx + len("1면")].strip()

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "시험지 목차에서 과목명과 시작 페이지 번호를 추출하세요."},
            {"role": "user", "content": toc_text}
        ],
        tools=tools,
        tool_choice={"type": "function", "function": {"name": "extract_subjects"}}
    )

    tool_call = response.choices[0].message.tool_calls
    if not tool_call:
        raise ValueError("1면에서 과목 구조를 추출할 수 없습니다.")

    subjects = json.loads(tool_call[0].function.arguments)["subjects"]
    if not subjects:
        raise ValueError("1면에서 과목 구조를 추출할 수 없습니다.")

    # end_page 계산
    for i, subject in enumerate(subjects):
        subject["end_page"] = subjects[i + 1]["start_page"] if i + 1 < len(subjects) else None

    return subjects

if __name__ == "__main__":
    result = extract_toc("output/full/2025_sport_instructor_level2_exam.txt")
    print(json.dumps(result, ensure_ascii=False, indent=2))
