from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity

def lsi_search(query, documents, n_components=100):
    vectorizer = TfidfVectorizer(
        stop_words='english',
        ngram_range=(1, 2),
        sublinear_tf=True
    )

    tfidf_matrix = vectorizer.fit_transform(documents)

    n_components = min(n_components, tfidf_matrix.shape[1] - 1)

    svd = TruncatedSVD(n_components=n_components)
    lsi_matrix = svd.fit_transform(tfidf_matrix)

    query_vec = vectorizer.transform([query])
    query_lsi = svd.transform(query_vec)

    similarity = cosine_similarity(query_lsi, lsi_matrix).flatten()

    results = list(zip(documents, similarity))
    results = sorted(results, key=lambda x: x[1], reverse=True)

    # 🔥 return lengkap
    return tfidf_matrix.toarray(), lsi_matrix, query_lsi, similarity, results