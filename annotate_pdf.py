import fitz  # PyMuPDF

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
            text_instances = page.search_for(proposed_val)

            for inst in text_instances:
                # Draw a red rectangle around the value
                color = {"Minor": (0, 1, 0), "Important": (1, 1, 0), "Very Important": (1, 0, 0)}.get(severity, (0.5, 0.5, 0.5))
                page.draw_rect(inst, color=color, width=1)

                # Add a text annotation above or next to the box
                text = f"{label}: {severity}"
                text_point = fitz.Point(inst.x0, inst.y0 - 10)
                page.insert_text(text_point, text, fontsize=10, color=color, overlay=False, fontname="helv")

    doc.save(output_path)
    print(f"✅ Annotated PDF saved as: {output_path}")
