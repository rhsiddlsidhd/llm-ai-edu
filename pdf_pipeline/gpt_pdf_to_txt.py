import fitz
import os

def pdf_to_text(pdf_file_path: str) -> str:
    doc = fitz.open(pdf_file_path)

    full_text = ''
    for page in doc:
        full_text += page.get_text()

    pdf_file_name = os.path.splitext(os.path.basename(pdf_file_path))[0]

    os.makedirs("output/full", exist_ok=True)
    txt_file_path = f"output/full/{pdf_file_name}.txt"
    with open(txt_file_path, 'w', encoding='utf-8') as f:
        f.write(full_text)

    print(f"저장 완료: {txt_file_path} ({len(full_text)}자)")
    return txt_file_path

if __name__ == "__main__":
    pdf_to_text("../pdf/2025_sport_instructor_level2_exam.pdf")
