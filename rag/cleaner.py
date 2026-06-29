import re


def clean_text(text):
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")
    text = text.replace("\u00A0", " ")
    text = text.replace("\x0c", "")


     # Remove page markers
    text = re.sub(r"---\s*Page\s*\d+\s*---", "", text)

    # Remove page numbers alone on a line
    text = re.sub(r"^\d+\s*$", "", text, flags=re.MULTILINE)

    # Remove journal header
    text = re.sub(
        r"International Journal of Law Management & Humanities",
        "",
        text
    )

    # Remove volume information
    text = re.sub(
        r"\[Vol\..*?\]",
        "",
        text
    )

    # Remove copyright line
    text = re.sub(
        r"©\s*\d{4}\..*",
        "",
        text
    )

    # Remove ISSN line
    text = re.sub(
        r"\[ISSN.*?\]",
        "",
        text
    )
    
    # Remove trailing spaces from each line
    text = re.sub(r"[ \t]+$", "", text, flags=re.MULTILINE)

    # Remove leading spaces from each line
    text = re.sub(r"^[ \t]+", "", text, flags=re.MULTILINE)

    # Collapse multiple spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Collapse blank lines containing spaces
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)


    return text.strip()


def clean_document(document):
    """
    Clean an entire document structure.

    Args:
        document (dict): Extracted document.

    Returns:
        dict: Cleaned document.
    """

    cleaned_pages = []

    for page in document["pages"]:
        cleaned_pages.append(
            {
                "page": page["page"],
                "text": clean_text(page["text"])
            }
        )

    return {
        "pages": cleaned_pages,
        "full_text": clean_text(document["full_text"]),
        "page_count": document["page_count"]
    }