def calculate_risk(
    validation_result,
    registry_result,
    tampering_result,
    face_result
):

    risk_score = 0
    factors = []

    # ==================================================
    # 1. DOCUMENT VALIDATION
    # ==================================================

    validation_score = validation_result.get("risk_score", 0)

    validation_points = min(validation_score, 30)

    if validation_points > 0:
        risk_score += validation_points

        factors.append({
            "name": "Document Validation Issues",
            "points": validation_points,
            "severity": "HIGH" if validation_points >= 20 else "MEDIUM"
        })
    else:
        factors.append({
            "name": "Document Validation",
            "points": 0,
            "severity": "LOW"
        })

    # ==================================================
    # 2. REGISTRY VERIFICATION
    # ==================================================

    registry_status = registry_result.get("status", "")

    if registry_status == "BLACKLISTED":

        risk_score += 40

        factors.append({
            "name": "Registry Blacklisted",
            "points": 40,
            "severity": "CRITICAL"
        })

    elif registry_status == "MISMATCH":

        risk_score += 25

        mismatches = registry_result.get("mismatches", [])

        mismatch_text = ", ".join(mismatches)

        factors.append({
            "name": "Registry Mismatch",
            "points": 25,
            "severity": "HIGH",
            "details": mismatch_text
        })

    elif registry_status == "NOT FOUND":

        risk_score += 15

        factors.append({
            "name": "Document Not Found in Registry",
            "points": 15,
            "severity": "MEDIUM"
        })

    elif registry_status == "NOT VERIFIED":

        risk_score += 10

        factors.append({
            "name": "Registry Verification Unavailable",
            "points": 10,
            "severity": "MEDIUM"
        })

    else:

        factors.append({
            "name": "Registry Verification",
            "points": 0,
            "severity": "LOW"
        })

    # ==================================================
    # 3. TAMPERING ANALYSIS
    # ==================================================

    tampering_status = tampering_result.get("status", "")

    tampering_score = tampering_result.get("score", 0)

    if tampering_status == "HIGH":

        risk_score += 25

        factors.append({
            "name": "High Tampering Indicator",
            "points": 25,
            "severity": "HIGH",
            "details": f"Forensic score: {tampering_score}"
        })

    elif tampering_status == "MEDIUM":

        risk_score += 12

        factors.append({
            "name": "Medium Tampering Indicator",
            "points": 12,
            "severity": "MEDIUM",
            "details": f"Forensic score: {tampering_score}"
        })

    elif tampering_status == "ERROR":

        risk_score += 5

        factors.append({
            "name": "Tampering Analysis Error",
            "points": 5,
            "severity": "MEDIUM"
        })

    else:

        factors.append({
            "name": "Tampering Analysis",
            "points": 0,
            "severity": "LOW"
        })

    # ==================================================
    # 4. FACE VERIFICATION
    # ==================================================

    face_status = face_result.get("status", "")
    face_score = face_result.get("score", 0)

    if face_status == "MISMATCH":

        risk_score += 25

        factors.append({
            "name": "Face Verification Mismatch",
            "points": 25,
            "severity": "HIGH",
            "details": f"Similarity score: {face_score}%"
        })

    elif face_status == "NO FACE":

        risk_score += 10

        factors.append({
            "name": "Face Not Detected",
            "points": 10,
            "severity": "MEDIUM"
        })

    elif face_status == "ERROR":

        risk_score += 5

        factors.append({
            "name": "Face Verification Error",
            "points": 5,
            "severity": "MEDIUM"
        })

    else:

        factors.append({
            "name": "Face Verification",
            "points": 0,
            "severity": "LOW",
            "details": f"Similarity score: {face_score}%"
        })

    # ==================================================
    # 5. FINAL SCORE
    # ==================================================

    risk_score = min(risk_score, 100)

    # ==================================================
    # 6. RISK LEVEL
    # ==================================================

    if risk_score < 30:

        risk_level = "LOW"

        recommendation = (
            "No major screening anomaly detected. "
            "Document may proceed to normal verification."
        )

    elif risk_score < 60:

        risk_level = "MEDIUM"

        recommendation = (
            "Potential screening anomalies detected. "
            "Manual review is recommended."
        )

    else:

        risk_level = "HIGH"

        recommendation = (
            "Significant screening anomalies detected. "
            "Manual review is strongly recommended."
        )

    # ==================================================
    # 7. COUNT RISK FACTORS
    # ==================================================

    active_factors = [
        factor for factor in factors
        if factor["points"] > 0
    ]

    # ==================================================
    # 8. FINAL RESULT
    # ==================================================

    return {
        "score": risk_score,
        "level": risk_level,
        "factors": factors,
        "active_factors": len(active_factors),
        "recommendation": recommendation
    }