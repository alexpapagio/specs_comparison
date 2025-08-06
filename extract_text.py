import os
import pdfplumber

def extract_text_from_pdf(path):
    with pdfplumber.open(path) as pdf:
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
        return full_text

def process_folder(pdf_folder, cache_folder):
    os.makedirs(cache_folder, exist_ok=True)
    for filename in os.listdir(pdf_folder):
        if filename.lower().endswith(".pdf"):
            base = os.path.splitext(filename)[0]
            pdf_path = os.path.join(pdf_folder, filename)
            txt_path = os.path.join(cache_folder, base + ".txt")

            if not os.path.exists(txt_path):
                print(f"🔍 Extracting text from {filename}")
                text = extract_text_from_pdf(pdf_path)
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(text)
            else:
                print(f"✅ Skipping {filename}, already cached.")

if __name__ == "__main__":
    process_folder("data/original", "cache/original_text")
    process_folder("data/alternative", "cache/alternative_text")
