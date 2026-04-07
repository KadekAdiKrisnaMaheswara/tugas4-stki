from rapidfuzz import fuzz
import numpy as np

def fuzzy_search(query, documents):
    scores = []
    for doc in documents:
        score = fuzz.ratio(query.lower(), doc.lower())
        scores.append(score)

    best_index = np.argmax(scores)

    return scores, best_index