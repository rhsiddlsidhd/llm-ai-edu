import os
import json

def merge_to_yearly_json(year: int, exam_name: str, subject_results: list[dict]) -> str:
    merged = {
        "year": year,
        "exam": exam_name,
        "subjects": {}
    }

    for result in subject_results:
        subject_name = result["subject"]
        merged["subjects"][subject_name] = result["questions"]

    os.makedirs("output/json", exist_ok=True)
    output_path = f"output/json/{year}_{exam_name}.json"
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    print(f"저장 완료: {output_path}")
    return output_path

if __name__ == "__main__":
    from extract_toc import extract_toc
    from split_by_subject import split_by_subject
    from subject_to_json import subject_to_json

    txt_file_path = "output/full/2025_sport_instructor_level2_exam.txt"

    subjects = extract_toc(txt_file_path)
    subject_files = split_by_subject(txt_file_path, subjects)

    subject_results = []
    for item in subject_files:
        result = subject_to_json(item["name"], item["path"])
        subject_results.append(result)

    merge_to_yearly_json(2025, "2급_스포츠지도사", subject_results)
