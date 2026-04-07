import pytesseract
from PIL import Image

# set path (kalau perlu)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

img = Image.open("KTP.jpg")
text = pytesseract.image_to_string(img)

print(text)