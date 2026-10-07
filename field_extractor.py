import re


def clean_value(value):
    """Clean OCR noise while keeping useful document text."""
    value = value.strip()
    value = re.sub(r"\s+", " ", value)
    value = value.strip(":-|")
    return value.strip()


def normalize_text(text):
    """Normalize OCR text for easier pattern matching."""
    text = text.replace("|", "I")
    text = text.replace("—", "-")
    text = text.replace("–", "-")
    text = re.sub(r"[ \t]+", " ", text)
    return text


def find_labeled_value(text, labels):
    """
    Find values after common document labels.
    Supports:
    NAME: Rahul Sharma
    Name - Rahul Sharma
    FULL NAME Rahul Sharma
    """
    label_pattern = "|".join(
        re.escape(label) for label in labels
    )

    pattern = rf"(?im)^\s*(?:{label_pattern})\s*(?::|-)?\s*(.+?)\s*$"

    match = re.search(pattern, text)

    if match:
        value = clean_value(match.group(1))

        # Avoid returning another label as the value.
        upper_value = value.upper()
        all_labels = [label.upper() for label in labels]

        if upper_value not in all_labels and len(value) > 1:
            return value

    return None


def find_date(text, labels):
    """Find DD/MM/YYYY or DD-MM-YYYY after a date label."""
    label_pattern = "|".join(
        re.escape(label) for label in labels
    )

    pattern = rf"(?im)^\s*(?:{label_pattern})\s*(?::|-)?\s*" \
              rf"(\d{{2}}[/-]\d{{2}}[/-]\d{{4}})\b"

    match = re.search(pattern, text)

    if match:
        return match.group(1).replace("-", "/")

    return None


def find_document_number(text):
    """Find common document/passport number formats."""
    patterns = [
        r"(?im)^\s*(?:DOCUMENT\s*(?:NUMBER|NO)|DOC\s*(?:NUMBER|NO)|PASSPORT\s*(?:NUMBER|NO)|PASSPORT\s*#)\s*(?::|-)?\s*([A-Z0-9]{6,15})\b",
        r"(?im)\b([A-Z]{1,3}[0-9]{6,12})\b"
    ]

    for pattern in patterns:
        match = re.search(pattern, text)

        if match:
            return match.group(1).upper()

    return None


def extract_fields(ocr_results):

    # Combine OCR output into readable text.
    raw_lines = []

    for item in ocr_results:
        text = item.get("text", "")

        if text:
            raw_lines.append(normalize_text(text))

    full_text = "\n".join(raw_lines)

    # Also create a single-line version for flexible matching.
    single_line_text = " ".join(raw_lines)

    fields = {
        "name": "Not Found",
        "date_of_birth": "Not Found",
        "document_number": "Not Found",
        "nationality": "Not Found",
        "date_of_expiry": "Not Found"
    }

    # =========================================================
    # NAME
    # =========================================================

    name = find_labeled_value(
        full_text,
        [
            "NAME",
            "FULL NAME",
            "SURNAME",
            "GIVEN NAME",
            "HOLDER NAME",
            "APPLICANT NAME"
        ]
    )

    if not name:
        # Flexible fallback for OCR that puts label and value
        # on the same line without punctuation.
        match = re.search(
            r"(?i)\b(?:FULL\s+NAME|NAME)\s*[:\-]?\s+"
            r"([A-Z][A-Z .]{2,50})\b",
            single_line_text
        )

        if match:
            name = clean_value(match.group(1))

    if name:
        fields["name"] = name.upper()

    # =========================================================
    # DATE OF BIRTH
    # =========================================================

    dob = find_date(
        full_text,
        [
            "DATE OF BIRTH",
            "DOB",
            "BIRTH DATE",
            "DATE OF BIRTH."
        ]
    )

    if not dob:
        match = re.search(
            r"(?i)\b(?:DATE\s+OF\s+BIRTH|DOB|BIRTH\s+DATE)"
            r"\s*[:\-]?\s*"
            r"(\d{2}[/-]\d{2}[/-]\d{4})",
            single_line_text
        )

        if match:
            dob = match.group(1).replace("-", "/")

    if dob:
        fields["date_of_birth"] = dob

    # =========================================================
    # DOCUMENT NUMBER
    # =========================================================

    document_number = find_document_number(
        full_text + "\n" + single_line_text
    )

    if document_number:
        fields["document_number"] = document_number

    # =========================================================
    # NATIONALITY
    # =========================================================

    nationality = find_labeled_value(
        full_text,
        [
            "NATIONALITY",
            "NATIONALITY CODE",
            "CITIZENSHIP"
        ]
    )

    if not nationality:
        match = re.search(
            r"(?i)\b(?:NATIONALITY|CITIZENSHIP)"
            r"\s*[:\-]?\s*([A-Z][A-Z ]{2,30})\b",
            single_line_text
        )

        if match:
            nationality = clean_value(match.group(1))

    if nationality:
        fields["nationality"] = nationality.upper()

    # =========================================================
    # DATE OF EXPIRY
    # =========================================================

    expiry = find_date(
        full_text,
        [
            "DATE OF EXPIRY",
            "EXPIRY DATE",
            "EXPIRATION DATE",
            "DATE OF EXPIRATION",
            "VALID UNTIL",
            "VALID TILL"
        ]
    )

    if not expiry:
        match = re.search(
            r"(?i)\b(?:DATE\s+OF\s+EXPIRY|EXPIRY\s+DATE|"
            r"EXPIRATION\s+DATE|DATE\s+OF\s+EXPIRATION|"
            r"VALID\s+UNTIL|VALID\s+TILL)"
            r"\s*[:\-]?\s*"
            r"(\d{2}[/-]\d{2}[/-]\d{4})",
            single_line_text
        )

        if match:
            expiry = match.group(1).replace("-", "/")

    if expiry:
        fields["date_of_expiry"] = expiry

    return fields
