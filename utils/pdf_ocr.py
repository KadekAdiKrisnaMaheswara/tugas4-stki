def extract_text_from_pdf(uploaded_file):
    import fitz  # PyMuPDF
    import pytesseract
    from PIL import Image
    import io

    text = ""

    pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    for page in pdf:
        # ambil text biasa
        page_text = page.get_text()

        if page_text.strip():
            text += page_text + "\n"
        else:
            # kalau kosong → OCR
            pix = page.get_pixmap()
            img = Image.open(io.BytesIO(pix.tobytes()))

            ocr_text = pytesseract.image_to_string(img)
            text += ocr_text + "\n"

    return text  # 🔥 WAJIB TEXT ASLI