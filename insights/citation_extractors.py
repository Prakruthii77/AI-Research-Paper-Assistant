import re

def extract_citations(text):
    patterns = [
        r"\([A-Za-z\s]+,\s\d{4}\)",
        r"\(\w+\set al\.,\s\d{4}\)",
        r"\[\d+\]"
    ]

    citations = []
    for pattern in patterns:
        found = re.findall(pattern, text)
        citations.extend(found)

    return list(set(citations))