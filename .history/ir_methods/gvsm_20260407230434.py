from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def gvsm_search(query, documents):
    vectorizer = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 2),
        sublinear_tf=True,
        norm='l2'
    )

    tfidf_matrix = vectorizer.fit_transform(documents)
    query_vec = vectorizer.transform([query])

    similarity = cosine_similarity(query_vec, tfidf_matrix).flatten()

    # 🔥 ranking hasil
    results = list(zip(documents, similarity))
    results = sorted(results, key=lambda x: x[1], reverse=True)

    return results