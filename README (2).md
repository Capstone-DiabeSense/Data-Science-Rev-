# 🩺 DiabeSense — Sistem Analisis Risiko Diabetes

> **Data Science Project** · Dataset BRFSS 2015 CDC · Streamlit Dashboard

Dashboard interaktif berbasis data untuk menganalisis faktor risiko diabetes menggunakan dataset *Behavioral Risk Factor Surveillance System (BRFSS) 2015* dari CDC Amerika Serikat. Proyek ini mencakup pipeline data science lengkap mulai dari *data wrangling*, *feature engineering*, *EDA*, hingga visualisasi interaktif.

---

## 📁 Struktur Repositori

```
Data-Science-Rev--main/
├── data/
│   ├── raw/
│   │   └── diabetes_binary_5050split_health_indicators_BRFSS2015.csv
│   └── processed/
│       ├── clean_diabetes_analysis_final-4 (1).csv
│       └── clean_diabetes_modeling_ready.csv
├── notebooks/
│   ├── data_wrangling_final_bersih.ipynb      # Tahap 1: Data Wrangling
│   ├── feature_engineering_dataset.ipynb      # Tahap 2: Feature Engineering
│   └── EDA_Visualisasi_dataset.ipynb          # Tahap 3: EDA & Visualisasi
└── diabetes-dashboard/
    ├── app.py                                  # Aplikasi Streamlit utama
    ├── style.py                                # Tema Dark/Light Mode
    ├── requirements.txt                        # Dependensi Python
    ├── runtime.txt                             # Versi Python
    ├── .streamlit/
    │   └── config.toml                         # Konfigurasi tema Streamlit
    └── clean_diabetes_analysis_final-4 (1).csv # Data untuk dashboard
```

---

## 📊 Tentang Dataset

| Atribut | Detail |
|---|---|
| **Sumber** | [Kaggle — Diabetes Health Indicators Dataset](https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset) |
| **Asal Data** | BRFSS 2015, CDC Amerika Serikat |
| **Jumlah Fitur** | 22 kolom (1 target + 21 fitur) |
| **Target** | `Diabetes_binary` (0 = Non-Diabetes, 1 = Diabetes) |
| **Split** | 50/50 (balanced dataset) |

**Fitur Utama:**
`HighBP`, `HighChol`, `BMI`, `Smoker`, `Stroke`, `HeartDiseaseorAttack`, `PhysActivity`, `Fruits`, `Veggies`, `HvyAlcoholConsump`, `AnyHealthcare`, `GenHlth`, `MentHlth`, `PhysHlth`, `Age`, `Education`, `Income`, dan lainnya.

---

## 🚀 Cara Replikasi & Menjalankan Proyek

### Prasyarat

Pastikan sistem kamu memiliki:
- **Python 3.11** (sesuai `runtime.txt`)
- **pip** atau **conda**
- **Git**
- **Jupyter Notebook** / **JupyterLab** (untuk menjalankan notebook)

---

### 1. Clone Repositori

```bash
git clone https://github.com/<username>/Data-Science-Rev.git
cd Data-Science-Rev
```

> Ganti `<username>` dengan username GitHub milikmu.

---

### 2. Buat Virtual Environment (Disarankan)

**Menggunakan `venv`:**
```bash
python -m venv venv

# Aktivasi — Windows
venv\Scripts\activate

# Aktivasi — macOS/Linux
source venv/bin/activate
```

**Menggunakan `conda`:**
```bash
conda create -n diabesense python=3.11
conda activate diabesense
```

---

### 3. Install Dependensi

**Untuk Streamlit Dashboard:**
```bash
pip install -r diabetes-dashboard/requirements.txt
```

**Untuk Notebook (tambahan library):**
```bash
pip install jupyter pandas numpy matplotlib seaborn scikit-learn plotly scipy pillow
```

Atau install semua sekaligus:
```bash
pip install jupyter pandas numpy matplotlib seaborn scikit-learn plotly scipy pillow streamlit
```

---

### 4. Jalankan Notebook (Pipeline Analisis)

Notebook harus dijalankan **secara berurutan** karena setiap tahap menghasilkan output yang digunakan oleh tahap berikutnya.

```bash
cd notebooks
jupyter notebook
```

Urutan eksekusi:

| Urutan | Notebook | Deskripsi |
|---|---|---|
| 1️⃣ | `data_wrangling_final_bersih.ipynb` | Pembersihan data, perbaikan tipe data, penanganan missing value |
| 2️⃣ | `feature_engineering_dataset.ipynb` | Pembuatan fitur baru: Age Group, BMI Category, Metabolic Risk Score |
| 3️⃣ | `EDA_Visualisasi_dataset.ipynb` | Analisis eksplorasi: faktor risiko, gaya hidup, demografis, komorbiditas, sosial-ekonomi |

> ⚠️ **Penting:** Pastikan dataset raw tersedia di `data/raw/` sebelum menjalankan notebook pertama.

---

### 5. Jalankan Streamlit Dashboard

```bash
cd diabetes-dashboard
streamlit run app.py
```

Dashboard akan otomatis terbuka di browser pada:
```
http://localhost:8501
```

---

## 🗺️ Fitur Dashboard (DiabeSense)

Dashboard memiliki **7 halaman analisis** yang dapat diakses melalui sidebar:

| Menu | Isi |
|---|---|
| **Overview** | Ringkasan dataset, distribusi target, statistik deskriptif |
| **Risk Factors** | Korelasi 21 fitur terhadap diabetes, top 5 faktor risiko, heatmap |
| **Lifestyle Analysis** | Analisis gaya hidup (aktivitas fisik, konsumsi sayur), uji Chi-Square |
| **Demographics & BMI** | Heatmap prevalensi Usia × BMI, distribusi kelompok demografis |
| **Metabolic Risk** | Metabolic Risk Score, tren komorbiditas klinis |
| **Socioeconomic Analysis** | Pengaruh pendapatan dan akses layanan kesehatan |
| **Conclusions** | Rangkuman temuan dan implikasi analisis |

**Fitur tambahan:**
- 🌙 Toggle **Dark Mode / Light Mode**
- 🔍 Filter data interaktif di sidebar
- 📊 Visualisasi menggunakan Plotly (interaktif & zoomable)

---

## ⚙️ Konfigurasi Tema Streamlit

Tema default sudah dikonfigurasi di `.streamlit/config.toml`:

```toml
[theme]
base = "light"
primaryColor = "#43C59A"
backgroundColor = "#f0f7f4"
secondaryBackgroundColor = "#e8f3f0"
textColor = "#1a2e28"
font = "sans serif"
```

Kamu bisa mengubah nilai ini sesuai preferensi.

---

## 🔬 Ringkasan Analisis (Temuan Utama)

Berdasarkan hasil EDA pada dataset BRFSS 2015:

- **Faktor risiko terkuat:** `GenHlth` (|r| = 0.41), `HighBP` (|r| = 0.38), `BMI` (|r| = 0.29)
- **Metabolic Risk Score** (gabungan 4 komorbiditas klinis) memiliki korelasi **r = 0.4248** — melampaui semua fitur tunggal
- Kelompok **tidak aktif + tidak konsumsi sayur** memiliki prevalensi diabetes tertinggi: **65.06%**
- Prevalensi diabetes meningkat signifikan seiring bertambahnya **usia** dan **kategori BMI**
- Individu **tanpa asuransi kesehatan** memiliki prevalensi lebih tinggi dibandingkan yang memiliki akses layanan kesehatan

---

## 🛠️ Teknologi yang Digunakan

| Kategori | Library |
|---|---|
| Dashboard | `streamlit` |
| Visualisasi | `plotly`, `matplotlib`, `seaborn` |
| Analisis Data | `pandas`, `numpy`, `scipy` |
| Notebook | `jupyter` |
| Gambar | `pillow` |

---

## 🐛 Troubleshooting

**Error: `ModuleNotFoundError`**
```bash
pip install -r diabetes-dashboard/requirements.txt
```

**Port 8501 sudah digunakan:**
```bash
streamlit run app.py --server.port 8502
```

**Notebook tidak menemukan dataset:**
Pastikan file CSV berada di `data/raw/diabetes_binary_5050split_health_indicators_BRFSS2015.csv`. Download dari [Kaggle](https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset) jika belum ada.

**Dashboard lambat saat filter data:**
Dataset berukuran ~6MB dan diproses langsung di memori. Pastikan RAM yang tersedia minimal **4GB**.

---

## 📄 Lisensi

Proyek ini dibuat untuk keperluan akademis. Dataset BRFSS 2015 merupakan data publik milik CDC dan tersedia di Kaggle.

---

<p align="center">
  Dibuat dengan ❤️ sebagai bagian dari proyek Data Science
</p>
