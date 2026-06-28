import re


def clean_text(text):
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")
    text = text.replace("\u00A0", " ")
    text = text.replace("\x0c", "")

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