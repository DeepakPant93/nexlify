import logging
from fastapi import UploadFile
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
import io
import os

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
    try:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as e:
        logging.exception("PDF extraction failed")
        raise


def extract_text_from_html(html_bytes: bytes) -> str:
    try:
        soup = BeautifulSoup(html_bytes, "html.parser")
        return soup.get_text(separator="\n", strip=True)
    except Exception as e:
        logging.exception("HTML extraction failed")
        raise
