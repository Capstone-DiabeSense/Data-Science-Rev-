# ============================================================
# style.py — Tema DiabeSense · Clean Professional Healthcare
# Brand Color: #43C59A (mint green / teal green)
#
# LIGHT MODE (Primary — sesuai referensi):
#   bg utama   : #f0f7f4
#   bg card    : #ffffff
#   sidebar    : linear-gradient(180deg, #1a7a5a, #0f4a35)
#   accent     : #43C59A
#   text       : #1a2e28
#   muted      : #6b8a80
#   border     : #d8ece5
#
# DARK MODE:
#   bg utama   : #060b0a
#   bg card    : #0e1615
#   sidebar    : linear-gradient(180deg, #0f4a35, #071f18)
#   accent     : #43C59A
#   text       : #e3ede9
#   muted      : #8ba6a0
#   border     : #182825
# ============================================================

# ── SHARED CSS (hero card, badges, etc — mode-independent) ──
_SHARED_CSS = """
/* ── HERO CARD ── */
.hero-card {
    background:
        radial-gradient(circle at 20% 60%, rgba(255,255,255,0.04), transparent 50%),
        linear-gradient(135deg, #145a42 0%, #1e8a65 45%, #43C59A 100%);
    border-radius: 1rem;
    padding: 2.5rem 2.25rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}

/* Subtle Batik Mandala Ornament on the right */
.hero-card::before {
    content: "";
    position: absolute;
    top: 0;
    right: 0;
    width: 60%;
    height: 100%;
    opacity: 0.05;
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='80' height='80' viewBox='0 0 80 80'%3E%3Cg fill='%23ffffff'%3E%3Cpath d='M40 0l40 40-40 40L0 40z'/%3E%3Ccircle cx='40' cy='40' r='20' stroke='%23ffffff' stroke-width='2' fill='none'/%3E%3Ccircle cx='40' cy='40' r='35' stroke='%23ffffff' stroke-width='1' stroke-dasharray='4,4' fill='none'/%3E%3C/g%3E%3C/svg%3E");
    background-repeat: repeat;
    mask-image: linear-gradient(to left, rgba(0, 0, 0, 1) 30%, rgba(0, 0, 0, 0) 100%);
    -webkit-mask-image: linear-gradient(to left, rgba(0, 0, 0, 1) 30%, rgba(0, 0, 0, 0) 100%);
    pointer-events: none;
}

/* Floating Concentric Glowing Rings */
.hero-card::after {
    content: "";
    position: absolute;
    top: 50%;
    right: -100px;
    transform: translateY(-50%);
    width: 420px;
    height: 420px;
    background: 
        radial-gradient(circle, transparent 65%, rgba(255, 255, 255, 0.08) 66%, rgba(255, 255, 255, 0.08) 67%, transparent 68%),
        radial-gradient(circle, transparent 48%, rgba(255, 255, 255, 0.06) 49%, rgba(255, 255, 255, 0.06) 50%, transparent 51%),
        radial-gradient(circle, transparent 32%, rgba(255, 255, 255, 0.05) 33%, rgba(255, 255, 255, 0.05) 34%, transparent 35%),
        radial-gradient(circle, rgba(255, 255, 255, 0.12) 0%, rgba(255, 255, 255, 0) 60%);
    pointer-events: none;
    border-radius: 50%;
}
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    color: #ffffff;
    font-size: 0.65rem;
    font-weight: 700;
    padding: 0.3rem 0.85rem;
    border-radius: 2rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 1rem;
    backdrop-filter: blur(4px);
}
.hero-title {
    color: #ffffff !important;
    font-size: 1.85rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em !important;
    margin: 0 0 0.5rem 0 !important;
    line-height: 1.2 !important;
}
.hero-desc {
    color: rgba(255,255,255,0.8);
    font-size: 0.9rem;
    line-height: 1.6;
    margin: 0;
    max-width: 600px;
}

/* ── Q BADGE ── */
.q-badge {
    display: inline-block;
    background: linear-gradient(135deg, #43C59A 0%, #208f6b 100%);
    color: #ffffff;
    font-size: 0.65rem;
    font-weight: 700;
    padding: 0.3rem 0.85rem;
    border-radius: 0.375rem;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

/* ── DATASET BOX (sidebar) ── */
.dataset-box {
    background: rgba(67, 197, 154, 0.12);
    border: 1px solid rgba(67, 197, 154, 0.25);
    border-radius: 0.5rem;
    padding: 0.65rem 0.85rem;
    margin-top: 0.5rem;
}
.dataset-box .ds-label {
    font-size: 0.6rem;
    font-weight: 700;
    color: #43C59A;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 0.2rem;
}
.dataset-box .ds-value {
    font-size: 0.78rem;
    font-weight: 500;
}
"""

# ────────────────────────────────────────────────────────────
# LIGHT MODE CSS
# ────────────────────────────────────────────────────────────
LIGHT_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

{_SHARED_CSS}

/* ── BASE ── */
html, body, [class*="css"], .stApp {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: #f0f7f4 !important;
    color: #1a2e28 !important;
}}
.stApp {{ background-color: #f0f7f4 !important; }}

/* ── SIDEBAR (dark green gradient) ── */
section[data-testid="stSidebar"] {{
    background: 
        radial-gradient(circle at 10% 10%, rgba(255, 255, 255, 0.06) 0%, transparent 60%),
        radial-gradient(circle at 90% 90%, rgba(67, 197, 154, 0.1) 0%, transparent 50%),
        url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='80' height='80' viewBox='0 0 80 80'%3E%3Cg fill='%23ffffff' fill-opacity='0.02'%3E%3Cpath d='M40 0l40 40-40 40L0 40z'/%3E%3Ccircle cx='40' cy='40' r='20' stroke='%23ffffff' stroke-width='1' stroke-opacity='0.015' fill='none'/%3E%3C/g%3E%3C/svg%3E") repeat,
        linear-gradient(180deg, #1a7a5a 0%, #0f4a35 100%) !important;
    border-right: none !important;
}}
section[data-testid="stSidebar"] * {{ color: #e3ede9 !important; }}

/* ── SIDEBAR INPUT OVERRIDES (LIGHT MODE LEGIBILITY & TRANSLUCENCY) ── */
/* Center the labels */
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {{
    text-align: center !important;
    justify-content: center !important;
    width: 100% !important;
    display: flex !important;
    margin-bottom: 0.5rem !important;
    color: #ffffff !important;
}}

/* Translucent File Uploader Card */
section[data-testid="stSidebar"] [data-testid="stFileUploader"] {{
    background-color: rgba(67, 197, 154, 0.12) !important;
    border: 1px solid rgba(67, 197, 154, 0.25) !important;
    border-radius: 0.75rem !important;
    padding: 1rem !important;
}}
/* Make inner dropzone transparent */
section[data-testid="stSidebar"] [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] {{
    background-color: transparent !important;
    border: none !important;
}}
/* Make uploader fonts white (#ffffff) for maximum legibility */
section[data-testid="stSidebar"] [data-testid="stFileUploader"] [data-testid="stWidgetLabel"] * {{
    color: #ffffff !important;
}}
section[data-testid="stSidebar"] [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] * {{
    color: #ffffff !important;
}}
section[data-testid="stSidebar"] [data-testid="stFileUploader"] svg {{
    fill: #ffffff !important;
}}
/* Premium styled Browse Files button */
section[data-testid="stSidebar"] [data-testid="stFileUploader"] button {{
    background-color: #43C59A !important;
    border: none !important;
    border-radius: 0.5rem !important;
    padding: 0.5rem 1rem !important;
}}
section[data-testid="stSidebar"] [data-testid="stFileUploader"] button * {{
    color: #0f4a35 !important;
    font-weight: 700 !important;
}}
section[data-testid="stSidebar"] [data-testid="stFileUploader"] button:hover {{
    background-color: #33b087 !important;
}}

/* Translucent Selectbox and Multiselect Cards */
section[data-testid="stSidebar"] .stSelectbox > div > div,
section[data-testid="stSidebar"] .stMultiSelect > div > div,
section[data-testid="stSidebar"] div[data-baseweb="select"],
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {{
    background-color: rgba(67, 197, 154, 0.12) !important;
    border: 1px solid rgba(67, 197, 154, 0.25) !important;
    border-radius: 0.75rem !important;
}}
section[data-testid="stSidebar"] .stSelectbox * {{
    color: #e3ede9 !important;
}}
section[data-testid="stSidebar"] .stMultiSelect * {{
    color: #e3ede9 !important;
}}
/* Solid brand green multiselect chips */
section[data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"] {{
    background-color: #43C59A !important;
    color: #1a2e28 !important;
    border-radius: 4px !important;
}}
section[data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"] * {{
    color: #1a2e28 !important;
}}

/* ── PREMIUM CLEAN NAVIGATION (NO BULLETS) ── */
section[data-testid="stSidebar"] .stRadio div[aria-checked] {{
    display: none !important;
}}
section[data-testid="stSidebar"] .stRadio label {{
    display: flex !important;
    align-items: center !important;
    padding: 0.6rem 0.9rem !important;
    margin-bottom: 0.35rem !important;
    border-radius: 8px !important;
    background-color: transparent !important;
    border: 1px solid transparent !important;
    border-left: 4px solid transparent !important;
    transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1) !important;
    cursor: pointer !important;
}}
section[data-testid="stSidebar"] .stRadio label:hover {{
    background-color: rgba(255, 255, 255, 0.08) !important;
    transform: translateY(-2px) translateX(2px) !important;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15) !important;
}}
section[data-testid="stSidebar"] .stRadio label:hover [aria-checked] + div {{
    color: #ffffff !important;
}}
section[data-testid="stSidebar"] .stRadio label:has([aria-checked="true"]) {{
    background-color: rgba(255, 255, 255, 0.15) !important;
    border-left: 4px solid #43C59A !important;
}}
section[data-testid="stSidebar"] .stRadio [aria-checked="true"] + div {{
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 0.94rem !important;
}}
section[data-testid="stSidebar"] .stRadio [aria-checked="false"] + div {{
    font-size: 0.94rem !important;
    color: rgba(255, 255, 255, 0.75) !important;
}}
section[data-testid="stSidebar"] .stRadio > div[role="radiogroup"] {{
    gap: 0.15rem !important;
}}
.dataset-box .ds-value {{ color: rgba(255,255,255,0.85); }}

/* ── HEADINGS ── */
h1, h2, h3, h4 {{
    color: #1a2e28 !important;
    font-weight: 700;
    letter-spacing: -0.025em;
}}

/* ── DIVIDER ── */
hr {{ border-color: #d8ece5 !important; margin: 1.25rem 0; }}

/* ── METRIC CARDS (left border style) ── */
.metric-card {{
    background-color: #ffffff;
    border: 1px solid #d8ece5;
    border-left: 4px solid #43C59A;
    padding: 1.25rem 1.25rem;
    border-radius: 0.75rem;
    text-align: left;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}
.metric-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(67,197,154,0.08);
}}
.metric-card h1 {{ font-size: 2rem; margin: 0 0 0.2rem 0; font-weight: 800; color: #43C59A; }}
.metric-card p  {{ font-size: 0.68rem; margin: 0; color: #6b8a80; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.08em; }}

.metric-card-red {{
    background-color: #ffffff;
    border: 1px solid #d8ece5;
    border-left: 4px solid #e05252;
    padding: 1.25rem 1.25rem;
    border-radius: 0.75rem;
    text-align: left;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}
.metric-card-red:hover {{ transform: translateY(-2px); box-shadow: 0 6px 16px rgba(224,82,82,0.08); }}
.metric-card-red h1 {{ font-size: 2rem; margin: 0 0 0.2rem 0; font-weight: 800; color: #e05252; }}
.metric-card-red p  {{ font-size: 0.68rem; margin: 0; color: #6b8a80; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.08em; }}

.metric-card-green {{
    background-color: #ffffff;
    border: 1px solid #d8ece5;
    border-left: 4px solid #43C59A;
    padding: 1.25rem 1.25rem;
    border-radius: 0.75rem;
    text-align: left;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}
.metric-card-green:hover {{ transform: translateY(-2px); box-shadow: 0 6px 16px rgba(67,197,154,0.08); }}
.metric-card-green h1 {{ font-size: 2rem; margin: 0 0 0.2rem 0; font-weight: 800; color: #43C59A; }}
.metric-card-green p  {{ font-size: 0.68rem; margin: 0; color: #6b8a80; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.08em; }}

.metric-card-orange {{
    background-color: #ffffff;
    border: 1px solid #d8ece5;
    border-left: 4px solid #d4940e;
    padding: 1.25rem 1.25rem;
    border-radius: 0.75rem;
    text-align: left;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}
.metric-card-orange:hover {{ transform: translateY(-2px); box-shadow: 0 6px 16px rgba(212,148,14,0.08); }}
.metric-card-orange h1 {{ font-size: 2rem; margin: 0 0 0.2rem 0; font-weight: 800; color: #d4940e; }}
.metric-card-orange p  {{ font-size: 0.68rem; margin: 0; color: #6b8a80; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.08em; }}

/* ── INSIGHT BOX ── */
.insight-box {{
    background-color: #ffffff !important;
    border: 1px solid #d8ece5 !important;
    border-left: 4px solid #43C59A !important;
    padding: 1.25rem 1.5rem !important;
    border-radius: 0.75rem !important;
    margin: 1.5rem 0 !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.03) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}}
.insight-box:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(67, 197, 154, 0.08) !important;
}}
.insight-box h4 {{ color: #0f7053 !important; margin-bottom: 0.5rem !important; font-size: 0.95rem !important; font-weight: 700 !important; }}
.insight-box p  {{ color: #1a2e28 !important; margin: 0 !important; font-size: 0.88rem !important; line-height: 1.7 !important; }}

/* ── SUMMARY BOX ── */
.summary-box {{
    background: #ffffff !important;
    border: 1px solid #d8ece5 !important;
    border-radius: 0.75rem !important;
    padding: 1.5rem 1.75rem !important;
    margin: 1.5rem 0 !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.03) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}}
.summary-box:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(67, 197, 154, 0.08) !important;
}}
.summary-box h3 {{
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    color: #0f7053 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    margin: 0 0 0.85rem 0 !important;
}}
.summary-box p {{
    font-size: 0.98rem !important;
    color: #1a2e28 !important;
    line-height: 1.7 !important;
    margin: 0 !important;
}}

/* ── STREAMLIT NATIVE ── */
div[data-testid="stMetricValue"] {{ font-size: 1.75rem; font-weight: 700; color: #1a2e28 !important; }}
div[data-testid="stMetricLabel"] {{ font-size: 0.8rem; color: #6b8a80 !important; font-weight: 500; }}

/* ── GRADIENT BUTTON ── */
.stButton > button {{
    background: linear-gradient(135deg, #43C59A 0%, #208f6b 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 0.75rem !important;
    font-weight: 700 !important;
    padding: 0.5rem 1.25rem !important;
    box-shadow: 0 3px 10px rgba(67,197,154,0.15) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}}
.stButton > button:hover {{
    transform: translateY(-1px) !important;
    box-shadow: 0 5px 18px rgba(67,197,154,0.25) !important;
}}

/* ── INPUT / SELECT ── */
.stSelectbox > div > div,
.stMultiSelect > div > div {{
    border: 1px solid #d8ece5 !important;
    border-radius: 0.75rem !important;
    background-color: #ffffff !important;
}}
.stSelectbox > div > div:hover,
.stMultiSelect > div > div:hover {{
    border-color: #43C59A !important;
}}

/* ── SLIDER ── */
.stSlider > div > div > div {{ background-color: #43C59A !important; }}

/* ── CHART CARDS ── */
div[data-testid="stPlotlyChart"] {{
    background-color: #ffffff !important;
    border: 1px solid #d8ece5 !important;
    border-radius: 0.75rem !important;
    padding: 1.25rem !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.03) !important;
    margin-bottom: 1.5rem !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}}
div[data-testid="stPlotlyChart"]:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(67, 197, 154, 0.08) !important;
}}

/* ── DATAFRAME CARDS ── */
.stDataFrame {{
    border: 1px solid #d8ece5 !important;
    border-radius: 0.75rem !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.03) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}}
.stDataFrame:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(67, 197, 154, 0.08) !important;
}}

/* ── ALERT ── */
div[data-testid="stAlert"] {{ border-radius: 0.75rem !important; }}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {{ border-bottom: 1px solid #d8ece5 !important; background-color: transparent !important; }}
.stTabs [data-baseweb="tab"] {{ color: #6b8a80 !important; font-weight: 500; background-color: transparent !important; }}
.stTabs [aria-selected="true"] {{ color: #43C59A !important; border-bottom-color: #43C59A !important; }}

/* ── UPLOAD ── */
[data-testid="stFileUploader"] {{
    border: 1px dashed #d8ece5 !important;
    border-radius: 0.75rem;
    background-color: #ffffff;
}}

/* ── SCROLLBAR ── */
::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: #f0f7f4; }}
::-webkit-scrollbar-thumb {{ background: #d8ece5; border-radius: 3px; }}
::-webkit-scrollbar-thumb:hover {{ background: #43C59A; }}
</style>
"""

# ────────────────────────────────────────────────────────────
# DARK MODE CSS
# ────────────────────────────────────────────────────────────
DARK_CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

{_SHARED_CSS}

/* ── BASE ── */
html, body, [class*="css"], .stApp {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background-color: #060b0a !important;
    background-image:
        radial-gradient(circle at 10% 20%, rgba(67,197,154,0.06) 0%, transparent 40%),
        radial-gradient(circle at 90% 80%, rgba(67,197,154,0.04) 0%, transparent 50%) !important;
    background-attachment: fixed !important;
    color: #e3ede9 !important;
}}
.stApp {{ background-color: #060b0a !important; }}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {{
    background: 
        radial-gradient(circle at 10% 10%, rgba(67, 197, 154, 0.08) 0%, transparent 60%),
        radial-gradient(circle at 90% 90%, rgba(67, 197, 154, 0.06) 0%, transparent 50%),
        url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='80' height='80' viewBox='0 0 80 80'%3E%3Cg fill='%23ffffff' fill-opacity='0.015'%3E%3Cpath d='M40 0l40 40-40 40L0 40z'/%3E%3Ccircle cx='40' cy='40' r='20' stroke='%23ffffff' stroke-width='1' stroke-opacity='0.01' fill='none'/%3E%3C/g%3E%3C/svg%3E") repeat,
        linear-gradient(180deg, #0f4a35 0%, #071f18 100%) !important;
    border-right: none !important;
}}
section[data-testid="stSidebar"] * {{ color: #e3ede9 !important; }}

/* ── SIDEBAR INPUT OVERRIDES (DARK MODE TRANSLUCENCY) ── */
/* Center the labels */
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {{
    text-align: center !important;
    justify-content: center !important;
    width: 100% !important;
    display: flex !important;
    margin-bottom: 0.5rem !important;
    color: #ffffff !important;
}}

/* Translucent File Uploader Card */
section[data-testid="stSidebar"] [data-testid="stFileUploader"] {{
    background-color: rgba(67, 197, 154, 0.12) !important;
    border: 1px solid rgba(67, 197, 154, 0.25) !important;
    border-radius: 0.75rem !important;
    padding: 1rem !important;
}}
/* Make inner dropzone transparent */
section[data-testid="stSidebar"] [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] {{
    background-color: transparent !important;
    border: none !important;
}}
/* Make uploader fonts white (#ffffff) */
section[data-testid="stSidebar"] [data-testid="stFileUploader"] [data-testid="stWidgetLabel"] * {{
    color: #ffffff !important;
}}
section[data-testid="stSidebar"] [data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] * {{
    color: #ffffff !important;
}}
section[data-testid="stSidebar"] [data-testid="stFileUploader"] svg {{
    fill: #ffffff !important;
}}
/* Premium styled Browse Files button */
section[data-testid="stSidebar"] [data-testid="stFileUploader"] button {{
    background-color: #43C59A !important;
    border: none !important;
    border-radius: 0.5rem !important;
    padding: 0.5rem 1rem !important;
}}
section[data-testid="stSidebar"] [data-testid="stFileUploader"] button * {{
    color: #0f4a35 !important;
    font-weight: 700 !important;
}}
section[data-testid="stSidebar"] [data-testid="stFileUploader"] button:hover {{
    background-color: #33b087 !important;
}}

/* Translucent Selectbox and Multiselect Cards */
section[data-testid="stSidebar"] .stSelectbox > div > div,
section[data-testid="stSidebar"] .stMultiSelect > div > div,
section[data-testid="stSidebar"] div[data-baseweb="select"],
section[data-testid="stSidebar"] div[data-baseweb="select"] > div {{
    background-color: rgba(67, 197, 154, 0.12) !important;
    border: 1px solid rgba(67, 197, 154, 0.25) !important;
    border-radius: 0.75rem !important;
}}
section[data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"] {{
    background-color: #43C59A !important;
    color: #060b0a !important;
    border-radius: 4px !important;
}}
section[data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"] * {{
    color: #060b0a !important;
}}

/* ── PREMIUM CLEAN NAVIGATION (NO BULLETS) ── */
section[data-testid="stSidebar"] .stRadio div[aria-checked] {{
    display: none !important;
}}
section[data-testid="stSidebar"] .stRadio label {{
    display: flex !important;
    align-items: center !important;
    padding: 0.6rem 0.9rem !important;
    margin-bottom: 0.35rem !important;
    border-radius: 8px !important;
    background-color: transparent !important;
    border: 1px solid transparent !important;
    border-left: 4px solid transparent !important;
    transition: all 0.22s cubic-bezier(0.4, 0, 0.2, 1) !important;
    cursor: pointer !important;
}}
section[data-testid="stSidebar"] .stRadio label:hover {{
    background-color: rgba(255, 255, 255, 0.08) !important;
    transform: translateY(-2px) translateX(2px) !important;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15) !important;
}}
section[data-testid="stSidebar"] .stRadio label:hover [aria-checked] + div {{
    color: #ffffff !important;
}}
section[data-testid="stSidebar"] .stRadio label:has([aria-checked="true"]) {{
    background-color: rgba(67, 197, 154, 0.15) !important;
    border-left: 4px solid #43C59A !important;
}}
section[data-testid="stSidebar"] .stRadio [aria-checked="true"] + div {{
    color: #43C59A !important;
    font-weight: 700 !important;
    font-size: 0.94rem !important;
}}
section[data-testid="stSidebar"] .stRadio [aria-checked="false"] + div {{
    font-size: 0.94rem !important;
    color: rgba(255, 255, 255, 0.68) !important;
}}
section[data-testid="stSidebar"] .stRadio > div[role="radiogroup"] {{
    gap: 0.15rem !important;
}}
.dataset-box .ds-value {{ color: rgba(255,255,255,0.85); }}

/* ── HEADINGS ── */
h1, h2, h3, h4 {{
    color: #e3ede9 !important;
    font-weight: 700;
    letter-spacing: -0.025em;
}}

/* ── DIVIDER ── */
hr {{ border-color: #182825 !important; margin: 1.25rem 0; }}

/* ── METRIC CARDS ── */
.metric-card {{
    background-color: #0e1615;
    border: 1px solid #182825;
    border-left: 4px solid #43C59A;
    padding: 1.25rem 1.25rem;
    border-radius: 0.75rem;
    text-align: left;
    margin-bottom: 1rem;
    box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}
.metric-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(67,197,154,0.08);
}}
.metric-card h1 {{ font-size: 2rem; margin: 0 0 0.2rem 0; font-weight: 800; color: #43C59A; }}
.metric-card p  {{ font-size: 0.68rem; margin: 0; color: #8ba6a0; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.08em; }}

.metric-card-red {{
    background-color: #0e1615;
    border: 1px solid #182825;
    border-left: 4px solid #f25c5c;
    padding: 1.25rem 1.25rem;
    border-radius: 0.75rem;
    text-align: left;
    margin-bottom: 1rem;
    box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}
.metric-card-red:hover {{ transform: translateY(-2px); box-shadow: 0 8px 24px rgba(242,92,92,0.06); }}
.metric-card-red h1 {{ font-size: 2rem; margin: 0 0 0.2rem 0; font-weight: 800; color: #f25c5c; }}
.metric-card-red p  {{ font-size: 0.68rem; margin: 0; color: #8ba6a0; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.08em; }}

.metric-card-green {{
    background-color: #0e1615;
    border: 1px solid #182825;
    border-left: 4px solid #43C59A;
    padding: 1.25rem 1.25rem;
    border-radius: 0.75rem;
    text-align: left;
    margin-bottom: 1rem;
    box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}
.metric-card-green:hover {{ transform: translateY(-2px); box-shadow: 0 8px 24px rgba(67,197,154,0.08); }}
.metric-card-green h1 {{ font-size: 2rem; margin: 0 0 0.2rem 0; font-weight: 800; color: #43C59A; }}
.metric-card-green p  {{ font-size: 0.68rem; margin: 0; color: #8ba6a0; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.08em; }}

.metric-card-orange {{
    background-color: #0e1615;
    border: 1px solid #182825;
    border-left: 4px solid #e59b3c;
    padding: 1.25rem 1.25rem;
    border-radius: 0.75rem;
    text-align: left;
    margin-bottom: 1rem;
    box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}}
.metric-card-orange:hover {{ transform: translateY(-2px); box-shadow: 0 8px 24px rgba(229,155,60,0.06); }}
.metric-card-orange h1 {{ font-size: 2rem; margin: 0 0 0.2rem 0; font-weight: 800; color: #e59b3c; }}
.metric-card-orange p  {{ font-size: 0.68rem; margin: 0; color: #8ba6a0; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.08em; }}

/* ── INSIGHT BOX ── */
.insight-box {{
    background-color: #0e1615 !important;
    border: 1px solid #182825 !important;
    border-left: 4px solid #43C59A !important;
    padding: 1.25rem 1.5rem !important;
    border-radius: 0.75rem !important;
    margin: 1.5rem 0 !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.2) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}}
.insight-box:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(67, 197, 154, 0.08) !important;
}}
.insight-box h4 {{ color: #43C59A !important; margin-bottom: 0.5rem !important; font-size: 0.95rem !important; font-weight: 700 !important; }}
.insight-box p  {{ color: #e3ede9 !important; margin: 0 !important; font-size: 0.88rem !important; line-height: 1.7 !important; }}

/* ── SUMMARY BOX ── */
.summary-box {{
    background: #0e1615 !important;
    border: 1px solid #182825 !important;
    border-radius: 0.75rem !important;
    padding: 1.5rem 1.75rem !important;
    margin: 1.5rem 0 !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.2) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}}
.summary-box:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(67, 197, 154, 0.08) !important;
}}
.summary-box h3 {{
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    color: #43C59A !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    margin: 0 0 0.85rem 0 !important;
}}
.summary-box p {{
    font-size: 0.98rem !important;
    color: #e3ede9 !important;
    line-height: 1.7 !important;
    margin: 0 !important;
}}

/* ── STREAMLIT NATIVE ── */
div[data-testid="stMetricValue"] {{ font-size: 1.75rem; font-weight: 700; color: #e3ede9 !important; }}
div[data-testid="stMetricLabel"] {{ font-size: 0.8rem; color: #8ba6a0 !important; font-weight: 500; }}

/* ── GRADIENT BUTTON ── */
.stButton > button {{
    background: linear-gradient(135deg, #43C59A 0%, #208f6b 100%) !important;
    color: #060b0a !important;
    border: none !important;
    border-radius: 0.75rem !important;
    font-weight: 700 !important;
    padding: 0.5rem 1.25rem !important;
    box-shadow: 0 3px 10px rgba(67,197,154,0.15) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}}
.stButton > button:hover {{
    transform: translateY(-1px) !important;
    box-shadow: 0 5px 18px rgba(67,197,154,0.25) !important;
}}

/* ── INPUT / SELECT ── */
.stSelectbox > div > div,
.stMultiSelect > div > div {{
    border: 1px solid #182825 !important;
    border-radius: 0.75rem !important;
    background-color: #0e1615 !important;
    color: #e3ede9 !important;
}}
.stSelectbox > div > div:hover,
.stMultiSelect > div > div:hover {{
    border-color: #43C59A !important;
}}

/* ── SLIDER ── */
.stSlider > div > div > div {{ background-color: #43C59A !important; }}

/* ── CHART CARDS ── */
div[data-testid="stPlotlyChart"] {{
    background-color: #0e1615 !important;
    border: 1px solid #182825 !important;
    border-radius: 0.75rem !important;
    padding: 1.25rem !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.2) !important;
    margin-bottom: 1.5rem !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}}
div[data-testid="stPlotlyChart"]:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(67, 197, 154, 0.08) !important;
}}

/* ── DATAFRAME CARDS ── */
.stDataFrame {{
    border: 1px solid #182825 !important;
    border-radius: 0.75rem !important;
    box-shadow: 0 4px 16px rgba(0,0,0,0.2) !important;
    transition: transform 0.2s ease, box-shadow 0.2s ease !important;
}}
.stDataFrame:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(67, 197, 154, 0.08) !important;
}}
[data-testid="stDataFrame"] {{ background-color: #0e1615 !important; }}

/* ── ALERT ── */
div[data-testid="stAlert"] {{ border-radius: 0.75rem !important; border: 1px solid #182825 !important; }}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {{ border-bottom: 1px solid #182825 !important; background-color: transparent !important; }}
.stTabs [data-baseweb="tab"] {{ color: #8ba6a0 !important; font-weight: 500; background-color: transparent !important; }}
.stTabs [aria-selected="true"] {{ color: #43C59A !important; border-bottom-color: #43C59A !important; }}
.stTabs [data-baseweb="tab-panel"] {{ background-color: transparent !important; }}

/* ── UPLOAD ── */
[data-testid="stFileUploader"] {{
    border: 1px dashed #182825 !important;
    border-radius: 0.75rem;
    background-color: #0e1615;
}}

/* ── SCROLLBAR ── */
::-webkit-scrollbar {{ width: 6px; height: 6px; }}
::-webkit-scrollbar-track {{ background: #060b0a; }}
::-webkit-scrollbar-thumb {{ background: #182825; border-radius: 3px; }}
::-webkit-scrollbar-thumb:hover {{ background: #43C59A; }}

/* ── RADIO ACTIVE ── */
.stRadio [aria-checked="true"] + div {{ color: #43C59A !important; }}
</style>
"""

# ── PLOTLY THEMES ──────────────────────────────────────────
DARK_PLOTLY = dict(
    font=dict(family="Inter, sans-serif", color="#e3ede9", size=12),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(t=30, b=30, l=10, r=10),
    xaxis=dict(showgrid=True, gridcolor="#182825", linecolor="#43C59A", zeroline=False, color="#8ba6a0"),
    yaxis=dict(showgrid=True, gridcolor="#182825", linecolor="#43C59A", zeroline=False, color="#8ba6a0"),
    legend=dict(bgcolor="#0e1615", bordercolor="#182825", borderwidth=1, font=dict(size=11, color="#e3ede9")),
    colorway=["#43C59A","#f25c5c","#e59b3c","#60a5fa","#a78bfa","#fb923c"],
)

LIGHT_PLOTLY = dict(
    font=dict(family="Inter, sans-serif", color="#1a2e28", size=12),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(t=30, b=30, l=10, r=10),
    xaxis=dict(showgrid=True, gridcolor="#d8ece5", linecolor="#43C59A", zeroline=False, color="#6b8a80"),
    yaxis=dict(showgrid=True, gridcolor="#d8ece5", linecolor="#43C59A", zeroline=False, color="#6b8a80"),
    legend=dict(bgcolor="#ffffff", bordercolor="#d8ece5", borderwidth=1, font=dict(size=11, color="#1a2e28")),
    colorway=["#43C59A","#dc2626","#d97706","#2563eb","#7c3aed","#ea580c"],
)

# Warna chart per mode
def get_colors(dark: bool):
    if dark:
        return {
            "accent":       "#43C59A",
            "danger":       "#f25c5c",
            "warning":      "#e59b3c",
            "info":         "#60a5fa",
            "diabetes":     "#f25c5c",
            "nondiabetes":  "#43C59A",
            "chart":        ["#43C59A","#f25c5c","#e59b3c","#60a5fa","#a78bfa"],
            "gradient_low": "#182825",
            "gradient_hi":  "#43C59A",
        }
    else:
        return {
            "accent":       "#43C59A",
            "danger":       "#dc2626",
            "warning":      "#d97706",
            "info":         "#2563eb",
            "diabetes":     "#dc2626",
            "nondiabetes":  "#43C59A",
            "chart":        ["#43C59A","#dc2626","#d97706","#2563eb","#7c3aed"],
            "gradient_low": "#e0f5ee",
            "gradient_hi":  "#43C59A",
        }
