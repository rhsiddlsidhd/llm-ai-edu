import os

txt_file_path = "output/2025_sport_instructor_level2_exam.txt"

with open(txt_file_path, 'r', encoding='utf-8') as f:
    full_text = f.read()

start_marker = "4면"
end_marker = "스포츠심리학(33)"

start_idx = full_text.find(start_marker)
end_idx = full_text.find(end_marker)

education_text = full_text[start_idx:end_idx].strip()

os.makedirs("output", exist_ok=True)
with open("output/2025_sports_pedagogy.txt", 'w', encoding='utf-8') as f:
    f.write(education_text)

print(f"추출 완료: {len(education_text)}자")

print(education_text[:200])
