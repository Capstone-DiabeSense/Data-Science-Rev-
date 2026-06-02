# ============================================================
# style.py — Tema DiabeSense (Dark & Light)
# Sesuai dengan web utama DiabeSense
#
# DARK MODE:
#   bg utama   : #0a1628  (biru gelap tua)
#   bg card    : #0f1f2e
#   bg sidebar : #0d1a26
#   accent     : #2dd4a3  (teal/mint DiabeSense)
#   foreground : #e8f4f0
#   muted      : #6b8fa8
#   border     : #1a3a4a
#
# LIGHT MODE:
#   bg utama   : #f0faf7  (mint sangat muda)
#   bg card    : #ffffff
#   bg sidebar : #e8f5f0
#   accent     : #0d9e7a  (teal lebih gelap agar kontras)
#   foreground : #0a1628
#   muted      : #4a7a6a
#   border     : #b8e0d4
# ============================================================

DARK_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── BASE ── */
html, body, [class*="css"], .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: #0a1628 !important;
    color: #e8f4f0 !important;
}
.stApp { background-color: #0a1628 !important; }

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background-color: #0d1a26 !important;
    border-right: 1px solid #1a3a4a !important;
}
section[data-testid="stSidebar"] * { color: #e8f4f0 !important; }
section[data-testid="stSidebar"] .stRadio label { color: #c8e8e0 !important; }

/* ── HEADINGS ── */
h1, h2, h3, h4 {
    color: #e8f4f0 !important;
    font-weight: 700;
    letter-spacing: -0.02em;
}

/* ── DIVIDER ── */
hr { border-color: #1a3a4a !important; margin: 1.25rem 0; }

/* ── METRIC CARDS ── */
.metric-card {
    background-color: #0f1f2e;
    border: 1px solid #1a3a4a;
    border-top: 3px solid #2dd4a3;
    padding: 1.25rem 1rem;
    border-radius: 0.75rem;
    text-align: center;
    margin-bottom: 1rem;
    box-shadow: 0 4px 16px rgba(0,0,0,0.3);
}
.metric-card h1 { font-size: 2.25rem; margin: 0 0 0.25rem 0; font-weight: 800; color: #2dd4a3; }
.metric-card p  { font-size: 0.85rem; margin: 0; color: #6b8fa8; font-weight: 500; }

.metric-card-red {
    background-color: #0f1f2e;
    border: 1px solid #1a3a4a;
    border-top: 3px solid #f87171;
    padding: 1.25rem 1rem;
    border-radius: 0.75rem;
    text-align: center;
    margin-bottom: 1rem;
    box-shadow: 0 4px 16px rgba(0,0,0,0.3);
}
.metric-card-red h1 { font-size: 2.25rem; margin: 0 0 0.25rem 0; font-weight: 800; color: #f87171; }
.metric-card-red p  { font-size: 0.85rem; margin: 0; color: #6b8fa8; font-weight: 500; }

.metric-card-green {
    background-color: #0f1f2e;
    border: 1px solid #1a3a4a;
    border-top: 3px solid #2dd4a3;
    padding: 1.25rem 1rem;
    border-radius: 0.75rem;
    text-align: center;
    margin-bottom: 1rem;
    box-shadow: 0 4px 16px rgba(0,0,0,0.3);
}
.metric-card-green h1 { font-size: 2.25rem; margin: 0 0 0.25rem 0; font-weight: 800; color: #2dd4a3; }
.metric-card-green p  { font-size: 0.85rem; margin: 0; color: #6b8fa8; font-weight: 500; }

.metric-card-orange {
    background-color: #0f1f2e;
    border: 1px solid #1a3a4a;
    border-top: 3px solid #fbbf24;
    padding: 1.25rem 1rem;
    border-radius: 0.75rem;
    text-align: center;
    margin-bottom: 1rem;
    box-shadow: 0 4px 16px rgba(0,0,0,0.3);
}
.metric-card-orange h1 { font-size: 2.25rem; margin: 0 0 0.25rem 0; font-weight: 800; color: #fbbf24; }
.metric-card-orange p  { font-size: 0.85rem; margin: 0; color: #6b8fa8; font-weight: 500; }

/* ── INSIGHT BOX ── */
.insight-box {
    background-color: #0d2233;
    border-left: 4px solid #2dd4a3;
    padding: 1rem 1.25rem;
    border-radius: 0 0.75rem 0.75rem 0;
    margin: 1.25rem 0;
}
.insight-box h4 { color: #2dd4a3 !important; margin-bottom: 0.4rem; font-size: 0.95rem; }
.insight-box p  { color: #a8cfc0 !important; margin: 0; font-size: 0.9rem; line-height: 1.6; }

/* ── STREAMLIT NATIVE ── */
div[data-testid="stMetricValue"] { font-size: 1.75rem; font-weight: 700; color: #e8f4f0 !important; }
div[data-testid="stMetricLabel"] { font-size: 0.8rem; color: #6b8fa8 !important; font-weight: 500; }

/* ── BUTTON ── */
.stButton > button {
    background-color: #2dd4a3 !important;
    color: #0a1628 !important;
    border: none;
    border-radius: 0.75rem;
    font-weight: 700;
    padding: 0.5rem 1.25rem;
}
.stButton > button:hover { background-color: #22c994 !important; }

/* ── INPUT / SELECT ── */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    border: 1px solid #1a3a4a !important;
    border-radius: 0.75rem !important;
    background-color: #0f1f2e !important;
    color: #e8f4f0 !important;
}

/* ── SLIDER ── */
.stSlider > div > div > div { background-color: #2dd4a3 !important; }

/* ── DATAFRAME ── */
.stDataFrame { border: 1px solid #1a3a4a !important; border-radius: 0.75rem; }
[data-testid="stDataFrame"] { background-color: #0f1f2e !important; }

/* ── ALERT ── */
div[data-testid="stAlert"] { border-radius: 0.75rem !important; }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] { border-bottom: 1px solid #1a3a4a !important; background-color: transparent !important; }
.stTabs [data-baseweb="tab"] { color: #6b8fa8 !important; font-weight: 500; background-color: transparent !important; }
.stTabs [aria-selected="true"] { color: #2dd4a3 !important; border-bottom-color: #2dd4a3 !important; }
.stTabs [data-baseweb="tab-panel"] { background-color: transparent !important; }

/* ── UPLOAD ── */
[data-testid="stFileUploader"] {
    border: 1px dashed #1a3a4a !important;
    border-radius: 0.75rem;
    background-color: #0f1f2e;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0a1628; }
::-webkit-scrollbar-thumb { background: #1a3a4a; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #2dd4a3; }

/* ── RADIO ACTIVE ── */
.stRadio [aria-checked="true"] + div { color: #2dd4a3 !important; }
</style>
"""

LIGHT_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── BASE ── */
html, body, [class*="css"], .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: #f0faf7 !important;
    color: #0a1628 !important;
}
.stApp { background-color: #f0faf7 !important; }

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
    background-color: #e8f5f0 !important;
    border-right: 1px solid #b8e0d4 !important;
}
section[data-testid="stSidebar"] * { color: #0a1628 !important; }

/* ── HEADINGS ── */
h1, h2, h3, h4 {
    color: #0a1628 !important;
    font-weight: 700;
    letter-spacing: -0.02em;
}

/* ── DIVIDER ── */
hr { border-color: #b8e0d4 !important; margin: 1.25rem 0; }

/* ── METRIC CARDS ── */
.metric-card {
    background-color: #ffffff;
    border: 1px solid #b8e0d4;
    border-top: 3px solid #0d9e7a;
    padding: 1.25rem 1rem;
    border-radius: 0.75rem;
    text-align: center;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(13,158,122,0.08);
}
.metric-card h1 { font-size: 2.25rem; margin: 0 0 0.25rem 0; font-weight: 800; color: #0d9e7a; }
.metric-card p  { font-size: 0.85rem; margin: 0; color: #4a7a6a; font-weight: 500; }

.metric-card-red {
    background-color: #ffffff;
    border: 1px solid #b8e0d4;
    border-top: 3px solid #dc2626;
    padding: 1.25rem 1rem;
    border-radius: 0.75rem;
    text-align: center;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(220,38,38,0.08);
}
.metric-card-red h1 { font-size: 2.25rem; margin: 0 0 0.25rem 0; font-weight: 800; color: #dc2626; }
.metric-card-red p  { font-size: 0.85rem; margin: 0; color: #4a7a6a; font-weight: 500; }

.metric-card-green {
    background-color: #ffffff;
    border: 1px solid #b8e0d4;
    border-top: 3px solid #0d9e7a;
    padding: 1.25rem 1rem;
    border-radius: 0.75rem;
    text-align: center;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(13,158,122,0.08);
}
.metric-card-green h1 { font-size: 2.25rem; margin: 0 0 0.25rem 0; font-weight: 800; color: #0d9e7a; }
.metric-card-green p  { font-size: 0.85rem; margin: 0; color: #4a7a6a; font-weight: 500; }

.metric-card-orange {
    background-color: #ffffff;
    border: 1px solid #b8e0d4;
    border-top: 3px solid #d97706;
    padding: 1.25rem 1rem;
    border-radius: 0.75rem;
    text-align: center;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(217,119,6,0.08);
}
.metric-card-orange h1 { font-size: 2.25rem; margin: 0 0 0.25rem 0; font-weight: 800; color: #d97706; }
.metric-card-orange p  { font-size: 0.85rem; margin: 0; color: #4a7a6a; font-weight: 500; }

/* ── INSIGHT BOX ── */
.insight-box {
    background-color: #e0f5ee;
    border-left: 4px solid #0d9e7a;
    padding: 1rem 1.25rem;
    border-radius: 0 0.75rem 0.75rem 0;
    margin: 1.25rem 0;
}
.insight-box h4 { color: #0a6e54 !important; margin-bottom: 0.4rem; font-size: 0.95rem; }
.insight-box p  { color: #1a4a3a !important; margin: 0; font-size: 0.9rem; line-height: 1.6; }

/* ── STREAMLIT NATIVE ── */
div[data-testid="stMetricValue"] { font-size: 1.75rem; font-weight: 700; color: #0a1628 !important; }
div[data-testid="stMetricLabel"] { font-size: 0.8rem; color: #4a7a6a !important; font-weight: 500; }

/* ── BUTTON ── */
.stButton > button {
    background-color: #0d9e7a !important;
    color: #ffffff !important;
    border: none;
    border-radius: 0.75rem;
    font-weight: 700;
    padding: 0.5rem 1.25rem;
}
.stButton > button:hover { background-color: #0b8a6a !important; }

/* ── INPUT / SELECT ── */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    border: 1px solid #b8e0d4 !important;
    border-radius: 0.75rem !important;
    background-color: #ffffff !important;
}

/* ── SLIDER ── */
.stSlider > div > div > div { background-color: #0d9e7a !important; }

/* ── DATAFRAME ── */
.stDataFrame { border: 1px solid #b8e0d4 !important; border-radius: 0.75rem; }

/* ── ALERT ── */
div[data-testid="stAlert"] { border-radius: 0.75rem !important; }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] { border-bottom: 1px solid #b8e0d4 !important; background-color: transparent !important; }
.stTabs [data-baseweb="tab"] { color: #4a7a6a !important; font-weight: 500; background-color: transparent !important; }
.stTabs [aria-selected="true"] { color: #0d9e7a !important; border-bottom-color: #0d9e7a !important; }

/* ── UPLOAD ── */
[data-testid="stFileUploader"] {
    border: 1px dashed #b8e0d4 !important;
    border-radius: 0.75rem;
    background-color: #ffffff;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #f0faf7; }
::-webkit-scrollbar-thumb { background: #b8e0d4; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #0d9e7a; }
</style>
"""

# ── PLOTLY THEMES ──────────────────────────────────────────
DARK_PLOTLY = dict(
    font=dict(family="Inter, sans-serif", color="#e8f4f0", size=12),
    paper_bgcolor="#0f1f2e",
    plot_bgcolor="#0f1f2e",
    margin=dict(t=30, b=30, l=10, r=10),
    xaxis=dict(showgrid=True, gridcolor="#1a3a4a", linecolor="#2dd4a3", zeroline=False, color="#6b8fa8"),
    yaxis=dict(showgrid=True, gridcolor="#1a3a4a", linecolor="#2dd4a3", zeroline=False, color="#6b8fa8"),
    legend=dict(bgcolor="#0f1f2e", bordercolor="#1a3a4a", borderwidth=1, font=dict(size=11, color="#e8f4f0")),
    colorway=["#2dd4a3","#f87171","#fbbf24","#60a5fa","#a78bfa","#fb923c"],
)

LIGHT_PLOTLY = dict(
    font=dict(family="Inter, sans-serif", color="#0a1628", size=12),
    paper_bgcolor="#ffffff",
    plot_bgcolor="#ffffff",
    margin=dict(t=30, b=30, l=10, r=10),
    xaxis=dict(showgrid=True, gridcolor="#b8e0d4", linecolor="#2dd4a3", zeroline=False, color="#4a7a6a"),
    yaxis=dict(showgrid=True, gridcolor="#b8e0d4", linecolor="#2dd4a3", zeroline=False, color="#4a7a6a"),
    legend=dict(bgcolor="#ffffff", bordercolor="#b8e0d4", borderwidth=1, font=dict(size=11, color="#0a1628")),
    colorway=["#0d9e7a","#dc2626","#d97706","#2563eb","#7c3aed","#ea580c"],
)

# Warna chart per mode
def get_colors(dark: bool):
    if dark:
        return {
            "accent":       "#2dd4a3",
            "danger":       "#f87171",
            "warning":      "#fbbf24",
            "info":         "#60a5fa",
            "diabetes":     "#f87171",
            "nondiabetes":  "#2dd4a3",
            "chart":        ["#2dd4a3","#f87171","#fbbf24","#60a5fa","#a78bfa"],
            "gradient_low": "#1a3a4a",
            "gradient_hi":  "#2dd4a3",
        }
    else:
        return {
            "accent":       "#0d9e7a",
            "danger":       "#dc2626",
            "warning":      "#d97706",
            "info":         "#2563eb",
            "diabetes":     "#dc2626",
            "nondiabetes":  "#0d9e7a",
            "chart":        ["#0d9e7a","#dc2626","#d97706","#2563eb","#7c3aed"],
            "gradient_low": "#e0f5ee",
            "gradient_hi":  "#0d9e7a",
        }
