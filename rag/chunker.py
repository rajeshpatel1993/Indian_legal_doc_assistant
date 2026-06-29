import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils.helpers import extract_main_topic, extract_article_numbers

def create_chunks(cleaned_text):
    """
    Create chunks from the cleaned text using RecursiveCharacterTextSplitter.

    Args:
        cleaned_text (str): The cleaned text to be split into chunks.

    Returns:
        list: A list of text chunks.
    """

    chunks = []
    MIN_WORD = 40

    #Get Main Topic
    main_topic = extract_main_topic(cleaned_text)

    # Split before:
    # 1. Right to Equality
    # 2. Right to Freedom
    pattern = r'(?=\n\d+\.\s+)'

    sections = re.split(pattern, cleaned_text)

    sections = [section.strip() for section in sections if section.strip()]

    for section in sections:
        # Skip introductory text
        if not re.match(r'^\d+\.\s+', section):
            continue
        heading = section.split("\n")[0].strip()

        #Remove
        # 1
        # 2
        sub_topic = re.sub(r'^\d+\.\s+', '', heading).strip()

        #Extract :
        # Article 14-18
        article_match = re.search(r'Article\s+(\d+(-\d+)?)', heading, re.IGNORECASE)

        articles = (article_match.group(1) if article_match else "")

        #final chunk text
        chunk_text = (f"{main_topic}\n\n"
                      f"{section}"
                      )
        
        word_count = len(chunk_text.split())
        if word_count < MIN_WORD:
            continue  # Skip this chunk if it has fewer than MIN_WORD words

        #Small chunk
        if len(chunk_text) < 1200:
            chunks.append({
                "main_topic": main_topic,
                "sub_topic": sub_topic,
                "articles": extract_article_numbers(articles),
                "text": chunk_text
            })
        else:
            # Split into smaller chunks
            smaller_chunks = get_text_chunks(chunk_text)
            for idx, chunk in enumerate(smaller_chunks):
                chunks.append({
                    "main_topic": main_topic,
                    "sub_topic": sub_topic,
                    "articles": extract_article_numbers(articles),
                    "chunk_index": idx ,
                    "text": chunk
                })

    return chunks
    

def get_text_chunks(text, chunk_size=1200, chunk_overlap=200):
    """
    Split the text into chunks using RecursiveCharacterTextSplitter.

    Args:
        text (str): The text to be split.
        chunk_size (int): The maximum size of each chunk.
        chunk_overlap (int): The number of overlapping characters between chunks.

    Returns:
        list: A list of text chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ". ", " ",""]
    )
    return text_splitter.split_text(text)