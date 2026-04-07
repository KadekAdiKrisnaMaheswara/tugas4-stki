import pytesseract
from pdf2image import convert_from_bytes
from PyPDF2 import PdfReader

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_pdf(file):
    text = ""

    try:
        reader = PdfReader(file)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()
    except:
        pass

    if text.strip() == "":
        images = convert_from_bytes(file.read())
        for img in images:
            img = img.convert("RGB")
            text += pytesseract.image_to_string(img)

    return text