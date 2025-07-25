import logging
import tempfile
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
    Extract text from PDF bytes, including OCR for image-based pages.
    """
    with tempfile.TemporaryDirectory() as path:
        pdf_path = os.path.join(path, "temp.pdf")
        with open(pdf_path, "wb") as f:
            f.write(pdf_bytes)

        reader = PdfReader(pdf_path)
        text_pages = []
        for page in reader.pages:
            text = page.extract_text()
            if text and text.strip():
                text_pages.append(text)
            else:
                # OCR fallback for image-based pages
                images = convert_from_path(pdf_path, first_page=reader.pages.index(
                    page)+1, last_page=reader.pages.index(page)+1)
                for img in images:
                    text_pages.append(pytesseract.image_to_string(img))

        return "\n".join(text_pages)


def extract_text_from_html(html_bytes: bytes) -> str:
    try:
        soup = BeautifulSoup(html_bytes, "html.parser")
        return soup.get_text(separator="\n", strip=True)
    except Exception as e:
        logging.exception("HTML extraction failed")
        raise
