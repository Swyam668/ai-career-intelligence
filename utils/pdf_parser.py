# import pdfplumber
# from io import BytesIO

import fitz  # PyMuPDF

# def extract_pdf_text(pdf_bytes):

#     text = ""

#     with pdfplumber.open(
#         BytesIO(pdf_bytes)
#     ) as pdf:

#         for page in pdf.pages:
#             text += page.extract_text() or ""

#     return text



def extract_pdf_text(pdf_bytes: bytes) -> str:
    text = ""

    with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
        for page in doc:
            text += page.get_text() + "\n"

    return text