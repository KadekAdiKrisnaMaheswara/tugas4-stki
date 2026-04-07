import re

from rapidfuzz import fuzz

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

def fuzzy_search(query, documents):
    results = []

    for doc in documents:

        if len(doc.split()) < 3:
            continue

        score = fuzz.partial_ratio(query.lower(), doc.lower())
        results.append((doc, score))

    # urutkan dari tertinggi
    results = sorted(results, key=lambda x: x[1], reverse=True)

    return results