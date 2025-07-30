import logging
import tempfile
from typing import List
from fastapi import UploadFile
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
import io
import os
from pdf2image import convert_from_path
import pytesseract

SUPPORTED_EXTENSIONS = [".pdf", ".html", ".htm", ".txt"]


async def extract_text_from_file(file: UploadFile) -> str:
    filename = file.filename
    extension = os.path.splitext(filename)[1].lower()

    try:
        content = await file.read()

        if extension == ".pdf":
            return extract_text_from_pdf(content)

        elif extension in [".html", ".htm"]:
            return extract_text_from_html(content)

        elif extension == ".txt":
            return content.decode("utf-8", errors="ignore")

        else:
            raise ValueError(f"Unsupported file extension: {extension}")

    except Exception as e:
        logging.exception("Failed to extract text from file")
        raise


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extract text from PDF bytes, with OCR fallback for image-based pages.
    """
    with tempfile.TemporaryDirectory() as path:
        pdf_path = os.path.join(path, "temp.pdf")
        with open(pdf_path, "wb") as f:
            f.write(pdf_bytes)

        reader = PdfReader(pdf_path)
        text_pages: List[str] = []

        for page_number, page in enumerate(reader.pages, start=1):
            try:
                text = page.extract_text()
                if text and text.strip():
                    text_pages.append(text)
                else:
                    # OCR fallback for image-based page
                    images = convert_from_path(
                        pdf_path, first_page=page_number, last_page=page_number)
                    for img in images:
                        ocr_text = pytesseract.image_to_string(img)
                        if ocr_text.strip():
                            text_pages.append(ocr_text)
            except Exception as e:
                text_pages.append(
                    f"[Error processing page {page_number}]: {e}")

        return "\n\n".join(text_pages)

def extract_text_from_html(html_bytes: bytes) -> str:
    try:
        soup = BeautifulSoup(html_bytes, "html.parser")
        return soup.get_text(separator="\n", strip=True)
    except Exception as e:
        logging.exception("HTML extraction failed")
        raise
