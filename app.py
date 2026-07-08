import streamlit as st
import requests

# ==========================
# KONFIGURASI HALAMAN
# ==========================

st.set_page_config(
    page_title="Breast Cancer Prediction",
    page_icon="🩺",
    layout="wide"
)

# ==========================
# CSS
# ==========================

st.markdown("""
<style>

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

h1{
    color:#1B365D;
    font-weight:700;
}

.stButton>button{
    width:100%;
    background:#1976D2;
    color:white;
    border-radius:10px;
    height:50px;
    font-size:18px;
    font-weight:bold;
    border:none;
}

.stButton>button:hover{
    background:#125DA6;
}

div[data-testid="stMetric"]{
    background:#F5F9FC;
    border-radius:12px;
    padding:15px;
}

</style>
""", unsafe_allow_html=True)

# ==========================
# SIDEBAR
# ==========================

with st.sidebar:

    st.title("🏥 SIPKOL")

    st.markdown("---")

    st.write("""
### Clinical Decision Support System

Aplikasi ini menggunakan metode

**Support Vector Machine (SVM)**

untuk memprediksi kemungkinan kanker payudara berdasarkan 30 fitur klinis pasien.
""")

    st.markdown("---")

    st.success("Model Accuracy : 96%")

    st.info("""
Masukkan seluruh data pasien kemudian tekan tombol **Predict**.
""")

# ==========================
# HEADER
# ==========================

st.title("🩺 Breast Cancer Prediction")

st.caption("Artificial Intelligence Clinical Decision Support System")

st.divider()

# ==========================
# LAYOUT
# ==========================

left,right = st.columns([2,1])

# ==========================
# INPUT
# ==========================

feature_names = [
"Radius Mean",
"Texture Mean",
"Perimeter Mean",
"Area Mean",
"Smoothness Mean",
"Compactness Mean",
"Concavity Mean",
"Concave Points Mean",
"Symmetry Mean",
"Fractal Dimension Mean",

"Radius SE",
"Texture SE",
"Perimeter SE",
"Area SE",
"Smoothness SE",
"Compactness SE",
"Concavity SE",
"Concave Points SE",
"Symmetry SE",
"Fractal Dimension SE",

"Worst Radius",
"Worst Texture",
"Worst Perimeter",
"Worst Area",
"Worst Smoothness",
"Worst Compactness",
"Worst Concavity",
"Worst Concave Points",
"Worst Symmetry",
"Worst Fractal Dimension"
]

inputs=[]

with left:

    with st.container(border=True):

        st.subheader("📋 Patient Clinical Features")

        for feature in feature_names:

            value = st.number_input(
                feature,
                value=0.0,
                format="%.4f"
            )

            inputs.append(value)

# ==========================
# HASIL
# ==========================

with right:

    with st.container(border=True):

        st.subheader("📊 Prediction Result")

        st.write("Klik tombol berikut untuk melakukan prediksi.")

        predict = st.button(
            "🔍 Predict",
            use_container_width=True
        )

# ==========================
# PREDIKSI
# ==========================

if predict:

    API_URL = "https://sipkolbreastcancer-va8q8xpl.b4a.run//predict"

    try:

        response = requests.post(
            API_URL,
            json={
                "features":inputs
            }
        )

        hasil = response.json()

        prediction = hasil["prediction"]

        probability = hasil["probability"]

        st.divider()

        col1,col2 = st.columns(2)

        with col1:

            st.metric(
                "Prediction Probability",
                f"{probability:.2%}"
            )

            st.progress(probability)

        with col2:

            if prediction.lower()=="malignant":

                st.error("🔴 Malignant")

            else:

                st.success("🟢 Benign")

    except Exception as e:

        st.error("Tidak dapat terhubung ke API.")

        st.exception(e)
