import streamlit as st

from utils.pdf_ocr import extract_text_from_pdf
from ir_methods.fuzzy import fuzzy_search
from ir_methods.gvsm import gvsm_search
from ir_methods.lsi import lsi_search

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
        results = fuzzy_search(query, documents)
    st.subheader("Hasil Pencarian (Fuzzy):")

for i, (doc, score) in enumerate(results[:5]):  # ambil top 5
    st.write(f"### Rank {i+1}")
    st.write(f"Score: {score}%")
    st.write(doc)

    if score > 70:
        st.success("Relevan Tinggi")
    elif score > 40:
        st.warning("Relevan Sedang")
    else:
        st.error("Kurang Relevan")

    st.write("---")

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