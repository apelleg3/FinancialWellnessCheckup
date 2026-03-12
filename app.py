"""
Financial Wellness Checkup — Interactive Assessment Tool
Built with Streamlit | All data processed locally in your session
"""

import streamlit as st
import json
import math
import io
from datetime import date

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Financial Wellness Checkup",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Works with Streamlit dark mode — DO NOT override color-scheme ────────── */

/* ── TYPOGRAPHY — consistent serif headings, sans body ─────────────────── */
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

/* All heading levels get serif */
h1, h2, h3, h4, h5,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4,
.step-title {
    font-family: 'DM Serif Display', serif !important;
    letter-spacing: -0.01em;
}
/* h4 size and color */
[data-testid="stMarkdownContainer"] h4,
h4 {
    font-size: 1.15rem !important;
    color: #F0EBFF !important;
    margin-bottom: 0.5rem !important;
}
/* Bold text stays sans-serif (it's body copy, not headings) */
[data-testid="stMarkdownContainer"] strong {
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600;
}
/* Labels on inputs use sans-serif */
[data-testid="stNumberInput"] label,
[data-testid="stSelectbox"] label,
[data-testid="stSlider"] label,
[data-testid="stTextInput"] label,
[data-testid="stRadio"] label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
}

/* Layout */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
.block-container { max-width: 820px; padding-top: 2rem; padding-bottom: 4rem; }

/* ── App header ── */
.app-header {
    background: linear-gradient(135deg, #2D1B5E 0%, #5B2FA0 100%);
    border-radius: 16px;
    padding: 2rem 2.5rem 1.75rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 24px rgba(91,47,160,0.35);
}
.app-header h1 { color: #F0EBFF; margin: 0; font-size: 2rem; font-family: 'DM Serif Display', serif; }
.app-header p  { color: #C9B8F5; margin: 0.4rem 0 0; font-size: 1rem; }

/* ── Progress bar ── */
.progress-wrap  { margin: 0 0 1.75rem; }
.progress-label { display:flex; justify-content:space-between; font-size:0.78rem; color:#A89BC2; margin-bottom:5px; }
.progress-label strong { color:#C084FC; }
.progress-track { background:#2A1D4E; border-radius:99px; height:8px; overflow:hidden; }
.progress-fill  { background:linear-gradient(90deg,#7C3AED,#C084FC); height:100%; border-radius:99px; transition:width 0.4s ease; }

/* ── Step title / subtitle ── */
.step-title    { font-family:'DM Serif Display',serif; font-size:1.7rem; color:#F0EBFF; margin:0 0 0.25rem; }
.step-subtitle { color:#C9B8F5; font-size:0.92rem; margin-bottom:1.5rem; line-height:1.55; }

/* ── Cards ── */
.card {
    background: #1A1033;
    border-radius: 14px;
    padding: 1.25rem 1.5rem;
    border: 1px solid #3D2B6B;
    margin-bottom: 1rem;
}
.card-green  { border-left:4px solid #4ADE80; background:#0D2818; }
.card-amber  { border-left:4px solid #FCD34D; background:#1A1200; }
.card-red    { border-left:4px solid #F87171; background:#1A0A0A; }
.card-blue   { border-left:4px solid #A78BFA; background:#1A1033; }
.card-purple { border-left:4px solid #A78BFA; background:#1A1033; }
.card-slate  { border-left:4px solid #6B7280; background:#1A1A2E; }

/* ── KPI grid ── */
.kpi-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(130px,1fr)); gap:0.85rem; margin:1rem 0; }
.kpi-box  { background:#0E0A1E; border-radius:10px; padding:0.9rem; border:1px solid #3D2B6B; text-align:center; }
.kpi-box .label { font-size:0.7rem; color:#A89BC2; text-transform:uppercase; letter-spacing:0.05em; font-weight:600; }
.kpi-box .value { font-size:1.45rem; font-weight:700; color:#F0EBFF; margin-top:3px; }

/* ── Citation ── */
.citation {
    font-size:0.78rem;
    color:#A89BC2;
    background:#0E0A1E;
    border-radius:8px;
    padding:0.85rem 1rem;
    margin-top:1rem;
    border-left:3px solid #7C3AED;
    line-height:1.6;
}
.citation a { color:#C084FC; }
.citation strong { color:#D4C8F0; }

/* ── Nav buttons ── */
.stButton > button {
    border-radius:10px !important;
    font-weight:600 !important;
    font-family:'DM Sans',sans-serif !important;
    transition:all 0.2s !important;
    font-size:0.95rem !important;
}
div[data-testid="column"]:first-child .stButton > button {
    background:#1A1033 !important;
    color:#C9B8F5 !important;
    border:2px solid #3D2B6B !important;
}
div[data-testid="column"]:last-child .stButton > button {
    background:linear-gradient(135deg,#5B2FA0,#7C3AED) !important;
    color:#F0EBFF !important;
    border:none !important;
}

/* ── Divider ── */
.divider { border:none; border-top:1px solid #3D2B6B; margin:1.75rem 0; }

/* ── Action items ── */
.action-item {
    display:flex; gap:12px; align-items:flex-start;
    background:#1A1033; border-radius:12px;
    padding:1rem 1.2rem; margin-bottom:0.75rem;
    border:1px solid #3D2B6B;
}
.action-icon { font-size:1.3rem; flex-shrink:0; }
.action-text strong { display:block; font-size:0.92rem; color:#F0EBFF; margin-bottom:4px; }
.action-text span   { font-size:0.85rem; color:#C9B8F5; line-height:1.5; }

/* ── Badges ── */
.badge { display:inline-block; font-size:0.68rem; font-weight:700; padding:2px 9px; border-radius:99px; margin-left:6px; text-transform:uppercase; letter-spacing:0.06em; }
.badge-critical { background:#3D0A0A; color:#FCA5A5; border:1px solid #F87171; }
.badge-high     { background:#2A1E00; color:#FDE68A; border:1px solid #FCD34D; }
.badge-medium   { background:#1A1033; color:#C4B5FD; border:1px solid #A78BFA; }
.badge-good     { background:#082010; color:#86EFAC; border:1px solid #4ADE80; }

/* ── Benchmark table ── */
.bench-table { width:100%; border-collapse:collapse; font-size:0.85rem; margin-top:0.5rem; }
.bench-table th { background:#2D1B5E; color:#F0EBFF; padding:10px 14px; text-align:left; font-weight:600; }
.bench-table td { padding:9px 14px; border-bottom:1px solid #2A1D4E; color:#D4C8F0; background:#1A1033; }
.bench-table tr.highlight td { background:#2D1B5E; font-weight:700; color:#F0EBFF; }
.bench-table tr:hover td { background:#1E1340; }

/* ── CFPB instrument ── */
.cfpb-part-header {
    background:#2D1B5E;
    color:#F0EBFF;
    border-radius:10px 10px 0 0;
    padding:0.85rem 1.2rem;
    font-weight:600;
    font-size:0.95rem;
    margin-top:1.5rem;
    line-height:1.4;
    border:1px solid #3D2B6B;
    border-bottom:none;
}
.cfpb-q-label {
    font-size:0.95rem;
    color:#F0EBFF;
    font-weight:600;
    margin:1rem 0 0.4rem;
    line-height:1.5;
}

/* ── BLS hint ── */
.bls-hint {
    font-size:0.78rem;
    color:#C4B5FD;
    background:#1A1033;
    border-radius:6px;
    padding:0.4rem 0.75rem;
    margin-bottom:0.75rem;
    border-left:3px solid #7C3AED;
}

/* ═══════════════════════════════════════════════════════════════════════════
   LIGHT MODE OVERRIDE
   When the user's browser / OS is in light mode, Streamlit may render a
   light background. These rules force our dark palette onto every surface
   so text always has sufficient contrast regardless of system settings.
   ═══════════════════════════════════════════════════════════════════════════ */
@media (prefers-color-scheme: light) {
    /* Page backgrounds */
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    section[data-testid="stMain"] > div,
    .main, .block-container,
    html, body {
        background-color: #0E0A1E !important;
        color: #F0EBFF !important;
    }
    /* All plain text */
    p, span, li, td, th, label, div,
    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stMarkdownContainer"] span {
        color: #D4C8F0 !important;
    }
    /* Headings */
    h1, h2, h3, h4, .step-title,
    [data-testid="stMarkdownContainer"] h1,
    [data-testid="stMarkdownContainer"] h2,
    [data-testid="stMarkdownContainer"] h3,
    [data-testid="stMarkdownContainer"] h4 {
        color: #F0EBFF !important;
    }
    /* Input widgets */
    [data-testid="stNumberInput"] input,
    [data-testid="stTextInput"] input,
    [data-baseweb="input"] input,
    [data-baseweb="select"] > div {
        background-color: #1A1033 !important;
        color: #F0EBFF !important;
        border-color: #3D2B6B !important;
    }
    /* Radio / checkbox labels */
    [data-testid="stRadio"] label span,
    [data-testid="stCheckbox"] label span {
        color: #D4C8F0 !important;
    }
    /* Selectbox text */
    [data-baseweb="select"] * { color: #F0EBFF !important; background-color: #1A1033 !important; }
    /* Captions */
    [data-testid="stCaptionContainer"] p,
    .stCaption { color: #A89BC2 !important; }
    /* Number input stepper buttons */
    [data-testid="stNumberInput"] button { color: #C084FC !important; }
    /* Slider */
    [data-testid="stSlider"] [data-baseweb="slider"] div { background: #3D2B6B !important; }
    /* Info / warning / error boxes */
    [data-testid="stAlert"] { background-color: #1A1033 !important; color: #D4C8F0 !important; }
    /* Our custom HTML elements — these have explicit background/color so they
       already work in both modes; no override needed for .card, .kpi-box etc. */
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
DEFAULTS = {
    "step": 0,
    # Demographics
    "age": 35, "salary": 60000, "ret_age": 67, "region": "U.S. National Average",
    # Goals
    "goals": [],
    "custom_goals": [],  # list of {"text": str, "horizon": str}
    # CFPB Well-Being (10 items, stored as score values with _score suffix)
    # Default: middle option for each item
    "cfpb": {f"q{i+1}_score": v[2] for i, (_, _, v) in enumerate([
        ("", "agree", [4,3,2,1,0]), ("", "agree", [4,3,2,1,0]),
        ("", "agree", [0,1,2,3,4]), ("", "agree", [4,3,2,1,0]),
        ("", "agree", [0,1,2,3,4]), ("", "agree", [0,1,2,3,4]),
        ("", "freq",  [0,1,2,3,4]), ("", "freq",  [4,3,2,1,0]),
        ("", "freq",  [0,1,2,3,4]), ("", "freq",  [0,1,2,3,4]),
    ])},
    # Confidence (8 areas)
    "conf": {
        "daily": 3, "emergency": 3, "saving": 3, "investing": 3,
        "retirement": 3, "insurance": 3, "tax": 3, "estate": 3,
    },
    # Net Worth
    "nw": {
        "cash": 0, "savings_nw": 0, "investments": 0,
        "retirement_accts": 0, "home": 0, "vehicle": 0,
        "cc_debt": 0, "student": 0, "auto_loan": 0,
        "mortgage": 0, "personal_loan": 0, "other_debt": 0,
    },
    # Cash Flow
    "income_net": 4500,
    "exp": {
        "housing": 1200, "utilities": 150, "transport": 400,
        "insurance": 250, "debt_min": 150,
        "groceries": 400, "entertainment": 200,
        "personal": 100, "other_flex": 100,
    },
    "occ_annual": 1800,
    # Emergency Fund
    "ef": 5000,
    # Retirement
    "ret_current": 40000,
    "ret_monthly": 400,
    "ret_return": 7.0,
}

for k, v in DEFAULTS.items():
    if k not in st.session_state:
        st.session_state[k] = v if not isinstance(v, dict) else {**v}

def ss(key): return st.session_state[key]
def ss_set(key, val): st.session_state[key] = val

# ─────────────────────────────────────────────
# DATA & BENCHMARKS
# ─────────────────────────────────────────────

# Federal Reserve SCF 2022 net worth by age (median, p75)
NW_BENCH = {
    "Under 35": (39_000, 155_000),
    "35–44":    (135_600, 461_000),
    "45–54":    (247_200, 742_000),
    "55–64":    (364_500, 1_166_000),
    "65–74":    (410_000, 1_217_000),
    "75+":      (335_600, 1_071_000),
}

# Fidelity retirement savings multiples by age
FIDELITY_MULT = {
    30: 1, 35: 2, 40: 3, 45: 4, 50: 6, 55: 7, 60: 8, 65: 9, 67: 10
}

# SCF 2022 median retirement savings by age
SCF_RET = {
    "Under 35": 18_880,
    "35–44":    45_000,
    "45–54":    115_000,
    "55–64":    185_000,
    "65–74":    200_000,
    "75+":      130_000,
}

def age_bracket(age):
    if age < 35:  return "Under 35"
    if age < 45:  return "35–44"
    if age < 55:  return "45–54"
    if age < 65:  return "55–64"
    if age < 75:  return "65–74"
    return "75+"

def fidelity_multiple(age):
    """Linear interpolation between Fidelity milestones."""
    ages = sorted(FIDELITY_MULT.keys())
    if age <= ages[0]:  return FIDELITY_MULT[ages[0]]
    if age >= ages[-1]: return FIDELITY_MULT[ages[-1]]
    for i in range(len(ages) - 1):
        a0, a1 = ages[i], ages[i+1]
        if a0 <= age <= a1:
            frac = (age - a0) / (a1 - a0)
            return FIDELITY_MULT[a0] + frac * (FIDELITY_MULT[a1] - FIDELITY_MULT[a0])
    return 10

def cfpb_raw_to_score(raw_total, age=None):
    """
    Official CFPB lookup table (self-administered questionnaire).
    Raw response value range: 0–40.
    Scores differ for age 18–61 vs. 62+.
    Source: CFPB Financial Well-Being Scale Scoring Worksheet (2017).
    """
    # {raw: (score_18_61, score_62_plus)}
    LOOKUP = {
        0:  (14, 14),  1:  (19, 20),  2:  (22, 24),  3:  (25, 26),
        4:  (27, 29),  5:  (29, 31),  6:  (31, 33),  7:  (32, 35),
        8:  (34, 36),  9:  (35, 38), 10:  (37, 39), 11:  (38, 41),
        12: (40, 42), 13:  (41, 44), 14:  (42, 45), 15:  (44, 46),
        16: (45, 48), 17:  (46, 49), 18:  (47, 50), 19:  (49, 52),
        20: (50, 53), 21:  (51, 54), 22:  (52, 56), 23:  (54, 57),
        24: (55, 58), 25:  (56, 60), 26:  (58, 61), 27:  (59, 63),
        28: (60, 64), 29:  (62, 66), 30:  (63, 67), 31:  (65, 69),
        32: (66, 71), 33:  (68, 73), 34:  (69, 75), 35:  (71, 77),
        36: (73, 79), 37:  (75, 82), 38:  (78, 84), 39:  (81, 88),
        40: (86, 95),
    }
    r = max(0, min(40, int(raw_total)))
    s_young, s_older = LOOKUP.get(r, (50, 50))
    if age is not None and age >= 62:
        return s_older
    return s_young

def cfpb_age_median(age):
    """
    CFPB (2017) Financial Well-Being in America — median scores by age group.
    Self-administered. Source: Table 1, CFPB Financial Well-Being in America report.
    """
    if age < 25:  return 51
    if age < 35:  return 52
    if age < 45:  return 54
    if age < 55:  return 54
    if age < 62:  return 55
    if age < 70:  return 59
    return 62

def monthly_expenses():
    exp = ss("exp")
    total = sum(exp.get(k, 0) for k in [
        "housing", "utilities", "transport", "insurance", "debt_min",
        "groceries", "entertainment", "personal", "other_flex"
    ])
    occ = ss("occ_annual") / 12
    return total + occ

def net_worth():
    nw = ss("nw")
    assets = sum([nw.get(k, 0) for k in
                  ("cash", "savings_nw", "investments", "retirement_accts", "home", "vehicle")])
    liabs  = sum([nw.get(k, 0) for k in
                  ("cc_debt", "student", "auto_loan", "mortgage", "personal_loan", "other_debt")])
    return assets, liabs, assets - liabs

def future_value(pv, pmt_monthly, annual_rate, years):
    if years <= 0: return pv
    r = annual_rate / 100 / 12
    n = years * 12
    if r == 0:
        return pv + pmt_monthly * n
    fv_pv  = pv  * (1 + r) ** n
    fv_pmt = pmt_monthly * ((1 + r) ** n - 1) / r
    return fv_pv + fv_pmt

def savings_rate():
    income = ss("income_net")
    exp    = monthly_expenses()
    surplus= income - exp
    gross_mo = ss("salary") / 12
    if gross_mo == 0: return 0, 0
    return surplus, (surplus / gross_mo) * 100

# ─────────────────────────────────────────────
# GOAL CATALOG (from Fisher & Montalto, 2010)
# ─────────────────────────────────────────────
GOAL_CATS = {
    "Short-Term (0–2 years)": [
        "Build or replenish emergency fund",
        "Pay off high-interest credit card debt",
        "Create or update a written budget",
        "Save for a vacation or major purchase",
        "Improve my credit score",
    ],
    "Medium-Term (3–5 years)": [
        "Save for a home down payment",
        "Pay off student loan debt",
        "Pay off auto loan",
        "Save for a wedding or major life event",
        "Start or grow a business",
        "Change careers or pursue additional education",
    ],
    "Long-Term (5+ years)": [
        "Maintain standard of living in retirement",
        "Save for children's or grandchildren's education",
        "Achieve financial independence / FIRE",
        "Pay off mortgage early",
        "Leave an inheritance or legacy",
        "Support aging parents or family members",
    ],
    "Ongoing Financial Security": [
        "Protect against major financial setbacks",
        "Ensure adequate insurance coverage (life, disability, umbrella)",
        "Minimize tax liability",
        "Diversify investments across asset classes",
        "Build generational wealth",
    ],
}

# Reverse lookup: goal text → its category/horizon label
GOAL_HORIZON_MAP = {
    goal: cat
    for cat, items in GOAL_CATS.items()
    for goal in items
}


# Official wording from CFPB Financial Well-Being Scale Questionnaire (2017)
# ─────────────────────────────────────────────

# Part 1 response options (left→right on paper = Completely→Not at all)
# We present them left-to-right: Completely, Very well, Somewhat, Very little, Not at all
CFPB_AGREE_OPTS  = ["Completely", "Very well", "Somewhat", "Very little", "Not at all"]
# Scored values for Part 1 (forward): Completely=4, Very well=3, Somewhat=2, Very little=1, Not at all=0
CFPB_AGREE_FWD   = [4, 3, 2, 1, 0]
# Scored values for Part 1 (reverse): Completely=0, Very well=1, Somewhat=2, Very little=3, Not at all=4
CFPB_AGREE_REV   = [0, 1, 2, 3, 4]

# Part 2 response options
CFPB_FREQ_OPTS   = ["Always", "Often", "Sometimes", "Rarely", "Never"]
# Scored values for Part 2 (forward): Always=4, Often=3, Sometimes=2, Rarely=1, Never=0
CFPB_FREQ_FWD    = [4, 3, 2, 1, 0]
# Scored values for Part 2 (reverse): Always=0, Often=1, Sometimes=2, Rarely=3, Never=4
CFPB_FREQ_REV    = [0, 1, 2, 3, 4]

# (statement_text, part, score_values_list)
# part = "agree" → Part 1 options; part = "freq" → Part 2 options
CFPB_ITEMS = [
    ("I could handle a major unexpected expense.",
     "agree", CFPB_AGREE_FWD),
    ("I am securing my financial future.",
     "agree", CFPB_AGREE_FWD),
    ("Because of my money situation, I feel like I will never have the things I want in life.",
     "agree", CFPB_AGREE_REV),
    ("I can enjoy life because of the way I'm managing my money.",
     "agree", CFPB_AGREE_FWD),
    ("I am just getting by financially.",
     "agree", CFPB_AGREE_REV),
    ("I am concerned that the money I have or will save won't last.",
     "agree", CFPB_AGREE_REV),
    ("Giving a gift for a wedding, birthday, or other occasion would put a strain on my finances for the month.",
     "freq",  CFPB_FREQ_REV),
    ("I have money left over at the end of the month.",
     "freq",  CFPB_FREQ_FWD),
    ("I am behind with my finances.",
     "freq",  CFPB_FREQ_REV),
    ("My finances control my life.",
     "freq",  CFPB_FREQ_REV),
]

# ─────────────────────────────────────────────
# BLS CONSUMER EXPENDITURE SURVEY 2022 — Monthly averages by region
# Source: U.S. Bureau of Labor Statistics, Consumer Expenditure Survey, 2022.
# Table 1101. Quintiles of income before taxes: Annual expenditure means.
# Regional data from BLS CE Survey 2022 regional tables (annual ÷ 12).
# ─────────────────────────────────────────────
BLS_MONTHLY = {
    # (shelter/mortgage, utilities, transport, groceries, dining_out, healthcare, entertainment, personal_care)
    # Source: BLS Consumer Expenditure Survey 2022, annual regional means ÷ 12
    "U.S. National Average": (1208, 385, 1025, 475, 303, 488, 288, 64),
    "U.S. Northeast":        (1452, 420, 1010, 540, 335, 460, 300, 72),
    "U.S. Midwest":          (1038, 418, 1058, 452, 268, 528, 268, 60),
    "U.S. South":            (1095, 408, 1082, 445, 288, 498, 262, 58),
    "U.S. West":             (1548, 378, 1092, 495, 355, 510, 338, 74),
}

def bls_hint(region, field):
    """Return a BLS average monthly dollar amount for the given field."""
    keys = ["housing", "utilities", "transport", "groceries",
            "dining_out", "healthcare", "entertainment", "personal_care"]
    vals = BLS_MONTHLY.get(region, BLS_MONTHLY["U.S. National Average"])
    if field in keys:
        amt = vals[keys.index(field)]
        return f'<div class="bls-hint">BLS national avg (2022): ~${amt:,}/mo for {region}</div>'
    return ""

# ─────────────────────────────────────────────
# PROGRESS HEADER
# ─────────────────────────────────────────────
STEPS = [
    "Welcome", "About You", "Goal Setting", "Well-Being Scale",
    "Your Score", "Financial Confidence", "Net Worth", "Cash Flow",
    "Emergency Fund", "Retirement", "Action Plan"
]

def render_header():
    st.markdown("""
    <div class="app-header">
        <h1>💰 Financial Wellness Checkup</h1>
        <p>A research-based interactive assessment of your financial health and well-being</p>
    </div>
    """, unsafe_allow_html=True)

def render_progress():
    step  = ss("step")
    total = len(STEPS)
    pct   = int((step + 1) / total * 100)
    label = STEPS[step]
    st.markdown(f"""
    <div class="progress-wrap">
        <div class="progress-label">
            <span>Step {step+1} of {total} — <strong>{label}</strong></span>
            <span>{pct}%</span>
        </div>
        <div class="progress-track">
            <div class="progress-fill" style="width:{pct}%"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def nav_buttons(back_label="← Back", next_label="Next →", hide_back=False):
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1])
    with c1:
        if not hide_back and ss("step") > 0:
            if st.button(back_label, use_container_width=True, key="nav_back"):
                ss_set("step", ss("step") - 1)
                st.rerun()
    with c2:
        if ss("step") < len(STEPS) - 1:
            if st.button(next_label, use_container_width=True, key="nav_next"):
                ss_set("step", ss("step") + 1)
                st.rerun()

def fmt_dollar(n):
    if abs(n) >= 1_000_000:
        return f"${n/1_000_000:.2f}M"
    if abs(n) >= 1_000:
        return f"${n:,.0f}"
    return f"${n:.0f}"

def metric_bar(label, val, max_val, color="#A78BFA", suffix=""):
    pct = min(100, max(0, val / max_val * 100)) if max_val else 0
    st.markdown(f"""
    <div class="metric-bar-wrap">
        <div class="metric-bar-label"><span>{label}</span><span><strong>{val:.1f}{suffix}</strong></span></div>
        <div class="metric-bar-track">
            <div class="metric-bar-fill" style="width:{pct:.1f}%;background:{color};border-radius:99px;height:10px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# STEP 0 — WELCOME
# ─────────────────────────────────────────────
def step_welcome():
    render_header()
    render_progress()

    st.markdown("""
    <p class="step-subtitle">
        This tool combines <strong>subjective well-being</strong> (how you feel about money) with
        <strong>objective financial health</strong> (net worth, cash flow, retirement readiness) to
        give you a complete picture — and a personalized action plan.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card card-blue">
        <strong>📋 What you'll complete:</strong>
        <ul style="margin:0.5rem 0 0; padding-left:1.2rem; color:#C084FC; font-size:0.9rem;">
            <li>Demographic profile &amp; goal-setting activity</li>
            <li>CFPB Financial Well-Being Scale (validated 10-item instrument)</li>
            <li>Financial confidence self-assessment</li>
            <li>Net worth calculation with peer benchmarks</li>
            <li>Cash flow &amp; savings rate analysis</li>
            <li>Emergency fund adequacy check</li>
            <li>Retirement readiness projection</li>
            <li>Personalized, evidence-based action plan</li>
        </ul>
        <span style="font-size:0.88rem;color:#FCD34D;"><i>Gathering financial information prior to starting will reduce completion time.</i></span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="card card-amber">
            <strong>⏱ Time required</strong><br>
            <span style="font-size:0.88rem;color:#FCD34D;">10–15 minutes</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="card card-green">
            <strong>🔒 Privacy</strong><br>
            <span style="font-size:0.88rem;color:#4ADE80;">All data stays in your browser session</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card card-slate">
        <strong>About Benchmarks in This Tool</strong><br><br>
        <span style="font-size:0.88rem;color:#D4C8F0;">
        <strong>Descriptive benchmarks</strong> (What others have) — drawn from Federal Reserve Survey of Consumer Finances data.
        Shows where you stand relative to peers. <em>Note: Most Americans are under-saved for retirement, so "average" ≠ "on track."</em><br><br>
        <strong>Prescriptive benchmarks</strong> (What you need) — research-based goals from Fidelity, actuarial science, and
        retirement income studies. These reflect what's actually needed for financial security.
        </span>
    </div>
    """, unsafe_allow_html=True)

    nav_buttons(hide_back=True, next_label="Begin Assessment →")

# ─────────────────────────────────────────────
# STEP 1 — DEMOGRAPHICS
# ─────────────────────────────────────────────
def step_demographics():
    render_header(); render_progress()
    st.markdown('<p class="step-title">About You</p>', unsafe_allow_html=True)
    st.markdown('<p class="step-subtitle">Basic information to personalize your benchmarks and recommendations.</p>', unsafe_allow_html=True)

    age = st.number_input("Your current age", 18, 80, ss("age"), step=1)
    ss_set("age", age)

    sal = st.number_input("Annual gross salary ($, before taxes)", 0, 2_000_000,
                          ss("salary"), step=1000, format="%d")
    ss_set("salary", sal)

    ret_age = st.number_input("Target retirement age", age + 1, 80,
                              max(age + 1, ss("ret_age")), step=1)
    ss_set("ret_age", ret_age)

    REGIONS = [
        "U.S. National Average",
        "U.S. Northeast",
        "U.S. Midwest",
        "U.S. South",
        "U.S. West",
        "Outside the U.S. (skip spending benchmarks)",
    ]
    current_region = ss("region")
    if current_region not in REGIONS:
        # handle old "Outside the United States" key
        if "Outside" in current_region:
            current_region = "Outside the U.S. (skip spending benchmarks)"
        else:
            current_region = "U.S. National Average"

    region = st.selectbox(
        "Region (United States) — select 'Outside the U.S.' to skip spending benchmarks",
        REGIONS,
        index=REGIONS.index(current_region),
        help="All benchmark and spending reference data in this tool come from U.S. federal surveys "
             "(BLS Consumer Expenditure Survey, Federal Reserve SCF, CFPB). "
             "If you are outside the United States, select 'Outside the U.S.' — "
             "spending hints will be hidden and you can still complete all other sections."
    )
    ss_set("region", region)

    if region.startswith("Outside"):
        st.warning("📌 **Outside the U.S. selected.** BLS spending reference figures will be hidden in the Cash Flow step. All other sections (net worth, retirement, well-being) are still available, though the benchmarks are U.S.-based and may not reflect your country's context.")

    yrs = ret_age - age
    mult = fidelity_multiple(age)
    st.markdown(f"""
    <div class="card card-blue" style="margin-top:1rem;">
        <strong>Your Profile</strong><br>
        <span style="font-size:0.9rem;color:#C084FC;">
        Age <strong>{age}</strong> · Annual salary <strong>{fmt_dollar(sal)}</strong> ·
        Retiring at <strong>{ret_age}</strong> ({yrs} years away) ·
        Fidelity retirement goal at your age: <strong>{mult:.1f}× salary = {fmt_dollar(mult * sal)}</strong>
        </span>
    </div>
    """, unsafe_allow_html=True)

    nav_buttons()

# ─────────────────────────────────────────────
# STEP 2 — GOAL SETTING
# ─────────────────────────────────────────────
def step_goals():
    render_header(); render_progress()
    st.markdown('<p class="step-title">Financial Goal Setting</p>', unsafe_allow_html=True)
    st.markdown("""
    <p class="step-subtitle">
        Explicitly naming goals helps overcome cognitive blind spots in financial planning.
        Select your top 3–5 priorities across different time horizons.
    </p>
    """, unsafe_allow_html=True)

    current_goals = set(ss("goals"))

    for cat, items in GOAL_CATS.items():
        st.markdown(f"**{cat}**")
        for item in items:
            checked = st.checkbox(item, value=(item in current_goals),
                                  key=f"goal_{item.replace(' ','_')[:30]}")
            if checked:
                current_goals.add(item)
            else:
                current_goals.discard(item)

    # ── Custom "Other" goals ─────────────────────────────────────────────────
    st.markdown("**Other / Custom Goals**")
    st.caption("Type a goal not listed above, choose a time horizon, then click + Add.")

    HORIZONS = ["Short-term (0–2 yrs)", "Medium-term (3–5 yrs)", "Long-term (5+ yrs)"]

    # Use a counter as part of the key to reset the input after add
    if "custom_goal_add_count" not in st.session_state:
        st.session_state["custom_goal_add_count"] = 0
    add_count = st.session_state["custom_goal_add_count"]

    col_new, col_hz_new, col_add = st.columns([3, 2, 1])
    with col_new:
        new_goal_text = st.text_input(
            "New custom goal",
            key=f"new_custom_goal_text_{add_count}",
            label_visibility="collapsed",
            placeholder="Type a new goal here…"
        )
    with col_hz_new:
        new_goal_hz = st.selectbox(
            "New goal horizon", HORIZONS,
            key=f"new_custom_goal_hz_{add_count}",
            label_visibility="collapsed"
        )
    with col_add:
        st.markdown("<div style='margin-top:0.35rem'></div>", unsafe_allow_html=True)
        if st.button("＋ Add", key="add_custom_goal"):
            txt = new_goal_text.strip()
            if txt:
                updated = ss("custom_goals") + [{"text": txt, "horizon": new_goal_hz}]
                ss_set("custom_goals", updated)
                st.session_state["custom_goal_add_count"] += 1  # new key = fresh input
                st.rerun()
            else:
                st.warning("Please type a goal before clicking Add.")

    # Display + edit existing custom goals
    custom_goals = ss("custom_goals")
    kept_customs = []
    for i, cg in enumerate(custom_goals):
        col_txt, col_hz, col_del = st.columns([3, 2, 1])
        with col_txt:
            new_text = st.text_input(
                f"Custom goal {i+1}", value=cg["text"],
                key=f"custom_goal_text_{i}", label_visibility="collapsed"
            )
        with col_hz:
            hz_idx = HORIZONS.index(cg["horizon"]) if cg["horizon"] in HORIZONS else 0
            new_hz = st.selectbox(
                f"Horizon {i+1}", HORIZONS, index=hz_idx,
                key=f"custom_goal_hz_{i}", label_visibility="collapsed"
            )
        with col_del:
            st.markdown("<div style='margin-top:0.35rem'></div>", unsafe_allow_html=True)
            if st.button("✕", key=f"del_custom_{i}", help="Remove"):
                continue
        if new_text.strip():
            kept_customs.append({"text": new_text.strip(), "horizon": new_hz})

    ss_set("custom_goals", kept_customs)

    # Combine preset + custom goals for count display
    all_custom_labels = [f"{cg['text']} ({cg['horizon']})" for cg in kept_customs]
    combined = current_goals | set(all_custom_labels)
    ss_set("goals", list(current_goals))

    n = len(current_goals) + len(kept_customs)

    if n == 0:
        st.info("Select at least one goal to continue.")
    elif n > 5:
        st.markdown(f"""
        <div class="card card-amber">
            ⚠️ You've selected <strong>{n} goals</strong>. Research suggests focusing on
            <strong>3–5 priorities</strong> is most effective for achievement.
            Consider narrowing your list to your highest-priority items.
        </div>
        """, unsafe_allow_html=True)
    else:
        all_display = sorted(current_goals) + [f"📝 {cg['text']} <em>({cg['horizon']})</em>" for cg in kept_customs]
        items_html = "".join(f"<li>{g}</li>" for g in all_display)
        st.markdown(f"""
        <div class="card card-green">
            ✅ <strong>{n} goal{'s' if n>1 else ''} selected</strong> — great focus!
            <ul style="margin:0.4rem 0 0;padding-left:1.2rem;font-size:0.88rem;color:#4ADE80;">
            {items_html}
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="citation">
        Sin, R., Murphy, R. O., &amp; Lamas, S. (2019). Goals-based financial planning: How simple lists
        can overcome cognitive blind spots. <em>Journal of Financial Planning, 32</em>(7), 32–43.<br>
        Fisher, P. J., &amp; Montalto, C. P. (2010). Effect of saving motives and horizon on saving behaviors.
        <em>Journal of Economic Psychology, 31</em>(1), 92–105.
        <a href="https://doi.org/10.1016/j.joep.2009.10.001">https://doi.org/10.1016/j.joep.2009.10.001</a>
    </div>
    """, unsafe_allow_html=True)

    nav_buttons()

# ─────────────────────────────────────────────
# STEP 3 — CFPB WELL-BEING SCALE
# Instrument layout matches the official CFPB questionnaire format.
# Score is NOT shown here — it reveals on the next step.
# ─────────────────────────────────────────────
def step_cfpb():
    render_header(); render_progress()

    st.markdown('<p class="step-title">Financial Well-Being Scale</p>', unsafe_allow_html=True)
    st.markdown("""
    <p class="step-subtitle">
        This 10-question scale was developed by the Consumer Financial Protection Bureau (CFPB)
        to measure financial well-being. Answer every question honestly — there are no right or wrong answers.
        Your score will appear on the next page.
    </p>
    """, unsafe_allow_html=True)

    # Styled section headers via HTML, radio inputs via native Streamlit (reliable cross-platform)
    st.markdown("""
    <style>
    .cfpb-part-header {
        background: #3D1A5C;
        color: white;
        border-radius: 10px 10px 0 0;
        padding: 0.85rem 1.2rem;
        font-weight: 600;
        font-size: 0.95rem;
        margin-top: 1.5rem;
        margin-bottom: 0;
        line-height: 1.4;
    }
    .cfpb-q-card {
        background: white;
        border: 1px solid #D4C9E8;
        border-top: none;
        padding: 1rem 1.2rem 0.5rem 1.2rem;
    }
    .cfpb-q-card:last-of-type {
        border-radius: 0 0 10px 10px;
        margin-bottom: 0.5rem;
    }
    .cfpb-q-card:nth-child(even) { background: #0E0A1E; }
    .cfpb-q-label {
        font-size: 0.92rem;
        color: #F0EBFF;
        font-weight: 500;
        margin-bottom: 0.4rem;
        line-height: 1.45;
    }
    /* Make radio options display inline and compact */
    div[data-testid="stRadio"] > div[role="radiogroup"] {
        flex-direction: row !important;
        flex-wrap: wrap;
        gap: 0.25rem 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

    cfpb = {k: v for k, v in ss("cfpb").items()}

    # ── Part 1 ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="cfpb-part-header">
        Part 1 &nbsp;|&nbsp; How well does this statement describe you or your situation?
    </div>
    """, unsafe_allow_html=True)

    part1_items = [(i, t, s) for i, (t, p, s) in enumerate(CFPB_ITEMS, 1) if p == "agree"]
    for idx, text, score_vals in part1_items:
        # Find current selection index
        current_score = cfpb.get(f"q{idx}_score", score_vals[2])
        try:
            cur_idx = score_vals.index(current_score)
        except ValueError:
            cur_idx = 2

        st.markdown(f'<div class="cfpb-q-label">{idx}. {text}</div>', unsafe_allow_html=True)
        choice = st.radio(
            label=f"q{idx}",
            options=CFPB_AGREE_OPTS,
            index=cur_idx,
            horizontal=True,
            key=f"cfpb_q{idx}",
            label_visibility="collapsed",
        )
        chosen_idx = CFPB_AGREE_OPTS.index(choice)
        cfpb[f"q{idx}_score"] = score_vals[chosen_idx]
        st.markdown("<div style='margin-bottom:0.75rem;border-bottom:1px solid #2D1B5E;'></div>",
                    unsafe_allow_html=True)

    # ── Part 2 ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div class="cfpb-part-header" style="margin-top:1.5rem;">
        Part 2 &nbsp;|&nbsp; How often does this statement apply to you?
    </div>
    """, unsafe_allow_html=True)

    part2_items = [(i, t, s) for i, (t, p, s) in enumerate(CFPB_ITEMS, 1) if p == "freq"]
    for idx, text, score_vals in part2_items:
        current_score = cfpb.get(f"q{idx}_score", score_vals[2])
        try:
            cur_idx = score_vals.index(current_score)
        except ValueError:
            cur_idx = 2

        st.markdown(f'<div class="cfpb-q-label">{idx}. {text}</div>', unsafe_allow_html=True)
        choice = st.radio(
            label=f"q{idx}",
            options=CFPB_FREQ_OPTS,
            index=cur_idx,
            horizontal=True,
            key=f"cfpb_q{idx}",
            label_visibility="collapsed",
        )
        chosen_idx = CFPB_FREQ_OPTS.index(choice)
        cfpb[f"q{idx}_score"] = score_vals[chosen_idx]
        st.markdown("<div style='margin-bottom:0.75rem;border-bottom:1px solid #2D1B5E;'></div>",
                    unsafe_allow_html=True)

    ss_set("cfpb", cfpb)

    st.markdown("""
    <div class="citation" style="margin-top:1.5rem;">
        <strong>Source:</strong> Consumer Financial Protection Bureau. (2017). <em>CFPB Financial Well-Being Scale: Scale development technical report.</em>
        <a href="https://www.consumerfinance.gov/data-research/research-reports/financial-well-being-scale/">
        https://www.consumerfinance.gov/data-research/research-reports/financial-well-being-scale/</a>
        &nbsp;·&nbsp; Questions reproduced verbatim per CFPB public use guidelines.
        &nbsp;·&nbsp; Scored using the official CFPB lookup table for self-administered questionnaires.
    </div>
    """, unsafe_allow_html=True)

    nav_buttons(next_label="See My Score →")


def _compute_cfpb_score():
    """Compute raw total and convert using official CFPB lookup table."""
    cfpb = ss("cfpb")
    raw = sum(cfpb.get(f"q{i+1}_score", v[2]) for i, (_, _, v) in enumerate(CFPB_ITEMS))
    return cfpb_raw_to_score(raw, age=ss("age")), raw



# ─────────────────────────────────────────────
# STEP 4 — CFPB SCORE REVEAL (standalone)
# ─────────────────────────────────────────────
def step_cfpb_score():
    render_header(); render_progress()
    st.markdown('<p class="step-title">Your Financial Well-Being Score</p>', unsafe_allow_html=True)

    score, raw = _compute_cfpb_score()
    age        = ss("age")
    peer_med   = cfpb_age_median(age)

    if age < 25:    age_label = "18–24"
    elif age < 35:  age_label = "25–34"
    elif age < 45:  age_label = "35–44"
    elif age < 55:  age_label = "45–54"
    elif age < 62:  age_label = "55–61"
    elif age < 70:  age_label = "62–69"
    else:           age_label = "70+"

    if score >= 61:
        sc_color = "#4ADE80"
        sc_tier  = "High financial well-being"
        sc_msg   = ("You report relatively high financial well-being — you feel in control of your day-to-day finances, "
                    "can absorb financial shocks, and are generally on track toward your goals. "
                    "Focus on maintaining these habits and building on this foundation.")
    elif score >= 41:
        sc_color = "#FCD34D"
        sc_tier  = "Moderate financial well-being"
        sc_msg   = ("You report moderate financial well-being — the most common range for working-age Americans. "
                    "Some areas feel manageable while others create stress. "
                    "The personalized action plan at the end of this assessment will identify the highest-impact improvements.")
    else:
        sc_color = "#F87171"
        sc_tier  = "Lower financial well-being"
        sc_msg   = ("You report lower financial well-being. This is more common than many people realize and is often "
                    "driven by specific, addressable gaps — such as high debt load, income volatility, or lack of "
                    "emergency savings. Your action plan will prioritize the most critical next steps.")

    diff     = score - peer_med
    diff_txt = (f"<strong style='color:#4ADE80'>+{diff} above</strong>" if diff > 0
                else f"<strong style='color:#F87171'>{diff} below</strong>" if diff < 0
                else "<strong>equal to</strong>")

    st.markdown(f"""
    <div class="card" style="border-left:5px solid {sc_color};background:#1A1033;padding:1.75rem 2rem;">
        <div style="font-size:0.75rem;color:#A89BC2;text-transform:uppercase;letter-spacing:0.08em;font-weight:600;margin-bottom:0.5rem;">
            Your CFPB Financial Well-Being Score
        </div>
        <div style="display:flex;align-items:flex-end;gap:1.25rem;flex-wrap:wrap;">
            <div style="font-size:5rem;font-weight:800;color:{sc_color};line-height:1;">{score}</div>
            <div style="flex:1;min-width:180px;">
                <div style="font-size:1.05rem;font-weight:700;color:#F0EBFF;">{sc_tier}</div>
                <div style="font-size:0.82rem;color:#D4C8F0;margin-top:4px;">out of 100 &nbsp;·&nbsp; Raw total: {raw}/40</div>
                <div style="font-size:0.85rem;color:#F0EBFF;margin-top:6px;font-weight:500;">
                    {diff_txt} the median for U.S. adults ages {age_label} (median: {peer_med})
                </div>
            </div>
        </div>
        <div style="margin-top:1.25rem;">
            <div style="position:relative;height:20px;background:#2A1D4E;border-radius:99px;overflow:hidden;">
                <div style="width:{score}%;height:100%;background:linear-gradient(90deg,#F87171 0%,#FCD34D 40%,#4ADE80 70%);border-radius:99px;"></div>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:0.75rem;color:#D4C8F0;margin-top:6px;font-weight:500;">
                <span>0 — Lower</span><span>40</span><span>Moderate — 60</span><span>80</span><span>Higher — 100</span>
            </div>
        </div>
        <p style="font-size:0.9rem;color:#F0EBFF;margin-top:1.25rem;line-height:1.6;">{sc_msg}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**How your score compares to U.S. adults by age group** *(CFPB National Financial Well-Being Survey, 2017)*")
    AGE_MEDIANS = [
        ("18–24", 51), ("25–34", 52), ("35–44", 54),
        ("45–54", 54), ("55–61", 55), ("62–69", 59), ("70+", 62),
    ]
    rows = ""
    for ag, med in AGE_MEDIANS:
        hl = ' class="highlight"' if ag == age_label else ""
        you_col = (f"<strong style='color:{sc_color}'>{score}</strong>" if ag == age_label else "")
        rows += f"<tr{hl}><td style='color:#F0EBFF'>{'▶ ' if ag==age_label else ''}{ag}</td><td style='text-align:center;color:#F0EBFF'>{med}</td><td style='text-align:center'>{you_col}</td></tr>"

    st.markdown(f"""
    <table class="bench-table">
        <thead><tr><th>Age Group</th><th style="text-align:center">Median Score</th><th style="text-align:center">Your Score</th></tr></thead>
        <tbody>{rows}</tbody>
    </table>
    <p style="font-size:0.8rem;color:#D4C8F0;margin-top:0.75rem;">
        Scores use the official CFPB lookup table (self-administered, adjusted for age).
        Well-being is best understood as progress over time — not a pass/fail threshold.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="citation">
        <strong>Sources:</strong><br>
        Consumer Financial Protection Bureau. (2017). <em>CFPB Financial Well-Being Scale: Scale development technical report.</em>
        <a href="https://www.consumerfinance.gov/data-research/research-reports/financial-well-being-scale/">
        https://www.consumerfinance.gov/data-research/research-reports/financial-well-being-scale/</a><br>
        Consumer Financial Protection Bureau. (2017). <em>Financial well-being in America.</em>
        <a href="https://www.consumerfinance.gov/data-research/research-reports/financial-well-being-in-america/">
        https://www.consumerfinance.gov/data-research/research-reports/financial-well-being-in-america/</a>
        (age-group median scores)
    </div>
    """, unsafe_allow_html=True)

    nav_buttons()


# ─────────────────────────────────────────────
# STEP 5 — FINANCIAL CONFIDENCE (one question at a time)
# ─────────────────────────────────────────────
def step_confidence():
    render_header(); render_progress()
    st.markdown('<p class="step-title">Financial Confidence</p>', unsafe_allow_html=True)
    st.markdown("""
    <p class="step-subtitle">
        Rate your confidence in each area. Research shows both overconfidence and
        underconfidence impair financial decision-making (Parker et al., 2012).
    </p>
    """, unsafe_allow_html=True)

    CONF_AREAS = [
        ("daily",      "Managing day-to-day finances",
         "How confident are you in managing your monthly budget, tracking spending, and avoiding overdrafts?"),
        ("emergency",  "Planning for financial emergencies",
         "How confident are you in your ability to handle an unexpected expense of $1,000 or more?"),
        ("saving",     "Saving consistently toward goals",
         "How confident are you in setting aside money regularly toward specific financial goals?"),
        ("investing",  "Understanding and using investments",
         "How confident are you in choosing and managing investment accounts (401k, IRA, brokerage)?"),
        ("retirement", "Planning for retirement",
         "How confident are you that you are on track to maintain your standard of living in retirement?"),
        ("insurance",  "Evaluating insurance coverage",
         "How confident are you that your health, life, disability, and other insurance coverage is adequate?"),
        ("tax",        "Basic tax planning",
         "How confident are you in understanding your tax situation and using tax-advantaged accounts?"),
        ("estate",     "Estate planning (will, beneficiaries)",
         "How confident are you that your will, beneficiary designations, and estate documents are up to date?"),
    ]
    CONF_KEYS  = [c[0] for c in CONF_AREAS]
    CONF_TOTAL = len(CONF_AREAS)

    # Track which question the user is on
    if "conf_q_idx" not in st.session_state:
        st.session_state["conf_q_idx"] = 0
    q_idx = st.session_state["conf_q_idx"]

    conf = ss("conf")
    options = ["1 – Not at all", "2 – Slightly", "3 – Moderately",
               "4 – Confident", "5 – Very confident"]

    # ── Progress within this step ─────────────────────────────────────────────
    inner_pct = int((q_idx / CONF_TOTAL) * 100)
    st.markdown(f"""
    <div style="margin-bottom:1.25rem;">
        <div style="display:flex;justify-content:space-between;font-size:0.78rem;color:#A89BC2;margin-bottom:4px;">
            <span>Question {q_idx + 1} of {CONF_TOTAL}</span>
            <span>{inner_pct}% complete</span>
        </div>
        <div style="background:#2A1D4E;border-radius:99px;height:6px;overflow:hidden;">
            <div style="width:{inner_pct}%;height:100%;background:linear-gradient(90deg,#7C3AED,#C084FC);border-radius:99px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if q_idx < CONF_TOTAL:
        key, label, hint = CONF_AREAS[q_idx]
        current = conf.get(key, 3) - 1

        st.markdown(f"### {label}")
        st.caption(hint)

        choice = st.radio(
            label, options=options, index=current, horizontal=True,
            label_visibility="collapsed", key=f"conf_{key}_q"
        )
        conf[key] = int(choice[0])
        ss_set("conf", conf)

        st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

        btn_col1, btn_col2 = st.columns([1, 1])
        with btn_col1:
            if q_idx > 0:
                if st.button("← Previous", key="conf_prev", use_container_width=True):
                    st.session_state["conf_q_idx"] = q_idx - 1
                    st.rerun()
        with btn_col2:
            if st.button("Next →" if q_idx < CONF_TOTAL - 1 else "See Results →",
                         key="conf_next", use_container_width=True):
                st.session_state["conf_q_idx"] = min(CONF_TOTAL, q_idx + 1)
                st.rerun()

    if q_idx >= CONF_TOTAL:
        # All answered — show summary and allow proceeding
        avg = sum(conf.get(k, 3) for k in CONF_KEYS) / CONF_TOTAL
        low_areas = [label for key, label, _ in CONF_AREAS if conf.get(key, 3) <= 2]

        conf_color = "#4ADE80" if avg >= 4 else "#FCD34D" if avg >= 3 else "#F87171"
        low_html = ""
        if low_areas:
            items_html = "".join(f"<li>{a}</li>" for a in low_areas)
            low_html = f"""<br><br><strong style='color:#F87171'>Areas rated ≤ 2 — priority for improvement:</strong>
            <ul style='font-size:0.88rem;color:#FCA5A5;margin:0.4rem 0 0;padding-left:1.3rem;'>{items_html}</ul>"""

        st.markdown(f"""
        <div class="card" style="border-left:5px solid {conf_color};margin-top:0.5rem;">
            <div style="font-size:1.05rem;font-weight:700;color:#F0EBFF;">Average Confidence: {avg:.1f} / 5</div>
            <div style="font-size:0.9rem;color:#D4C8F0;margin-top:0.4rem;">
            {"Strong overall confidence — maintain and build on it." if avg >= 4
             else "Moderate confidence — target lower-rated areas for education or professional advice." if avg >= 3
             else "Several areas need attention — consider financial education or one-on-one guidance."}
            </div>
            {low_html}
        </div>
        """, unsafe_allow_html=True)

        if st.button("← Review answers", key="conf_review"):
            st.session_state["conf_q_idx"] = 0
            st.rerun()

        st.markdown("""
        <div class="citation">
            Parker, A. M., de Bruin, W. B., Yoong, J., &amp; Willis, R. (2012). Inappropriate confidence and retirement planning:
            Four studies with a national sample. <em>Journal of Behavioral Decision Making, 25</em>(4), 382–389.
            <a href="https://doi.org/10.1002/bdm.745">https://doi.org/10.1002/bdm.745</a>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        nav_buttons()
    else:
        # Show back/forward page nav at bottom too (disabled until complete)
        st.markdown("<hr class='divider'>", unsafe_allow_html=True)
        c1, c2 = st.columns([1, 1])
        with c1:
            if st.button("← Back to Score", key="conf_pg_back", use_container_width=True):
                ss_set("step", ss("step") - 1)
                st.rerun()
        with c2:
            st.button("Complete all questions to continue →", key="conf_pg_next_disabled",
                      use_container_width=True, disabled=True)


# ─────────────────────────────────────────────
# STEP 6 — NET WORTH
# ─────────────────────────────────────────────
def step_networth():
    render_header(); render_progress()
    st.markdown('<p class="step-title">Net Worth Calculation</p>', unsafe_allow_html=True)
    st.markdown('<p class="step-subtitle">Your net worth (assets minus liabilities) is a snapshot of your overall financial position. On desktop, assets appear left and liabilities right.</p>', unsafe_allow_html=True)

    nw = ss("nw")

    # Use two Streamlit columns — they stack naturally on narrow screens
    col_a, col_l = st.columns(2, gap="large")

    with col_a:
        st.markdown("#### 🟢 Assets")
        nw["cash"]             = st.number_input("Cash & Checking", 0, 50_000_000,
            nw.get("cash", 0), step=500, format="%d", key="nw_cash")
        nw["savings_nw"]       = st.number_input("Savings / CDs", 0, 50_000_000,
            nw.get("savings_nw", 0), step=500, format="%d", key="nw_savings_nw")
        nw["investments"]      = st.number_input("Taxable investments", 0, 50_000_000,
            nw.get("investments", 0), step=500, format="%d", key="nw_investments")
        nw["retirement_accts"] = st.number_input("Retirement accounts (401k/IRA/Roth)", 0, 50_000_000,
            nw.get("retirement_accts", 0), step=500, format="%d", key="nw_retirement_accts")
        nw["home"]             = st.number_input("Home / real estate value", 0, 50_000_000,
            nw.get("home", 0), step=500, format="%d", key="nw_home")
        nw["vehicle"]          = st.number_input("Vehicle(s) value", 0, 500_000,
            nw.get("vehicle", 0), step=500, format="%d", key="nw_vehicle")

    with col_l:
        st.markdown("#### 🔴 Liabilities")
        nw["cc_debt"]       = st.number_input("Credit card debt", 0, 1_000_000,
            nw.get("cc_debt", 0), step=500, format="%d", key="nw_cc_debt")
        nw["student"]       = st.number_input("Student loans", 0, 1_000_000,
            nw.get("student", 0), step=500, format="%d", key="nw_student")
        nw["auto_loan"]     = st.number_input("Auto loan(s)", 0, 200_000,
            nw.get("auto_loan", 0), step=500, format="%d", key="nw_auto_loan")
        nw["mortgage"]      = st.number_input("Mortgage balance", 0, 10_000_000,
            nw.get("mortgage", 0), step=500, format="%d", key="nw_mortgage")
        nw["personal_loan"] = st.number_input("Personal / other loans", 0, 500_000,
            nw.get("personal_loan", 0), step=500, format="%d", key="nw_personal_loan")
        nw["other_debt"]    = st.number_input("Other debts (HELOC, medical, etc.)", 0, 500_000,
            nw.get("other_debt", 0), step=500, format="%d", key="nw_other_debt")

    ss_set("nw", nw)
    assets, liabs, total = net_worth()
    age    = ss("age")
    bracket = age_bracket(age)
    bench_med, bench_p75 = NW_BENCH[bracket]

    nw_color = "#4ADE80" if total > bench_med else "#FCD34D" if total >= 0 else "#F87171"
    tier = ("Top 25% for your age group" if total > bench_p75
            else "Above median for your age group" if total > bench_med
            else "Below median for your age group")

    st.markdown(f"""
    <div class="card" style="border-left:5px solid {nw_color};margin-top:1.5rem;">
        <div class="kpi-grid">
            <div class="kpi-box">
                <div class="label">Total Assets</div>
                <div class="value" style="color:#4ADE80">{fmt_dollar(assets)}</div>
            </div>
            <div class="kpi-box">
                <div class="label">Total Liabilities</div>
                <div class="value" style="color:#F87171">{fmt_dollar(liabs)}</div>
            </div>
            <div class="kpi-box">
                <div class="label">Net Worth</div>
                <div class="value" style="color:{nw_color}">{fmt_dollar(total)}</div>
            </div>
        </div>
        <div style="margin-top:1rem;font-size:0.9rem;color:#F0EBFF;font-weight:500;">
            {tier} &nbsp;·&nbsp;
            Peer median: <strong>{fmt_dollar(bench_med)}</strong> &nbsp;·&nbsp;
            75th percentile: <strong>{fmt_dollar(bench_p75)}</strong>
        </div>
        <div style="margin-top:0.5rem;font-size:0.82rem;color:#D4C8F0;">
            ⚠️ <em>Descriptive benchmark only</em> — reflects what peers have, not what is needed for financial security.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Under-25 / negative net worth context ─────────────────────────────────
    if age < 25 or total < 0:
        if age < 25 and total < 0:
            headline = "A negative net worth is very common and expected at your age."
            body = (
                "Most people under 25 have more debt than assets — student loans, car payments, "
                "and credit cards taken on before income catches up. This is not a crisis; "
                "it is a starting point. <strong>What matters most right now is the trajectory, "
                "not the number.</strong> If your net worth is improving each year — even slowly — "
                "you are doing the right things. Use this tool quarterly to track your progress."
            )
            tips = [
                "Avoid taking on new high-interest debt (credit cards > 20% APR).",
                "Even $25–50/month into a savings account builds the habit that compounds later.",
                "If you have student loans, confirm your repayment plan and income-driven options.",
                "Your biggest asset right now is time — compound interest works most powerfully over long horizons.",
            ]
        elif age < 25:
            headline = "You're off to a strong start for your age."
            body = (
                "Having a positive net worth before age 25 puts you ahead of most of your peers. "
                "Many people in this age group are still working through student loans or early-career "
                "expenses. Keep building on this foundation — the habits you establish now "
                "will compound significantly over the next few decades."
            )
            tips = [
                "Start or increase retirement contributions — time is your greatest asset.",
                "Build your emergency fund to 3 months before investing in taxable accounts.",
                "Avoid lifestyle inflation as your income grows.",
            ]
        else:
            headline = "A negative net worth is something to track — but not to despair about."
            body = (
                "Many people carry negative net worth at various life stages, particularly when "
                "student loans, mortgages, or unexpected expenses are part of the picture. "
                "<strong>The direction of change matters more than the current number.</strong> "
                "If you reduce debt and grow assets consistently, the trajectory will turn positive. "
                "Focus on the highest-interest debt first (typically credit cards), then build "
                "your emergency fund, then address longer-term goals."
            )
            tips = [
                "Track your net worth quarterly — even small improvements are meaningful progress.",
                "Prioritize eliminating high-interest debt (credit cards) before building investments.",
                "A fee-only financial counselor (NFCC.org) can help if debt feels overwhelming.",
            ]

        tips_html = "".join(f"<li style='margin-bottom:4px'>{t}</li>" for t in tips)
        st.markdown(f"""
        <div class="card card-blue" style="margin-top:0.5rem;">
            <div style="font-size:0.95rem;font-weight:700;color:#F0EBFF;margin-bottom:0.5rem;">
                💡 {headline}
            </div>
            <div style="font-size:0.88rem;color:#D4C8F0;line-height:1.6;margin-bottom:0.75rem;">
                {body}
            </div>
            <ul style="font-size:0.85rem;color:#C4B5FD;margin:0;padding-left:1.3rem;line-height:1.7;">
                {tips_html}
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("**Net Worth Benchmarks by Age — Federal Reserve SCF 2022**")
    rows = ""
    for ag, (med, p75) in NW_BENCH.items():
        hl = ' class="highlight"' if ag == bracket else ""
        rows += f'<tr{hl}><td style="color:#F0EBFF">{"▶ " if ag==bracket else ""}{ag}</td><td style="color:#F0EBFF">{fmt_dollar(med)}</td><td style="color:#F0EBFF">{fmt_dollar(p75)}</td></tr>'
    st.markdown(f"""
    <table class="bench-table">
        <thead><tr><th>Age Group</th><th>Median Net Worth</th><th>75th Percentile</th></tr></thead>
        <tbody>{rows}</tbody>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="citation">
        Board of Governors of the Federal Reserve System. (2023). <em>Survey of Consumer Finances, 2022.</em>
        <a href="https://www.federalreserve.gov/econres/scfindex.htm">https://www.federalreserve.gov/econres/scfindex.htm</a>
    </div>
    """, unsafe_allow_html=True)


    nav_buttons()

# ─────────────────────────────────────────────
# STEP 6 — CASH FLOW
# ─────────────────────────────────────────────
# ─────────────────────────────────────────────
# STEP 7 — CASH FLOW
# ─────────────────────────────────────────────
def step_cashflow():
    render_header(); render_progress()
    st.markdown('<p class="step-title">Cash Flow Analysis</p>', unsafe_allow_html=True)
    st.markdown('<p class="step-subtitle">Understanding where your money goes is the foundation of financial planning.</p>', unsafe_allow_html=True)

    region = ss("region")
    outside_us = region.startswith("Outside")
    bls = BLS_MONTHLY.get(region, BLS_MONTHLY["U.S. National Average"])
    # indices: shelter, utilities, transport, groceries, dining_out, healthcare, entertainment, personal_care

    if outside_us:
        st.markdown("""
        <div class="card card-slate">
            <strong>📌 Outside the U.S.</strong><br>
            <span style="font-size:0.85rem;color:#D4C8F0;">
            BLS spending reference data is U.S.-only and has been hidden. Enter your actual expenses below.
            </span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="card card-blue">
            <strong>Reference figures: BLS Consumer Expenditure Survey 2022 — {region}</strong><br>
            <span style="font-size:0.85rem;color:#D4C8F0;">
            The dollar hints below show average monthly spending from the U.S. Bureau of Labor Statistics
            Consumer Expenditure Survey 2022 for the <strong>{region}</strong> region.
            These are <em>averages across all income levels</em> — your situation may differ.
            All data are expressed in 2022 U.S. dollars.
            </span>
        </div>
        """, unsafe_allow_html=True)

    def bls_cap(text):
        """Render BLS hint as a caption under a field — only if U.S. region selected."""
        if not outside_us:
            st.caption(f"📊 BLS 2022 avg ({region}): {text}")

    income = st.number_input("Monthly net (take-home) income after taxes ($)",
                             0, 100_000, ss("income_net"), step=100, format="%d")
    ss_set("income_net", income)
    gross_mo = ss("salary") / 12
    st.caption(f"Your estimated gross monthly income: {fmt_dollar(gross_mo)}")

    exp = ss("exp")

    st.markdown("#### Fixed Expenses *(same each month)*")

    exp["housing"] = st.number_input("Housing (rent or mortgage payment only)",
        0, 20_000, exp.get("housing", 0), step=50, format="%d", key="exp_housing")
    bls_cap(f"Housing/shelter ~${bls[0]:,}/mo")

    exp["utilities"] = st.number_input("Utilities (electric, gas, water, internet, phone)",
        0, 3_000, exp.get("utilities", 0), step=25, format="%d", key="exp_utilities")
    bls_cap(f"Utilities ~${bls[1]:,}/mo")

    exp["transport"] = st.number_input("Transportation (car payment, gas, auto insurance, transit)",
        0, 10_000, exp.get("transport", 0), step=25, format="%d", key="exp_transport")
    bls_cap(f"All transportation ~${bls[2]:,}/mo (includes vehicle payments, gas, insurance, maintenance)")

    exp["insurance"] = st.number_input("Insurance (health, life, disability — not auto)",
        0, 5_000, exp.get("insurance", 0), step=25, format="%d", key="exp_insurance")

    exp["debt_min"] = st.number_input("Minimum debt payments (student loans, credit cards, personal loans)",
        0, 10_000, exp.get("debt_min", 0), step=25, format="%d", key="exp_debt_min")

    st.markdown("#### Flexible Expenses *(variable each month)*")

    exp["groceries"] = st.number_input("Groceries & household supplies",
        0, 5_000, exp.get("groceries", 0), step=25, format="%d", key="exp_groceries")
    bls_cap(f"Groceries ~${bls[3]:,}/mo")

    exp["entertainment"] = st.number_input("Dining out & entertainment",
        0, 5_000, exp.get("entertainment", 0), step=25, format="%d", key="exp_entertainment")
    bls_cap(f"Dining out ~${bls[4]:,}/mo")

    exp["personal"] = st.number_input("Personal care & clothing",
        0, 3_000, exp.get("personal", 0), step=10, format="%d", key="exp_personal")
    bls_cap(f"Personal care ~${bls[7]:,}/mo")

    exp["other_flex"] = st.number_input("Other variable expenses (subscriptions, childcare, pet care, etc.)",
        0, 5_000, exp.get("other_flex", 0), step=25, format="%d", key="exp_other_flex")
    bls_cap(f"Healthcare out-of-pocket ~${bls[5]:,}/mo · Recreation ~${bls[6]:,}/mo")

    st.markdown("#### Occasional / Annual Expenses")
    occ = st.number_input(
        "Annual total (gifts, travel, car maintenance, medical copays, home repairs, etc.)",
        0, 200_000, ss("occ_annual"), step=100, format="%d")
    ss_set("occ_annual", occ)
    ss_set("exp", exp)

    total_exp = monthly_expenses()
    surplus, sr = savings_rate()

    if sr >= 20:
        sr_color, sr_msg = "#4ADE80", "🌟 Excellent savings rate — on track for long-term security."
    elif sr >= 15:
        sr_color, sr_msg = "#4ADE80", "✅ Good savings rate — meeting the 15% research-based guideline."
    elif sr >= 10:
        sr_color, sr_msg = "#FCD34D", "⚠️ Moderate savings rate. Aim for 15–20% for long-term security."
    elif surplus > 0:
        sr_color, sr_msg = "#FCD34D", "⚠️ Low savings rate. Look for opportunities to reduce expenses or increase income."
    else:
        sr_color, sr_msg = "#F87171", "🚨 Expenses exceed income. Addressing this gap is the top priority."

    st.markdown(f"""
    <div class="card" style="border-left:5px solid {sr_color};margin-top:1.5rem;">
        <div class="kpi-grid">
            <div class="kpi-box"><div class="label">Net Income</div><div class="value">{fmt_dollar(income)}/mo</div></div>
            <div class="kpi-box"><div class="label">Total Expenses</div><div class="value" style="color:#F87171">{fmt_dollar(total_exp)}/mo</div></div>
            <div class="kpi-box"><div class="label">Monthly Surplus</div><div class="value" style="color:{sr_color}">{fmt_dollar(surplus)}</div></div>
            <div class="kpi-box"><div class="label">Savings Rate</div><div class="value" style="color:{sr_color}">{sr:.1f}%</div></div>
        </div>
        <p style="margin-top:1rem;font-size:0.9rem;color:#F0EBFF;font-weight:500;">{sr_msg}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="citation">
        <strong>Sources:</strong><br>
        U.S. Bureau of Labor Statistics. (2023). <em>Consumer Expenditure Survey, 2022.</em>
        <a href="https://www.bls.gov/cex/">https://www.bls.gov/cex/</a>
        (Table 1101: Regional expenditure means, annual data divided by 12 for monthly estimates.
        All figures are U.S.-based averages across consumer units and income levels.)<br>
        Pfau, W. D. (2011). Safe savings rates: A new approach to retirement planning over the life cycle.
        <em>Journal of Financial Planning, 24</em>(5), 42–50.
        (15% savings rate guideline)
    </div>
    """, unsafe_allow_html=True)

    nav_buttons()

# ─────────────────────────────────────────────
# STEP 7 — EMERGENCY FUND
# ─────────────────────────────────────────────
def step_emergency():
    render_header(); render_progress()
    st.markdown('<p class="step-title">Emergency Fund Assessment</p>', unsafe_allow_html=True)
    st.markdown("""
    <p class="step-subtitle">
        An adequate emergency fund is the single most impactful first step toward financial security.
        It prevents debt accumulation during unexpected events.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card card-red">
        <strong>📊 National Context (Federal Reserve, 2024):</strong><br>
        <ul style="margin:0.5rem 0 0;padding-left:1.2rem;font-size:0.88rem;color:#991b1b;">
            <li>37% of U.S. adults could not cover a $400 emergency without borrowing or selling assets</li>
            <li>28% of adults skipped needed medical care due to cost</li>
            <li>Households without emergency savings are 3× more likely to carry high-interest debt</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    ef = st.number_input("Current emergency fund savings ($)",
                         0, 5_000_000, ss("ef"), step=100, format="%d")
    ss_set("ef", ef)

    monthly_exp = monthly_expenses()
    months_covered = (ef / monthly_exp) if monthly_exp > 0 else 0
    target_3mo  = monthly_exp * 3
    target_6mo  = monthly_exp * 6
    gap_3mo     = max(0, target_3mo - ef)
    gap_6mo     = max(0, target_6mo - ef)

    if months_covered >= 6:
        color, tier = "#4ADE80", "✅ Fully funded"
    elif months_covered >= 3:
        color, tier = "#FCD34D", "⚠️ Partially funded"
    else:
        color, tier = "#F87171", "🚨 Underfunded"

    can_cover_400 = "✅ Yes" if ef >= 400 else "❌ No"
    can_cover_2k  = "✅ Yes" if ef >= 2000 else "❌ No"

    st.markdown(f"""
    <div class="card" style="border-left:4px solid {color};margin-top:1rem;">
        <div class="kpi-grid">
            <div class="kpi-box"><div class="label">Current Fund</div><div class="value">{fmt_dollar(ef)}</div></div>
            <div class="kpi-box"><div class="label">Months Covered</div><div class="value" style="color:{color}">{months_covered:.1f}</div></div>
            <div class="kpi-box"><div class="label">3-Month Target</div><div class="value">{fmt_dollar(target_3mo)}</div></div>
            <div class="kpi-box"><div class="label">6-Month Target</div><div class="value">{fmt_dollar(target_6mo)}</div></div>
        </div>
        <div style="margin-top:1rem;font-size:0.88rem;">
            <strong>{tier}</strong>
            {"" if months_covered >= 6
             else f" — Gap to 3-month minimum: <strong style='color:#F87171'>{fmt_dollar(gap_3mo)}</strong>" if months_covered < 3
             else f" — Gap to 6-month goal: <strong style='color:#FCD34D'>{fmt_dollar(gap_6mo)}</strong>"}
        </div>
        <div style="margin-top:0.75rem;font-size:0.85rem;color:#D4C8F0;">
            Cover $400 emergency: <strong>{can_cover_400}</strong>
            &nbsp;|&nbsp; Cover $2,000 emergency: <strong>{can_cover_2k}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Progress bar
    metric_bar("Progress toward 6-month goal", min(months_covered, 6), 6,
               color="#4ADE80" if months_covered >= 6 else "#FCD34D" if months_covered >= 3 else "#F87171",
               suffix=" months")

    if months_covered < 3:
        monthly_to_3mo = gap_3mo / 12
        st.markdown(f"""
        <div class="card card-blue">
            💡 <strong>Getting started:</strong> Saving <strong>{fmt_dollar(monthly_to_3mo)}/month</strong>
            would fund a 3-month emergency fund in one year.
            Consider automating a transfer on payday — research shows automation increases
            savings rates by 40% or more (Madrian &amp; Shea, 2001).
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="citation">
        <strong>Sources:</strong><br>
        Board of Governors of the Federal Reserve System. (2024). <em>Report on the economic well-being of U.S. households in 2023.</em>
        <a href="https://www.federalreserve.gov/publications/report-economic-well-being-us-households.htm">
        https://www.federalreserve.gov/publications/report-economic-well-being-us-households.htm</a><br>
        Madrian, B. C., &amp; Shea, D. F. (2001). The power of suggestion: Inertia in 401(k) participation and savings behavior.
        <em>Quarterly Journal of Economics, 116</em>(4), 1149–1187.
        <a href="https://doi.org/10.1162/003355301753265543">https://doi.org/10.1162/003355301753265543</a>
    </div>
    """, unsafe_allow_html=True)

    nav_buttons()

# ─────────────────────────────────────────────
# STEP 8 — RETIREMENT READINESS
# ─────────────────────────────────────────────
def step_retirement():
    render_header(); render_progress()
    st.markdown('<p class="step-title">Retirement Readiness Analysis</p>', unsafe_allow_html=True)
    st.markdown("""
    <p class="step-subtitle">
        Combining prescriptive (what you need) and descriptive (what peers have) benchmarks
        gives you a complete picture of retirement readiness.
    </p>
    """, unsafe_allow_html=True)

    nw = ss("nw")
    default_ret = nw.get("retirement_accts", 0) or ss("ret_current")

    ret_saved = st.number_input("Current total retirement savings ($)",
                                0, 20_000_000, default_ret, step=500, format="%d")
    ss_set("ret_current", ret_saved)
    nw["retirement_accts"] = ret_saved
    ss_set("nw", nw)

    ret_monthly = st.number_input("Monthly retirement contribution (incl. employer match, $)",
                                  0, 50_000, ss("ret_monthly"), step=50, format="%d")
    ss_set("ret_monthly", ret_monthly)

    ret_return = st.number_input(
        "Expected annual return (% per year)",
        min_value=1.0, max_value=15.0,
        value=float(ss("ret_return")),
        step=0.5,
        format="%.1f"
    )
    ss_set("ret_return", ret_return)

    # Context card for rate of return
    if ret_return <= 5.0:
        rr_note = "Conservative — appropriate for bond-heavy or near-retirement portfolios."
        rr_color = "#FCD34D"
    elif ret_return <= 8.0:
        rr_note = "Moderate — reasonable for a diversified stock/bond portfolio over a long horizon."
        rr_color = "#4ADE80"
    elif ret_return <= 10.0:
        rr_note = "Historically in range — the S&P 500's 30-year average annualized return is ~10% (nominal, before inflation)."
        rr_color = "#4ADE80"
    else:
        rr_note = "Optimistic — exceeds the historical S&P 500 long-run average. Use with caution for planning purposes."
        rr_color = "#F87171"

    st.markdown(f"""
    <div class="card" style="border-left:4px solid {rr_color};padding:0.85rem 1.2rem;margin-top:0;margin-bottom:1rem;">
        <div style="font-size:0.88rem;color:#D4C8F0;">
            <strong style="color:#F0EBFF;">About this rate:</strong> {rr_note}
        </div>
        <div style="font-size:0.8rem;color:#A89BC2;margin-top:0.5rem;">
            The S&amp;P 500 (500 largest U.S.-listed companies) has returned approximately
            <strong style="color:#D4C8F0;">10% annually on average over 30 years</strong> (nominal).
            Adjusted for inflation (~3%/yr), the real return is closer to 7%.
            Diversified portfolios including bonds typically return less.
            Past performance does not guarantee future results.
        </div>
        <div style="font-size:0.75rem;color:#7A6A94;margin-top:0.4rem;">
            Sources: Macrotrends. (2024). <em>S&amp;P 500 historical annual returns.</em>
            <a href="https://www.macrotrends.net/2526/sp-500-historical-annual-returns" style="color:#A78BFA;">macrotrends.net</a> ·
            NerdWallet. (2024). <em>Average stock market return.</em>
            <a href="https://www.nerdwallet.com/investing/learn/average-stock-market-return" style="color:#A78BFA;">nerdwallet.com</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.caption(
        f"📊 You selected {ret_return:.1f}%. For context: the S&P 500 has averaged ~10%/year "
        "over the past 30 years (before inflation). A diversified portfolio (stocks + bonds) "
        "typically averages 6–8%. More conservative (bonds-heavy) portfolios average 3–5%. "
        "Adjust for your actual asset allocation and risk tolerance."
    )
    st.markdown("""
    <div class="citation" style="margin-top:0.25rem;margin-bottom:1rem;">
        Historical return benchmark: NerdWallet. (2024). <em>Average stock market return.</em>
        <a href="https://www.nerdwallet.com/investing/learn/average-stock-market-return">
        https://www.nerdwallet.com/investing/learn/average-stock-market-return</a>
    </div>
    """, unsafe_allow_html=True)

    age         = ss("age")
    ret_age     = ss("ret_age")
    salary      = ss("salary")
    bracket     = age_bracket(age)
    years_left  = max(0, ret_age - age)

    # Fidelity prescriptive benchmark
    mult_now    = fidelity_multiple(age)
    mult_at_ret = fidelity_multiple(ret_age)
    goal_now    = mult_now * salary
    goal_ret    = mult_at_ret * salary

    # SCF descriptive benchmark
    scf_peer = SCF_RET[bracket]

    # Projection
    projected = future_value(ret_saved, ret_monthly, ret_return, years_left)

    # Gap analysis
    gap_now     = goal_now - ret_saved
    gap_proj    = goal_ret - projected

    color_now  = "#4ADE80" if ret_saved >= goal_now  else "#F87171"
    color_proj = "#4ADE80" if projected  >= goal_ret else "#F87171"

    st.markdown(f"""
    <div class="card card-blue">
        <strong>Your Fidelity Milestone (Prescriptive — What You Need)</strong><br>
        <span style="font-size:0.85rem;color:#C084FC;">
        Goal at your age ({age}): <strong>{mult_now:.1f}× salary = {fmt_dollar(goal_now)}</strong><br>
        Goal at retirement ({ret_age}): <strong>{mult_at_ret:.1f}× salary = {fmt_dollar(goal_ret)}</strong>
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ── Peer comparison color ─────────────────────────────────────────────────
    if ret_saved >= scf_peer * 1.25:
        peer_color = "#4ADE80"
        peer_tier  = "Well above peer median"
        peer_icon  = "🟢"
    elif ret_saved >= scf_peer * 0.9:
        peer_color = "#FCD34D"
        peer_tier  = "Near peer median"
        peer_icon  = "🟡"
    else:
        peer_color = "#F87171"
        peer_tier  = "Below peer median"
        peer_icon  = "🔴"

    # ── Current position vs. Fidelity goal ───────────────────────────────────
    st.markdown(f"""
    <div class="card" style="border-left:5px solid {color_now};margin-top:0.75rem;">
        <div style="font-size:0.82rem;color:#A89BC2;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:0.75rem;">
            Where you stand today vs. the Fidelity milestone for your age
        </div>
        <div class="kpi-grid">
            <div class="kpi-box">
                <div class="label">Your Current Savings</div>
                <div class="value">{fmt_dollar(ret_saved)}</div>
                <div style="font-size:0.7rem;color:#A89BC2;margin-top:3px;">What you have now</div>
            </div>
            <div class="kpi-box">
                <div class="label">Fidelity Goal at Age {age}</div>
                <div class="value" style="color:{color_now}">{fmt_dollar(goal_now)}</div>
                <div style="font-size:0.7rem;color:#A89BC2;margin-top:3px;">{mult_now:.1f}× your annual salary — prescriptive target</div>
            </div>
            <div class="kpi-box">
                <div class="label">Gap / Surplus Today</div>
                <div class="value" style="color:{color_now}">
                    {"+" if gap_now <= 0 else "-"}{fmt_dollar(abs(gap_now))}
                </div>
                <div style="font-size:0.7rem;color:#A89BC2;margin-top:3px;">{"Ahead of Fidelity goal" if gap_now <= 0 else "Behind Fidelity goal"}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Peer comparison — separate, color-coded, with undersaving context ─────
    st.markdown(f"""
    <div class="card" style="border-left:5px solid {peer_color};margin-top:0.75rem;">
        <div style="font-size:0.82rem;color:#A89BC2;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:0.6rem;">
            How you compare to peers your age (descriptive — what others have)
        </div>
        <div class="kpi-grid">
            <div class="kpi-box">
                <div class="label">Your Savings</div>
                <div class="value">{fmt_dollar(ret_saved)}</div>
            </div>
            <div class="kpi-box">
                <div class="label">Peer Median (SCF 2022)</div>
                <div class="value">{fmt_dollar(scf_peer)}</div>
                <div style="font-size:0.7rem;color:#A89BC2;margin-top:3px;">Median for ages {bracket}</div>
            </div>
            <div class="kpi-box">
                <div class="label">vs. Peer Median</div>
                <div class="value" style="color:{peer_color}">
                    {peer_icon} {peer_tier}
                </div>
            </div>
        </div>
        <div style="margin-top:0.85rem;padding:0.6rem 0.8rem;background:#0E0A1E;border-radius:8px;border-left:3px solid #FCD34D;">
            <div style="font-size:0.82rem;color:#FDE68A;font-weight:600;margin-bottom:0.25rem;">
                ⚠️ Important context: peer median ≠ sufficient
            </div>
            <div style="font-size:0.8rem;color:#D4C8F0;line-height:1.55;">
                Research consistently shows that most Americans are <strong>significantly under-saved for retirement</strong>.
                Being above the peer median means you're doing better than most — but it does not mean you're on track
                to meet your own retirement income needs. The <strong>Fidelity milestone above</strong> is the
                more meaningful target for adequacy.
            </div>
            <div style="font-size:0.75rem;color:#A89BC2;margin-top:0.4rem;">
                Source: Munnell, A. H., &amp; Chen, A. (2021). <em>401(k)/IRA holdings in 2019: An update from the SCF.</em>
                Center for Retirement Research at Boston College, Issue Brief 21-5.
                <a href="https://crr.bc.edu/briefs/401kira-holdings-in-2019-an-update-from-the-scf/" style="color:#C084FC;">crr.bc.edu</a>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Projection card ───────────────────────────────────────────────────────
    st.markdown(f"""
    <div class="card" style="border-left:5px solid {color_proj};margin-top:0.75rem;">
        <div style="font-size:0.82rem;color:#A89BC2;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:0.75rem;">
            Projected retirement savings at age {ret_age} (with {ret_return:.1f}% annual return)
        </div>
        <div class="kpi-grid">
            <div class="kpi-box">
                <div class="label">Projected Savings</div>
                <div class="value" style="color:{color_proj}">{fmt_dollar(projected)}</div>
                <div style="font-size:0.7rem;color:#A89BC2;margin-top:3px;">If contributions continue</div>
            </div>
            <div class="kpi-box">
                <div class="label">Fidelity Goal at {ret_age}</div>
                <div class="value">{fmt_dollar(goal_ret)}</div>
                <div style="font-size:0.7rem;color:#A89BC2;margin-top:3px;">{mult_at_ret:.1f}× salary — prescriptive target</div>
            </div>
            <div class="kpi-box">
                <div class="label">Projected Gap / Surplus</div>
                <div class="value" style="color:{color_proj}">
                    {"+" if projected >= goal_ret else "-"}{fmt_dollar(abs(gap_proj))}
                </div>
                <div style="font-size:0.7rem;color:#A89BC2;margin-top:3px;">{"On track" if projected >= goal_ret else "Shortfall at retirement"}</div>
            </div>
            <div class="kpi-box">
                <div class="label">Years to Retirement</div>
                <div class="value">{years_left}</div>
                <div style="font-size:0.7rem;color:#A89BC2;margin-top:3px;">Time to grow savings</div>
            </div>
        </div>
        <p style="font-size:0.78rem;color:#A89BC2;margin-top:0.75rem;line-height:1.5;">
            ⚠️ Assumes constant {ret_return:.1f}% annual return and consistent contributions.
            Does <strong>not</strong> account for inflation (~3%/yr), taxes on withdrawals, or
            Social Security income. Consult a CFP® for personalized projections.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Fidelity milestone table
    st.markdown("**Fidelity Retirement Savings Milestones (Prescriptive)**")
    milestones = [(30,1),(35,2),(40,3),(45,4),(50,6),(55,7),(60,8),(65,9),(67,10)]
    rows = ""
    for a, m in milestones:
        hl = ' class="highlight"' if abs(a - age) <= 2 else ""
        rows += (f'<tr{hl}><td>{"▶ " if abs(a-age)<=2 else ""}Age {a}</td>'
                 f'<td>{m}× salary</td>'
                 f'<td>{fmt_dollar(m * salary)}</td></tr>')
    st.markdown(f"""
    <table class="bench-table">
        <thead><tr><th>Milestone Age</th><th>Multiple of Salary</th><th>Your Goal ({fmt_dollar(salary)}/yr)</th></tr></thead>
        <tbody>{rows}</tbody>
    </table>
    """, unsafe_allow_html=True)

    # SCF descriptive table
    st.markdown("**Federal Reserve SCF Median Retirement Savings by Age (Descriptive)**")
    rows2 = ""
    for ag, med in SCF_RET.items():
        hl = ' class="highlight"' if ag == bracket else ""
        rows2 += f'<tr{hl}><td>{"▶ " if ag==bracket else ""}{ag}</td><td>{fmt_dollar(med)}</td><td style="font-size:0.78rem;color:#A89BC2;">What peers have — not a sufficiency target</td></tr>'
    st.markdown(f"""
    <table class="bench-table">
        <thead><tr><th>Age Group</th><th>Median Retirement Savings</th><th>Note</th></tr></thead>
        <tbody>{rows2}</tbody>
    </table>
    """, unsafe_allow_html=True)

    if projected < goal_ret:
        extra_needed_mo = (gap_proj / ((((1 + ret_return/100/12)**( years_left*12) - 1) / (ret_return/100/12)) if ret_return > 0 else years_left*12))
        st.markdown(f"""
        <div class="card card-amber">
            💡 <strong>To close the projected gap:</strong> increasing your monthly contribution
            by approximately <strong>{fmt_dollar(max(0, extra_needed_mo))}/month</strong> could
            reach your retirement goal — assuming returns stay constant.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="citation">
        <strong>Sources:</strong><br>
        Fidelity Investments. (2024). <em>How much do I need to retire?</em>
        <a href="https://www.fidelity.com/viewpoints/retirement/how-much-do-i-need-to-retire">
        https://www.fidelity.com/viewpoints/retirement/how-much-do-i-need-to-retire</a><br>
        Board of Governors of the Federal Reserve System. (2023). <em>Survey of Consumer Finances, 2022.</em>
        <a href="https://www.federalreserve.gov/econres/scfindex.htm">https://www.federalreserve.gov/econres/scfindex.htm</a><br>
        Munnell, A. H., &amp; Chen, A. (2021). <em>401(k)/IRA holdings in 2019: An update from the SCF.</em>
        Center for Retirement Research at Boston College, Issue Brief 21-5.
        <a href="https://crr.bc.edu/briefs/401kira-holdings-in-2019-an-update-from-the-scf/">
        https://crr.bc.edu/briefs/401kira-holdings-in-2019-an-update-from-the-scf/</a>
    </div>
    """, unsafe_allow_html=True)

    nav_buttons()

# ─────────────────────────────────────────────
# PDF REPORT GENERATOR
# ─────────────────────────────────────────────
def generate_pdf(data: dict) -> bytes:
    """Build a formatted Financial Wellness Summary PDF using reportlab."""
    buf = io.BytesIO()

    # ── Document setup ────────────────────────────────────────────────────────
    doc = SimpleDocTemplate(
        buf, pagesize=letter,
        leftMargin=0.85*inch, rightMargin=0.85*inch,
        topMargin=0.9*inch,   bottomMargin=0.85*inch,
    )

    # ── Color palette ─────────────────────────────────────────────────────────
    PLUM     = colors.HexColor("#2D1B5E")
    LAVENDER = colors.HexColor("#7C3AED")
    LIGHT_PU = colors.HexColor("#EDE5F5")
    GREEN    = colors.HexColor("#166534")
    GREEN_BG = colors.HexColor("#D1FAE5")
    AMBER    = colors.HexColor("#92400E")
    AMBER_BG = colors.HexColor("#FEF3C7")
    RED      = colors.HexColor("#991B1B")
    RED_BG   = colors.HexColor("#FEE2E2")
    MID_GRAY = colors.HexColor("#374151")
    RULE     = colors.HexColor("#C4B5FD")
    WHITE    = colors.white
    NEAR_BLK = colors.HexColor("#111827")

    # ── Styles ────────────────────────────────────────────────────────────────
    base = getSampleStyleSheet()

    def ps(name, parent="Normal", **kw):
        return ParagraphStyle(name, parent=base[parent], **kw)

    S = {
        "title":    ps("title",    fontSize=22, textColor=PLUM,
                       fontName="Helvetica-Bold", spaceAfter=4, leading=26),
        "subtitle": ps("subtitle", fontSize=10, textColor=LAVENDER,
                       spaceAfter=2),
        "dateline": ps("dateline", fontSize=8.5, textColor=MID_GRAY,
                       spaceAfter=16),
        "h1":       ps("h1", "Heading1", fontSize=13, textColor=PLUM,
                       fontName="Helvetica-Bold", spaceBefore=14, spaceAfter=5,
                       leading=16),
        "h2":       ps("h2", "Heading2", fontSize=10.5, textColor=LAVENDER,
                       fontName="Helvetica-Bold", spaceBefore=8, spaceAfter=3),
        "body":     ps("body", fontSize=9.5, textColor=MID_GRAY, leading=14,
                       spaceAfter=4),
        "small":    ps("small", fontSize=8, textColor=MID_GRAY, leading=11,
                       spaceAfter=3),
        "goal_h":   ps("goal_h", fontSize=9, textColor=PLUM,
                       fontName="Helvetica-Bold", spaceBefore=6, spaceAfter=1),
        "goal_i":   ps("goal_i", fontSize=9, textColor=MID_GRAY, leading=13,
                       leftIndent=12, spaceAfter=1),
        "action_t": ps("action_t", fontSize=9.5, textColor=NEAR_BLK,
                       fontName="Helvetica-Bold", spaceAfter=2),
        "action_d": ps("action_d", fontSize=8.5, textColor=MID_GRAY, leading=13,
                       leftIndent=12, spaceAfter=6),
        "cite":     ps("cite", fontSize=7.5, textColor=colors.HexColor("#6B7280"),
                       leading=10, spaceAfter=2),
    }

    def rule(color=RULE, thickness=0.8):
        return HRFlowable(width="100%", thickness=thickness,
                          color=color, spaceAfter=8, spaceBefore=2)

    def kpi_table(rows):
        """rows = list of (label, value, status_color_hex or None)"""
        tdata = [[
            Paragraph(f"<b>{lbl}</b>", ps("kl", fontSize=7.5, textColor=colors.HexColor("#6B7280"),
                      fontName="Helvetica-Bold")),
            Paragraph(val, ps("kv", fontSize=11, textColor=colors.HexColor(col) if col else NEAR_BLK,
                      fontName="Helvetica-Bold"))
        ] for lbl, val, col in rows]
        t = Table(tdata, colWidths=[None, None], repeatRows=0)
        t.setStyle(TableStyle([
            ("ALIGN", (0,0), (-1,-1), "LEFT"),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#F9F5FF")),
            ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#DDD5EC")),
            ("INNERGRID", (0,0), (-1,-1), 0.25, colors.HexColor("#EDE5F5")),
            ("TOPPADDING", (0,0), (-1,-1), 5),
            ("BOTTOMPADDING", (0,0), (-1,-1), 5),
            ("LEFTPADDING", (0,0), (-1,-1), 7),
            ("RIGHTPADDING", (0,0), (-1,-1), 7),
        ]))
        return t

    def badge_para(text, bg_hex, fg_hex):
        style = ps("badge", fontSize=8, textColor=colors.HexColor(fg_hex),
                   fontName="Helvetica-Bold", backColor=colors.HexColor(bg_hex),
                   borderPadding=2)
        return Paragraph(text, style)

    # ── Story ─────────────────────────────────────────────────────────────────
    story = []
    d = data  # shorthand

    # Header
    story.append(Paragraph("Financial Wellness Checkup", S["title"]))
    story.append(Paragraph("Personalized Assessment Summary", S["subtitle"]))
    story.append(Paragraph(
        f"Completed: {d['date']} &nbsp;·&nbsp; "
        f"Age: {d['age']} &nbsp;·&nbsp; "
        f"Salary: {d['salary_fmt']} &nbsp;·&nbsp; "
        f"Region: {d['region']}",
        S["dateline"]
    ))
    story.append(rule(PLUM, 1.5))

    # ── 1. Financial Snapshot ─────────────────────────────────────────────────
    story.append(Paragraph("Financial Snapshot", S["h1"]))

    def status_hex(val, good_thresh, warn_thresh, higher_is_better=True):
        if higher_is_better:
            return "#166534" if val >= good_thresh else "#92400E" if val >= warn_thresh else "#991B1B"
        else:
            return "#166534" if val <= good_thresh else "#92400E" if val <= warn_thresh else "#991B1B"

    snap_rows = [
        ("Net Worth",           d["net_worth_fmt"],        None),
        ("CFPB Well-Being Score",
         f"{d['cfpb_score']}/100 — {d['cfpb_tier']}",
         status_hex(d['cfpb_score'], 61, 41)),
        ("Emergency Fund",
         f"{d['ef_months']:.1f} months of expenses",
         status_hex(d['ef_months'], 6, 3)),
        ("Savings Rate",
         f"{d['savings_rate']:.1f}% of gross income",
         status_hex(d['savings_rate'], 15, 10)),
        ("Retirement Savings",  d['ret_saved_fmt'],         None),
        ("Retirement Goal (Fidelity)",
         f"{d['ret_goal_fmt']} ({d['ret_mult']:.1f}x salary)",
         None),
        ("Retirement Projection",
         d['ret_projected_fmt'],
         status_hex(d['ret_projected'], d['ret_goal'], d['ret_goal'] * 0.8)),
        ("Avg. Financial Confidence",
         f"{d['avg_conf']:.1f} / 5",
         status_hex(d['avg_conf'], 4, 3)),
    ]
    story.append(kpi_table(snap_rows))
    story.append(Spacer(1, 8))
    story.append(rule())

    # ── 2. Goals ──────────────────────────────────────────────────────────────
    story.append(Paragraph("Your Financial Goals", S["h1"]))
    story.append(Paragraph(
        "Goals are organized by time horizon. Custom goals show the horizon you selected.",
        S["small"]
    ))
    story.append(Spacer(1, 4))

    # Group preset goals by horizon
    grouped = {}
    for g in d["preset_goals"]:
        cat = GOAL_HORIZON_MAP.get(g, "Ongoing Financial Security")
        grouped.setdefault(cat, []).append(g)

    # Render in order
    cat_order = ["Short-Term (0–2 years)", "Medium-Term (3–5 years)",
                 "Long-Term (5+ years)", "Ongoing Financial Security"]
    any_preset = False
    for cat in cat_order:
        items = grouped.get(cat, [])
        if items:
            any_preset = True
            story.append(KeepTogether([
                Paragraph(cat, S["goal_h"]),
                *[Paragraph(f"• {g}", S["goal_i"]) for g in items],
            ]))

    # Custom goals
    if d["custom_goals"]:
        story.append(Paragraph("Custom Goals", S["goal_h"]))
        for cg in d["custom_goals"]:
            story.append(Paragraph(
                f"• {cg['text']}  <font color='#7C3AED'><i>({cg['horizon']})</i></font>",
                S["goal_i"]
            ))

    if not any_preset and not d["custom_goals"]:
        story.append(Paragraph("No goals selected.", S["body"]))

    story.append(Spacer(1, 4))
    story.append(rule())

    # ── 3. Action Plan ────────────────────────────────────────────────────────
    story.append(Paragraph("Priority Action Steps", S["h1"]))
    story.append(Paragraph(
        "Ranked by evidence-based impact on financial well-being.",
        S["small"]
    ))
    story.append(Spacer(1, 6))

    priority_cfg = {
        "critical": ("#FEE2E2", "#991B1B", "CRITICAL"),
        "high":     ("#FEF3C7", "#92400E", "HIGH PRIORITY"),
        "medium":   ("#EDE5F5", "#4C1D95", "RECOMMENDED"),
        "good":     ("#D1FAE5", "#166534", "MAINTAIN"),
    }
    for i, a in enumerate(d["actions"], 1):
        bg, fg, lbl = priority_cfg.get(a["priority"], ("#F3F4F6", "#374151", ""))
        badge_style = ps(
            f"bdg{i}", fontSize=7, textColor=colors.HexColor(fg),
            fontName="Helvetica-Bold", backColor=colors.HexColor(bg),
            leftIndent=0,
        )
        badge_para = Paragraph(f"  {lbl}  ", badge_style)
        badge_tbl = Table([[badge_para]], colWidths=[1.2*inch])
        badge_tbl.setStyle(TableStyle([
            ("BOX",           (0,0), (0,0), 0.5, colors.HexColor(fg)),
            ("TOPPADDING",    (0,0), (-1,-1), 2),
            ("BOTTOMPADDING", (0,0), (-1,-1), 2),
            ("LEFTPADDING",   (0,0), (-1,-1), 4),
            ("RIGHTPADDING",  (0,0), (-1,-1), 4),
        ]))
        title_para = Paragraph(f"{i}. {a['title']}", S["action_t"])
        row_tbl = Table([[badge_tbl, title_para]], colWidths=[1.3*inch, None])
        row_tbl.setStyle(TableStyle([
            ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
            ("LEFTPADDING",   (0,0), (-1,-1), 0),
            ("RIGHTPADDING",  (0,0), (-1,-1), 0),
            ("TOPPADDING",    (0,0), (-1,-1), 2),
            ("BOTTOMPADDING", (0,0), (-1,-1), 2),
        ]))
        story.append(KeepTogether([
            row_tbl,
            Paragraph(a["detail"], S["action_d"]),
        ]))

    story.append(rule())

    # ── 4. Resources ─────────────────────────────────────────────────────────
    story.append(Paragraph("Evidence-Based Resources", S["h1"]))
    resources = [
        ("CFPB Financial Well-Being Tools",
         "consumerfinance.gov/consumer-tools/financial-well-being/"),
        ("SmartAboutMoney.org (NEFE)",
         "smartaboutmoney.org"),
        ("MyMoney.gov — U.S. Federal Financial Literacy Portal",
         "mymoney.gov"),
        ("NFCC.org — Nonprofit Credit Counseling",
         "nfcc.org"),
        ("NAPFA.org — Fee-Only Fiduciary Financial Advisors",
         "napfa.org/find-an-advisor"),
    ]
    for label, url in resources:
        story.append(Paragraph(
            f"• <b>{label}</b>: <font color='#7C3AED'>{url}</font>",
            S["body"]
        ))

    story.append(Spacer(1, 10))
    story.append(rule(PLUM, 1.0))

    # ── Footer ────────────────────────────────────────────────────────────────
    story.append(Paragraph(
        "This report was generated by the Financial Wellness Checkup tool. "
        "All data was entered by the user and processed locally — nothing was stored or transmitted. "
        "This is not financial, legal, or tax advice. Consult a qualified CFP® for personalized guidance. "
        "Re-take this assessment quarterly to track your progress.",
        S["cite"]
    ))
    story.append(Paragraph(
        "Key sources: CFPB (2017); Federal Reserve SCF (2022); Fidelity Investments (2024); "
        "Lusardi &amp; Mitchell (2014); Madrian &amp; Shea (2001); BLS Consumer Expenditure Survey (2022).",
        S["cite"]
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Built by <font color='#7C3AED'>Andrea Pellegrini</font> "
        "(andreapellegrini.info) with assistance from Claude Sonnet 4.6 (Anthropic). "
        "Pellegrini, A. (2025). <i>Financial Wellness Checkup</i> [Interactive assessment tool]. "
        "Retrieved from financialwellnesscheckup.streamlit.app",
        S["cite"]
    ))
    story.append(Paragraph(
        "Return to the tool anytime to update your goals and financial outlook: "
        "financialwellnesscheckup.streamlit.app",
        ps("tool_url", fontSize=7.5, textColor=colors.HexColor("#7C3AED"), leading=10)
    ))

    doc.build(story)
    return buf.getvalue()


# ─────────────────────────────────────────────
# STEP 9 — ACTION PLAN
# ─────────────────────────────────────────────
def step_action_plan():
    render_header(); render_progress()
    st.markdown('<p class="step-title">Your Personalized Action Plan</p>', unsafe_allow_html=True)

    # Gather computed values
    age         = ss("age")
    salary      = ss("salary")
    bracket     = age_bracket(age)
    _, _, total_nw = net_worth()
    monthly_exp = monthly_expenses()
    ef          = ss("ef")
    ef_months   = (ef / monthly_exp) if monthly_exp > 0 else 0
    surplus, sr = savings_rate()
    ret_saved   = ss("ret_current")
    ret_age     = ss("ret_age")
    years_left  = max(0, ret_age - age)
    projected   = future_value(ret_saved, ss("ret_monthly"), ss("ret_return"), years_left)
    mult_ret    = fidelity_multiple(ret_age)
    goal_ret    = mult_ret * salary
    goals       = ss("goals")
    cfpb_score, _ = _compute_cfpb_score()
    conf        = ss("conf")
    avg_conf    = sum(conf.values()) / len(conf)
    nw_data     = ss("nw")
    cc_debt     = nw_data.get("cc_debt", 0)

    # ── Snapshot ──────────────────────────────
    st.markdown("#### 📊 Your Financial Snapshot")
    ef_color  = "#4ADE80" if ef_months >= 6 else "#FCD34D" if ef_months >= 3 else "#F87171"
    sr_color  = "#4ADE80" if sr >= 15 else "#FCD34D" if sr >= 10 else "#F87171"
    ret_color = "#4ADE80" if projected >= goal_ret else "#F87171"
    cfpb_color= "#4ADE80" if cfpb_score >= 61 else "#FCD34D" if cfpb_score >= 41 else "#F87171"

    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-box"><div class="label">Net Worth</div><div class="value">{fmt_dollar(total_nw)}</div></div>
        <div class="kpi-box"><div class="label">Emergency Fund</div><div class="value" style="color:{ef_color}">{ef_months:.1f} mo</div></div>
        <div class="kpi-box"><div class="label">Savings Rate</div><div class="value" style="color:{sr_color}">{sr:.1f}%</div></div>
        <div class="kpi-box"><div class="label">CFPB Score</div><div class="value" style="color:{cfpb_color}">{cfpb_score}/100</div></div>
        <div class="kpi-box"><div class="label">Retirement Projection</div><div class="value" style="color:{ret_color}">{fmt_dollar(projected)}</div></div>
        <div class="kpi-box"><div class="label">Retirement Goal</div><div class="value">{fmt_dollar(goal_ret)}</div></div>
    </div>
    """, unsafe_allow_html=True)

    if goals or ss("custom_goals"):
        st.markdown("#### 🎯 Your Financial Goals")
        st.caption("Goals are grouped by time horizon. Work through them in order — short-term first.")

        # Group preset goals by horizon
        grouped = {}
        for g in goals:
            cat = GOAL_HORIZON_MAP.get(g, "Ongoing Financial Security")
            grouped.setdefault(cat, []).append(g)

        # Horizon badges config
        horizon_cfg = {
            "Short-Term (0–2 years)":    ("#FCD34D", "#1A1200", "SHORT-TERM  0–2 yrs"),
            "Medium-Term (3–5 years)":   ("#A78BFA", "#0E0A1E", "MEDIUM-TERM  3–5 yrs"),
            "Long-Term (5+ years)":      ("#4ADE80", "#082010", "LONG-TERM  5+ yrs"),
            "Ongoing Financial Security":("#94A3B8", "#0F172A", "ONGOING"),
        }
        cat_order = ["Short-Term (0–2 years)", "Medium-Term (3–5 years)",
                     "Long-Term (5+ years)", "Ongoing Financial Security"]

        for cat in cat_order:
            items = grouped.get(cat, [])
            if not items:
                continue
            accent, bg, badge_txt = horizon_cfg[cat]
            badge_html = f"<span style='background:{accent};color:{bg};font-size:0.65rem;font-weight:700;padding:2px 8px;border-radius:99px;letter-spacing:0.06em;'>{badge_txt}</span>"
            items_html = "".join(
                f"<li style='margin-bottom:4px;'>{g}</li>"
                for g in items
            )
            st.markdown(f"""
            <div style="margin-bottom:0.75rem;">
                {badge_html}
                <ul style="margin:0.4rem 0 0;padding-left:1.3rem;font-size:0.9rem;color:#D4C8F0;line-height:1.6;">
                    {items_html}
                </ul>
            </div>
            """, unsafe_allow_html=True)

        if ss("custom_goals"):
            custom_html = "".join(
                f"<li style='margin-bottom:4px;'>{cg['text']} "
                f"<span style='font-size:0.78rem;color:#C084FC;'>({cg['horizon']})</span></li>"
                for cg in ss("custom_goals")
            )
            st.markdown(f"""
            <div style="margin-bottom:0.75rem;">
                <span style='background:#C084FC;color:#0E0A1E;font-size:0.65rem;font-weight:700;padding:2px 8px;border-radius:99px;letter-spacing:0.06em;'>CUSTOM GOALS</span>
                <ul style="margin:0.4rem 0 0;padding-left:1.3rem;font-size:0.9rem;color:#D4C8F0;line-height:1.6;">
                    {custom_html}
                </ul>
            </div>
            """, unsafe_allow_html=True)

    # ── Priority Action Items ──────────────────
    st.markdown("#### ✅ Priority Action Steps")
    st.caption("Items are ranked by evidence-based impact on financial well-being.")

    actions = []

    # 1. Emergency Fund (highest impact)
    if ef_months < 3:
        actions.append({
            "icon": "🚨", "priority": "critical",
            "title": "Build your emergency fund — top priority",
            "detail": (
                f"You have {ef_months:.1f} months of expenses covered. "
                f"Aim for 3 months ({fmt_dollar(monthly_exp * 3)}) first, then 6 months ({fmt_dollar(monthly_exp * 6)}). "
                "Open a dedicated high-yield savings account. Automate a monthly transfer — "
                "automation increases savings rates significantly (Madrian & Shea, 2001)."
            )
        })
    elif ef_months < 6:
        actions.append({
            "icon": "⚠️", "priority": "high",
            "title": "Top off your emergency fund to 6 months",
            "detail": (
                f"You have {ef_months:.1f} months covered — a 3-month minimum, but 6 months "
                f"is the standard recommendation. Gap to goal: {fmt_dollar(max(0, monthly_exp*6 - ef))}."
            )
        })

    # 2. High-interest debt
    if cc_debt > 0:
        actions.append({
            "icon": "💳", "priority": "critical",
            "title": f"Pay off credit card debt ({fmt_dollar(cc_debt)})",
            "detail": (
                "Credit card debt typically carries 20–27% APR — the highest guaranteed "
                "return available is paying it off. Use the avalanche method (highest rate first) "
                "for mathematically optimal results. Freeing this cash flow accelerates every other goal."
            )
        })

    # 3. Retirement savings rate
    ret_contrib_pct = (ss("ret_monthly") * 12 / salary * 100) if salary > 0 else 0
    if ret_contrib_pct < 10:
        actions.append({
            "icon": "📈", "priority": "high",
            "title": "Increase retirement contributions to at least 10–15% of gross income",
            "detail": (
                f"You're contributing approximately {ret_contrib_pct:.1f}% of gross income. "
                "The research consensus is 15% (including employer match) for adequate retirement security. "
                "If your employer offers a 401(k) match, ensure you contribute at least enough to get the full match — "
                "that is a 50–100% guaranteed return on those dollars."
            )
        })

    # 4. Retirement projection gap
    if projected < goal_ret:
        actions.append({
            "icon": "🏦", "priority": "high",
            "title": f"Close your retirement savings gap ({fmt_dollar(goal_ret - projected)} projected shortfall)",
            "detail": (
                f"At your current pace, you're projected to reach {fmt_dollar(projected)} by age {ret_age}, "
                f"vs. the Fidelity goal of {fmt_dollar(goal_ret)} ({mult_ret:.1f}× your salary). "
                "Consider: increasing monthly contributions, delaying retirement by 1–2 years (reduces "
                "gap significantly due to compounding), and ensuring investments are appropriately "
                "allocated for your time horizon."
            )
        })

    # 5. Savings rate
    if sr < 10:
        actions.append({
            "icon": "💰", "priority": "high",
            "title": f"Improve your savings rate (currently {sr:.1f}% — target 15–20%)",
            "detail": (
                "Review flexible expenses for cuts. Common high-ROI targets: "
                "meal planning (saves avg. $200–400/mo vs. dining out), reviewing subscription services, "
                "and negotiating recurring bills (insurance, internet, phone). "
                "Even a 3% increase in savings rate compounded over decades makes a substantial difference."
            )
        })

    # 6. Low confidence areas
    low_conf = [k for k, v in conf.items() if v <= 2]
    conf_label_map = {
        "daily": "day-to-day money management", "emergency": "emergency planning",
        "saving": "savings strategies", "investing": "investing",
        "retirement": "retirement planning", "insurance": "insurance",
        "tax": "tax planning", "estate": "estate planning",
    }
    if low_conf:
        areas_str = ", ".join(conf_label_map[k] for k in low_conf[:3])
        actions.append({
            "icon": "📚", "priority": "medium",
            "title": f"Build financial knowledge in: {areas_str}",
            "detail": (
                "Financial literacy is associated with higher savings rates, better retirement outcomes, "
                "and lower debt burden (Lusardi & Mitchell, 2014). "
                "Free evidence-based resources: MyMoney.gov (federal financial education portal), "
                "NEFE's SmartAboutMoney.org, and CFPB's Consumer Tools library. "
                "Consider a one-time session with a fee-only CFP® for personalized guidance."
            )
        })

    # 7. CFPB low well-being
    if cfpb_score < 41:
        actions.append({
            "icon": "🧠", "priority": "medium",
            "title": "Address financial stress and anxiety",
            "detail": (
                "Your CFPB well-being score suggests meaningful financial stress. "
                "Research links financial stress to poorer health outcomes and impaired decision-making. "
                "Beyond the financial steps above, consider: connecting with a nonprofit credit counselor "
                "(NFCC.org), exploring income-contingent repayment options for student loans, "
                "and using the CFPB's 'Your Money, Your Goals' toolkit for structured planning."
            )
        })

    # 8. No written budget
    if "Create or update a written budget" in goals or sr < 0:
        actions.append({
            "icon": "📋", "priority": "medium",
            "title": "Create and maintain a written budget",
            "detail": (
                "Adults with a written budget save more and carry less high-interest debt. "
                "The 50/30/20 framework is a practical starting point: 50% needs, 30% wants, 20% savings/debt. "
                "Tools: YNAB, Mint (free), or a simple spreadsheet. "
                "Review monthly — a budget review takes 15 minutes and improves accuracy over time."
            )
        })

    # 9. Generic good habits if doing well
    if not actions:
        actions.append({
            "icon": "🌟", "priority": "good",
            "title": "Maintain and optimize your strong financial foundation",
            "detail": (
                "You appear to be in a strong financial position. Next-level steps: "
                "review asset allocation annually, ensure beneficiary designations are current, "
                "consider tax-loss harvesting in taxable accounts, and review insurance coverage annually. "
                "Consider consulting a fee-only CFP® every 2–3 years for a comprehensive review."
            )
        })

    priority_labels = {
        "critical": ("badge-critical", "Critical"),
        "high":     ("badge-high",     "High Priority"),
        "medium":   ("badge-medium",   "Recommended"),
        "good":     ("badge-good",     "Maintain"),
    }

    for a in actions:
        badge_cls, badge_lbl = priority_labels[a["priority"]]
        st.markdown(f"""
        <div class="action-item">
            <div class="action-icon">{a["icon"]}</div>
            <div class="action-text">
                <strong>{a["title"]} <span class="badge {badge_cls}">{badge_lbl}</span></strong>
                <span>{a["detail"]}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Resources ─────────────────────────────
    st.markdown("#### 🔗 Evidence-Based Resources")
    st.markdown("""
    <div class="card card-slate">
        <ul style="margin:0;padding-left:1.2rem;font-size:0.88rem;color:#D4C8F0;line-height:2;">
            <li>📊 <a href="https://www.consumerfinance.gov/consumer-tools/financial-well-being/" target="_blank">CFPB Financial Well-Being Tools</a> — validated assessment & planning resources</li>
            <li>🎓 <a href="https://www.smartaboutmoney.org" target="_blank">SmartAboutMoney.org (NEFE)</a> — free, research-based financial education</li>
            <li>🏛️ <a href="https://www.mymoney.gov" target="_blank">MyMoney.gov</a> — U.S. federal financial literacy portal</li>
            <li>📞 <a href="https://www.nfcc.org" target="_blank">NFCC.org</a> — nonprofit credit counseling (free or low-cost)</li>
            <li>👤 <a href="https://www.napfa.org/find-an-advisor" target="_blank">NAPFA.org</a> — fee-only fiduciary financial advisors</li>
            <li>📱 <a href="https://www.consumerfinance.gov/consumer-tools/your-money-your-goals/" target="_blank">CFPB "Your Money, Your Goals" Toolkit</a></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # ── Save / Print ──────────────────────────────────────────────────────────
    st.markdown("#### 💾 Save or Print Your Report")
    _, _, total_nw = net_worth()

    # Determine CFPB tier label
    cfpb_tier = ("High well-being" if cfpb_score >= 61
                 else "Moderate well-being" if cfpb_score >= 41
                 else "Lower well-being")

    pdf_data = {
        "date":             date.today().strftime("%B %d, %Y"),
        "age":              age,
        "salary_fmt":       fmt_dollar(salary),
        "region":           ss("region"),
        "net_worth_fmt":    fmt_dollar(total_nw),
        "cfpb_score":       cfpb_score,
        "cfpb_tier":        cfpb_tier,
        "ef_months":        ef_months,
        "savings_rate":     sr,
        "ret_saved_fmt":    fmt_dollar(ret_saved),
        "ret_goal_fmt":     fmt_dollar(goal_ret),
        "ret_mult":         mult_ret,
        "ret_projected_fmt":fmt_dollar(projected),
        "ret_projected":    projected,
        "ret_goal":         goal_ret,
        "avg_conf":         avg_conf,
        "preset_goals":     goals,
        "custom_goals":     ss("custom_goals"),
        "actions":          actions,
    }

    try:
        pdf_bytes = generate_pdf(pdf_data)
        st.download_button(
                label="⬇️ Download PDF Report",
                data=pdf_bytes,
                file_name=f"financial-wellness-{date.today().isoformat()}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
    except Exception as e:
        st.warning(f"PDF generation unavailable: {e}. Please take a screenshot to save your results.")

    st.markdown("""
    <div class="card card-purple" style="text-align:center;margin-top:1.5rem;">
        <strong style="font-size:1.05rem;">Financial wellness is a journey, not a destination.</strong><br>
        <span style="font-size:0.88rem;color:#C4B5FD;">
        Small, consistent improvements compound over time — in your savings and in your well-being.
        Re-take this assessment quarterly to track your progress.
        </span>
        <div style="margin-top:0.75rem;font-size:0.78rem;color:#A89BC2;">
            🔗 Return anytime at
            <a href="https://financialwellnesscheckup.streamlit.app/" target="_blank"
               style="color:#C084FC;font-weight:600;">financialwellnesscheckup.streamlit.app</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="citation">
        <strong>Key Sources for Action Plan Recommendations:</strong><br>
        Lusardi, A., &amp; Mitchell, O. S. (2014). The economic importance of financial literacy: Theory and evidence.
        <em>Journal of Economic Literature, 52</em>(1), 5–44. <a href="https://doi.org/10.1257/jel.52.1.5">https://doi.org/10.1257/jel.52.1.5</a><br>
        Madrian, B. C., &amp; Shea, D. F. (2001). The power of suggestion: Inertia in 401(k) participation and savings behavior.
        <em>Quarterly Journal of Economics, 116</em>(4), 1149–1187. <a href="https://doi.org/10.1162/003355301753265543">https://doi.org/10.1162/003355301753265543</a><br>
        National Endowment for Financial Education. (2023). <em>Financial education and decision-making.</em>
        <a href="https://www.nefe.org/research">https://www.nefe.org/research</a><br>
        Choi, J. J., Laibson, D., Madrian, B. C., &amp; Metrick, A. (2004). For better or for worse: Default effects and
        401(k) savings behavior. In D. Wise (Ed.), <em>Perspectives on the Economics of Aging</em> (pp. 81–126). University of Chicago Press.
        <a href="https://doi.org/10.7208/chicago/9780226903286.001.0001">https://doi.org/10.7208/chicago/9780226903286.001.0001</a><br><br>
        <strong>Tool citation:</strong>
        Pellegrini, A. (2025). <em>Financial Wellness Checkup</em> [Interactive assessment tool].
        Built with assistance from Claude Sonnet 4.6 (Anthropic).
        <a href="https://financialwellnesscheckup.streamlit.app/" style="color:#C084FC;">
        https://financialwellnesscheckup.streamlit.app/</a> ·
        Developer: <a href="https://andreapellegrini.info" style="color:#C084FC;">andreapellegrini.info</a>
    </div>
    """, unsafe_allow_html=True)

    nav_buttons(next_label="Complete ✓")

# ─────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────
STEP_FNS = [
    step_welcome, step_demographics, step_goals, step_cfpb,
    step_cfpb_score, step_confidence, step_networth, step_cashflow,
    step_emergency, step_retirement, step_action_plan,
]

STEP_FNS[ss("step")]()
