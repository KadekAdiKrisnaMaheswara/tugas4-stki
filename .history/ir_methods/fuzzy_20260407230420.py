import re
from rapidfuzz import fuzz

def expand_query(query):
    q = query.lower()

    expansions = {
        "otoritas jasa keuangan": ["ojk", "lembaga keuangan"],
        "bank": ["perbankan", "financial institution"],
    }

    for key, vals in expansions.items():
        if key in q:
            q += " " + " ".join(vals)

    return q

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

def fuzzy_search(query, documents):
    query = expand_query(query)
    query_clean = clean_text(query)

    results = []

    for doc in documents:
        doc_clean = clean_text(doc)

        if len(doc_clean.split()) < 3:
            continue

        # 🔥 multi scoring
        score1 = fuzz.token_sort_ratio(query_clean, doc_clean)
        score2 = fuzz.partial_ratio(query_clean, doc_clean)
        score3 = fuzz.token_set_ratio(query_clean, doc_clean)

        # 🔥 weighted score
        final_score = (0.4 * score1) + (0.3 * score2) + (0.3 * score3)

        # 🔥 keyword overlap bonus
        overlap = len(set(query_clean.split()) & set(doc_clean.split()))
        final_score += overlap * 2

        results.append((doc, final_score))

    return sorted(results, key=lambda x: x[1], reverse=True)