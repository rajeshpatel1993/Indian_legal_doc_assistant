import streamlit as st
from rag.ingestor import extract_text_from_pdf


st.set_page_config(page_title="PDF Text Extractor", page_icon="📄", layout="wide")
st.title("⚖️ Indian Legal Document Assistant")
st.write("Upload a legal PDF document to extract its text.")


pdf_file = st.file_uploader("Upload PDF file", type=["pdf"])

# ---------------------------------------------------
# Process Uploaded PDF
# ---------------------------------------------------

if pdf_file is not None:
    try:
        #Read Uploaded PDF as bytes
        pdf_bytes = pdf_file.read()

        # Extract text using the ingestor module
        result = extract_text_from_pdf(pdf_bytes)

        pages = result["pages"]
        full_text = result["full_text"]
        page_count = result["page_count"]

        # Success Message
        st.success(f"Successfully uploaded: {pdf_file.name}")
        st.info(f"Total Pages: {page_count}")

        # ---------------------------------------------------
        # Page-wise Text
        # ---------------------------------------------------
        st.subheader("📄 Page-wise Extracted Text")

        for page in pages:
            with st.expander(f"Page {page['page']}"):
                st.text_area(
                    label=f"Page {page['page']}",
                    value=page["text"],
                    height=200,
                    key=f"page_{page['page']}"
                )
        
        # ---------------------------------------------------
        # Full Document Text
        # ---------------------------------------------------
        st.subheader("📚 Complete Document")
        st.text_area(
            label="Full Extracted Text",
            value=full_text,
            height=500,
            key="full_text"
        )
    except Exception as e:
        st.error(f"Error processing PDF: {str(e)}")


