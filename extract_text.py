
import pdfplumber

def extract_text_from_pdf(path):
    with pdfplumber.open(path) as pdf:
        full_text = ""
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
        return full_text

# Change these paths if needed
original_path = "data/D104 - spec.pdf"
proposed_path = "data/D104 - alt.pdf"

original_text = extract_text_from_pdf(original_path)
proposed_text = extract_text_from_pdf(proposed_path)

# Save text output for reference
with open("data/original_text.txt", "w") as f:
    f.write(original_text)

with open("data/proposed_text.txt", "w") as f:
    f.write(proposed_text)

print("✅ Text extracted and saved to .txt files!")
