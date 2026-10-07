import cv2


def verify_faces(document_image, selfie_image):

    try:
        # Load images
        document = cv2.imread(document_image)
        selfie = cv2.imread(selfie_image)

        if document is None or selfie is None:
            return {
                "status": "ERROR",
                "score": 0,
                "message": "Unable to read one or both images."
            }

        # Convert to grayscale
        document_gray = cv2.cvtColor(document, cv2.COLOR_BGR2GRAY)
        selfie_gray = cv2.cvtColor(selfie, cv2.COLOR_BGR2GRAY)

        # Load OpenCV face detector
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades +
            "haarcascade_frontalface_default.xml"
        )

        # Detect faces
        document_faces = face_cascade.detectMultiScale(
            document_gray,
            scaleFactor=1.1,
            minNeighbors=5
        )

        selfie_faces = face_cascade.detectMultiScale(
            selfie_gray,
            scaleFactor=1.1,
            minNeighbors=5
        )

        # Check whether faces were detected
        if len(document_faces) == 0:
            return {
                "status": "NO FACE",
                "score": 0,
                "message": "No face detected in the document image."
            }

        if len(selfie_faces) == 0:
            return {
                "status": "NO FACE",
                "score": 0,
                "message": "No face detected in the selfie."
            }

        # Prototype comparison based on detected face regions
        document_face = document_gray[
            document_faces[0][1]:
            document_faces[0][1] + document_faces[0][3],
            document_faces[0][0]:
            document_faces[0][0] + document_faces[0][2]
        ]

        selfie_face = selfie_gray[
            selfie_faces[0][1]:
            selfie_faces[0][1] + selfie_faces[0][3],
            selfie_faces[0][0]:
            selfie_faces[0][0] + selfie_faces[0][2]
        ]

        # Resize faces to same dimensions
        document_face = cv2.resize(document_face, (100, 100))
        selfie_face = cv2.resize(selfie_face, (100, 100))

        # Calculate similarity
        difference = cv2.absdiff(document_face, selfie_face)
        mean_difference = difference.mean()

        similarity = max(0, 100 - (mean_difference / 255 * 100))

        similarity = round(similarity, 2)

        if similarity >= 70:
            status = "MATCH"
            message = "Face appears similar to the document photograph."
        else:
            status = "MISMATCH"
            message = "Face does not appear sufficiently similar."

        return {
            "status": status,
            "score": similarity,
            "message": message
        }

    except Exception as e:

        return {
            "status": "ERROR",
            "score": 0,
            "message": str(e)
        }