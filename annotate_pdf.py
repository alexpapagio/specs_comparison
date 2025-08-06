import fitz  # PyMuPDF
import re

def annotate_pdf_with_differences(pdf_path, differences, output_path):
    doc = fitz.open(pdf_path)

    for page in doc:
        for item in differences:
            proposed_val = item["Proposed"]
            severity = item["Severity"]
            label = item["Attribute"]

            if not proposed_val or severity == "Same" or severity == "Missing":
                continue

            # Search for proposed value on the page
            text_instances = find_text_variants(page, proposed_val)

            for inst in text_instances:
                # Draw a red rectangle around the value
                color = {"Minor": (0, 1, 0), "Important": (1, 1, 0), "Very Important": (1, 0, 0)}.get(severity, (0.5, 0.5, 0.5))
                page.draw_rect(inst, color=color, width=1)

                # Add a text annotation above or next to the box
                text = f"{label}: {severity}"
                text_point = fitz.Point(inst.x0, inst.y0 - 10)
                page.insert_text(text_point, text, fontsize=10, color=color, overlay=False, fontname="helv")

            if not text_instances:
                page.insert_text(fitz.Point(30, page.rect.height - 30), f"{label}: {severity} (not found)", fontsize=10, color=color)

    doc.save(output_path)
    print(f"✅ Annotated PDF saved as: {output_path}")


def find_text_variants(page, value):
    variants = [value]

    # Normalize values
    if "lumens" in value.lower():
        stripped = re.sub(r"\s*lumens?", "", value, flags=re.I).strip()
        variants.append(stripped)
    if "mm" in value.lower():
        mm_val = re.findall(r"[\d.]+", value)
        if mm_val:
            inch_val = round(float(mm_val[0]) / 25.4, 2)
            variants.append(f'{inch_val}"')

    hits = []
    for v in variants:
        hits.extend(page.search_for(v))
    return hits
