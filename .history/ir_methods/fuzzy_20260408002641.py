import re
from rapidfuzz import fuzz

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

def tokenize(text):
    return clean_text(text).split()

def fuzzy_search(query, documents):
    query_clean = clean_text(query)
    query_tokens = set(tokenize(query))

    results = []

    for doc in documents:
        doc_clean = clean_text(doc)
        doc_tokens = set(doc_clean.split())

        if len(doc_tokens) < 3:
            continue

        # 🔥 multi scoring
        score_sort = fuzz.token_sort_ratio(query_clean, doc_clean)
        score_set = fuzz.token_set_ratio(query_clean, doc_clean)
        score_partial = fuzz.partial_ratio(query_clean, doc_clean)

        # 🔥 gabungan skor
        score = (0.4 * score_sort) + (0.4 * score_set) + (0.2 * score_partial)

        # 🔥 keyword overlap (biar ga cuma mirip string)
        overlap = len(query_tokens & doc_tokens)
        score += overlap * 3

        # 🔥 penalti kalau terlalu beda
        if overlap == 0:
            score *= 0.7

        results.append((doc, score))

    return sorted(results, key=lambda x: x[1], reverse=True)