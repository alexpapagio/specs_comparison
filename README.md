# Lighting Spec Comparator

This tool compares lighting specification sheets using PDF extraction, attribute comparison, and annotated outputs.

## Features
- Extract text from original/proposed lighting spec PDFs
- Use regex + LLM to extract attributes
- Compare attributes with customizable logic
- Annotate differences on the proposed spec PDF

## How to Use
1. Place PDFs in `/original` and `/alternative`
2. Run:
```bash
python extract_text.py
python main.py
