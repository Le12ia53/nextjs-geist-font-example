from google.cloud import vision
import pytesseract
from PIL import Image
import io

def hybrid_ocr(image_bytes: bytes) -> str:
    """
    Perform hybrid OCR using Google Vision API and Tesseract as fallback.
    Returns extracted text.
    """
    # Google Vision OCR
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_bytes)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    if response.error.message:
        # If Google Vision fails, fallback to Tesseract
        return tesseract_ocr(image_bytes)
    if texts:
        return texts[0].description
    else:
        return tesseract_ocr(image_bytes)

def tesseract_ocr(image_bytes: bytes) -> str:
    """
    Perform OCR using Tesseract.
    """
    image = Image.open(io.BytesIO(image_bytes))
    text = pytesseract.image_to_string(image, lang='por')
    return text
