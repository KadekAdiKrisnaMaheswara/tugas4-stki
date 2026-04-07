import streamlit as st
import re

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

# =========================
# 🔧 FUNGSI RELEVANSI
# =========================
def get_relevance_label(score, method):
    if method == "Fuzzy":
        if score > 60:
            return "Tinggi"
        elif score > 40:
            return "Sedang"
        else:
            return "Rendah"
    else:
        if score > 0.7:
            return "Tinggi"
        elif score > 0.4:
            return "Sedang"
        else:
            return "Rendah"


if uploaded_file and query:

    # =========================
    # 📄 EXTRACT PDF
    # =========================
    text = extract_text_from_pdf(uploaded_file)

    # =========================
    # ✂️ SPLIT DOKUMEN
    # =========================
    documents = re.split(r'\n+', text)
    documents = [doc.strip() for doc in documents if len(doc.strip()) > 20]

    st.subheader("Dokumen:")
    st.write("Jumlah dokumen:", len(documents))

    if len(documents) < 2:
        st.error("Dokumen terlalu sedikit untuk diproses!")
        st.stop()

    # =========================
    # 🔍 FUZZY
    # =========================
    if method == "Fuzzy":
        results = fuzzy_search(query, documents)

        st.subheader("Step: Hasil Similarity Semua Dokumen")

        show_all_similarity = st.checkbox("Tampilkan semua similarity dokumen")

        sim_results = results if show_all_similarity else results[:10]

        for i, (doc, score) in enumerate(sim_results):
            st.write(f"{score:.2f}% - {doc}")
            st.markdown("---")

        st.subheader("Step: Hasil Pencarian (Fuzzy)")

        for i, (doc, score) in enumerate(results[:10]):
            st.markdown(f"### 🔹 Rank {i+1}")
            st.write(f"**Score:** {score:.2f}%")
            st.write(f"**Relevansi:** {get_relevance_label(score, 'Fuzzy')}")
            st.info(doc)
            st.markdown("---")

        top_score = results[0][1]
        st.success(f"Kesimpulan: Dokumen paling relevan = {get_relevance_label(top_score, 'Fuzzy')}")

    # =========================
    # 🔍 GVSM
    # =========================
tfidf, qvec, sim, results = gvsm_search(query, documents)

st.subheader("Step 1: TF-IDF Matrix")
st.write(tfidf)

st.subheader("Step 2: Query Vector")
st.write(qvec)

st.subheader("Step 3: Cosine Similarity")
st.write(sim)

st.subheader("Step 4: Ranking")

for i, (doc, score) in enumerate(results[:5]):
    st.markdown(f"### 🔹 Rank {i+1}")
    st.write(f"**Score:** {score:.4f}")
    st.write(f"**Relevansi:** {get_relevance_label(score, 'GVSM')}")
    st.info(doc)
    st.markdown("---")

        top_score = results[0][1]
        st.success(f"Kesimpulan: Dokumen paling relevan = {get_relevance_label(top_score, 'GVSM')}")

    # =========================
    # 🔍 LSI
    # =========================
    elif method == "LSI":
        results = lsi_search(query, documents)

        st.subheader("Hasil Pencarian (LSI)")

        tfidf, qvec, sim, results = gvsm_search(query, documents)

        st.subheader("Step 1: TF-IDF Matrix")
        st.write(tfidf)

        st.subheader("Step 2: Query Vector")
        st.write(qvec)

        st.subheader("Step 3: Cosine Similarity")
        st.write(sim)

        st.subheader("Step 4: Ranking")

        for i, (doc, score) in enumerate(results[:5]):
            st.markdown(f"### 🔹 Rank {i+1}")
            st.write(f"**Score:** {score:.4f}")
            st.write(f"**Relevansi:** {get_relevance_label(score, 'LSI')}")
            st.info(doc)
            st.markdown("---")

        top_score = results[0][1]
        st.success(f"Kesimpulan: Dokumen paling relevan = {get_relevance_label(top_score, 'LSI')}")