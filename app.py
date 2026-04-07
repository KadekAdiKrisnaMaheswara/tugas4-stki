import streamlit as st
import re

from utils.pdf_ocr import extract_text_from_pdf
from ir_methods.fuzzy import fuzzy_search
from ir_methods.gvsm import gvsm_search
from ir_methods.lsi import lsi_search

st.set_page_config(page_title="IR System", layout="wide")

st.title("📚 Information Retrieval System")

# =========================
# 📥 INPUT
# =========================
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")

with col2:
    query = st.text_input("Masukkan Query")

method = st.selectbox("Pilih Metode", ["Fuzzy", "GVSM", "LSI"])

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


# =========================
# 🚀 PROSES
# =========================
if uploaded_file and query:

    # 📄 Extract PDF
    text = extract_text_from_pdf(uploaded_file)

    # ✂️ Split dokumen
    documents = re.split(r'\n+', text)
    documents = [doc.strip() for doc in documents if len(doc.strip()) > 20]

    st.divider()

    # 📊 Info dokumen
    colA, colB = st.columns(2)
    colA.metric("Jumlah Dokumen", len(documents))
    colB.metric("Query", query)

    if len(documents) < 2:
        st.error("Dokumen terlalu sedikit untuk diproses!")
        st.stop()

    # =========================
    # 🔍 FUZZY
    # =========================
    if method == "Fuzzy":

        results = fuzzy_search(query, documents)

        with st.expander("📊 Step 1: Semua Similarity"):
            show_all = st.checkbox("Tampilkan semua", key="fuzzy_all")

            sim_results = results if show_all else results[:10]

            for doc, score in sim_results:
                st.write(f"{score:.2f}% - {doc}")
                st.markdown("---")

        st.subheader("🏆 Ranking Hasil")

        for i, (doc, score) in enumerate(results[:5]):
            with st.container():
                st.markdown(f"### 🔹 Rank {i+1}")
                st.write(f"Score: {score:.2f}%")
                st.write(f"Relevansi: {get_relevance_label(score, 'Fuzzy')}")
                st.info(doc)

        top_score = results[0][1]
        st.success(f"Kesimpulan: {get_relevance_label(top_score, 'Fuzzy')}")

    # =========================
    # 🔍 GVSM
    # =========================
    elif method == "GVSM":

        tfidf, qvec, sim, results = gvsm_search(query, documents)

        with st.expander("📊 Step 1: TF-IDF Matrix"):
            st.write(tfidf)

        with st.expander("📊 Step 2: Query Vector"):
            st.write(qvec)

        with st.expander("📊 Step 3: Cosine Similarity"):
            st.write(sim)

        st.subheader("🏆 Ranking Hasil")

        for i, (doc, score) in enumerate(results[:5]):
            with st.container():
                st.markdown(f"### 🔹 Rank {i+1}")
                st.write(f"Score: {score:.4f}")
                st.write(f"Relevansi: {get_relevance_label(score, 'GVSM')}")
                st.info(doc)

        top_score = results[0][1]
        st.success(f"Kesimpulan: {get_relevance_label(top_score, 'GVSM')}")

    # =========================
    # 🔍 LSI
    # =========================
    elif method == "LSI":

        tfidf, lsi, qlsi, sim, results = lsi_search(query, documents)

        with st.expander("📊 Step 1: TF-IDF Matrix"):
            st.write(tfidf)

        with st.expander("📊 Step 2: LSI Matrix (SVD)"):
            st.write(lsi)

        with st.expander("📊 Step 3: Query LSI"):
            st.write(qlsi)

        with st.expander("📊 Step 4: Similarity"):
            st.write(sim)

        st.subheader("🏆 Ranking Hasil")

        for i, (doc, score) in enumerate(results[:5]):
            with st.container():
                st.markdown(f"### 🔹 Rank {i+1}")
                st.write(f"Score: {score:.4f}")
                st.write(f"Relevansi: {get_relevance_label(score, 'LSI')}")
                st.info(doc)

        top_score = results[0][1]
        st.success(f"Kesimpulan: {get_relevance_label(top_score, 'LSI')}")

else:
    st.info("Silakan upload PDF dan masukkan query terlebih dahulu.")