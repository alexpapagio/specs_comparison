from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig
import torch
import re
import json

# Load LLM
model_id = "microsoft/phi-3-mini-128k-instruct"

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4"
)

tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    device_map="auto",
    quantization_config=bnb_config
)

pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

# Improved prompt
PROMPT_TEMPLATE = """
You are a lighting specification parser.

Below is a technical spec document for a light fixture. Your task is to extract these fields and return them as JSON:
- Colour Temperature (CCT)
- Beam Angle
- Wattage
- Output (lm)
- Diameter
- Dimming Type (e.g., Dali, 0-10V, Phase, DMX, Mains Dimming, TBC)
- Trim Finish

Only respond with the JSON, and make your best guess based on available data (including options or diagrams). Ignore unrelated information.

Spec Document:
\"\"\"
{spec_text}
\"\"\"
"""

def extract_semantic_attributes(spec_text):
    # Truncate or chunk if too long
    max_len = 3500  # Approx ~1000 tokens
    if len(spec_text) > max_len:
        spec_text = spec_text[:max_len]

    prompt = PROMPT_TEMPLATE.format(spec_text=spec_text)

    print("🧠 Extracting attributes from cleaned full text...")
    try:
        output = pipe(prompt, max_new_tokens=512, do_sample=False)[0]['generated_text']
        json_text = re.search(r"\{.*\}", output, re.DOTALL).group()
        result = json.loads(json_text)
        print("✅ Extracted Attributes:")
        for k, v in result.items():
            print(f"  {k}: {v}")
        return result
    except Exception as e:
        print(f"❌ Failed to extract attributes: {e}")
        return {}
