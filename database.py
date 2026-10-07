import sqlite3

DATABASE = "screening_history.db"


def init_database():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS screenings (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            screening_id TEXT,
            date_time TEXT,

            document_name TEXT,
            document_type TEXT,
            document_number TEXT,
            person_name TEXT,

            ocr_confidence REAL,

            risk_score INTEGER,
            risk_level TEXT,

            registry_status TEXT,
            tampering_status TEXT,
            face_status TEXT,

            report_filename TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_screening(
    screening_id,
    date_time,
    document_name,
    document_type,
    document_number,
    person_name,
    ocr_confidence,
    risk_score,
    risk_level,
    registry_status,
    tampering_status,
    face_status,
    report_filename
):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO screenings (

            screening_id,
            date_time,
            document_name,
            document_type,
            document_number,
            person_name,
            ocr_confidence,
            risk_score,
            risk_level,
            registry_status,
            tampering_status,
            face_status,
            report_filename

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        screening_id,
        date_time,
        document_name,
        document_type,
        document_number,
        person_name,
        ocr_confidence,
        risk_score,
        risk_level,
        registry_status,
        tampering_status,
        face_status,
        report_filename
    ))

    conn.commit()
    conn.close()


def get_screenings():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM screenings
        ORDER BY id DESC
    """)

    screenings = cursor.fetchall()

    conn.close()

    return screenings


def get_screening_statistics():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM screenings")
    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM screenings
        WHERE risk_level = 'LOW'
    """)
    low = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM screenings
        WHERE risk_level = 'HIGH'
    """)
    high = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*)
        FROM screenings
        WHERE risk_level = 'MEDIUM'
    """)
    medium = cursor.fetchone()[0]

    conn.close()

    return {
        "total": total,
        "low": low,
        "medium": medium,
        "high": high
    }