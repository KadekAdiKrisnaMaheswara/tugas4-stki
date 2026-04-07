from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def lsi_search(query, documents):
    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(documents)

    svd = TruncatedSVD(n_components=2)
    lsi_matrix = svd.fit_transform(tfidf_matrix)

    query_vec = vectorizer.transform([query])
    query_lsi = svd.transform(query_vec)

    similarity = cosine_similarity(query_lsi, lsi_matrix)

    best_index = np.argmax(similarity)

    return tfidf_matrix.toarray(), lsi_matrix, query_lsi, similarity, best_index