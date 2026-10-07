import re


def classify_document(ocr_results):

    if not ocr_results:
        return {
            "type": "UNKNOWN",
            "confidence": 0,
            "message": "No OCR text available for document classification."
        }

    text = " ".join(
        item.get("text", "")
        for item in ocr_results
    ).upper()

    text = re.sub(r"\s+", " ", text)

    scores = {
        "PASSPORT": 0,
        "VISA": 0,
        "IDENTITY DOCUMENT": 0
    }

    passport_keywords = [
        "PASSPORT",
        "P<",
        "NATIONALITY",
        "DATE OF BIRTH",
        "DATE OF EXPIRY",
        "PLACE OF BIRTH",
        "AUTHORITY"
    ]

    for keyword in passport_keywords:
        if keyword in text:
            scores["PASSPORT"] += 1

    visa_keywords = [
        "VISA",
        "ENTRY",
        "VALID FROM",
        "VALID UNTIL",
        "ENTRIES",
        "DURATION OF STAY",
        "ISSUED AT"
    ]

    for keyword in visa_keywords:
        if keyword in text:
            scores["VISA"] += 1

    id_keywords = [
        "IDENTITY CARD",
        "IDENTIFICATION",
        "ID CARD",
        "DATE OF BIRTH",
        "NATIONALITY",
        "GENDER",
        "ADDRESS"
    ]

    for keyword in id_keywords:
        if keyword in text:
            scores["IDENTITY DOCUMENT"] += 1

    document_type = max(
        scores,
        key=scores.get
    )

    highest_score = scores[document_type]

    if highest_score == 0:
        return {
            "type": "UNKNOWN",
            "confidence": 0,
            "message": "Document type could not be determined."
        }

    confidence = min(
        95,
        round((highest_score / 7) * 100)
    )

    if highest_score < 2:
        return {
            "type": "UNKNOWN",
            "confidence": confidence,
            "message": (
                "Insufficient indicators for reliable "
                "document classification."
            )
        }

    return {
        "type": document_type,
        "confidence": confidence,
        "message": (
            f"Document classified as {document_type}."
        )
    }