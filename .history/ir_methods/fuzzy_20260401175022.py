import re

from rapidfuzz import fuzz

def clean

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