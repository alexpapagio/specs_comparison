import re

def extract_spec_attributes(text):
    results = {}

    # 1. CCT (Colour Temperature)
    match = re.search(r"(\d{4})[-–](\d{4})\s*K", text)
    if match:
        results["Colour Temperature (CCT)"] = f"{match.group(1)}-{match.group(2)} K"

    # 2. Beam Angle
    match = re.findall(r"(\d{1,3})°\s*Beam Angle", text, flags=re.IGNORECASE)
    if match:
        results["Beam Angle"] = f"{match[-1]}°"

    # 3. Wattage
    match = re.search(r"(\d{1,2}\.?\d*)\s*W\s*Wattage", text)
    if match:
        results["Wattage"] = f"{match.group(1)} W"

    # 4. Output (Lumens)
    match = re.search(r"Fixture Output\s+(\d+)", text)
    if match:
        results["Output (lm)"] = f"{match.group(1)} lm"

    # 5. Diameter
    match = re.search(r"Diameter:(\d+)\s*mm", text)
    if match:
        results["Diameter"] = f"{match.group(1)} mm"

    # 6. Dimming Type
    match = re.search(r"(\bDali\b|0-10V|Phase|DMX)", text, flags=re.IGNORECASE)
    if match:
        results["Dimming Type"] = match.group(1)

    # 7. Trim Finish
    match = re.search(r"Trim Finish\s+(.+)", text)
    if match:
        results["Trim Finish"] = match.group(1).strip()

    return results

    # Print extracted attributes
    print("✅ Extracted Attributes:")
    for k, v in results.items():
        print(f"{k}: {v}")
