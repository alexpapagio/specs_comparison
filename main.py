from extract_attributes import extract_spec_attributes
from semantic_extractor import extract_semantic_attributes
from compare_specs import compare_specs
from annotate_pdf import annotate_pdf_with_differences
import os

# Load saved texts
original_dir = "data/original"
alternative_dir = "data/alternative"
cache_original = "cache/original_text"
cache_alt =  "cache/alternative_text"
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

original_files = [f for f in os.listdir(original_dir) if f.endswith(".pdf")]

for file in original_files:
    base = os.path.splitext(file)[0]
    original_pdf = os.path.join(original_dir, file)
    alternative_pdf = os.path.join(alternative_dir, file)

    if not os.path.exists(alternative_pdf):
        print(f"⚠️ Skipping {file} — no alternative provided.")
        continue

    print (f"🔍 Processing {file}...")

    # Load cached text
    with open(os.path.join(cache_original, base) + ".txt", "r") as f:
         original_text = f.read()
    with open(os.path.join(cache_alt, base) + ".txt", "r") as f:
         proposed_text = f.read()



    # Extract attributes from original text (using regex)
    original_attrs = extract_spec_attributes(original_text)

    # Extract attributes from proposed text (using LLM)
    proposed_attrs = extract_semantic_attributes(proposed_text)

    # Compare attributes
    comparison = compare_specs(original_attrs, proposed_attrs)


    # Annotate the alternative PDF with differences
    output_pdf = os.path.join(output_dir, f"{base}_annotated.pdf")
    annotate_pdf_with_differences(alternative_pdf, comparison, output_pdf)

    # Print comparison results

    print("\n📋 Comparison Summary:")
    for row in comparison:
        print(f"{row['Attribute']}: {row['Original']} → {row['Proposed']} = {row['Severity']}")
