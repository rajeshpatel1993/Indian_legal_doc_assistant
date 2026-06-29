import re

def extract_main_topic(cleaned_text):
    lines = [
        line.strip()
        for line in cleaned_text.split("\n")
        if line.strip()
    ]

    for line in lines:
        # Matches:
        # I. FUNDAMENTAL RIGHTS...
        # II. DIRECTIVE PRINCIPLES...
        # III. UNION EXECUTIVE...
        if re.match(r'^[IVX]+\.\s+', line):
            return line

    return "Unknown Topic"

def extract_article_numbers(article_text):
    if not article_text:
        return []

    numbers = []

    ranges = re.findall(r"(\d+)\s*-\s*(\d+)", article_text)

    for start, end in ranges:
        numbers.extend(range(int(start), int(end) + 1))

    singles = re.findall(r"\b\d+\b", article_text)

    for n in singles:
        n = int(n)
        if n not in numbers:
            numbers.append(n)

    return sorted(numbers)