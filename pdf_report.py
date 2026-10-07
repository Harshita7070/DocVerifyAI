from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from datetime import datetime
import os


def generate_pdf_report(
    filename,
    extracted_fields,
    ocr_confidence,
    document_type,
    mrz_result,
    validation_result,
    registry_result,
    tampering_result,
    face_result,
    risk_result
):

    os.makedirs("reports", exist_ok=True)

    timestamp = datetime.now()

    report_id = timestamp.strftime("DV-%Y%m%d-%H%M%S")

    pdf_filename = f"{report_id}.pdf"

    pdf_path = os.path.join(
        "reports",
        pdf_filename
    )

    document = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=9,
        textColor=colors.grey
    )

    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontSize=13,
        spaceBefore=12,
        spaceAfter=8
    )

    small_style = ParagraphStyle(
        "Small",
        parent=styles["Normal"],
        fontSize=8,
        textColor=colors.grey
    )

    story = []

    # =====================================================
    # TITLE
    # =====================================================

    story.append(
        Paragraph(
            "DOCVERIFY AI",
            title_style
        )
    )

    story.append(
        Paragraph(
            "FORENSIC DOCUMENT SCREENING REPORT",
            subtitle_style
        )
    )

    story.append(Spacer(1, 8))

    # =====================================================
    # REPORT INFORMATION
    # =====================================================

    report_info = [
        ["Screening ID", report_id],
        [
            "Generated",
            timestamp.strftime("%d/%m/%Y %H:%M:%S")
        ],
        ["Uploaded File", filename]
    ]

    table = Table(
        report_info,
        colWidths=[45 * mm, 125 * mm]
    )

    table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.HexColor("#eeeeee")
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                9
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                6
            )
        ])
    )

    story.append(table)

    # =====================================================
    # 1. DOCUMENT INFORMATION
    # =====================================================

    story.append(
        Paragraph(
            "1. DOCUMENT INFORMATION",
            section_style
        )
    )

    document_info = [
        ["Field", "Detected Value"],

        [
            "Document Type",
            document_type.get(
                "type",
                "UNKNOWN"
            )
        ],

        [
            "Document Number",
            extracted_fields.get(
                "document_number",
                "Not Found"
            )
        ],

        [
            "Name",
            extracted_fields.get(
                "name",
                "Not Found"
            )
        ],

        [
            "Date of Birth",
            extracted_fields.get(
                "date_of_birth",
                "Not Found"
            )
        ],

        [
            "Nationality",
            extracted_fields.get(
                "nationality",
                "Not Found"
            )
        ],

        [
            "Date of Expiry",
            extracted_fields.get(
                "date_of_expiry",
                "Not Found"
            )
        ]
    ]

    table = Table(
        document_info,
        colWidths=[55 * mm, 115 * mm]
    )

    table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#222222")
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                9
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                6
            )
        ])
    )

    story.append(table)

    # =====================================================
    # 2. OCR ANALYSIS
    # =====================================================

    story.append(
        Paragraph(
            "2. OCR ANALYSIS",
            section_style
        )
    )

    ocr_data = [
        [
            "OCR Confidence",
            f'{ocr_confidence.get("score", 0)}%'
        ],

        [
            "Confidence Level",
            ocr_confidence.get(
                "level",
                "UNKNOWN"
            )
        ],

        [
            "Analysis",
            ocr_confidence.get(
                "message",
                ""
            )
        ]
    ]

    table = Table(
        ocr_data,
        colWidths=[55 * mm, 115 * mm]
    )

    table.setStyle(
        TableStyle([
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.HexColor("#eeeeee")
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                9
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                6
            )
        ])
    )

    story.append(table)

    # =====================================================
    # 3. MRZ ANALYSIS
    # =====================================================

    story.append(
        Paragraph(
            "3. MRZ ANALYSIS",
            section_style
        )
    )

    mrz_data = [
        [
            "MRZ Status",
            mrz_result.get(
                "status",
                "UNKNOWN"
            )
        ],

        [
            "MRZ Score",
            f'{mrz_result.get("score", 0)}%'
        ],

        [
            "Message",
            mrz_result.get(
                "message",
                ""
            )
        ]
    ]

    table = Table(
        mrz_data,
        colWidths=[55 * mm, 115 * mm]
    )

    table.setStyle(
        TableStyle([
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.HexColor("#eeeeee")
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                9
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                6
            )
        ])
    )

    story.append(table)

    # =====================================================
    # 4. DOCUMENT VALIDATION
    # =====================================================

    story.append(
        Paragraph(
            "4. DOCUMENT VALIDATION",
            section_style
        )
    )

    validation_data = [
        [
            "Risk Score",
            str(
                validation_result.get(
                    "risk_score",
                    0
                )
            )
        ],

        [
            "Risk Level",
            validation_result.get(
                "risk_level",
                "UNKNOWN"
            )
        ]
    ]

    for check in validation_result.get(
        "checks",
        []
    ):

        validation_data.append([
            check.get(
                "check",
                ""
            ),

            (
                f'{check.get("status", "")} - '
                f'{check.get("message", "")}'
            )
        ])

    table = Table(
        validation_data,
        colWidths=[55 * mm, 115 * mm]
    )

    table.setStyle(
        TableStyle([
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "BACKGROUND",
                (0, 0),
                (0, 1),
                colors.HexColor("#eeeeee")
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                8
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                5
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                5
            )
        ])
    )

    story.append(table)

    # =====================================================
    # 5. REGISTRY VERIFICATION
    # =====================================================

    story.append(
        Paragraph(
            "5. REGISTRY VERIFICATION",
            section_style
        )
    )

    registry_data = [
        [
            "Status",
            registry_result.get(
                "status",
                "UNKNOWN"
            )
        ],

        [
            "Message",
            registry_result.get(
                "message",
                ""
            )
        ]
    ]

    if registry_result.get("mismatches"):

        registry_data.append([
            "Mismatched Fields",

            ", ".join(
                registry_result.get(
                    "mismatches",
                    []
                )
            )
        ])

    table = Table(
        registry_data,
        colWidths=[55 * mm, 115 * mm]
    )

    table.setStyle(
        TableStyle([
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.HexColor("#eeeeee")
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                9
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                6
            )
        ])
    )

    story.append(table)

    # =====================================================
    # 6. FORENSIC ANALYSIS
    # =====================================================

    story.append(
        Paragraph(
            "6. FORENSIC ANALYSIS",
            section_style
        )
    )

    forensic_data = [
        [
            "Analysis",
            "Status",
            "Score"
        ],

        [
            "Tampering",

            tampering_result.get(
                "status",
                "UNKNOWN"
            ),

            str(
                tampering_result.get(
                    "score",
                    0
                )
            )
        ],

        [
            "Face Verification",

            face_result.get(
                "status",
                "UNKNOWN"
            ),

            f'{face_result.get("score", 0)}%'
        ]
    ]

    table = Table(
        forensic_data,
        colWidths=[
            60 * mm,
            55 * mm,
            55 * mm
        ]
    )

    table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#222222")
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                9
            ),
            (
                "ALIGN",
                (2, 1),
                (2, -1),
                "CENTER"
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                6
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                6
            )
        ])
    )

    story.append(table)

    # =====================================================
    # 7. FINAL SCREENING RISK
    # =====================================================

    story.append(
        Paragraph(
            "7. FINAL SCREENING RISK",
            section_style
        )
    )

    risk_data = [
        [
            "Risk Score",
            f'{risk_result.get("score", 0)} / 100'
        ],

        [
            "Risk Level",
            risk_result.get(
                "level",
                "UNKNOWN"
            )
        ],

        [
            "Active Risk Factors",
            str(
                risk_result.get(
                    "active_factors",
                    0
                )
            )
        ],

        [
            "Recommendation",
            risk_result.get(
                "recommendation",
                ""
            )
        ]
    ]

    table = Table(
        risk_data,
        colWidths=[55 * mm, 115 * mm]
    )

    table.setStyle(
        TableStyle([
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.HexColor("#eeeeee")
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                9
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            ),
            (
                "TOPPADDING",
                (0, 0),
                (-1, -1),
                7
            ),
            (
                "BOTTOMPADDING",
                (0, 0),
                (-1, -1),
                7
            )
        ])
    )

    story.append(table)

    story.append(Spacer(1, 15))

    # =====================================================
    # OPERATIONAL NOTICE
    # =====================================================

    story.append(
        Paragraph(
            "Operational Notice: This report is generated by an "
            "AI-assisted document screening prototype. Results are "
            "preliminary screening indicators and should not be treated "
            "as definitive proof of identity fraud or document forgery. "
            "Manual verification is recommended for flagged cases.",
            small_style
        )
    )

    # BUILD PDF
    document.build(story)

    return pdf_path, report_id