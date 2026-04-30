import os
import re

def split_by_subject(txt_file_path: str, subjects: list[dict]) -> list[dict]:
    with open(txt_file_path, 'r', encoding='utf-8') as f:
        full_text = f.read()

    def find_page_marker(text: str, page: int, start: int = 0) -> int:
        pattern = re.compile(r'(?<!\d)' + re.escape(str(page)) + r'면')
        match = pattern.search(text, start)
        return match.start() if match else -1

    os.makedirs("output/subjects", exist_ok=True)

    results = []
    for subject in subjects:
        name = subject["name"]
        start_page = subject["start_page"]
        end_page = subject["end_page"]

        start_idx = find_page_marker(full_text, start_page)
        if start_idx == -1:
            raise ValueError(f"'{name}' 시작 마커({start_page}면)를 찾을 수 없습니다.")

        if end_page is not None:
            end_idx = find_page_marker(full_text, end_page, start_idx + 1)
            if end_idx == -1:
                raise ValueError(f"'{name}' 끝 마커({end_page}면)를 찾을 수 없습니다.")
            subject_text = full_text[start_idx:end_idx].strip()
        else:
            subject_text = full_text[start_idx:].strip()

        output_path = f"output/subjects/{name}.txt"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(subject_text)

        print(f"저장: {output_path} ({len(subject_text)}자)")
        results.append({"name": name, "path": output_path})

    return results

if __name__ == "__main__":
    from extract_toc import extract_toc
    txt_file_path = "output/full/2025_sport_instructor_level2_exam.txt"
    subjects = extract_toc(txt_file_path)
    split_by_subject(txt_file_path, subjects)
