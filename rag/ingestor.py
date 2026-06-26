"""
ingestor.py

This module is responsible for reading PDF documents and extracting
text page-by-page using PyMuPDF.

Responsibilities:
- Open PDF from bytes
- Extract text from each page
- Return structured data for downstream RAG pipeline

"""
import fitz  # PyMuPDF
def extract_text_from_pdf(pdf_bytes):
    """
        Extract text from a PDF document.

        Args:
            pdf_bytes (bytes): The PDF file content in bytes.
        
        Returns:
        dict:
            {
                "pages": [
                    {
                        "page": 1,
                        "text": "Page 1 content..."
                    },
                    {
                        "page": 2,
                        "text": "Page 2 content..."
                    }
                ],
                "full_text": "...",
                "page_count": 10
            }
    """
    pdf_document = fitz.open(stream=pdf_bytes,filetype="pdf")
    pages = []
    full_text = []

    try:
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            page_text = page.get_text()
            pages.append({"page": page_num + 1, "text":page_text})
            full_text.append(f"\n\n--- Page {page_num + 1} ---\n\n{page_text}")
        return {
            "pages": pages,
            "full_text": "".join(full_text),
            "page_count": pdf_document.page_count
        }
    finally:
        pdf_document.close()
