import re

from rapidfuzz import fuzz

def expand_query(query):
    if "otoritas jasa keuangan" in query.lower():
        return query + " ojk"
    return query

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

def fuzzy_search(query, documents):
    results = []

    for doc in documents:

        if len(doc.split()) < 3:
            continue

        score = (
        0.5 * fuzz.token_set_ratio(clean_text(query), clean_text(doc)) +
        0.5 * fuzz.partial_ratio(clean_text(query), clean_text(doc))
    )

        results.append((doc, score))

    # urutkan dari tertinggi
    results = sorted(results, key=lambda x: x[1], reverse=True)

    return results