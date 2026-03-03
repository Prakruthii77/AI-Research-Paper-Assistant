def split_sections(text):
    text_lower = text.lower()
    sections = {}

    headers = [
        "abstract",
        "introduction",
        "methodology",
        "methods",
        "results",
        "discussion",
        "conclusion",
        "limitations"
    ]

    for header in headers:
        if header in text_lower:
            parts = text_lower.split(header)
            if len(parts) > 1:
                extracted = parts[1][:3000]
                sections[header] = extracted

    return sections