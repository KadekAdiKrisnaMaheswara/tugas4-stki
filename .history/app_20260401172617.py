import streamlit as st

from utils.pdf_ocr import extract_text_from_pdf
from methods.fuzzy import fuzzy_search
from methods.gvsm import gvsm_search
from methods.lsi import lsi_search

st.title("Information Retrieval System")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")
query = st.text_input("Masukkan Query")

method = st.selectbox("Pilih Metode", [
    "Fuzzy",
    "GVSM",
    "LSI"
])

if uploaded_file and query:

    text = extract_text_from_pdf(uploaded_file)

    documents = text.split("\n")
    documents = [doc.strip() for doc in documents if doc.strip() != ""]

    st.subheader("Dokumen:")
    st.write(documents)

    if method == "Fuzzy":
        scores, idx = fuzzy_search(query, documents)

        st.write(scores)
        st.success(documents[idx])

    elif method == "GVSM":
        tfidf, qvec, sim, idx = gvsm_search(query, documents)

        st.write("TF-IDF:", tfidf)
        st.write("Query:", qvec)
        st.write("Similarity:", sim)

        st.success(documents[idx])

    elif method == "LSI":
        tfidf, lsi, qlsi, sim, idx = lsi_search(query, documents)

        st.write("TF-IDF:", tfidf)
        st.write("LSI:", lsi)
        st.write("Query LSI:", qlsi)
        st.write("Similarity:", sim)

        st.success(documents[idx])