import streamlit as st
import fitz
from rag.ingestor import extract_text_from_pdf

st.set_page_config(page_title="PDF Text Extractor", page_icon="📄", layout="wide")
st.title("PDF Text Extractor 📄 using pymupdf")



pdf_file = st.file_uploader("Upload PDF file", type="pdf")

if pdf_file is not None:
    try:
        #Read Uploaded PDF bytes
        pdf_bytes = pdf_file.read()

        pages_text, full_text, page_count = extract_text_from_pdf(
            pdf_bytes
        )

        st.success(
            f"PDF '{pdf_file.name}' uploaded successfully!"
            )
        st.info(f"Total Pages: {page_count}")
        st.subheader("Page-wise Extracted Text")

        for page_num, page_text in pages_text:
            with st.expander(f"Page {page_num}"):
                st.text_area(
                    label=f"Extracted Text from Page {page_num}",
                    value=page_text,
                    height=200,
                    key=f"page_{page_num}_text",
                )

        st.subheader("Full Extracted Text")
        st.text_area(label="Full Extracted Text", value=full_text, height=500, key="full_text")


    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")



