import streamlit as st
from rag.ingestor import extract_text_from_pdf
from rag.cleaner import clean_text
from rag.cleaner import clean_document
from rag.chunker import create_chunks, get_text_chunks

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

        cleaned_pages = []

        # Extract text using the ingestor module
        result = extract_text_from_pdf(pdf_bytes)

        # for page in result["pages"]:
        #     print(repr(page["text"][:500]))

        result = clean_document(result)

        pages = result["pages"]

        
        full_text = result["full_text"]
        page_count = result["page_count"]

        # Success Message
        st.success(f"Successfully uploaded: {pdf_file.name}")
        st.info(f"Total Pages: {page_count}")

        final_chunks = create_chunks(cleaned_text=full_text,source=pdf_file.name,document_name = pdf_file.name.replace(".pdf",""))
        st.write(f"Total Chunks Created: {len(final_chunks)}")
        st.write("### Chunks Overview")
        for idx, chunk in enumerate(final_chunks):
            st.write(f"**Chunk {idx + 1}:**")
            st.write(f"chunk_id: {chunk['chunk_id']}")
            st.write(f"document_name: {chunk['document_name']}")
            st.write(f"source: {chunk['source']}")
            st.write(f"- Main Topic: {chunk['main_topic']}")
            st.write(f"- Sub Topic: {chunk['sub_topic']}")
            st.write(f"- Articles: {chunk['articles']}")
            st.text_area(
                label=f"Chunk {idx + 1} Text",
                value=chunk["text"],
                height=150,
                key=f"chunk_{idx + 1}"
            )


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


