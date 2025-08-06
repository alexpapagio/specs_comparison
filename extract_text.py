import fitz  # PyMuPDF

def extract_text_blocks(pdf_path):
    doc = fitz.open(pdf_path)
    all_pages_text = []

    for page_num, page in enumerate(doc):
        blocks = page.get_text("blocks")  # returns list of (x0, y0, x1, y1, "text", block_no, block_type)
        blocks = sorted(blocks, key=lambda b: (round(b[1]), b[0]))  # sort top-to-bottom, then left-to-right

        text_lines = []
        for block in blocks:
            text = block[4].strip()
            if text:
                text_lines.append(text)

        page_text = "\n".join(text_lines)
        all_pages_text.append(page_text)

    return "\n\n".join(all_pages_text)

if __name__ == "__main__":
    text = extract_text_blocks("data/alternative/D104.pdf")

    with open("cache/alternative_text/D104_mu.txt", "w", encoding="utf-8") as f:
        f.write(text)
