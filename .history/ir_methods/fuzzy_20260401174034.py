from rapidfuzz import fuzz

def fuzzy_search(query, documents):
    results = []

    for doc in documents:
        score = fuzz.ratio(query.lower(), doc.lower())
        results.append((doc, score))

    # urutkan dari tertinggi
    results = sorted(results, key=lambda x: x[1], reverse=True)

    return results