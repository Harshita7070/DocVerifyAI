# 🔍 DocVerify AI
### AI-Based Fake Identity & Document Screening System

DocVerify AI is an AI-assisted document screening system designed to detect potentially fake, manipulated, or suspicious identity documents.

The system combines OCR, document classification, field extraction, document validation, registry verification, tampering detection, face verification, MRZ detection, and risk scoring to provide a consolidated screening result.

> **SIH 2026 Project — SIH26188**

---

## 📌 Problem Statement

Fake identity documents and manipulated documents can be used for identity fraud, unauthorized access, financial fraud, and other cyber-related activities.

Traditional document verification processes can be time-consuming and may require manual inspection of multiple document properties.

DocVerify AI aims to provide a faster preliminary screening mechanism by analyzing multiple document characteristics through a single platform.

---

## 🎯 Objectives

- Extract information from identity documents using OCR.
- Automatically classify uploaded documents.
- Extract important fields such as name and document number.
- Validate extracted information.
- Detect possible document tampering.
- Perform prototype face verification.
- Detect possible MRZ information.
- Check document information against a simulated registry.
- Calculate an overall risk score.
- Generate a screening report.
- Maintain screening history through an admin dashboard.

---

## ✨ Key Features

### 1. 📄 Document Upload

Users can upload an identity document for screening.

The system processes the uploaded document and performs multiple verification checks.

### 2. 🔤 OCR Processing

EasyOCR is used to extract text from the uploaded document.

The system also calculates an OCR confidence value to indicate the quality of extracted text.

### 3. 🗂️ Document Classification

The uploaded document is analyzed and classified based on document-related keywords and extracted information.

### 4. 🔎 Field Extraction

Important information is extracted from the OCR output, including:

- Person Name
- Document Number
- Other available identity fields

### 5. ✅ Document Validation

Extracted fields are checked using validation rules to identify potentially invalid or suspicious information.

### 6. 🏛️ Registry Verification

The system checks extracted document information against a **simulated registry database**.

> This is a prototype simulation and does not connect to real government databases or APIs.

### 7. 🛡️ Tampering Detection

The system performs image analysis to identify possible signs of document manipulation.

The result acts as a screening indicator and should not be considered definitive proof of forgery.

### 8. 👤 Face Verification

A prototype face verification module compares available face information from the document and verification input.

This feature is intended for demonstration purposes.

### 9. 🪪 MRZ Detection

The system detects possible Machine Readable Zone (MRZ) information using pattern-based detection.

### 10. ⚠️ Risk Scoring

Different verification results are combined to calculate an overall risk score.

The system categorizes the result into:

- 🟢 LOW
- 🟡 MEDIUM
- 🔴 HIGH

### 11. 📑 PDF Report Generation

A screening report can be generated containing the verification results and risk assessment.

### 12. 👨‍💼 Admin Dashboard

The admin dashboard provides:

- Login authentication
- Screening history
- Screening statistics
- Document information
- Risk levels
- Verification results
- Report access

### 13. 🗄️ Screening History

Screening information is stored locally using SQLite for the prototype.

---



# 🔄 System Workflow

```text
                ┌─────────────────────┐
                │   Upload Document   │
                └──────────┬──────────┘
                           ↓
                ┌─────────────────────┐
                │     OCR Analysis    │
                └──────────┬──────────┘
                           ↓
                ┌─────────────────────┐
                │ Document Classifier │
                └──────────┬──────────┘
                           ↓
                ┌─────────────────────┐
                │   Field Extraction  │
                └──────────┬──────────┘
                           ↓
             ┌─────────────┴─────────────┐
             ↓             ↓             ↓
        Validation    Tampering      MRZ Detection
             │         Detection           │
             └─────────────┬─────────────┘
                           ↓
                ┌─────────────────────┐
                │ Registry Verification│
                └──────────┬──────────┘
                           ↓
                ┌─────────────────────┐
                │  Face Verification  │
                └──────────┬──────────┘
                           ↓
                ┌─────────────────────┐
                │    Risk Scoring     │
                └──────────┬──────────┘
                           ↓
                ┌─────────────────────┐
                │ Screening Result    │
                └──────────┬──────────┘
                           ↓
                ┌─────────────────────┐
                │    PDF Report       │
                └─────────────────────┘

                🧠 Technology Stack
Backend
Python
Flask

Artificial Intelligence / Image Processing
EasyOCR
OpenCV
NumPy
Pillow

Data Processing
Pandas

Database
SQLite

Report Generation
ReportLab

Frontend
HTML
CSS
JavaScript
Flask Jinja Templates

Development Tools
Visual Studio Code
Git
GitHub

📁 Project Structure
DocVerifyAI/
│
├── app.py
├── database.py
├── document_classifier.py
├── face_verification.py
├── field_extractor.py
├── mrz_detector.py
├── ocr_engine.py
├── pdf_report.py
├── registry.py
├── risk_engine.py
├── tampering.py
├── validation.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   ├── ...
│
├── uploads/
│
└── reports/

⚙️ Installation
1. Clone the repository
git clone https://github.com/YOUR_USERNAME/DocVerifyAI.git

Move into the project directory:

cd DocVerifyAI
2. Create a virtual environment
Windows
python -m venv venv

Activate it:

venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Run the application
python app.py

Open your browser and visit:

http://127.0.0.1:5000

🔐 Security Considerations

The system is designed as a prototype for document screening and cybersecurity research.

Important security considerations include:

Uploaded documents should be handled securely.
Sensitive personal information should not be exposed.
Production systems should use secure authentication.
API credentials should be stored using environment variables.
Real government databases should only be accessed through authorized APIs.
Personal identity documents should not be stored unnecessarily.

⚠️ Limitations

This project is currently a prototype.

Registry
The registry verification module uses simulated data and does not connect to real government databases.

Face Verification
The current face verification module is a prototype and should not be treated as production-grade biometric authentication.

Tampering Detection
Tampering detection provides indicators of possible manipulation but cannot guarantee that a document is forged.

MRZ Detection
The current MRZ module uses pattern-based detection and is not a complete ICAO-compliant MRZ verification system.

Risk Score
The risk score is intended for preliminary screening and should not be used as the sole basis for a legal or identity decision.

🚀 Future Scope

The system can be further improved by implementing:

Real authorized government/API registry integration
Advanced AI-based document forgery detection
Deep-learning based face verification
ICAO-compliant MRZ parsing
Advanced document classification models
Cloud database integration
PostgreSQL support
Secure role-based authentication
Multi-factor authentication
Audit logs
Improved fraud detection models
Real-time verification APIs
Secure cloud storage
Mobile application support
🎓 SIH 2026

Problem Statement: SIH26188
Project: AI-Based Fake Identity & Document Screening System

This project was developed as a prototype to demonstrate how AI, OCR, image processing, validation techniques, and risk analysis can be combined for preliminary identity-document screening.

👩‍💻 Project Purpose

DocVerify AI demonstrates a multi-layered approach to document screening by combining several independent verification mechanisms instead of relying on a single check.

The objective is to assist verification workflows by providing a consolidated screening result and identifying potentially suspicious documents for further human review.

📜 Disclaimer

This project is an academic/prototype implementation.

It is not a replacement for official identity verification systems, government databases, certified biometric systems, or professional forensic examination.

Only synthetic, fictional, or authorized test documents should be used while demonstrating the system.

⭐ Project Status
Prototype / SIH 2026 MVP
📬 Contact

Developer: Harshita Jamdar

GitHub:
https://github.com/Harshita7070

⭐ If you find this project useful, consider giving the repository a star.


### 3. Save it

Press:

**Ctrl + S**

Then we'll push the README to GitHub.

### 4. Before pushing

Don't run `git add .` blindly yet. Run:

```powershell
git status
