import streamlit as st      # Library untuk membuat aplikasi web interaktif
import requests             # Library untuk mengirim HTTP request ke API

# =====================================
# KONFIGURASI HALAMAN
# =====================================

st.set_page_config(
    page_title="Breast Cancer Prediction",   # Judul halaman pada browser
    page_icon="🩺",                           # Ikon halaman
    layout="wide"                            # Menggunakan tampilan layar penuh
)

# URL endpoint API FastAPI yang digunakan untuk prediksi
API_URL = "https://sipkolbreastcancer-va8q8xpl.b4a.run/predict"

# Membuat session HTTP agar koneksi ke API dapat digunakan kembali
session = requests.Session()

# =====================================
# CSS
# =====================================

st.markdown("""
<style>

.block-container{
    padding-top:2rem;       /* Memberikan jarak bagian atas halaman */
    padding-bottom:2rem;    /* Memberikan jarak bagian bawah halaman */
}

h1{
    color:#1B365D;          /* Warna judul */
    font-weight:700;        /* Ketebalan huruf */
}

.stButton>button{
    width:100%;             /* Tombol memenuhi lebar container */
    background:#1976D2;     /* Warna tombol */
    color:white;            /* Warna teks */
    border-radius:10px;     /* Membuat sudut tombol melengkung */
    height:50px;            /* Tinggi tombol */
    font-size:18px;         /* Ukuran font */
    font-weight:bold;       /* Font tebal */
    border:none;            /* Menghilangkan border */
}

.stButton>button:hover{
    background:#125DA6;     /* Warna tombol ketika diarahkan mouse */
}

div[data-testid="stMetric"]{
    background:#F5F9FC;     /* Warna latar metric */
    border-radius:12px;     /* Sudut melengkung */
    padding:15px;           /* Jarak isi metric */
}

</style>
""", unsafe_allow_html=True)   # Mengizinkan HTML/CSS dijalankan

# =====================================
# SIDEBAR
# =====================================

with st.sidebar:                    # Membuat sidebar

    st.title("🏥 Hospital")           # Judul sidebar

    st.markdown("---")              # Garis pemisah

    st.write("""
### Clinical Decision Support System

Aplikasi ini menggunakan metode

**Support Vector Machine (SVM)**

untuk memprediksi kemungkinan kanker payudara berdasarkan 30 fitur klinis pasien.
""")

    st.markdown("---")

    st.success("Model Accuracy : 96%")     # Menampilkan informasi akurasi model

    st.info("Masukkan seluruh data pasien kemudian klik **Predict**.")  # Petunjuk penggunaan

# =====================================
# HEADER
# =====================================

st.title("🩺 Breast Cancer Prediction")   # Judul utama aplikasi

st.caption("Artificial Intelligence Clinical Decision Support System")   # Subjudul

st.divider()                              # Garis pembatas

# =====================================
# DAFTAR FITUR
# =====================================

feature_names = [

# Daftar 30 fitur yang digunakan sebagai input model SVM

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

# Membagi halaman menjadi dua kolom
left, right = st.columns([2,1])

# =====================================
# FORM INPUT
# =====================================

with left:                               # Kolom kiri untuk input

    with st.form("prediction_form"):     # Form agar aplikasi tidak rerun setiap input berubah

        with st.container(border=True):  # Membuat container dengan border

            st.subheader("📋 Patient Clinical Features")

            inputs = []                  # Menyimpan seluruh nilai input

            for feature in feature_names:      # Melakukan perulangan sebanyak 30 fitur

                value = st.number_input(       # Membuat input angka
                    feature,
                    value=0.0,
                    format="%.4f"
                )

                inputs.append(value)           # Menambahkan nilai ke dalam list

        predict = st.form_submit_button(       # Tombol submit form
            "🔍 Predict",
            use_container_width=True
        )

# =====================================
# HASIL PREDIKSI
# =====================================

with right:                            # Kolom kanan

    with st.container(border=True):

        st.subheader("📊 Prediction Result")

        # Mengecek apakah sudah pernah melakukan prediksi
        if "prediction" not in st.session_state:

            st.info("Silakan isi seluruh data pasien kemudian klik Predict.")

        else:

            # Mengambil hasil prediksi dari session_state
            probability = st.session_state["probability"]

            prediction = st.session_state["prediction"]

            # Menampilkan probabilitas prediksi
            st.metric(
                "Prediction Probability",
                f"{probability:.2%}"
            )

            # Menampilkan progress bar berdasarkan probabilitas
            st.progress(float(probability))

            # Menampilkan hasil klasifikasi
            if prediction.lower() == "malignant":

                st.error("🔴 Malignant")

            else:

                st.success("🟢 Benign")

# =====================================
# PROSES PREDIKSI
# =====================================

# Proses hanya dijalankan ketika tombol Predict ditekan
if predict:

    try:

        # Menampilkan indikator loading
        with st.spinner("Sedang melakukan prediksi..."):

            # Mengirim data ke API menggunakan metode POST
            response = session.post(
                API_URL,
                json={"features": inputs},
                timeout=10         # Maksimal menunggu 10 detik
            )

            response.raise_for_status()    # Mengecek apakah request berhasil

            hasil = response.json()        # Mengubah response JSON menjadi dictionary Python

            # Menyimpan hasil prediksi ke session_state
            st.session_state["prediction"] = hasil["prediction"]

            st.session_state["probability"] = hasil["probability"]

        st.rerun()     # Memuat ulang halaman agar hasil langsung ditampilkan

    except requests.exceptions.Timeout:

        st.error("⏱️ API timeout. Silakan coba beberapa saat lagi.")

    except requests.exceptions.ConnectionError:

        st.error("❌ Tidak dapat terhubung ke API.")

    except requests.exceptions.HTTPError as e:

        st.error(f"HTTP Error : {e}")

    except Exception as e:

        st.exception(e)      # Menampilkan detail error jika terjadi kesalahan
