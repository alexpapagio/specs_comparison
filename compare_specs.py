import re

def parse_numeric(val):
    try:
        return float(re.findall(r"[\d.]+", val)[0])
    except:
        return None

def extract_all_angles(text):
    print(f"Extracting angles from: {text}")
    return [float(n) for n in re.findall(r"\d{1,3}(?:\.\d+)?", text)]

def compare_beam_angles(original, proposed):
    orig_angle = parse_numeric(original)
    proposed_angles = extract_all_angles(proposed)
    print(f"Original angle: {orig_angle}, Proposed angles: {proposed_angles}")

    if not orig_angle or not proposed_angles:
        return "Missing"

    closest = min(proposed_angles, key=lambda x: abs(x - orig_angle))
    diff = abs(closest - orig_angle)

    if diff <= 3:
        return "Minor"
    elif diff <= 6:
        return "Important"
    else:
        return "Very Important"

def compare_wattage(original, proposed):
    # Detect W/m or W
    if "/m" in original.lower() or "/m" in proposed.lower():
        return "Very Important"  # mismatch in units

    o = parse_numeric(original)
    p = parse_numeric(proposed)
    if o is None or p is None:
        return "Missing"

    diff = abs(p - o)
    if diff <= 3:
        return "Minor"
    elif diff <= 5:
        return "Important"
    else:
        return "Very Important"

def compare_diameter(original, proposed):
    o = parse_numeric(original)
    p = parse_numeric(proposed)
    if o is None or p is None:
        return "Missing"

    diff = abs(p - o)
    if diff <= 5:
        return "Minor"
    elif diff <= 10:
        return "Important"
    else:
        return "Very Important"

def compare_cct(original, proposed):
    o = parse_numeric(original)
    p = parse_numeric(proposed)
    if o is None or p is None:
        return "Missing"

    diff = abs(p - o)
    if diff <= 100:
        return "Minor"
    elif diff <= 300:
        return "Important"
    else:
        return "Very Important"

def compare_specs(original, proposed):
    comparison = []

    for key in original.keys():
        o_val = original.get(key)
        p_val = proposed.get(key)

        if o_val is None or p_val is None:
            severity = "Missing"
        elif o_val == p_val:
            severity = "Same"
        else:
            key_lower = key.lower()

            if "beam" in key_lower:
                print(f"Comparing beam angles: {o_val} vs {p_val}")
                severity = compare_beam_angles(o_val, p_val)

            elif "watt" in key_lower:
                severity = compare_wattage(o_val, p_val)

            elif "diameter" in key_lower:
                severity = compare_diameter(o_val, p_val)

            elif "cct" in key_lower or "colour temperature" in key_lower:
                severity = compare_cct(o_val, p_val)

            else:
                # Default numeric or string logic
                o_num = parse_numeric(o_val)
                p_num = parse_numeric(p_val)

                if o_num is not None and p_num is not None:
                    diff_pct = abs(p_num - o_num) / o_num * 100
                    if diff_pct < 5:
                        severity = "Minor"
                    elif diff_pct < 15:
                        severity = "Important"
                    else:
                        severity = "Very Important"
                else:
                    if o_val.lower() == p_val.lower():
                        severity = "Same"
                    elif key_lower in ["mounting type", "trim finish", "dimming type"]:
                        severity = "Very Important"
                    else:
                        severity = "Important"

        comparison.append({
            "Attribute": key,
            "Original": o_val,
            "Proposed": p_val,
            "Severity": severity
        })

    return comparison
