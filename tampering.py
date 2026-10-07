from PIL import Image, ImageChops, ImageEnhance
import os


def detect_tampering(image_path):

    try:
        # Open original image
        original = Image.open(image_path).convert("RGB")

        # Create temporary JPEG copy
        temp_path = "uploads/ela_temp.jpg"
        original.save(temp_path, "JPEG", quality=90)

        # Open compressed image
        compressed = Image.open(temp_path).convert("RGB")

        # Compare original and compressed image
        difference = ImageChops.difference(original, compressed)

        # Enhance differences
        enhanced = ImageEnhance.Brightness(difference).enhance(10)

        # Calculate average difference
        pixels = list(enhanced.getdata())

        total_difference = 0

        for pixel in pixels:
            total_difference += sum(pixel) / 3

        average_difference = total_difference / len(pixels)

        # Remove temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)

        # Determine risk
        if average_difference < 10:
            status = "LOW"
            message = "No significant compression anomalies detected."
        elif average_difference < 25:
            status = "MEDIUM"
            message = "Some compression anomalies were detected."
        else:
            status = "HIGH"
            message = "Significant compression anomalies were detected."

        return {
            "status": status,
            "score": round(average_difference, 2),
            "message": message
        }

    except Exception as e:

        return {
            "status": "ERROR",
            "score": 0,
            "message": str(e)
        }