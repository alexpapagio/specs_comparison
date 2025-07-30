from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig
import torch
import re
import json

# Model setup
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

def extract_semantic_attributes(spec_text):
    prompt = f"""
You are a smart assistant. Read the lighting specification text below and extract the following attributes.

Return only a JSON object with these fields:
- Colour Temperature (CCT)
- Beam Angle
- Wattage
- Output (lm)
- Diameter
- Dimming Type (Dali, 0-10V, Phase, DMX, Mains Dimming, TBC etc.)
- Trim Finish

Text:
\"\"\"{spec_text}\"\"\"
"""

    output = pipe(prompt, max_new_tokens=512, do_sample=False )[0]['generated_text']

    try:
        json_text = re.search(r"\{.*\}", output, re.DOTALL).group()
        result = json.loads(json_text)
        print("✅ Extracted Semantic Attributes:")
        for k, v in result.items():
            print(f"{k}: {v}")
        return result
    except Exception as e:
        print("⚠️ Could not parse JSON output:")
        print(output)
        return {}
