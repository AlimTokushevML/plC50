import os
import base64
import pickle
import subprocess

import streamlit as st
import pandas as pd
from PIL import Image

# =========================
# Descriptor Calculation
# =========================
def desc_calc():
    padel_cmd = [
        "java",
        "-Xms2G",
        "-Xmx2G",
        "-Djava.awt.headless=true",
        "-jar", "./PaDEL-Descriptor/PaDEL-Descriptor.jar",
        "-removesalt",
        "-standardizenitro",
        "-fingerprints",
        "-descriptortypes", "./PaDEL-Descriptor/PubchemFingerprinter.xml",
        "-dir", "./",
        "-file", "descriptors_output.csv"
    ]
    try:
        process = subprocess.Popen(padel_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        if process.returncode != 0:
            st.error("Descriptor calculation failed.")
            st.code(error.decode())
        else:
            if os.path.exists("molecule.smi"):
                os.remove("molecule.smi")
    except Exception as e:
        st.error(f"Error running PaDEL-Descriptor: {e}")

# =========================
# File Download Link
# =========================
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="prediction.csv">📥 Download Predictions</a>'
    return href

# =========================
# Load Model and Predict
# =========================
def build_model(input_data, molecule_names):
    model = pickle.load(open('acetylcholinesterase_model.pkl', 'rb'))
    prediction = model.predict(input_data)

    st.subheader('🔬 Prediction Results')
    prediction_output = pd.Series(prediction, name='pIC50')
    result_df = pd.concat([molecule_names, prediction_output], axis=1)
    st.write(result_df)
    st.markdown(filedownload(result_df), unsafe_allow_html=True)

# =========================
# UI Header
# =========================
st.markdown("""
# 🧪 Bioactivity Prediction App (Acetylcholinesterase)

This app predicts the bioactivity of molecules as inhibitors of the **Acetylcholinesterase** enzyme, a drug target for **Alzheimer's disease**.
""")

# =========================
# Session State Init
# =========================
if 'predict_clicked' not in st.session_state:
    st.session_state.predict_clicked = False
if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

# =========================
# Sidebar File Upload
# =========================
with st.sidebar.header('1. Upload Your Molecule File (.txt or .smi format)'):
    uploaded_file = st.sidebar.file_uploader("Upload input file", type=['txt', 'smi'])

# =========================
# Handle Button Click
# =========================
if st.sidebar.button('⚙️ Predict'):
    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file
        st.session_state.predict_clicked = True
    else:
        st.warning("Please upload a `.txt` or `.smi` file to begin.")
        st.session_state.predict_clicked = False

# =========================
# Main Prediction Logic
# =========================
if st.session_state.predict_clicked and st.session_state.uploaded_file is not None:
    uploaded_file = st.session_state.uploaded_file

    load_data = pd.read_table(uploaded_file, sep=' ', header=None)
    load_data.to_csv('molecule.smi', sep='\t', header=False, index=False)

    st.subheader('📂 Original Input Data')
    st.write(load_data)

    with st.spinner('Calculating molecular descriptors...'):
        desc_calc()

    st.subheader('🧬 Calculated Descriptors')
    desc = pd.read_csv('descriptors_output.csv')
    st.write(desc)
    st.write(f"Shape: {desc.shape}")

    st.subheader('🎯 Model Input Descriptors (Subset)')
    Xlist = list(pd.read_csv('descriptor_list.csv').columns)
    desc_subset = desc[Xlist]
    st.write(desc_subset)
    st.write(f"Shape: {desc_subset.shape}")

    molecule_names = pd.Series(load_data[1], name='Molecule Name')
    build_model(desc_subset, molecule_names)
