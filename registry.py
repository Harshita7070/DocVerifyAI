# Simulated document registry
# This is for prototype/demo purposes only.

DOCUMENT_REGISTRY = {

    "DOC1234567": {
        "name": "RAHUL SHARMA",
        "date_of_birth": "12/05/2004",
        "nationality": "INDIAN",
        "status": "ACTIVE"
    },

    "DOC9876543": {
        "name": "PRIYA PATIL",
        "date_of_birth": "20/08/2003",
        "nationality": "INDIAN",
        "status": "ACTIVE"
    },

    "DOC5555555": {
        "name": "AMIT KUMAR",
        "date_of_birth": "15/01/2002",
        "nationality": "INDIAN",
        "status": "BLACKLISTED"
    }
}


def check_registry(fields):

    document_number = fields["document_number"]

    # Document number not detected
    if document_number == "Not Found":
        return {
            "status": "NOT VERIFIED",
            "message": "Document number was not detected.",
            "record": None
        }

    # Search simulated registry
    record = DOCUMENT_REGISTRY.get(document_number.upper())

    # Document not found
    if record is None:
        return {
            "status": "NOT FOUND",
            "message": "Document number was not found in the registry.",
            "record": None
        }

    # Document found
    if record["status"] == "BLACKLISTED":
        return {
            "status": "BLACKLISTED",
            "message": "Document is present in the registry but is blacklisted.",
            "record": record
        }

    # Compare extracted information
    mismatches = []

    if fields["name"].upper() != record["name"]:
        mismatches.append("Name")

    if fields["date_of_birth"] != record["date_of_birth"]:
        mismatches.append("Date of Birth")

    if fields["nationality"].upper() != record["nationality"]:
        mismatches.append("Nationality")

    if mismatches:
        return {
            "status": "MISMATCH",
            "message": "Registry record found, but some details do not match.",
            "record": record,
            "mismatches": mismatches
        }

    return {
        "status": "VERIFIED",
        "message": "Document details match the registry record.",
        "record": record,
        "mismatches": []
    }