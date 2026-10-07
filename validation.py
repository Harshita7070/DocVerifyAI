from datetime import datetime


def validate_document(fields):

    checks = []
    risk_score = 0

    # 1. Check missing fields
    for field_name, value in fields.items():
        if value == "Not Found":
            checks.append({
                "check": field_name.replace("_", " ").title(),
                "status": "FAILED",
                "message": "Information not found"
            })
            risk_score += 15

    # 2. Check document number
    document_number = fields["document_number"]

    if document_number != "Not Found":
        if len(document_number) >= 6:
            checks.append({
                "check": "Document Number",
                "status": "PASSED",
                "message": "Valid document number format"
            })
        else:
            checks.append({
                "check": "Document Number",
                "status": "WARNING",
                "message": "Document number appears too short"
            })
            risk_score += 10

    # 3. Check expiry date
    expiry = fields["date_of_expiry"]

    if expiry != "Not Found":
        try:
            expiry_date = datetime.strptime(expiry, "%d/%m/%Y")
            today = datetime.today()

            if expiry_date >= today:
                checks.append({
                    "check": "Document Expiry",
                    "status": "PASSED",
                    "message": "Document is not expired"
                })
            else:
                checks.append({
                    "check": "Document Expiry",
                    "status": "FAILED",
                    "message": "Document has expired"
                })
                risk_score += 30

        except ValueError:
            checks.append({
                "check": "Document Expiry",
                "status": "WARNING",
                "message": "Invalid date format"
            })
            risk_score += 10

    # 4. Check nationality
    nationality = fields["nationality"]

    if nationality != "Not Found":
        checks.append({
            "check": "Nationality",
            "status": "PASSED",
            "message": "Nationality information detected"
        })

    # Limit score to 100
    risk_score = min(risk_score, 100)

    # Risk level
    if risk_score < 30:
        risk_level = "LOW"
    elif risk_score < 60:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "checks": checks
    }