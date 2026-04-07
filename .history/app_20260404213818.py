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

if uploaded_file and query:

    text = extract_text_from_pdf(uploaded_file)

    documents = re.split(r'\n+', text)
    documents = [doc.strip() for doc in documents if len(doc.strip()) > 20]

