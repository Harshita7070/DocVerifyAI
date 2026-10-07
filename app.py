from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    redirect,
    url_for,
    session
)

import os
from datetime import datetime

# =========================
# PROJECT MODULES
# =========================

from ocr_engine import extract_text, calculate_ocr_confidence
from field_extractor import extract_fields
from validation import validate_document
from registry import check_registry
from tampering import detect_tampering
from face_verification import verify_faces
from risk_engine import calculate_risk
from mrz_detector import detect_mrz
from document_classifier import classify_document
from pdf_report import generate_pdf_report

# Database
from database import (
    init_database,
    add_screening,
    get_screenings,
    get_screening_statistics
)


# =========================
# FLASK APP
# =========================

app = Flask(__name__)

# Secret key for admin session
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")


# =========================
# FOLDERS
# =========================

UPLOAD_FOLDER = "uploads"
REPORT_FOLDER = "reports"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["REPORT_FOLDER"] = REPORT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)


# =========================
# ADMIN CREDENTIALS
# =========================

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

# =========================
# DATABASE INITIALIZATION
# =========================

init_database()


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================================
# TEST RESULT PAGE
# =========================================================

@app.route("/test-template")
def test_template():

    return render_template(
        "result.html",

        filename="sample_passport.jpg",

        ocr_results=[],

        ocr_confidence=92.5,

        mrz_result={
            "detected": True,
            "score": 85
        },

        document_type="PASSPORT",

        extracted_fields={
            "name": "RAHUL SHARMA",
            "dob": "12/05/2004",
            "document_number": "DOC1234567",
            "nationality": "INDIAN",
            "expiry": "12/05/2030"
        },

        validation_result={
            "valid": True,
            "issues": []
        },

        registry_result={
            "found": True,
            "status": "ACTIVE"
        },

        tampering_result={
            "tampering_detected": False
        },

        face_result={
            "match": True,
            "similarity": 91
        },

        risk_result={
            "level": "LOW",
            "score": 10,
            "factors": []
        },

        report_id="DV-TEST-001",
        report_filename="DV-TEST-001.pdf"
    )


# =========================================================
# ADMIN LOGIN
# =========================================================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        if (
            username == ADMIN_USERNAME
            and password == ADMIN_PASSWORD
        ):

            session["admin_logged_in"] = True

            return redirect(url_for("admin_dashboard"))

        else:

            return render_template(
                "admin_login.html",
                error="Invalid username or password."
            )

    return render_template("admin_login.html")


# =========================================================
# ADMIN LOGOUT
# =========================================================

@app.route("/admin/logout")
def admin_logout():

    session.pop("admin_logged_in", None)

    return redirect(url_for("admin_login"))


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/admin")
def admin_dashboard():

    if not session.get("admin_logged_in"):

        return redirect(url_for("admin_login"))

    # Get statistics from database
    statistics = get_screening_statistics()

    # Get screening history
    screenings = get_screenings()

    # Simulated registry contains 3 records
    registry_count = 3

    return render_template(
        "admin_dashboard.html",
        statistics=statistics,
        screenings=screenings,
        registry_count=registry_count
    )


# =========================================================
# DOCUMENT UPLOAD + VERIFICATION
# =========================================================

@app.route("/upload", methods=["POST"])
def upload():

    # -----------------------------------------------------
    # GET FILES
    # -----------------------------------------------------

    document = request.files.get("document")
    selfie = request.files.get("selfie")

    if not document or document.filename == "":
        return "No document selected."

    if not selfie or selfie.filename == "":
        return "No selfie selected."


    # -----------------------------------------------------
    # SAVE DOCUMENT
    # -----------------------------------------------------

    document_filename = document.filename

    document_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        document_filename
    )

    document.save(document_path)


    # -----------------------------------------------------
    # SAVE SELFIE
    # -----------------------------------------------------

    selfie_filename = "selfie_" + selfie.filename

    selfie_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        selfie_filename
    )

    selfie.save(selfie_path)


    # =====================================================
    # OCR
    # =====================================================

    ocr_results = extract_text(document_path)

    ocr_confidence = calculate_ocr_confidence(
        ocr_results
    )


    # =====================================================
    # FIELD EXTRACTION
    # =====================================================

    extracted_fields = extract_fields(
        ocr_results
    )


    # =====================================================
    # MRZ DETECTION
    # =====================================================

    mrz_result = detect_mrz(
        ocr_results
    )


    # =====================================================
    # DOCUMENT CLASSIFICATION
    # =====================================================

    document_type = classify_document(
        ocr_results
    )


    # =====================================================
    # VALIDATION
    # =====================================================

    validation_result = validate_document(
        extracted_fields
    )


    # =====================================================
    # REGISTRY
    # =====================================================

    registry_result = check_registry(
        extracted_fields
    )


    # =====================================================
    # TAMPERING
    # =====================================================

    tampering_result = detect_tampering(
        document_path
    )


    # =====================================================
    # FACE VERIFICATION
    # =====================================================

    face_result = verify_faces(
        document_path,
        selfie_path
    )


    # =====================================================
    # RISK CALCULATION
    # =====================================================

    risk_result = calculate_risk(
        validation_result,
        registry_result,
        tampering_result,
        face_result
    )


    # =====================================================
    # PDF REPORT
    # =====================================================

    pdf_path, report_id = generate_pdf_report(

        document_filename,

        extracted_fields,

        ocr_confidence,

        document_type,

        mrz_result,

        validation_result,

        registry_result,

        tampering_result,

        face_result,

        risk_result
    )


    report_filename = os.path.basename(
        pdf_path
    )


    # =====================================================
    # DATABASE-SAFE VALUES
    # =====================================================

    # -----------------------------------------------------
    # DOCUMENT TYPE
    # -----------------------------------------------------

    if isinstance(document_type, dict):

        database_document_type = (
            document_type.get("type")
            or document_type.get("document_type")
            or document_type.get("name")
            or "UNKNOWN"
        )

    else:

        database_document_type = document_type


    # -----------------------------------------------------
    # OCR CONFIDENCE
    # -----------------------------------------------------

    if isinstance(ocr_confidence, dict):

        ocr_confidence_db = (
            ocr_confidence.get("confidence")
            or ocr_confidence.get("average")
            or ocr_confidence.get("score")
            or 0
        )

    else:

        ocr_confidence_db = ocr_confidence


    try:

        ocr_confidence_db = float(
            ocr_confidence_db
        )

    except (TypeError, ValueError):

        ocr_confidence_db = 0.0


    # -----------------------------------------------------
    # RISK SCORE
    # -----------------------------------------------------

    if isinstance(risk_result, dict):

        risk_score_db = (
            risk_result.get("score")
            or 0
        )

        risk_level_db = (
            risk_result.get("level")
            or "UNKNOWN"
        )

    else:

        risk_score_db = 0
        risk_level_db = "UNKNOWN"


    try:

        risk_score_db = int(
            risk_score_db
        )

    except (TypeError, ValueError):

        risk_score_db = 0


    # -----------------------------------------------------
    # REGISTRY STATUS
    # -----------------------------------------------------

    if isinstance(registry_result, dict):

        registry_status_db = (
            registry_result.get("status")
            or "NOT FOUND"
        )

    else:

        registry_status_db = str(
            registry_result
        )


    # -----------------------------------------------------
    # TAMPERING STATUS
    # -----------------------------------------------------

    if isinstance(tampering_result, dict):

        tampering_detected = (
            tampering_result.get(
                "tampering_detected",
                False
            )
        )

        if tampering_detected:

            tampering_status_db = "DETECTED"

        else:

            tampering_status_db = "CLEAR"

    else:

        tampering_status_db = str(
            tampering_result
        )


    # -----------------------------------------------------
    # FACE STATUS
    # -----------------------------------------------------

    if isinstance(face_result, dict):

        face_match = face_result.get(
            "match",
            False
        )

        if face_match:

            face_status_db = "MATCH"

        else:

            face_status_db = "NO MATCH"

    else:

        face_status_db = str(
            face_result
        )


    # -----------------------------------------------------
    # PERSON NAME
    # -----------------------------------------------------

    person_name_db = extracted_fields.get(
        "name",
        "UNKNOWN"
    )

    if isinstance(person_name_db, dict):

        person_name_db = str(
            person_name_db
        )


    # -----------------------------------------------------
    # DOCUMENT NUMBER
    # -----------------------------------------------------

    document_number_db = extracted_fields.get(
        "document_number",
        "UNKNOWN"
    )

    if isinstance(document_number_db, dict):

        document_number_db = str(
            document_number_db
        )


    # =====================================================
    # SAVE SCREENING HISTORY
    # =====================================================

    add_screening(

        screening_id=report_id,

        date_time=datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        document_name=document_filename,

        document_type=str(
            database_document_type
        ),

        document_number=str(
            document_number_db
        ),

        person_name=str(
            person_name_db
        ),

        ocr_confidence=ocr_confidence_db,

        risk_score=risk_score_db,

        risk_level=str(
            risk_level_db
        ),

        registry_status=str(
            registry_status_db
        ),

        tampering_status=str(
            tampering_status_db
        ),

        face_status=str(
            face_status_db
        ),

        report_filename=report_filename
    )


    # =====================================================
    # RESULT PAGE
    # =====================================================

    return render_template(

        "result.html",

        filename=document_filename,

        ocr_results=ocr_results,

        ocr_confidence=ocr_confidence,

        mrz_result=mrz_result,

        document_type=document_type,

        extracted_fields=extracted_fields,

        validation_result=validation_result,

        registry_result=registry_result,

        tampering_result=tampering_result,

        face_result=face_result,

        risk_result=risk_result,

        report_id=report_id,

        report_filename=report_filename
    )


# =========================================================
# DOWNLOAD PDF REPORT
# =========================================================

@app.route("/download-report/<filename>")
def download_report(filename):

    return send_from_directory(

        app.config["REPORT_FOLDER"],

        filename,

        as_attachment=True
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )