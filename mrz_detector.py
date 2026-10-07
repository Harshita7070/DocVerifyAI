import re


def detect_mrz(ocr_results):

    if not ocr_results:
        return {
            "status": "NOT DETECTED",
            "score": 0,
            "message": "No OCR text available for MRZ analysis.",
            "lines": []
        }

    lines = []

    for item in ocr_results:

        text = item.get("text", "").upper().strip()

        if not text:
            continue

        # Remove spaces because MRZ normally uses continuous characters.
        cleaned = re.sub(r"\s+", "", text)

        lines.append(cleaned)

    mrz_candidates = []

    for line in lines:

        # MRZ uses A-Z, 0-9 and <
        if re.fullmatch(r"[A-Z0-9<]{20,44}", line):

            if "<" in line or re.search(r"[A-Z]{2,3}[0-9]", line):

                mrz_candidates.append(line)

    # -------------------------------------------------
    # Check for two-line passport-style MRZ
    # -------------------------------------------------

    if len(mrz_candidates) >= 2:

        candidate_lines = mrz_candidates[-2:]

        score = 90

        return {
            "status": "DETECTED",
            "score": score,
            "message": "Passport-style MRZ pattern detected.",
            "lines": candidate_lines
        }

    # -------------------------------------------------
    # Single MRZ-like line
    # -------------------------------------------------

    if len(mrz_candidates) == 1:

        return {
            "status": "PARTIAL",
            "score": 60,
            "message": "A partial MRZ-like pattern was detected.",
            "lines": mrz_candidates
        }

    # -------------------------------------------------
    # No MRZ
    # -------------------------------------------------

    return {
        "status": "NOT DETECTED",
        "score": 0,
        "message": "No MRZ pattern was detected in the OCR output.",
        "lines": []
    }