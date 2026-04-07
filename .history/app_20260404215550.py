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

        st.subheader("Hasil Pencarian (Fuzzy)")

        #toogle untuk menampilkan semua hasil
        show_all = st.checkbox("Tampilkan Semua Hasil")

        #tentukan batasan untuk menampilkan hasil
        if show_all
        st.subheader("Step: Hasil Similarity Semua Dokumen")

        for doc, score in results:
            st.write(f"{score:.2f}% - {doc}")

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
    elif method == "GVSM":
        tfidf, qvec, sim = gvsm_search(query, documents)

        st.subheader("Hasil Pencarian (GVSM)")

        st.subheader("Step 1: TF-IDF Matrix")
        st.write(tfidf)

        st.subheader("Step 2: Query Vector")
        st.write(qvec)

        st.subheader("Step 3: Cosine Similarity")
        st.write(sim)

        sorted_idx = sim.argsort()[::-1]
        top_n = min(5, len(sim))

        for rank, i in enumerate(sorted_idx[:top_n]):
            st.markdown(f"### 🔹 Rank {rank+1}")
            st.write(f"**Score:** {sim[i]:.4f}")
            st.write(f"**Relevansi:** {get_relevance_label(sim[i], 'GVSM')}")
            st.info(documents[i])
            st.markdown("---")

        top_score = sim[sorted_idx[0]]
        st.success(f"Kesimpulan: Dokumen paling relevan = {get_relevance_label(top_score, 'GVSM')}")

    # =========================
    # 🔍 LSI
    # =========================
    elif method == "LSI":
        tfidf, lsi, qlsi, sim = lsi_search(query, documents)

        st.subheader("Hasil Pencarian (LSI)")

        st.subheader("Step 1: TF-IDF Matrix")
        st.write(tfidf)

        st.subheader("Step 2: LSI Matrix (SVD)")
        st.write(lsi)

        st.subheader("Step 3: Query LSI")
        st.write(qlsi)

        st.subheader("Step 4: Similarity")
        st.write(sim)

        sorted_idx = sim.argsort()[::-1]
        top_n = min(5, len(sim))

        for rank, i in enumerate(sorted_idx[:top_n]):
            st.markdown(f"### 🔹 Rank {rank+1}")
            st.write(f"**Score:** {sim[i]:.4f}")
            st.write(f"**Relevansi:** {get_relevance_label(sim[i], 'LSI')}")
            st.info(documents[i])
            st.markdown("---")

        top_score = sim[sorted_idx[0]]
        st.success(f"Kesimpulan: Dokumen paling relevan = {get_relevance_label(top_score, 'LSI')}")