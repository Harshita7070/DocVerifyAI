import easyocr

reader = easyocr.Reader(['en'], gpu=False)


def extract_text(image_path):

    results = reader.readtext(image_path)

    extracted_text = []

    for result in results:

        text = result[1]
        confidence = result[2]

        extracted_text.append({
            "text": text,
            "confidence": round(confidence * 100, 2)
        })

    return extracted_text


def calculate_ocr_confidence(ocr_results):

    if not ocr_results:
        return {
            "score": 0,
            "level": "LOW",
            "message": "No text was detected."
        }

    total_confidence = 0

    for result in ocr_results:
        total_confidence += result.get("confidence", 0)

    average_confidence = total_confidence / len(ocr_results)

    average_confidence = round(average_confidence, 2)

    if average_confidence >= 85:

        level = "HIGH"
        message = "OCR extraction quality is high."

    elif average_confidence >= 60:

        level = "MEDIUM"
        message = "OCR extraction quality is moderate."

    else:

        level = "LOW"
        message = "OCR extraction quality is low. Manual verification is recommended."

    return {
        "score": average_confidence,
        "level": level,
        "message": message
    }