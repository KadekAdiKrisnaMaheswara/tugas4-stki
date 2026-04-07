from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def gvsm_search(query, documents):
    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(documents)
    query_vec = vectorizer.transform([query])

    similarity = cosine_similarity(query_vec, tfidf_matrix)

    best_index = np.argmax(similarity)

    return tfidf_matrix.toarray(), query_vec.toarray(), similarity, best_index