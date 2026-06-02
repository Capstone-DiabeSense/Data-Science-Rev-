# ============================================================
# DASHBOARD ANALISIS DIABETES INDONESIA — STREAMLIT APP
# Dataset: BRFSS 2015 Diabetes Health Indicators
# Tema: DiabeSense (Dark & Light Mode)
# ============================================================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
try:
    from scipy.stats import chi2_contingency
except (ImportError, AttributeError):
    def chi2_contingency(observed, correction=True):
        import math
        def gammp(a, x):
            if x < 0.0 or a <= 0.0:
                return 0.0
            if x < a + 1.0:
                sum_val = 1.0 / a
                ap = a
                delta = sum_val
                for i in range(1, 100):
                    ap += 1.0
                    delta *= x / ap
                    sum_val += delta
                    if abs(delta) < abs(sum_val) * 1e-15:
                        break
                return sum_val * math.exp(-x + a * math.log(x) - math.lgamma(a))
            else:
                tiny = 1e-30
                b = x + 1.0 - a
                c = 1.0 / tiny
                d = 1.0 / b
                h = d
                for i in range(1, 100):
                    an = -i * (i - a)
                    b += 2.0
                    d = an * d + b
                    if abs(d) < tiny:
                        d = tiny
                    c = b + an / c
                    if abs(c) < tiny:
                        c = tiny
                    d = 1.0 / d
                    delta = c * d
                    h *= delta
                    if abs(delta - 1.0) < 1e-15:
                        break
                return 1.0 - h * math.exp(-x + a * math.log(x) - math.lgamma(a))

        obs = np.array(observed, dtype=float)
        row_sums = obs.sum(axis=1)
        col_sums = obs.sum(axis=0)
        total = obs.sum()
        
        expected = np.outer(row_sums, col_sums) / total
        dof = (obs.shape[0] - 1) * (obs.shape[1] - 1)
        
        if dof == 1 and correction:
            chi2 = np.sum((np.abs(obs - expected) - 0.5) ** 2 / expected)
        else:
            chi2 = np.sum((obs - expected) ** 2 / expected)
            
        p = 1.0 - gammp(dof / 2.0, chi2 / 2.0)
        return chi2, p, dof, expected

from style import DARK_CSS, LIGHT_CSS, DARK_PLOTLY, LIGHT_PLOTLY, get_colors

# ============================================================
# KONFIGURASI HALAMAN
# ============================================================

st.set_page_config(
    page_title="DiabeSense · Risk Analytics",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── DARK / LIGHT TOGGLE ────────────────────────────────────
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False   # default: light

# Toggle button di pojok kanan atas via sidebar top
with st.sidebar:
    mode_label = "Light Mode" if st.session_state.dark_mode else "Dark Mode"
    if st.button(mode_label, use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# ── INJECT CSS sesuai mode ─────────────────────────────────
is_dark = st.session_state.dark_mode
st.markdown(DARK_CSS if is_dark else LIGHT_CSS, unsafe_allow_html=True)

# ── INJECT 3D GLOWING BULB IN HERO-CARD ─────────────────────
import base64
try:
    with open("glowing_3d_bulb.png", "rb") as f:
        bulb_base64 = base64.b64encode(f.read()).decode()
    st.markdown(f"""
    <style>
    .hero-card.insight-card::after {{
        right: 50px !important;
        width: 250px !important;
        height: 250px !important;
        background-image: 
            url("data:image/png;base64,{bulb_base64}"),
            radial-gradient(circle, transparent 65%, rgba(255, 255, 255, 0.08) 66%, rgba(255, 255, 255, 0.08) 67%, transparent 68%),
            radial-gradient(circle, transparent 48%, rgba(255, 255, 255, 0.06) 49%, rgba(255, 255, 255, 0.06) 50%, transparent 51%),
            radial-gradient(circle, transparent 32%, rgba(255, 255, 255, 0.05) 33%, rgba(255, 255, 255, 0.05) 34%, transparent 35%),
            radial-gradient(circle, rgba(255, 255, 255, 0.12) 0%, rgba(255, 255, 255, 0) 60%) !important;
        background-position: center center, center, center, center, center !important;
        background-repeat: no-repeat !important;
        background-size: contain, cover, cover, cover, cover !important;
    }}
    @media (max-width: 800px) {{
        .hero-card.insight-card::after {{
            display: none !important;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)
except Exception:
    pass

# ── PLOTLY THEME sesuai mode ───────────────────────────────
PLOTLY_LAYOUT   = DARK_PLOTLY if is_dark else LIGHT_PLOTLY
C               = get_colors(is_dark)
COLOR_DIABETES  = C["diabetes"]
COLOR_NONDIABETES = C["nondiabetes"]

def apply_theme(fig, height=400):
    fig.update_layout(**PLOTLY_LAYOUT, height=height)
    return fig

# ============================================================
# LOAD & CACHE DATA
# ============================================================

@st.cache_data
def load_data(path) -> pd.DataFrame:
    df = pd.read_csv(path)

    def bmi_category(bmi):
        if bmi < 18.5:   return "Underweight"
        elif bmi < 23:   return "Normal"
        elif bmi < 25:   return "Overweight"
        elif bmi < 30:   return "Obesity I"
        else:            return "Obesity II"

    df["BMI_Category"] = df["BMI"].apply(bmi_category)
    df["BMI_Category"] = pd.Categorical(
        df["BMI_Category"],
        categories=["Underweight","Normal","Overweight","Obesity I","Obesity II"],
        ordered=True
    )

    def age_group(age):
        if age <= 3:    return "18-34"
        elif age <= 6:  return "35-49"
        elif age <= 9:  return "50-64"
        else:           return "65+"

    df["Age_Group"] = df["Age"].apply(age_group)
    df["Age_Group"] = pd.Categorical(
        df["Age_Group"],
        categories=["18-34","35-49","50-64","65+"],
        ordered=True
    )

    df["metabolic_risk_score"] = (
        df["HighBP"] + df["HighChol"] + df["HeartDiseaseorAttack"] + df["Stroke"]
    )
    return df

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    fg   = "#e3ede9" if is_dark else "#182d28"
    muted = "#8ba6a0" if is_dark else "#537069"
    accent = C["accent"]

    st.markdown(f"""
    <div style="padding:0.75rem 0 1.25rem 0; text-align:center;">
        <div style="display:inline-flex; align-items:center; justify-content:center; gap:0.5rem; margin-bottom:0.35rem;">
            <span style="font-size:1.25rem; font-weight:800; color:#ffffff; letter-spacing:-0.02em; line-height:1;">DiabeSense</span>
        </div>
        <div style="font-size:0.75rem; color:rgba(255,255,255,0.55); letter-spacing:0.04em;">
            Risk Analytics Platform
        </div>
    </div>
    """, unsafe_allow_html=True)

    menu = st.radio(
        " ",
        [
            "Overview",
            "Risk Factors",
            "Lifestyle Analysis",
            "Demographics & BMI",
            "Metabolic Risk",
            "Socioeconomic Analysis",
            "Conclusions",
        ],
        label_visibility="collapsed"
    )

    st.divider()

    uploaded_file = st.file_uploader(
        "Upload dataset CSV", type=["csv"],
        help="Upload file clean_diabetes_analysis_final-4 (1).csv"
    )

    if uploaded_file:
        raw_df = pd.read_csv(uploaded_file)
        st.success(f"{raw_df.shape[0]:,} baris dimuat")
    else:
        try:
            raw_df = pd.read_csv("clean_diabetes_analysis_final-4 (1).csv")
        except FileNotFoundError:
            st.error("File tidak ditemukan. Upload CSV di atas.")
            st.stop()

    df = load_data(uploaded_file if uploaded_file else "clean_diabetes_analysis_final-4 (1).csv")

    status_filter = st.multiselect(
        "Status Diabetes",
        options=["Non-Diabetes (0)", "Diabetes (1)"],
        default=["Non-Diabetes (0)", "Diabetes (1)"]
    )

    bmi_range = st.slider(
        "Rentang BMI",
        float(df["BMI"].min()), float(df["BMI"].max()),
        (float(df["BMI"].min()), float(df["BMI"].max()))
    )

    selected_vals = []
    if "Non-Diabetes (0)" in status_filter: selected_vals.append(0)
    if "Diabetes (1)"     in status_filter: selected_vals.append(1)

    df_filtered = df[df["Diabetes_binary"].isin(selected_vals)] if selected_vals else df.copy()
    df_filtered = df_filtered[
        (df_filtered["BMI"] >= bmi_range[0]) & (df_filtered["BMI"] <= bmi_range[1])
    ]

    st.divider()
    st.markdown(f"""
    <div class="dataset-box">
        <div class="ds-label">Dataset</div>
        <div class="ds-value">{len(df_filtered):,} responden · {len(df_filtered.columns)} variabel</div>
    </div>
    """, unsafe_allow_html=True)
    st.caption("© 2026 DiabeSense")

# ============================================================
# PAGE: OVERVIEW DATASET
# ============================================================

if menu == "Overview":
    # ── HERO CARD
    st.markdown("""
    <div class="hero-card">
        <div class="hero-badge">Dashboard</div>
        <h1 class="hero-title">Diabetes Risk Overview</h1>
        <p class="hero-desc">Ringkasan analitik komprehensif terhadap faktor risiko diabetes
        berdasarkan data klinis, metabolik, gaya hidup, dan sosial ekonomi.</p>
    </div>
    """, unsafe_allow_html=True)

    # ── METRIK UTAMA ──────────────────────────────────────────
    total         = len(df_filtered)
    n_diabetes    = (df_filtered["Diabetes_binary"] == 1).sum()
    n_nondiabetes = (df_filtered["Diabetes_binary"] == 0).sum()
    pct_diabetes  = n_diabetes / total * 100 if total > 0 else 0
    avg_bmi       = df_filtered["BMI"].mean()
    avg_age_code  = df_filtered["Age"].mean()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="metric-card">
            <h1>{total:,}</h1><p>Total Responden</p></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card">
            <h1>{n_diabetes:,}</h1><p>Kasus Diabetes</p></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card">
            <h1>{n_nondiabetes:,}</h1><p>Non Diabetes</p></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="metric-card">
            <h1>{pct_diabetes:.1f}%</h1><p>Prevalensi Diabetes</p></div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="summary-box">
        <h3>Executive Summary — Ringkasan 5 Pertanyaan Bisnis</h3>
        <p>Dari {total:,} responden BRFSS 2015, prevalensi diabetes mencapai sekitar {pct_diabetes:.1f}%.
        Analisis ini menjawab 5 pertanyaan bisnis utama untuk mengidentifikasi faktor-faktor
        yang paling berkaitan dengan risiko diabetes.</p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── BARIS 1: Pie + Distribusi BMI ────────────────────────
    st.subheader("1 · Distribusi Target & BMI")
    col_left, col_right = st.columns(2)

    with col_left:
        fig_pie = px.pie(
            values=[n_nondiabetes, n_diabetes],
            names=["Non-Diabetes", "Diabetes"],
            color_discrete_sequence=[COLOR_NONDIABETES, COLOR_DIABETES],
            hole=0.5,
        )
        fig_pie.update_traces(
            textposition="outside", textinfo="percent+label",
            marker=dict(line=dict(color="#ffffff", width=2))
        )
        apply_theme(fig_pie, 320)
        fig_pie.update_layout(showlegend=True, margin=dict(t=20,b=20,l=20,r=20))
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_right:
        fig_bmi = px.histogram(
            df_filtered, x="BMI", color="Diabetes_binary",
            color_discrete_map={0: COLOR_NONDIABETES, 1: COLOR_DIABETES},
            labels={"Diabetes_binary": "Status", "BMI": "BMI"},
            barmode="overlay", opacity=0.75, nbins=50
        )
        apply_theme(fig_bmi, 320)
        fig_bmi.update_layout(
            legend=dict(title="Status", orientation="h", y=-0.22),
            margin=dict(t=20,b=20,l=10,r=10)
        )
        st.plotly_chart(fig_bmi, use_container_width=True)

    st.divider()

    # ── BARIS 2: Distribusi Fitur Biner ──────────────────────
    st.subheader("2 · Prevalensi Fitur Biner per Status Diabetes")
    st.markdown(
        "<span style='color:#737373;font-size:0.875rem;'>Persentase nilai '1' (Ya) "
        "untuk setiap fitur biner, dipisah antara kelompok Diabetes vs Non-Diabetes.</span>",
        unsafe_allow_html=True
    )

    binary_cols = ["HighBP","HighChol","Smoker","Stroke","HeartDiseaseorAttack",
                   "PhysActivity","Veggies","HvyAlcoholConsump","DiffWalk","NoDocbcCost"]

    binary_label = {
        "HighBP":"Hipertensi", "HighChol":"Kolesterol Tinggi",
        "Smoker":"Perokok", "Stroke":"Stroke",
        "HeartDiseaseorAttack":"Penyakit Jantung", "PhysActivity":"Aktif Fisik",
        "Veggies":"Konsumsi Sayur", "HvyAlcoholConsump":"Alkohol Berat",
        "DiffWalk":"Sulit Berjalan", "NoDocbcCost":"Hambatan Biaya"
    }

    bin_rows = []
    for col in binary_cols:
        for status, label in [(0,"Non-Diabetes"),(1,"Diabetes")]:
            subset = df_filtered[df_filtered["Diabetes_binary"]==status]
            pct = subset[col].mean() * 100
            bin_rows.append({"Fitur": binary_label[col], "Status": label, "Persentase (%)": round(pct,2)})
    bin_df = pd.DataFrame(bin_rows)

    fig_bin = px.bar(
        bin_df, x="Fitur", y="Persentase (%)", color="Status",
        barmode="group",
        color_discrete_map={"Non-Diabetes": COLOR_NONDIABETES, "Diabetes": COLOR_DIABETES},
        text=bin_df["Persentase (%)"].apply(lambda x: f"{x:.1f}%")
    )
    fig_bin.update_traces(textposition="outside", textfont_size=9)
    apply_theme(fig_bin, 400)
    fig_bin.update_layout(
        xaxis_tickangle=-20,
        legend=dict(orientation="h", y=1.08),
        yaxis=dict(title="Persentase (%)", range=[0,110])
    )
    st.plotly_chart(fig_bin, use_container_width=True)

    st.divider()

    # ── BARIS 3: Box Plot Fitur Kontinu ──────────────────────
    st.subheader("3 · Distribusi Fitur Kontinu per Status Diabetes")
    st.markdown(
        "<span style='color:#737373;font-size:0.875rem;'>Box plot menunjukkan sebaran "
        "nilai median, IQR, dan outlier untuk setiap fitur numerik.</span>",
        unsafe_allow_html=True
    )

    cont_col_options = ["BMI","GenHlth","MentHlth","PhysHlth","Age","Income"]
    sel_cont = st.multiselect(
        "Pilih fitur untuk ditampilkan",
        options=cont_col_options,
        default=["BMI","GenHlth","MentHlth","PhysHlth"]
    )

    if sel_cont:
        df_melt = df_filtered[sel_cont + ["Diabetes_binary"]].melt(
            id_vars="Diabetes_binary", var_name="Fitur", value_name="Nilai"
        )
        df_melt["Status"] = df_melt["Diabetes_binary"].map({0:"Non-Diabetes",1:"Diabetes"})

        fig_box = px.box(
            df_melt, x="Fitur", y="Nilai", color="Status",
            color_discrete_map={"Non-Diabetes": COLOR_NONDIABETES, "Diabetes": COLOR_DIABETES},
            notched=True,
            points=False,
        )
        apply_theme(fig_box, 420)
        fig_box.update_layout(
            legend=dict(orientation="h", y=1.08),
            xaxis_title="Fitur",
            yaxis_title="Nilai"
        )
        st.plotly_chart(fig_box, use_container_width=True)

    st.divider()

    # ── BARIS 4: Distribusi Usia & Kategori BMI ──────────────
    st.subheader("4 · Distribusi Kelompok Usia & Kategori BMI")
    c1, c2 = st.columns(2)

    with c1:
        age_order = ["18-34","35-49","50-64","65+"]
        age_dist = df_filtered.groupby(["Age_Group","Diabetes_binary"]).size().reset_index(name="Jumlah")
        age_dist["Status"] = age_dist["Diabetes_binary"].map({0:"Non-Diabetes",1:"Diabetes"})
        age_pct = df_filtered.groupby("Age_Group").size().reset_index(name="Total")
        fig_age = px.bar(
            age_dist, x="Age_Group", y="Jumlah", color="Status",
            barmode="stack",
            color_discrete_map={"Non-Diabetes":COLOR_NONDIABETES,"Diabetes":COLOR_DIABETES},
            category_orders={"Age_Group": age_order},
            text_auto=False
        )
        apply_theme(fig_age, 320)
        fig_age.update_layout(
            title="Distribusi Kelompok Usia",
            xaxis_title="Kelompok Usia",
            legend=dict(orientation="h", y=1.08)
        )
        st.plotly_chart(fig_age, use_container_width=True)

    with c2:
        bmi_order = ["Underweight","Normal","Overweight","Obesity I","Obesity II"]
        bmi_dist = df_filtered.groupby(["BMI_Category","Diabetes_binary"]).size().reset_index(name="Jumlah")
        bmi_dist["Status"] = bmi_dist["Diabetes_binary"].map({0:"Non-Diabetes",1:"Diabetes"})
        fig_bmicat = px.bar(
            bmi_dist, x="BMI_Category", y="Jumlah", color="Status",
            barmode="stack",
            color_discrete_map={"Non-Diabetes":COLOR_NONDIABETES,"Diabetes":COLOR_DIABETES},
            category_orders={"BMI_Category": bmi_order}
        )
        apply_theme(fig_bmicat, 320)
        fig_bmicat.update_layout(
            title="Distribusi Kategori BMI Asia-Pacific",
            xaxis_title="Kategori BMI",
            legend=dict(orientation="h", y=1.08)
        )
        st.plotly_chart(fig_bmicat, use_container_width=True)

    st.divider()

    # ── BARIS 5: Missing Values & Tipe Data ──────────────────
    st.subheader("5 · Kualitas Data")
    c1, c2 = st.columns(2)

    with c1:
        missing = df_filtered.isnull().sum().reset_index()
        missing.columns = ["Fitur","Missing Values"]
        missing["Persentase (%)"] = (missing["Missing Values"] / len(df_filtered) * 100).round(2)
        missing = missing.sort_values("Missing Values", ascending=False)

        if missing["Missing Values"].sum() == 0:
            st.success("Tidak ada missing values pada dataset.")
            miss_scale = (
                [[0, "#182825"], [1, "#f25c5c"]] if is_dark
                else [[0, "#e8f3f0"], [1, "#dc2626"]]
            )
            fig_miss = px.bar(
                missing.head(10), x="Persentase (%)", y="Fitur",
                orientation="h",
                color="Persentase (%)",
                color_continuous_scale=miss_scale,
                text="Persentase (%)"
            )
            fig_miss.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
            apply_theme(fig_miss, 340)
            fig_miss.update_layout(
                coloraxis_showscale=False,
                title="Missing Values per Fitur",
                yaxis=dict(autorange="reversed")
            )
            st.plotly_chart(fig_miss, use_container_width=True)
        else:
            fig_miss = px.bar(
                missing[missing["Missing Values"]>0],
                x="Persentase (%)", y="Fitur",
                orientation="h",
                color="Persentase (%)",
                color_continuous_scale=[[0,"#ebebeb"],[1,"#dc2626"]],
                text="Persentase (%)"
            )
            fig_miss.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
            apply_theme(fig_miss, 340)
            fig_miss.update_layout(coloraxis_showscale=False, title="Missing Values per Fitur")
            st.plotly_chart(fig_miss, use_container_width=True)

    with c2:
        st.markdown("**Tipe Data per Fitur**")
        _min  = df_filtered.apply(lambda c: round(c.min(), 2)  if pd.api.types.is_numeric_dtype(c) else "-")
        _max  = df_filtered.apply(lambda c: round(c.max(), 2)  if pd.api.types.is_numeric_dtype(c) else "-")
        _mean = df_filtered.apply(lambda c: round(c.mean(), 2) if pd.api.types.is_numeric_dtype(c) else "-")
        dtype_df = pd.DataFrame({
            "Fitur": df_filtered.columns,
            "Tipe Data": df_filtered.dtypes.astype(str).values,
            "Min": _min.values,
            "Max": _max.values,
            "Mean": _mean.values,
        })
        st.dataframe(
            dtype_df,
            use_container_width=True, height=340
        )

        st.divider()

    # ── BARIS 6: Preview & Statistik Deskriptif ──────────────
    st.subheader("6 · Preview & Statistik Deskriptif")
    tab1, tab2, tab3 = st.tabs(["Preview Data", "Statistik Deskriptif", "Kamus Fitur"])

    with tab1:
        n_show = st.slider("Jumlah baris yang ditampilkan", 5, 50, 10)
        st.dataframe(df_filtered.head(n_show).style.format(precision=2), use_container_width=True)

    with tab2:
        st.dataframe(
            df_filtered.describe().T.round(2)
            .style.bar(subset=["mean"], color="#43C59A44")
            .bar(subset=["std"],  color="#8ba6a044"),
            use_container_width=True
        )

    with tab3:
        feature_info = {
            "Fitur": ["HighBP","HighChol","BMI","Smoker","Stroke","HeartDiseaseorAttack",
                    "PhysActivity","Veggies","HvyAlcoholConsump","GenHlth","MentHlth",
                    "PhysHlth","DiffWalk","Age","Income","NoDocbcCost","Diabetes_binary"],
            "Tipe": ["Biner","Biner","Kontinu","Biner","Biner","Biner","Biner","Biner",
                    "Biner","Ordinal","Kontinu","Kontinu","Biner","Ordinal","Ordinal",
                    "Biner","Biner (Target)"],
            "Deskripsi": [
                "Hipertensi (1=Ya)", "Kolesterol Tinggi (1=Ya)", "Indeks Massa Tubuh",
                "Perokok ≥100 batang seumur hidup (1=Ya)", "Pernah stroke (1=Ya)",
                "Penyakit jantung atau serangan jantung (1=Ya)",
                "Aktivitas fisik selain kerja (1=Ya)", "Konsumsi sayuran ≥1x/hari (1=Ya)",
                "Konsumsi alkohol berat (1=Ya)", "Kondisi kesehatan umum (1=Sangat Baik – 5=Buruk)",
                "Hari dengan kesehatan mental buruk (30 hari terakhir)",
                "Hari dengan kesehatan fisik buruk (30 hari terakhir)",
                "Kesulitan berjalan/naik tangga (1=Ya)",
                "Kelompok usia (1=18-24 s.d. 13=80+)",
                "Tingkat pendapatan (1=Terendah – 8=Tertinggi)",
                "Tidak bisa ke dokter karena biaya (1=Ya)", "Status diabetes (1=Diabetes)"
            ]
        }
        st.dataframe(pd.DataFrame(feature_info), use_container_width=True)

# ============================================================
# PAGE: Q1 — FAKTOR RISIKO UTAMA
# ============================================================

elif menu == "Risk Factors":
    st.markdown("""
    <div class="hero-card">
        <div class="hero-badge">Analisis Faktor</div>
        <h1 class="hero-title">Q1 — Faktor Risiko Utama</h1>
        <p class="hero-desc">Dari 16 indikator kesehatan, faktor mana yang paling signifikan membedakan penderita dan non-penderita diabetes?</p>
    </div>
    """, unsafe_allow_html=True)

    num_cols = [c for c in df_filtered.columns
                if df_filtered[c].dtype in [np.float64, np.int64]
                and c not in ["Diabetes_binary","metabolic_risk_score"]]

    corr = df_filtered[num_cols + ["Diabetes_binary"]].corr()["Diabetes_binary"].drop("Diabetes_binary")
    corr_df = pd.DataFrame({
        "Fitur": corr.index,
        "Korelasi |r|": corr.abs().values,
        "Nilai r": corr.values
    }).sort_values("Korelasi |r|", ascending=False).reset_index(drop=True)

    col1, col2 = st.columns([1.4, 1])

    with col1:
        st.subheader("Korelasi Absolut Terhadap Diabetes")
        corr_scale = (
            [[0, "#182825"], [1, "#43C59A"]] if is_dark
            else [[0, "#e8f3f0"], [1, "#33b087"]]
        )
        fig_corr = px.bar(
            corr_df, x="Korelasi |r|", y="Fitur",
            orientation="h",
            color="Korelasi |r|",
            color_continuous_scale=corr_scale,
            text=corr_df["Korelasi |r|"].round(3),
        )
        fig_corr.update_traces(textposition="outside", texttemplate="%{text:.3f}")
        apply_theme(fig_corr, 480)
        fig_corr.update_layout(
            yaxis=dict(autorange="reversed"),
            coloraxis_showscale=False,
            margin=dict(t=20,b=20,l=10,r=70)
        )
        st.plotly_chart(fig_corr, use_container_width=True)

    with col2:
        st.subheader("Top 5 Faktor Risiko")
        top5 = corr_df.head(5)
        rank_colors = (
            ["#10221e", "#162f2a", "#1d3c35", "#244941", "#2b564c"] if is_dark
            else ["#e6f5f0", "#d1ebe2", "#bde1d4", "#a9d7c6", "#94cdc7"]
        )
        text_color = "#e3ede9" if is_dark else "#182d28"
        for i, row in top5.iterrows():
            st.markdown(f"""
            <div style="background:{rank_colors[i]};color:{text_color};
                padding:10px 14px;border-radius:0.625rem;margin-bottom:8px;
                display:flex;justify-content:space-between;align-items:center;
                border:1px solid {'#1f3a34' if is_dark else '#c2ebd9'};">
                <span style="font-weight:600;font-size:0.9rem;">#{i+1} {row['Fitur']}</span>
                <span style="font-size:1rem;font-weight:700;
                    background:rgba({'255,255,255' if is_dark else '0,0,0'},0.1);
                    padding:2px 8px;border-radius:4px;">
                    {row['Korelasi |r|']:.4f}
                </span>
            </div>""", unsafe_allow_html=True)

        st.subheader("Semua Fitur")
        st.dataframe(
            corr_df[["Fitur","Korelasi |r|","Nilai r"]].style.format(
                {"Korelasi |r|": "{:.4f}", "Nilai r": "{:.4f}"}
            ).bar(subset=["Korelasi |r|"], color="#43C59A66"),
            use_container_width=True, height=280
        )

    

    st.divider()
    st.subheader("Heatmap Korelasi Antar Fitur")
    top_n = st.slider("Tampilkan top-N fitur", 5, 16, 10)
    top_feats   = corr_df.head(top_n)["Fitur"].tolist() + ["Diabetes_binary"]
    corr_matrix = df_filtered[top_feats].corr().round(3)

    heat_scale = (
        [[0,"#f25c5c"],[0.5,"#0e1615"],[1,"#43C59A"]] if is_dark
        else [[0,"#dc2626"],[0.5,"#ffffff"],[1,"#33b087"]]
    )
    fig_heat = px.imshow(
        corr_matrix, text_auto=True,
        color_continuous_scale=heat_scale,
        zmin=-1, zmax=1, aspect="auto"
    )
    apply_theme(fig_heat, 500)
    fig_heat.update_layout(margin=dict(t=20,b=20))
    st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown("""<div class="hero-card insight-card">
    <h1 class="hero-title">Insight — Faktor Risiko Utama</h1>
    <p class="hero-desc">Analisis korelasi terhadap 16 indikator kesehatan menunjukkan bahwa lima faktor dengan hubungan terkuat terhadap diabetes adalah <b>GenHlth</b> (|r| = 0,4076), <b>HighBP</b> (|r| = 0,3815), <b>BMI</b> (|r| = 0,2934), <b>HighChol</b> (|r| = 0,2892), dan <b>Age</b> (|r| = 0,2787).<br><br>
    GenHlth merupakan indikator tunggal terkuat — semakin buruk kondisi kesehatan yang dilaporkan responden, semakin sering ditemukan pada kelompok diabetes. HighBP berada di posisi kedua dengan nilai yang sangat dekat, menunjukkan bahwa hipertensi merupakan karakteristik yang paling sering menyertai penderita diabetes pada dataset ini.<br><br>
    Sebaliknya, faktor gaya hidup seperti PhysActivity (|r| = 0,1587), Smoker (|r| = 0,0860), Veggies (|r| = 0,0783), dan HvyAlcoholConsump (|r| = 0,0949) memiliki korelasi lebih rendah — artinya kemampuannya membedakan kelompok risiko lebih kecil dibandingkan faktor klinis.<br><br>
    <b>Implikasi:</b> Sistem skrining sebaiknya memprioritaskan indikator klinis (kondisi kesehatan umum, hipertensi, BMI, kolesterol, usia) karena memiliki hubungan paling kuat dengan status diabetes dan menjadi dasar pemilihan fitur untuk model machine learning.</p>
    </div>""", unsafe_allow_html=True)

# ============================================================
# PAGE: Q2 — GAYA HIDUP & KEBIASAAN
# ============================================================

elif menu == "Lifestyle Analysis":
    st.markdown("""
    <div class="hero-card">
        <div class="hero-badge">Analisis Kebiasaan</div>
        <h1 class="hero-title">Q2 — Gaya Hidup & Kebiasaan</h1>
        <p class="hero-desc">Apakah individu yang tidak aktif secara fisik dan jarang mengonsumsi sayuran memiliki proporsi diabetes yang signifikan lebih tinggi?</p>
    </div>
    """, unsafe_allow_html=True)

    lifestyle = df_filtered.copy()
    lifestyle["Kelompok"] = (
        lifestyle["PhysActivity"].map({0:"Tidak Aktif",1:"Aktif"})
        + " | " +
        lifestyle["Veggies"].map({0:"Jarang Sayur",1:"Rutin Sayur"})
    )
    order = ["Tidak Aktif | Jarang Sayur","Tidak Aktif | Rutin Sayur",
             "Aktif | Jarang Sayur","Aktif | Rutin Sayur"]

    lt = lifestyle.groupby("Kelompok")["Diabetes_binary"].mean() * 100
    lt = lt.reindex(order).reset_index()
    lt.columns = ["Kelompok","Prevalensi Diabetes (%)"]
    lt["Non Diabetes (%)"] = 100 - lt["Prevalensi Diabetes (%)"]

    col1, col2 = st.columns([1.3, 1])

    with col1:
        st.subheader("Proporsi Diabetes per Kelompok Gaya Hidup")
        fig_stacked = go.Figure()
        nd_colors = ["#3d9e8c","#2d8a78","#1a7a6a","#0d6a5a"]
        d_colors  = ["#dc2626","#b91c1c","#991b1b","#7f1d1d"]

        for i, row in lt.iterrows():
            fig_stacked.add_trace(go.Bar(
                name="Non Diabetes" if i == 0 else "",
                x=[row["Kelompok"]], y=[row["Non Diabetes (%)"]],
                marker_color=nd_colors[i], showlegend=(i==0),
                text=f"{row['Non Diabetes (%)']:.1f}%",
                textposition="inside", textfont_color="white"
            ))
            fig_stacked.add_trace(go.Bar(
                name="Diabetes" if i == 0 else "",
                x=[row["Kelompok"]], y=[row["Prevalensi Diabetes (%)"]],
                marker_color=d_colors[i], showlegend=(i==0),
                text=f"{row['Prevalensi Diabetes (%)']:.1f}%",
                textposition="inside", textfont_color="white"
            ))

        apply_theme(fig_stacked, 400)
        fig_stacked.update_layout(
            barmode="stack",
            xaxis_tickangle=-15,
            legend=dict(orientation="h", y=1.08),
            margin=dict(t=40,b=40)
        )
        st.plotly_chart(fig_stacked, use_container_width=True)

    with col2:
        st.subheader("Tabel Prevalensi")
        st.dataframe(
            lt.style.format({"Prevalensi Diabetes (%)": "{:.2f}%", "Non Diabetes (%)": "{:.2f}%"})
            .bar(subset=["Prevalensi Diabetes (%)"], color="#dc262640"),
            use_container_width=True
        )

        st.subheader("Uji Chi-Square")
        contingency = pd.crosstab(
            [df_filtered["PhysActivity"], df_filtered["Veggies"]],
            df_filtered["Diabetes_binary"]
        )
        try:
            chi2, p, dof, _ = chi2_contingency(contingency)
            significance = "SIGNIFIKAN" if p < 0.05 else "Tidak Signifikan"
            st.metric("Chi-square Statistic", f"{chi2:,.2f}")
            st.metric("P-value", f"{p:.6f}")
            st.metric("Derajat Kebebasan (dof)", dof)
            if p < 0.05:
                st.success(f"**{significance}** (p < 0.05)")
            else:
                st.error(f"**{significance}** (p ≥ 0.05)")
        except Exception:
            st.warning("Tidak cukup data untuk uji chi-square.")

    st.divider()
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Efek Aktivitas Fisik")
        pa = df_filtered.groupby("PhysActivity")["Diabetes_binary"].mean() * 100
        fig_pa = px.bar(
            x=["Tidak Aktif (0)","Aktif (1)"], y=pa.values,
            color=["Tidak Aktif (0)","Aktif (1)"],
            color_discrete_map={"Tidak Aktif (0)":"#dc2626","Aktif (1)":"#3d9e8c"},
            text=[f"{v:.1f}%" for v in pa.values],
            labels={"x":"Aktivitas Fisik","y":"Prevalensi Diabetes (%)"}
        )
        fig_pa.update_traces(textposition="outside")
        apply_theme(fig_pa, 300)
        fig_pa.update_layout(showlegend=False, yaxis_range=[0, max(pa.values)*1.2])
        st.plotly_chart(fig_pa, use_container_width=True)

    with c2:
        st.subheader("Efek Konsumsi Sayuran")
        vg = df_filtered.groupby("Veggies")["Diabetes_binary"].mean() * 100
        fig_vg = px.bar(
            x=["Jarang Sayur (0)","Rutin Sayur (1)"], y=vg.values,
            color=["Jarang Sayur (0)","Rutin Sayur (1)"],
            color_discrete_map={"Jarang Sayur (0)":"#dc2626","Rutin Sayur (1)":"#3d9e8c"},
            text=[f"{v:.1f}%" for v in vg.values],
            labels={"x":"Konsumsi Sayuran","y":"Prevalensi Diabetes (%)"}
        )
        fig_vg.update_traces(textposition="outside")
        apply_theme(fig_vg, 300)
        fig_vg.update_layout(showlegend=False, yaxis_range=[0, max(vg.values)*1.2])
        st.plotly_chart(fig_vg, use_container_width=True)

    st.markdown("""<div class="hero-card insight-card">
    <h1 class="hero-title">Insight — Gaya Hidup & Kebiasaan</h1>
    <p class="hero-desc">Terdapat perbedaan prevalensi diabetes yang besar antar kelompok gaya hidup. Kelompok <b>tidak aktif fisik + tidak rutin sayur</b> memiliki prevalensi tertinggi sebesar <b>65,06%</b> — artinya sekitar dua dari tiga individu dalam kelompok ini adalah penderita diabetes.<br><br>
    Sebaliknya, kelompok <b>aktif fisik + rutin sayur</b> memiliki prevalensi terendah sebesar <b>43,34%</b>. Selisih antar kedua kelompok mencapai <b>21,72 poin persentase</b>.<br><br>
    Pola bertingkat terlihat jelas: pada kelompok tidak rutin sayur, aktivitas fisik menurunkan prevalensi dari 65,06% → 52,10%. Pada kelompok aktif fisik, konsumsi sayuran rutin menurunkan prevalensi dari 52,10% → 43,34%. Uji Chi-Square menghasilkan nilai statistik 2026,84 dengan <b>p-value &lt; 0,001</b>, membuktikan perbedaan ini signifikan secara statistik.<br><br>
    <b>Implikasi:</b> Aktivitas fisik dan konsumsi sayuran mudah diperoleh dari pengguna tanpa pemeriksaan medis, sehingga sangat cocok sebagai komponen skrining awal berbasis web atau aplikasi.</p>
    </div>""", unsafe_allow_html=True)


# ============================================================
# PAGE: Q3 — DEMOGRAFIS: USIA & BMI
# ============================================================

elif menu == "Demographics & BMI":
    st.markdown("""
    <div class="hero-card">
        <div class="hero-badge">Analisis Demografis</div>
        <h1 class="hero-title">Q3 — Demografis: Usia & BMI</h1>
        <p class="hero-desc">Bagaimana distribusi prevalensi diabetes berdasarkan kelompok usia dan kategori BMI Asia-Pacific?</p>
    </div>
    """, unsafe_allow_html=True)

    age_order = ["18-34","35-49","50-64","65+"]
    bmi_order = ["Underweight","Normal","Overweight","Obesity I","Obesity II"]

    heatmap_data = pd.crosstab(
        df_filtered["Age_Group"], df_filtered["BMI_Category"],
        values=df_filtered["Diabetes_binary"], aggfunc="mean"
    ) * 100
    heatmap_data = heatmap_data.reindex(age_order)[bmi_order].round(1)

    col1, col2 = st.columns([1.3, 1])

    with col1:
        st.subheader("Heatmap Prevalensi Diabetes (Usia × BMI)")
        hm_scale = (
            [[0,"#0e1615"],[0.5,"#43C59A"],[1,"#f25c5c"]] if is_dark
            else [[0,"#f4FAF8"],[0.5,"#33b087"],[1,"#dc2626"]]
        )
        fig_hm = px.imshow(
            heatmap_data, text_auto=True,
            color_continuous_scale=hm_scale,
            labels=dict(x="Kategori BMI Asia-Pacific", y="Kelompok Usia",
                        color="Prevalensi (%)"),
            aspect="auto"
        )
        fig_hm.update_traces(texttemplate="%{z:.1f}%")
        apply_theme(fig_hm, 350)
        fig_hm.update_layout(margin=dict(t=20,b=20))
        st.plotly_chart(fig_hm, use_container_width=True)

    with col2:
        st.subheader("Tabel Prevalensi (%)")
        st.dataframe(
            heatmap_data.style.format("{:.1f}")
            .bar(color="#43C59A55"),
            use_container_width=True
        )
        max_val = heatmap_data.max().max()
        min_val = heatmap_data.min().min()
        max_idx = heatmap_data.stack().idxmax()
        min_idx = heatmap_data.stack().idxmin()
        st.metric("Prevalensi Tertinggi", f"{max_val:.1f}%",
                  f"Usia {max_idx[0]} × BMI {max_idx[1]}")
        st.metric("Prevalensi Terendah", f"{min_val:.1f}%",
                  f"Usia {min_idx[0]} × BMI {min_idx[1]}")

    st.divider()
    st.subheader("Tren Prevalensi Diabetes per BMI & Kelompok Usia")
    bmi_trend = heatmap_data.reset_index().melt(
        id_vars="Age_Group", var_name="BMI Category", value_name="Prevalensi (%)"
    )
    bmi_trend["Age_Group"] = pd.Categorical(bmi_trend["Age_Group"], categories=age_order, ordered=True)

    fig_line = px.line(
        bmi_trend, x="Age_Group", y="Prevalensi (%)", color="BMI Category",
        markers=True, text="Prevalensi (%)",
        color_discrete_sequence=["#2d5c8e","#3d9e8c","#c9a227","#d97b45","#dc2626"],
        labels={"Age_Group":"Kelompok Usia","Prevalensi (%)":"Prevalensi Diabetes (%)"}
    )
    fig_line.update_traces(texttemplate="%{y:.1f}%", textposition="top center",
                           line_width=2.5, marker_size=7)
    apply_theme(fig_line, 420)
    fig_line.update_layout(legend_title="Kategori BMI")
    st.plotly_chart(fig_line, use_container_width=True)

    st.divider()
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Distribusi Kelompok Usia")
        age_counts = df_filtered.groupby(["Age_Group","Diabetes_binary"]).size().reset_index(name="Count")
        age_counts["Status"] = age_counts["Diabetes_binary"].map({0:"Non-Diabetes",1:"Diabetes"})
        fig_age = px.bar(
            age_counts, x="Age_Group", y="Count", color="Status",
            barmode="group",
            color_discrete_map={"Non-Diabetes":COLOR_NONDIABETES,"Diabetes":COLOR_DIABETES},
            category_orders={"Age_Group":age_order}
        )
        apply_theme(fig_age, 320)
        st.plotly_chart(fig_age, use_container_width=True)

    with c2:
        st.subheader("Distribusi Kategori BMI")
        bmi_counts = df_filtered.groupby(["BMI_Category","Diabetes_binary"]).size().reset_index(name="Count")
        bmi_counts["Status"] = bmi_counts["Diabetes_binary"].map({0:"Non-Diabetes",1:"Diabetes"})
        fig_bmicat = px.bar(
            bmi_counts, x="BMI_Category", y="Count", color="Status",
            barmode="group",
            color_discrete_map={"Non-Diabetes":COLOR_NONDIABETES,"Diabetes":COLOR_DIABETES},
            category_orders={"BMI_Category":bmi_order}
        )
        apply_theme(fig_bmicat, 320)
        st.plotly_chart(fig_bmicat, use_container_width=True)

    st.markdown("""<div class="hero-card insight-card">
    <h1 class="hero-title">Insight — Demografis: Usia & BMI</h1>
    <p class="hero-desc">Heatmap menunjukkan pola yang sangat jelas: prevalensi diabetes meningkat konsisten seiring bertambahnya usia dan meningkatnya kategori BMI.<br><br>
    Pada usia <b>18–34 tahun</b>, prevalensi berada di kisaran 5,3%–5,7% untuk kategori underweight hingga overweight, namun melonjak ke <b>22,3%</b> pada Obesity II. Pola yang sama terlihat di usia <b>35–49 tahun</b> (9,8% → 47,3%) and <b>50–64 tahun</b> (20,4% → 67,1%).<br><br>
    Prevalensi tertinggi ditemukan pada <b>usia 65+ dengan Obesity II sebesar 75,9%</b> — tiga dari empat individu pada kelompok ini adalah penderita diabetes. Sebaliknya, prevalensi terendah ada pada usia 18–34 dengan BMI normal/underweight, hanya sekitar <b>5%</b>.<br><br>
    Perbedaan antara kelompok risiko terendah dan tertinggi mencapai lebih dari <b>70 poin persentase</b>.<br><br>
    <b>Implikasi:</b> Usia dan BMI merupakan variabel paling efektif untuk segmentasi risiko tanpa memerlukan pemeriksaan laboratorium — ideal untuk sistem skrining berbasis web atau aplikasi.</p>
    </div>""", unsafe_allow_html=True)


# ============================================================
# PAGE: Q4 — KOMORBIDITAS KLINIS
# ============================================================

elif menu == "Metabolic Risk":
    st.markdown("""
    <div class="hero-card">
        <div class="hero-badge">Analisis Komorbiditas</div>
        <h1 class="hero-title">Q4 — Komorbiditas Klinis</h1>
        <p class="hero-desc">Seberapa besar pengaruh akumulasi komorbiditas klinis (HighBP, HighChol, HeartDisease, Stroke) terhadap probabilitas diabetes?</p>
    </div>
    """, unsafe_allow_html=True)

    risk_table = df_filtered.groupby("metabolic_risk_score")["Diabetes_binary"].agg(
        ["mean","count"]
    ).reset_index()
    risk_table.columns = ["Jumlah Komorbiditas","Prevalensi Diabetes (%)","Jumlah Responden"]
    risk_table["Prevalensi Diabetes (%)"] = (risk_table["Prevalensi Diabetes (%)"] * 100).round(2)

    c1, c2, c3 = st.columns(3)
    with c1:
        prev_0 = risk_table.loc[risk_table["Jumlah Komorbiditas"]==0,"Prevalensi Diabetes (%)"].values
        st.metric("Prevalensi (0 komorbiditas)", f"{prev_0[0]:.1f}%" if len(prev_0) else "N/A")
    with c2:
        prev_2 = risk_table.loc[risk_table["Jumlah Komorbiditas"]==2,"Prevalensi Diabetes (%)"].values
        st.metric("Prevalensi (2 komorbiditas)", f"{prev_2[0]:.1f}%" if len(prev_2) else "N/A")
    with c3:
        prev_4 = risk_table.loc[risk_table["Jumlah Komorbiditas"]==4,"Prevalensi Diabetes (%)"].values
        st.metric("Prevalensi (4 komorbiditas)", f"{prev_4[0]:.1f}%" if len(prev_4) else "N/A")

    st.divider()
    col1, col2 = st.columns([1.3, 1])

    with col1:
        st.subheader("Tren Prevalensi vs Jumlah Komorbiditas")
        fig_risk = go.Figure()
        accent_color = C["accent"]
        marker_color = "#e3ede9" if is_dark else "#182d28"
        fill_color = "rgba(67,197,154,0.12)" if is_dark else "rgba(51,176,135,0.08)"
        fig_risk.add_trace(go.Scatter(
            x=risk_table["Jumlah Komorbiditas"],
            y=risk_table["Prevalensi Diabetes (%)"],
            mode="lines+markers+text",
            text=[f"{v:.1f}%" for v in risk_table["Prevalensi Diabetes (%)"]],
            textposition="top center",
            line=dict(color=accent_color, width=2.5),
            marker=dict(size=10, color=marker_color, line=dict(color=accent_color, width=2)),
            fill="tozeroy",
            fillcolor=fill_color
        ))
        apply_theme(fig_risk, 380)
        fig_risk.update_layout(
            xaxis=dict(title="Jumlah Komorbiditas", tickmode="linear", dtick=1),
            yaxis=dict(title="Prevalensi Diabetes (%)", range=[0,100])
        )
        st.plotly_chart(fig_risk, use_container_width=True)

    with col2:
        st.subheader("Tabel Risiko")
        st.dataframe(
            risk_table.style.format({
                "Prevalensi Diabetes (%)": "{:.2f}%",
                "Jumlah Responden": "{:,}"
            }).bar(subset=["Prevalensi Diabetes (%)"], color="#43C59A33"),
            use_container_width=True
        )

        st.subheader("Korelasi Metabolic Risk Score")
        corr_val = df_filtered[["metabolic_risk_score","Diabetes_binary"]].corr().iloc[0,1]
        st.metric("Korelasi (r)", f"{corr_val:.4f}")
        st.info(f"Korelasi **{corr_val:.4f}** lebih tinggi dari GenHlth tunggal (r≈0.41). "
                "Skor gabungan lebih prediktif.")

    st.divider()
    st.subheader("Prevalensi Diabetes per Komorbiditas Individual")
    comorbidities = {
        "HighBP":              "Hipertensi",
        "HighChol":            "Kolesterol Tinggi",
        "HeartDiseaseorAttack":"Penyakit Jantung",
        "Stroke":              "Stroke"
    }
    cols_c = st.columns(4)
    bar_colors = ["#2d5c8e","#3d9e8c","#d97b45","#dc2626"]
    for idx, (col_name, label) in enumerate(comorbidities.items()):
        with cols_c[idx]:
            cdata = df_filtered.groupby(col_name)["Diabetes_binary"].mean() * 100
            fig_c = px.bar(
                x=["Tidak (0)","Ya (1)"],
                y=[cdata.get(0,0), cdata.get(1,0)],
                color=["Tidak (0)","Ya (1)"],
                color_discrete_map={"Tidak (0)":"#ebebeb","Ya (1)":bar_colors[idx]},
                text=[f"{cdata.get(0,0):.1f}%", f"{cdata.get(1,0):.1f}%"],
                title=label
            )
            fig_c.update_traces(textposition="outside",
                                marker_line_color="#ffffff", marker_line_width=1)
            apply_theme(fig_c, 280)
            fig_c.update_layout(
                showlegend=False,
                yaxis_range=[0,100],
                title_font_size=12,
                margin=dict(t=40,b=10,l=10,r=10)
            )
            st.plotly_chart(fig_c, use_container_width=True)

    st.markdown("""<div class="hero-card insight-card">
    <h1 class="hero-title">Insight — Komorbiditas Klinis</h1>
    <p class="hero-desc">Terdapat hubungan yang sangat kuat antara jumlah komorbiditas klinis (hipertensi, kolesterol tinggi, penyakit jantung, stroke) dan prevalensi diabetes.<br><br>
    Kelompok <b>tanpa komorbiditas</b> memiliki prevalensi 19,09%. Dengan satu komorbiditas meningkat menjadi <b>46,19%</b>, dua komorbiditas <b>69,45%</b>, tiga komorbiditas <b>77,97%</b>, dan empat komorbiditas mencapai <b>84,02%</b>.<br><br>
    Metabolic Risk Score (gabungan keempat komorbiditas) memiliki korelasi <b>r = 0,4248</b> terhadap diabetes — bahkan melampaui GenHlth (0,4076) yang sebelumnya merupakan fitur individu dengan korelasi tertinggi. Ini menunjukkan bahwa kombinasi indikator klinis mampu menjelaskan status diabetes lebih baik daripada fitur tunggal manapun.<br><br>
    <b>Implikasi:</b> Metabolic Risk Score sangat potensial digunakan sebagai indikator tunggal dalam sistem skrining karena merangkum kondisi klinis kompleks ke dalam satu skor yang mudah dipahami pengguna maupun tenaga kesehatan.</p>
    </div>""", unsafe_allow_html=True)

# ============================================================
# PAGE: Q5 — SOSIAL-EKONOMI & AKSES KESEHATAN
# ============================================================

elif menu == "Socioeconomic Analysis":
    st.markdown("""
    <div class="hero-card">
        <div class="hero-badge">Analisis Sosial Ekonomi</div>
        <h1 class="hero-title">Q5 — Sosial-Ekonomi & Akses Kesehatan</h1>
        <p class="hero-desc">Apakah individu dengan pendapatan rendah dan hambatan biaya kesehatan memiliki prevalensi diabetes lebih tinggi?</p>
    </div>
    """, unsafe_allow_html=True)

    income_label = {
        1:"1(terendah)", 2:"2", 3:"3", 4:"4",
        5:"5", 6:"6", 7:"7", 8:"8(tertinggi)"
    }

    income_table = df_filtered.groupby("Income")["Diabetes_binary"].mean() * 100
    income_table = income_table.reset_index()
    income_table.columns = ["Income Level","Prevalensi Diabetes (%)"]
    income_table["Prevalensi Diabetes (%)"] = income_table["Prevalensi Diabetes (%)"].round(2)
    income_table["Keterangan"] = income_table["Income Level"].map(income_label)

    col1, col2 = st.columns([1.3, 1])

    with col1:
        st.subheader("Prevalensi Diabetes Berdasarkan Tingkat Pendapatan")
        fig_income = go.Figure()
        accent_color = C["accent"]
        marker_color = "#e3ede9" if is_dark else "#182d28"
        fill_color = "rgba(67,197,154,0.12)" if is_dark else "rgba(51,176,135,0.08)"
        fig_income.add_trace(go.Scatter(
            x=income_table["Keterangan"],
            y=income_table["Prevalensi Diabetes (%)"],
            mode="lines+markers+text",
            text=[f"{v:.1f}%" for v in income_table["Prevalensi Diabetes (%)"]],
            textposition="top center",
            line=dict(color=accent_color, width=2.5),
            marker=dict(size=9, color=marker_color, line=dict(color=accent_color, width=1.5)),
            fill="tozeroy",
            fillcolor=fill_color
        ))
        apply_theme(fig_income, 380)
        fig_income.update_layout(
            xaxis=dict(title="Tingkat Pendapatan (USD/tahun)", tickangle=-15),
            yaxis=dict(title="Prevalensi Diabetes (%)", range=[0,80])
        )
        st.plotly_chart(fig_income, use_container_width=True)

    with col2:
        st.subheader("Tabel Pendapatan & Diabetes")
        st.dataframe(
            income_table[["Income Level","Keterangan","Prevalensi Diabetes (%)"]].style.format(
                {"Prevalensi Diabetes (%)": "{:.2f}%"}
            ).bar(subset=["Prevalensi Diabetes (%)"], color=C["accent"] + "33"),
            use_container_width=True, height=280
        )
        diff = income_table["Prevalensi Diabetes (%)"].max() - income_table["Prevalensi Diabetes (%)"].min()
        st.metric("Selisih Tertinggi – Terendah", f"{diff:.2f} pp")

    st.divider()
    st.subheader("Hambatan Biaya Kesehatan (NoDocbcCost)")
    c1, c2 = st.columns(2)

    with c1:
        nodoc = df_filtered.groupby("NoDocbcCost")["Diabetes_binary"].mean() * 100
        fig_nodoc = px.bar(
            x=["Tidak Terhambat (0)","Terhambat Biaya (1)"],
            y=[nodoc.get(0,0), nodoc.get(1,0)],
            color=["Tidak Terhambat (0)","Terhambat Biaya (1)"],
            color_discrete_map={
                "Tidak Terhambat (0)": COLOR_NONDIABETES,
                "Terhambat Biaya (1)": COLOR_DIABETES
            },
            text=[f"{nodoc.get(0,0):.1f}%", f"{nodoc.get(1,0):.1f}%"],
            labels={"x":"Hambatan Biaya","y":"Prevalensi Diabetes (%)"},
            title="Prevalensi Diabetes vs Hambatan Biaya"
        )
        fig_nodoc.update_traces(textposition="outside",
                                marker_line_color="#ffffff", marker_line_width=1)
        apply_theme(fig_nodoc, 340)
        fig_nodoc.update_layout(showlegend=False, yaxis_range=[0,80], margin=dict(t=50,b=20))
        st.plotly_chart(fig_nodoc, use_container_width=True)

    with c2:
        st.subheader("Uji Chi-Square: NoDocbcCost vs Diabetes")
        contingency_n = pd.crosstab(df_filtered["NoDocbcCost"], df_filtered["Diabetes_binary"])
        try:
            chi2_n, p_n, dof_n, _ = chi2_contingency(contingency_n)
            st.metric("Chi-square Statistic", f"{chi2_n:,.4f}")
            st.metric("P-value", f"{p_n:.6f}")
            st.metric("Derajat Kebebasan", dof_n)
            if p_n < 0.05:
                st.success("SIGNIFIKAN secara statistik (p < 0.05)")
            else:
                st.warning("Tidak signifikan (p ≥ 0.05)")
        except Exception:
            st.warning("Tidak cukup data untuk uji chi-square.")

        nodoc_table = df_filtered.groupby("NoDocbcCost")["Diabetes_binary"].agg(
            ["mean","count"]
        ).reset_index()
        nodoc_table.columns = ["NoDocbcCost","Prevalensi (%)","Jumlah"]
        nodoc_table["Prevalensi (%)"] = (nodoc_table["Prevalensi (%)"] * 100).round(2)
        nodoc_table["NoDocbcCost"] = nodoc_table["NoDocbcCost"].map({0:"Tidak Terhambat",1:"Terhambat Biaya"})
        st.dataframe(nodoc_table, use_container_width=True, hide_index=True)

    st.markdown("""<div class="hero-card insight-card">
    <h1 class="hero-title">Insight — Sosial-Ekonomi & Akses Kesehatan</h1>
    <p class="hero-desc">Terdapat hubungan konsisten antara tingkat pendapatan dan prevalensi diabetes. Kelompok <b>pendapatan terendah</b> memiliki prevalensi <b>65,99%</b>, sedangkan kelompok <b>pendapatan tertinggi</b> hanya <b>34,85%</b> — selisih <b>31,14 poin persentase</b>, hampir dua kali lipat.<br><br>
    Pola menurun cukup konsisten: setelah mencapai puncak pada Income Level 2 sebesar 68,61%, prevalensi diabetes terus turun seiring meningkatnya pendapatan hingga titik terendah di Income Level 8.<br><br>
    Uji Chi-Square terhadap variabel <b>NoDocbcCost</b> (hambatan biaya ke dokter) menghasilkan <b>p-value &lt; 0,001</b>, membuktikan hubungan signifikan secara statistik antara hambatan biaya kesehatan dan status diabetes.<br><br>
    <b>Implikasi:</b> Tingkat pendapatan dan hambatan biaya memberikan informasi tambahan yang tidak sepenuhnya tercermin oleh indikator klinis. Kedua variabel ini layak dipertahankan dalam sistem skrining risiko diabetes karena mencerminkan dimensi sosial-ekonomi yang nyata.</p>
    </div>""", unsafe_allow_html=True)


# ============================================================
# PAGE: KESIMPULAN Analisis
# ============================================================

elif menu == "Conclusions":
    st.title("Kesimpulan Akhir Analisis Diabetes Indonesia")
    st.markdown(
        f"<span style='color:{'#6b8fa8' if is_dark else '#4a7a6a'};font-size:0.95rem;'>"
        "Ringkasan temuan analisis eksploratif terhadap 70.692 responden dataset BRFSS 2015 "
        "— mencakup faktor klinis, gaya hidup, demografis, dan sosial-ekonomi.</span>",
        unsafe_allow_html=True
    )
    st.divider()

    # ── INTRO BOX ─────────────────────────────────────────────
    st.markdown("""<div class="hero-card">
    <h1 class="hero-title">Gambaran Umum</h1>
    <p class="hero-desc">Diabetes terbukti merupakan kondisi multidimensi yang tidak dapat dijelaskan oleh satu faktor tunggal.
    Hasil Analisis menunjukkan bahwa interaksi antara faktor klinis, kebiasaan hidup, kelompok usia, akumulasi
    komorbiditas, dan kondisi sosial-ekonomi secara bersama-sama membentuk profil risiko seseorang.
    Tidak ada variabel yang berdiri sendiri — semua saling memperkuat.</p>
    </div>""", unsafe_allow_html=True)

    st.divider()

    # ── RINGKASAN TEMUAN ──────────────────────────────────────
    st.subheader("Ringkasan Temuan Utama per Analisis")

    findings = [
        {
            "q": "Q1 — Faktor Risiko Utama",
            "color": C["accent"],
            "finding": (
                "GenHlth (|r|=0,41), HighBP (|r|=0,38), BMI (|r|=0,29), HighChol (|r|=0,29), dan Age (|r|=0,28) "
                "merupakan lima faktor dengan korelasi tertinggi terhadap diabetes. Faktor klinis dan metabolik "
                "terbukti jauh lebih kuat membedakan penderita dan non-penderita dibandingkan faktor perilaku "
                "seperti merokok (|r|=0,09) atau konsumsi sayuran (|r|=0,08). GenHlth sebagai indikator "
                "tunggal terkuat — semakin buruk kondisi kesehatan umum yang dilaporkan, semakin tinggi "
                "kemungkinan responden berada di kelompok diabetes."
            ),
            "implication": "Sistem skrining harus memprioritaskan indikator klinis sebagai input utama. Kelima variabel ini menjadi kandidat fitur terkuat untuk tahap pemodelan machine learning."
        },
        {
            "q": "Q2 — Gaya Hidup & Kebiasaan",
            "color": C["accent"],
            "finding": (
                "Kelompok tidak aktif fisik + jarang sayur memiliki prevalensi diabetes 65,06% — sekitar "
                "dua dari tiga individu adalah penderita. Sebaliknya, kelompok aktif + rutin sayur hanya 43,34%. "
                "Selisih 21,72 poin persentase. Aktivitas fisik memberikan penurunan terbesar (65,06% → 52,10%), "
                "sedangkan konsumsi sayuran memberikan efek protektif tambahan (52,10% → 43,34%). "
                "Uji Chi-Square mengonfirmasi hubungan ini signifikan (χ²=2026,84, p<0,001)."
            ),
            "implication": "Aktivitas fisik dan pola makan adalah pertanyaan skrining yang mudah dikumpulkan tanpa pemeriksaan klinis — cocok sebagai komponen awal sistem skrining berbasis aplikasi."
        },
        {
            "q": "Q3 — Demografis: Usia & BMI",
            "color": C["warning"],
            "finding": (
                "Prevalensi meningkat konsisten pada setiap kombinasi usia dan BMI. Titik terendah: "
                "usia 18–34 + BMI normal = 5,6%. Titik tertinggi: usia 65+ + Obesity II = 75,9%. "
                "Perbedaan lebih dari 70 poin persentase. Pada usia 35–49, Obesity II sudah membawa "
                "prevalensi ke 47,3% — hampir separuh kelompok tersebut adalah penderita diabetes. "
                "Di usia 50–64, bahkan BMI normal pun sudah mencatat prevalensi 20,4%."
            ),
            "implication": "Usia dan BMI sangat efektif untuk segmentasi risiko tanpa pemeriksaan laboratorium. Keduanya menjadi filter pertama yang ideal dalam alur skrining digital."
        },
        {
            "q": "Q4 — Komorbiditas Klinis",
            "color": C["danger"],
            "finding": (
                "Metabolic Risk Score (gabungan HighBP + HighChol + HeartDiseaseorAttack + Stroke) menunjukkan "
                "eskalasi kuat: 0 komorbiditas=19,09% → 1=46,19% → 2=69,45% → 3=77,97% → 4=84,02%. "
                "Korelasi skor gabungan (r=0,4248) bahkan melampaui GenHlth (r=0,4076) yang merupakan "
                "fitur individual terkuat — membuktikan bahwa kombinasi indikator klinis lebih prediktif "
                "daripada satu indikator tunggal manapun."
            ),
            "implication": "Metabolic Risk Score berpotensi digunakan sebagai indikator ringkas yang mudah dipahami pengguna dan tenaga kesehatan untuk menilai tingkat risiko secara cepat."
        },
        {
            "q": "Q5 — Sosial-Ekonomi & Akses",
            "color": C["info"],
            "finding": (
                "Prevalensi pada kelompok pendapatan terendah mencapai 65,99%, hampir dua kali lipat "
                "dibandingkan kelompok pendapatan tertinggi (34,85%) — selisih 31,14 poin persentase. "
                "Pola penurunan konsisten dari Income Level 2 (68,61%) hingga Level 8 (34,85%). "
                "Hambatan biaya kesehatan (NoDocbcCost) juga terbukti signifikan secara statistik (p<0,001), "
                "menunjukkan bahwa keterbatasan akses layanan turut berkontribusi pada tingginya prevalensi."
            ),
            "implication": "Faktor sosial-ekonomi memberikan informasi yang tidak tercermin oleh indikator klinis saja. Pendapatan dan hambatan biaya layak dipertahankan sebagai variabel pendukung dalam sistem skrining."
        },
    ]

    _bg_card   = "#0e1615" if is_dark else "#ffffff"
    _border    = "#182825" if is_dark else "#d8ece5"
    _text_main = "#e3ede9" if is_dark else "#1a2e28"
    _text_muted = "#8ba6a0" if is_dark else "#6b8a80"

    for f in findings:
        st.markdown(f"""
        <div style="border:1px solid {_border}; border-left:5px solid {f['color']};
             background:{_bg_card}; padding:1.15rem 1.35rem;
             border-radius:0.75rem; margin-bottom:0.875rem;
             box-shadow: 0 4px 16px rgba(0,0,0,{'0.2' if is_dark else '0.03'});">
            <div style="font-weight:700; color:{f['color']}; margin-bottom:0.4rem; font-size:0.95rem;">
                {f['q']}
            </div>
            <p style="margin:0 0 0.4rem 0; font-size:0.88rem; color:{_text_main}; line-height:1.7;">
                <b>Temuan:</b> {f['finding']}
            </p>
            <p style="margin:0; font-size:0.85rem; color:{_text_muted}; line-height:1.6;">
                <b>Implikasi:</b> {f['implication']}
            </p>
        </div>""", unsafe_allow_html=True)

    st.divider()

    # ── PROFIL RISIKO ──────────────────────────────────────────
    st.subheader("Profil Risiko Tinggi vs Rendah")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown(f"""
        <div style="background:{'#1f1111' if is_dark else '#fff5f5'};
             border:1px solid {'#3a1c1c' if is_dark else '#ffd1d1'};
             border-top:4px solid {C['danger']};
             padding:1.25rem; border-radius:0.75rem;">
            <div style="font-weight:700; color:{C['danger']}; margin-bottom:0.75rem; font-size:1rem;">
                Profil Risiko Tinggi
            </div>
            <ul style="margin:0; padding-left:1.25rem; font-size:0.88rem; line-height:2;
                       color:{'#ffd1d1' if is_dark else '#991b1b'};">
                <li>Usia 65 tahun ke atas</li>
                <li>BMI kategori Obesity I atau Obesity II</li>
                <li>Memiliki hipertensi dan/atau kolesterol tinggi</li>
                <li>Riwayat penyakit jantung atau stroke</li>
                <li>Kondisi kesehatan umum buruk (GenHlth 4–5)</li>
                <li>Tidak aktif secara fisik dan jarang konsumsi sayuran</li>
                <li>Pendapatan rendah dengan hambatan akses layanan kesehatan</li>
            </ul>
        </div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div style="background:{'#0c1a17' if is_dark else '#f0faf7'};
             border:1px solid {'#18342e' if is_dark else '#c6eade'};
             border-top:4px solid {C['accent']};
             padding:1.25rem; border-radius:0.75rem;">
            <div style="font-weight:700; color:{C['accent']}; margin-bottom:0.75rem; font-size:1rem;">
                Profil Risiko Rendah
            </div>
            <ul style="margin:0; padding-left:1.25rem; font-size:0.88rem; line-height:2;
                       color:{'#bcd1cc' if is_dark else '#0f7053'};">
                <li>Usia 18–34 tahun</li>
                <li>BMI normal atau underweight (standar Asia-Pacific)</li>
                <li>Tidak memiliki hipertensi maupun kolesterol tinggi</li>
                <li>Tidak ada riwayat penyakit jantung atau stroke</li>
                <li>Kondisi kesehatan umum baik (GenHlth 1–2)</li>
                <li>Aktif secara fisik dan rutin mengonsumsi sayuran</li>
                <li>Akses layanan kesehatan memadai tanpa hambatan biaya</li>
            </ul>
        </div>""", unsafe_allow_html=True)

    st.divider()

    # ── REKOMENDASI ────────────────────────────────────────────
    st.subheader("Rekomendasi Strategis")

    recs = [
        ("⚖️", "Pengendalian Berat Badan",
         "Program penurunan berat badan dan pengelolaan obesitas harus menjadi prioritas utama, terutama pada kelompok usia 35 tahun ke atas — kombinasi usia dan BMI tinggi membawa prevalensi diabetes hingga 75,9%."),
        ("🩺", "Manajemen Hipertensi & Kolesterol",
         "Deteksi dan pengelolaan HighBP serta HighChol secara dini dapat memutus rantai komorbiditas. Keduanya adalah dua dari lima faktor paling prediktif dalam dataset dan berkontribusi langsung pada Metabolic Risk Score."),
        ("🏃‍♂️", "Peningkatan Aktivitas Fisik",
         "Mendorong aktivitas fisik rutin dapat menurunkan prevalensi diabetes hingga 12,96 poin persentase bahkan tanpa perubahan pola makan. Terbukti signifikan secara statistik (p<0,001)."),
        ("🥗", "Edukasi Pola Makan Sehat",
         "Konsumsi sayuran rutin memberikan efek protektif tambahan di atas aktivitas fisik. Keduanya sebaiknya dikemas sebagai paket intervensi gaya hidup yang terintegrasi, bukan program terpisah."),
        ("👴", "Skrining Dini Kelompok Usia Lanjut",
         "Kelompok usia 50+ menunjukkan lonjakan prevalensi signifikan bahkan pada BMI normal (20,4%). Program skrining proaktif dan berkala pada kelompok ini berpotensi mendeteksi kasus lebih awal."),
        ("🏥", "Akses Layanan Kesehatan Merata",
         "Kelompok pendapatan rendah memiliki prevalensi hampir dua kali lipat kelompok pendapatan tertinggi. Subsidi layanan dan program skrining gratis dapat menjangkau populasi berisiko tinggi yang kurang terlayani."),
    ]

    _card_bg   = "#0e1615" if is_dark else "#ffffff"
    _card_border = "#182825" if is_dark else "#d8ece5"
    _card_txt  = "#8ba6a0" if is_dark else "#6b8a80"
    _title_c   = "#e3ede9" if is_dark else "#1a2e28"

    cols_r = st.columns(2)
    for i, (emoji, title, desc) in enumerate(recs):
        with cols_r[i % 2]:
            st.markdown(f"""
            <div style="background:{_card_bg}; border-radius:0.75rem; padding:1.15rem 1.35rem;
                 border:1px solid {_card_border}; border-top:4px solid {C['accent']};
                 margin-bottom:1rem;
                 box-shadow: 0 4px 16px rgba(0,0,0,{'0.2' if is_dark else '0.03'});">
                <p style="font-size:0.95rem; font-weight:700; margin:0 0 0.45rem;
                          color:{_title_c};">{emoji} &nbsp;{title}</p>
                <p style="color:{_card_txt}; margin:0; font-size:0.86rem;
                          line-height:1.65;">{desc}</p>
            </div>""", unsafe_allow_html=True)

    st.divider()

    # ── KESIMPULAN AKHIR ───────────────────────────────────────
    st.markdown("""<div class="hero-card">
    <h1 class="hero-title">Kesimpulan Akhir</h1>
    <p class="hero-desc">Profil individu dengan risiko diabetes tertinggi adalah mereka yang berusia lanjut, memiliki BMI
    tinggi (obesitas), mengalami hipertensi dan kolesterol tinggi, memiliki beberapa komorbiditas klinis,
    menjalani gaya hidup kurang aktif, serta berada pada kondisi sosial-ekonomi yang terbatas.<br><br>
    Diabetes bukan kondisi yang dapat dijelaskan oleh satu faktor saja. Strategi pencegahan paling efektif
    adalah yang memadukan pengendalian faktor klinis, perubahan gaya hidup, dan peningkatan akses layanan
    kesehatan secara bersamaan — bukan hanya berfokus pada perubahan perilaku individu semata.<br><br>
    Dataset BRFSS 2015 memberikan landasan empiris yang kuat untuk membangun sistem skrining risiko diabetes
    berbasis data yang dapat menjangkau populasi luas tanpa bergantung sepenuhnya pada pemeriksaan
    laboratorium.</p>
    </div>""", unsafe_allow_html=True)

    st.info(
        "**Catatan:** Dashboard ini dibangun berdasarkan EDA dataset BRFSS 2015. "
        "Hasil analisis bersifat deskriptif dan korelasional, bukan kausal. "
        "Diperlukan analisis lanjutan (modeling ML) untuk membangun sistem prediksi diabetes."
    )