"""
Financial Wellness Checkup — Interactive Assessment Tool
Built with Streamlit | All data processed locally in your session
"""

import streamlit as st
import json
import math
from datetime import date

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

/* ── Palette reference (WCAG AA verified) ───────────────────────────────────
   Plum dark   #3D1A5C  14:1 on white   Primary brand / headers
   Plum mid    #6B3FA0   7:1 on white   Accents / borders / info
   Forest grn  #1E5C3A   7.5:1 on wht  Success / positive states
   Amber dark  #7A4F00   8.5:1 on wht  Warning / caution states
   Crimson     #8B1A1A   9:1 on white   Critical / danger states
   Text dark   #1A0A2E  15:1 on white   Primary headings
   Text body   #3D2C5C   9.5:1          Body copy
   Text muted  #5E4D78   5.5:1          Labels / captions (large text ok)
   Text xmute  #7A6A94   4.6:1          Footnotes (large/UI text only)
   ─────────────────────────────────────────────────────────────────────────── */

/* Base */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #FAF7F4;
}
h1, h2, h3 {
    font-family: 'DM Serif Display', serif;
    letter-spacing: -0.02em;
}

/* Hide default streamlit chrome */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main container */
.block-container {
    max-width: 820px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* Card containers */
.card {
    background: white;
    border-radius: 16px;
    padding: 1.5rem 2rem;
    border: 1px solid #DDD5EC;
    margin-bottom: 1rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
.card-green  { border-left: 4px solid #1E5C3A; background: #E8F5EE; }
.card-amber  { border-left: 4px solid #7A4F00; background: #FEF9ED; }
.card-red    { border-left: 4px solid #8B1A1A; background: #FDF0F0; }
.card-blue   { border-left: 4px solid #6B3FA0; background: #F3EDFA; }
.card-purple { border-left: 4px solid #6B3FA0; background: #F3EDFA; }
.card-slate  { border-left: 4px solid #5E4D78; background: #FAF7F4; }

/* Hero header */
.app-header {
    background: linear-gradient(135deg, #3D1A5C 0%, #6B3FA0 100%);
    color: white;
    border-radius: 20px;
    padding: 2.5rem 2.5rem 2rem;
    margin-bottom: 2rem;
    box-shadow: 0 8px 32px rgba(30,58,95,0.18);
}
.app-header h1 { color: white; margin: 0; font-size: 2.1rem; }
.app-header p  { color: #E8D9F8; margin: 0.4rem 0 0; font-size: 1.05rem; }

/* Progress bar */
.progress-wrap  { margin: 0 0 2rem; }
.progress-label { display: flex; justify-content: space-between; font-size: 0.78rem; color: #5E4D78; margin-bottom: 6px; }
.progress-track { background: #D4C9E8; border-radius: 99px; height: 8px; width: 100%; overflow: hidden; }
.progress-fill  { background: linear-gradient(90deg, #6B3FA0, #9B72CF); height: 100%; border-radius: 99px; transition: width 0.4s ease; }

/* Step title */
.step-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.75rem;
    color: #1A0A2E;
    margin: 0 0 0.3rem;
}
.step-subtitle { color: #5E4D78; font-size: 0.95rem; margin-bottom: 1.5rem; }

/* KPI grid */
.kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 1rem; margin: 1rem 0; }
.kpi-box  { background: white; border-radius: 12px; padding: 1rem; border: 1px solid #D4C9E8; text-align: center; }
.kpi-box .label { font-size: 0.75rem; color: #5E4D78; text-transform: uppercase; letter-spacing: 0.05em; }
.kpi-box .value { font-size: 1.6rem; font-weight: 700; color: #3D1A5C; margin-top: 2px; }

/* Metric bar */
.metric-bar-wrap { margin: 0.6rem 0; }
.metric-bar-label { display: flex; justify-content: space-between; font-size: 0.82rem; color: #3D2C5C; margin-bottom: 4px; }
.metric-bar-track { background: #D4C9E8; border-radius: 99px; height: 10px; }
.metric-bar-fill  { height: 100%; border-radius: 99px; }

/* Citation block */
.citation {
    font-size: 0.72rem;
    color: #5E4D78;
    background: #FAF7F4;
    border-radius: 8px;
    padding: 0.75rem 1rem;
    margin-top: 1rem;
    border-left: 3px solid #C4B8DE;
    line-height: 1.5;
}

/* Nav buttons */
.stButton > button {
    border-radius: 10px !important;
    font-weight: 500 !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: all 0.2s ease !important;
}
div[data-testid="column"]:first-child .stButton > button {
    background: #F2EDF9 !important;
    color: #3D2C5C !important;
    border: 1px solid #D4C9E8 !important;
}
div[data-testid="column"]:last-child .stButton > button {
    background: linear-gradient(135deg, #3D1A5C, #6B3FA0) !important;
    color: white !important;
    border: none !important;
}

/* Checkbox styling */
.stCheckbox label span { font-size: 0.9rem; }

/* Section divider */
.divider { border: none; border-top: 1px solid #D4C9E8; margin: 1.5rem 0; }

/* Action item */
.action-item {
    display: flex; gap: 12px; align-items: flex-start;
    background: white; border-radius: 12px;
    padding: 1rem 1.2rem; margin-bottom: 0.75rem;
    border: 1px solid #D4C9E8;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.action-icon { font-size: 1.4rem; flex-shrink: 0; }
.action-text strong { display: block; font-size: 0.92rem; color: #1A0A2E; margin-bottom: 2px; }
.action-text span   { font-size: 0.82rem; color: #5E4D78; }

/* Priority badge */
.badge {
    display: inline-block; font-size: 0.68rem; font-weight: 600;
    padding: 2px 8px; border-radius: 99px; margin-left: 6px;
    text-transform: uppercase; letter-spacing: 0.06em;
}
.badge-critical { background: #FDEAEA; color: #8B1A1A; }
.badge-high     { background: #FEF4DC; color: #7A4F00; }
.badge-medium   { background: #EDE5F5; color: #3D1A5C; }
.badge-good     { background: #E4F4EC; color: #1E5C3A; }

/* Benchmark table */
.bench-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; margin-top: 0.5rem; }
.bench-table th { background: #3D1A5C; color: white; padding: 8px 12px; text-align: left; }
.bench-table td { padding: 7px 12px; border-bottom: 1px solid #D4C9E8; }
.bench-table tr.highlight td { background: #EDE5F5; font-weight: 600; }
.bench-table tr:hover td { background: #FAF7F4; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────
DEFAULTS = {
    "step": 0,
    # Demographics
    "age": 35, "salary": 60000, "ret_age": 67, "region": "National Average",
    # Goals
    "goals": [],
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
        "housing": 1200, "transport": 400, "insurance": 250, "debt_min": 150,
        "groceries": 400, "utilities": 150, "personal": 100,
        "entertainment": 200, "other_flex": 100,
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
    fixed = sum([exp.get("housing", 0), exp.get("transport", 0),
                 exp.get("insurance", 0), exp.get("debt_min", 0)])
    flex  = sum([exp.get("groceries", 0), exp.get("utilities", 0),
                 exp.get("personal", 0), exp.get("entertainment", 0),
                 exp.get("other_flex", 0)])
    occ   = ss("occ_annual") / 12
    return fixed + flex + occ

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

# ─────────────────────────────────────────────
# CFPB QUESTIONS (validated 10-item scale)
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
# PROGRESS HEADER
# ─────────────────────────────────────────────
STEPS = [
    "Welcome", "About You", "Goal Setting", "CFPB Well-Being",
    "Financial Confidence", "Net Worth", "Cash Flow",
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

def metric_bar(label, val, max_val, color="#6B3FA0", suffix=""):
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
        <ul style="margin:0.5rem 0 0; padding-left:1.2rem; color:#3D1A5C; font-size:0.9rem;">
            <li>Demographic profile &amp; goal-setting activity</li>
            <li>CFPB Financial Well-Being Scale (validated 10-item instrument)</li>
            <li>Financial confidence self-assessment</li>
            <li>Net worth calculation with peer benchmarks</li>
            <li>Cash flow &amp; savings rate analysis</li>
            <li>Emergency fund adequacy check</li>
            <li>Retirement readiness projection</li>
            <li>Personalized, evidence-based action plan</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="card card-amber">
            <strong>⏱ Time required</strong><br>
            <span style="font-size:0.88rem;color:#7A4F00;">10–15 minutes</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="card card-green">
            <strong>🔒 Privacy</strong><br>
            <span style="font-size:0.88rem;color:#1E5C3A;">All data stays in your browser session</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card card-slate">
        <strong>About Benchmarks in This Tool</strong><br><br>
        <span style="font-size:0.88rem;color:#3D2C5C;">
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

    c1, c2 = st.columns(2)
    with c1:
        age = st.number_input("Your current age", 18, 80, ss("age"), step=1)
        ss_set("age", age)
        ret_age = st.number_input("Target retirement age", age + 1, 80,
                                  max(age + 1, ss("ret_age")), step=1)
        ss_set("ret_age", ret_age)
    with c2:
        sal = st.number_input("Annual gross salary ($, before taxes)", 0, 2_000_000,
                              ss("salary"), step=1000, format="%d")
        ss_set("salary", sal)
        region = st.selectbox("Region (for cost-of-living context)",
                              ["National Average", "Northeast", "Midwest", "South", "West"],
                              index=["National Average","Northeast","Midwest","South","West"].index(ss("region")))
        ss_set("region", region)

    yrs = ret_age - age
    mult = fidelity_multiple(age)
    st.markdown(f"""
    <div class="card card-blue" style="margin-top:1rem;">
        <strong>Your Profile</strong><br>
        <span style="font-size:0.9rem;color:#3D1A5C;">
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
        cols = st.columns(2)
        for i, item in enumerate(items):
            with cols[i % 2]:
                checked = st.checkbox(item, value=(item in current_goals),
                                      key=f"goal_{item.replace(' ','_')[:30]}")
                if checked:
                    current_goals.add(item)
                else:
                    current_goals.discard(item)

    ss_set("goals", list(current_goals))
    n = len(current_goals)

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
        st.markdown(f"""
        <div class="card card-green">
            ✅ <strong>{n} goal{'s' if n>1 else ''} selected</strong> — great focus!
            <ul style="margin:0.4rem 0 0;padding-left:1.2rem;font-size:0.88rem;color:#1E5C3A;">
            {"".join(f"<li>{g}</li>" for g in sorted(current_goals))}
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="citation">
        <strong>Sources:</strong><br>
        Sin, R., Murphy, R. O., &amp; Lamas, S. (2019). Goals-based financial planning: How simple lists can overcome
        cognitive blind spots. <em>Journal of Financial Planning, 32</em>(7), 32–43.<br>
        Fisher, P. J., &amp; Montalto, C. P. (2010). Effect of saving motives and horizon on saving behaviors.
        <em>Journal of Economic Psychology, 31</em>(1), 92–105. <a href="https://doi.org/10.1016/j.joep.2009.10.001">https://doi.org/10.1016/j.joep.2009.10.001</a>
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

    # Extra CSS for the instrument table layout
    st.markdown("""
    <style>
    .cfpb-section-header {
        background: #3D1A5C;
        color: white;
        border-radius: 10px 10px 0 0;
        padding: 0.9rem 1.2rem;
        font-weight: 600;
        font-size: 0.95rem;
        margin-top: 1.5rem;
        margin-bottom: 0;
    }
    .cfpb-col-headers {
        display: grid;
        align-items: center;
        background: #EDE5F5;
        padding: 0.6rem 1.2rem;
        border-left: 1px solid #C4B8DE;
        border-right: 1px solid #C4B8DE;
        font-size: 0.78rem;
        font-weight: 600;
        color: #3D1A5C;
        text-align: center;
        gap: 6px;
    }
    .cfpb-col-headers-p1 { grid-template-columns: 2fr 1fr 1fr 1fr 1fr 1fr; }
    .cfpb-col-headers-p2 { grid-template-columns: 2fr 1fr 1fr 1fr 1fr 1fr; }
    .cfpb-col-headers span:first-child { text-align: left; }

    .cfpb-row {
        display: grid;
        align-items: center;
        padding: 0.75rem 1.2rem;
        border-left: 1px solid #C4B8DE;
        border-right: 1px solid #C4B8DE;
        border-bottom: 1px solid #D4C9E8;
        gap: 6px;
        background: white;
        font-size: 0.9rem;
        color: #1A0A2E;
    }
    .cfpb-row-p1 { grid-template-columns: 2fr 1fr 1fr 1fr 1fr 1fr; }
    .cfpb-row-p2 { grid-template-columns: 2fr 1fr 1fr 1fr 1fr 1fr; }
    .cfpb-row:last-child { border-radius: 0 0 10px 10px; border-bottom: 1px solid #C4B8DE; }
    .cfpb-row:nth-child(even) { background: #FAF7F4; }

    /* Hide radio label, show only circle */
    div[data-testid="stRadio"] > label { display: none; }
    div[data-testid="stRadio"] > div {
        display: flex;
        justify-content: space-around;
        gap: 0;
    }
    div[data-testid="stRadio"] > div > label {
        display: flex !important;
        flex-direction: column;
        align-items: center;
        flex: 1;
        cursor: pointer;
    }
    div[data-testid="stRadio"] > div > label > div:first-child { display: none; }
    </style>
    """, unsafe_allow_html=True)

    cfpb = {k: v for k, v in ss("cfpb").items()}  # copy

    # ── Part 1 ───────────────────────────────
    st.markdown("""
    <div class="cfpb-section-header">
        Part 1 &nbsp;|&nbsp; How well does this statement describe you or your situation?
    </div>
    <div class="cfpb-col-headers cfpb-col-headers-p1">
        <span>This statement describes me…</span>
        <span>Completely</span>
        <span>Very well</span>
        <span>Somewhat</span>
        <span>Very little</span>
        <span>Not at all</span>
    </div>
    """, unsafe_allow_html=True)

    part1_items = [(i, t, s) for i, (t, p, s) in enumerate(CFPB_ITEMS, 1) if p == "agree"]

    for idx, text, score_vals in part1_items:
        col_stmt, c1, c2, c3, c4, c5 = st.columns([2, 1, 1, 1, 1, 1])
        with col_stmt:
            st.markdown(f"<div style='padding:0.4rem 0;font-size:0.9rem;'>{idx}. {text}</div>",
                        unsafe_allow_html=True)
        # current index: find which option was previously selected
        current_score = cfpb.get(f"q{idx}_score", score_vals[2])  # default Somewhat/Sometimes
        try:
            cur_idx = score_vals.index(current_score)
        except ValueError:
            cur_idx = 2

        radio_cols = [c1, c2, c3, c4, c5]
        chosen = None
        for opt_i, (col, opt_label) in enumerate(zip(radio_cols, CFPB_AGREE_OPTS)):
            with col:
                selected = st.radio(
                    label=f"q{idx}_opt{opt_i}",
                    options=[opt_label],
                    index=0 if opt_i == cur_idx else None,
                    key=f"cfpb_{idx}_{opt_i}",
                    label_visibility="collapsed",
                )
                if selected:
                    chosen = opt_i

        if chosen is not None:
            cfpb[f"q{idx}_score"] = score_vals[chosen]
        else:
            cfpb[f"q{idx}_score"] = score_vals[cur_idx]

    # ── Part 2 ───────────────────────────────
    st.markdown("""
    <div class="cfpb-section-header" style="margin-top:1.5rem;">
        Part 2 &nbsp;|&nbsp; How often does this statement apply to you?
    </div>
    <div class="cfpb-col-headers cfpb-col-headers-p2">
        <span>This statement applies to me…</span>
        <span>Always</span>
        <span>Often</span>
        <span>Sometimes</span>
        <span>Rarely</span>
        <span>Never</span>
    </div>
    """, unsafe_allow_html=True)

    part2_items = [(i, t, s) for i, (t, p, s) in enumerate(CFPB_ITEMS, 1) if p == "freq"]

    for idx, text, score_vals in part2_items:
        col_stmt, c1, c2, c3, c4, c5 = st.columns([2, 1, 1, 1, 1, 1])
        with col_stmt:
            st.markdown(f"<div style='padding:0.4rem 0;font-size:0.9rem;'>{idx}. {text}</div>",
                        unsafe_allow_html=True)
        current_score = cfpb.get(f"q{idx}_score", score_vals[2])
        try:
            cur_idx = score_vals.index(current_score)
        except ValueError:
            cur_idx = 2

        radio_cols = [c1, c2, c3, c4, c5]
        chosen = None
        for opt_i, (col, opt_label) in enumerate(zip(radio_cols, CFPB_FREQ_OPTS)):
            with col:
                selected = st.radio(
                    label=f"q{idx}_opt{opt_i}",
                    options=[opt_label],
                    index=0 if opt_i == cur_idx else None,
                    key=f"cfpb_{idx}_{opt_i}",
                    label_visibility="collapsed",
                )
                if selected:
                    chosen = opt_i

        if chosen is not None:
            cfpb[f"q{idx}_score"] = score_vals[chosen]
        else:
            cfpb[f"q{idx}_score"] = score_vals[cur_idx]

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
# STEP 4 — FINANCIAL CONFIDENCE (+ CFPB score reveal)
# ─────────────────────────────────────────────
def step_confidence():
    render_header(); render_progress()

    # ── CFPB Score Reveal ────────────────────
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
        sc_color = "#1E5C3A"
        sc_tier  = "High financial well-being"
        sc_msg   = ("You report relatively high financial well-being. You feel in control of your day-to-day finances, "
                    "can absorb financial shocks, and are on track toward your goals. Focus on maintaining "
                    "these habits and building on your strong foundation.")
    elif score >= 41:
        sc_color = "#7A4F00"
        sc_tier  = "Moderate financial well-being"
        sc_msg   = ("You report moderate financial well-being — the most common range for working-age Americans. "
                    "Some areas feel manageable while others create stress. The personalized action plan "
                    "at the end of this assessment will highlight the highest-impact improvements.")
    else:
        sc_color = "#8B1A1A"
        sc_tier  = "Lower financial well-being"
        sc_msg   = ("You report lower financial well-being. This is more common than many people realize and is often "
                    "driven by specific, addressable gaps — such as high debt load, income volatility, or lack of "
                    "emergency savings. Your action plan will prioritize the most critical next steps.")

    diff     = score - peer_med
    diff_txt = (f"<strong style='color:#1E5C3A'>+{diff} above</strong>" if diff > 0
                else f"<strong style='color:#8B1A1A'>{diff} below</strong>" if diff < 0
                else "<strong>equal to</strong>")

    # Score gauge bar
    gauge_pct = score  # 0–100
    st.markdown(f"""
    <div class="card" style="border-left:4px solid {sc_color};background:#fafafa;padding:1.5rem 2rem;">
        <div style="font-size:0.75rem;color:#5E4D78;text-transform:uppercase;letter-spacing:0.08em;margin-bottom:0.25rem;">
            Your CFPB Financial Well-Being Score
        </div>
        <div style="display:flex;align-items:flex-end;gap:1rem;flex-wrap:wrap;">
            <div style="font-size:4.5rem;font-weight:800;color:{sc_color};line-height:1;">{score}</div>
            <div style="flex:1;min-width:180px;">
                <div style="font-size:0.9rem;font-weight:600;color:#1A0A2E;">{sc_tier}</div>
                <div style="font-size:0.82rem;color:#5E4D78;margin-top:2px;">out of 100 &nbsp;·&nbsp; Raw total: {raw}/40</div>
                <div style="font-size:0.82rem;color:#3D2C5C;margin-top:4px;">
                    {diff_txt} the median for U.S. adults ages {age_label} (median: {peer_med})
                </div>
            </div>
        </div>

        <!-- Gauge bar -->
        <div style="margin-top:1rem;">
            <div style="position:relative;height:18px;background:#D4C9E8;border-radius:99px;overflow:hidden;">
                <div style="width:{gauge_pct}%;height:100%;background:linear-gradient(90deg,#8B1A1A 0%,#7A4F00 40%,#1E5C3A 70%);border-radius:99px;transition:width 0.5s;"></div>
            </div>
            <div style="display:flex;justify-content:space-between;font-size:0.68rem;color:#7A6A94;margin-top:4px;">
                <span>0 — Lower</span><span>40</span><span>Moderate — 60</span><span>80</span><span>Higher — 100</span>
            </div>
        </div>

        <p style="font-size:0.88rem;color:#3D2C5C;margin-top:1rem;line-height:1.55;">{sc_msg}</p>
    </div>
    """, unsafe_allow_html=True)

    # Age-group comparison table
    st.markdown("**How scores compare across age groups** *(CFPB National Survey, 2017)*")
    AGE_MEDIANS = [
        ("18–24", 51), ("25–34", 52), ("35–44", 54),
        ("45–54", 54), ("55–61", 55), ("62–69", 59), ("70+", 62),
    ]
    rows = ""
    for ag, med in AGE_MEDIANS:
        hl = ' class="highlight"' if ag == age_label else ""
        you_col = (f"<strong style='color:{sc_color}'>{score} (you)</strong>"
                   if ag == age_label else "")
        rows += f"<tr{hl}><td>{'▶ ' if ag==age_label else ''}{ag}</td><td style='text-align:center'>{med}</td><td style='text-align:center'>{you_col}</td></tr>"

    st.markdown(f"""
    <table class="bench-table">
        <thead>
            <tr>
                <th>Age Group</th>
                <th style="text-align:center">Median Score</th>
                <th style="text-align:center">Your Score</th>
            </tr>
        </thead>
        <tbody>{rows}</tbody>
    </table>
    <p style="font-size:0.78rem;color:#7A6A94;margin-top:0.5rem;">
        Scores are produced using the CFPB official lookup table adjusted for age and self-administration.
        Financial well-being is best understood as progress over time — not a fixed pass/fail threshold.
    </p>
    """, unsafe_allow_html=True)

    st.markdown("<hr class='divider'>", unsafe_allow_html=True)

    # ── Financial Confidence ─────────────────
    st.markdown('<p class="step-title">Financial Confidence</p>', unsafe_allow_html=True)
    st.markdown("""
    <p class="step-subtitle">
        Rate your confidence in each area from 1 (Not confident) to 5 (Very confident).
        Research shows that both overconfidence and underconfidence impair financial decision-making.
    </p>
    """, unsafe_allow_html=True)

    CONF_AREAS = {
        "daily":      "Managing day-to-day finances",
        "emergency":  "Planning for financial emergencies",
        "saving":     "Saving consistently toward goals",
        "investing":  "Understanding and using investments",
        "retirement": "Planning for retirement",
        "insurance":  "Evaluating insurance coverage",
        "tax":        "Basic tax planning",
        "estate":     "Estate planning (will, beneficiaries)",
    }
    conf = ss("conf")
    options = ["1 – Not confident", "2 – Slightly", "3 – Moderately",
               "4 – Confident", "5 – Very confident"]

    for key, label in CONF_AREAS.items():
        current = conf.get(key, 3) - 1
        st.markdown(f"**{label}**")
        choice = st.radio(label, options=options, index=current, horizontal=True,
                          label_visibility="collapsed", key=f"conf_{key}")
        conf[key] = int(choice[0])

    ss_set("conf", conf)
    avg = sum(conf.values()) / len(conf)
    low_areas = [CONF_AREAS[k] for k, v in conf.items() if v <= 2]

    conf_color = "#1E5C3A" if avg >= 4 else "#7A4F00" if avg >= 3 else "#8B1A1A"
    st.markdown(f"""
    <div class="card" style="border-left:4px solid {conf_color};margin-top:1.5rem;">
        <strong>Average Confidence: {avg:.1f} / 5</strong><br>
        <span style="font-size:0.88rem;color:#3D2C5C;">
        {"Strong overall confidence — maintain and build on it." if avg >= 4
         else "Moderate confidence — target low-rated areas for education or professional advice." if avg >= 3
         else "Several areas need attention — consider financial education or professional guidance."}
        </span>
        {"<br><br><strong style='color:#8B1A1A'>Areas rated ≤ 2 (priority for improvement):</strong><ul style='font-size:0.85rem;color:#8B1A1A;margin:0.3rem 0 0;padding-left:1.2rem;'>" + "".join(f"<li>{a}</li>" for a in low_areas) + "</ul>" if low_areas else ""}
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="citation">
        <strong>Sources:</strong><br>
        Consumer Financial Protection Bureau. (2017). <em>Financial well-being in America.</em>
        <a href="https://www.consumerfinance.gov/data-research/research-reports/financial-well-being-in-america/">
        https://www.consumerfinance.gov/data-research/research-reports/financial-well-being-in-america/</a>
        (age-group median scores, Table 1)<br>
        Parker, A. M., de Bruin, W. B., Yoong, J., &amp; Willis, R. (2012). Inappropriate confidence and retirement planning:
        Four studies with a national sample. <em>Journal of Behavioral Decision Making, 25</em>(4), 382–389.
        <a href="https://doi.org/10.1002/bdm.745">https://doi.org/10.1002/bdm.745</a>
    </div>
    """, unsafe_allow_html=True)

    nav_buttons()

# ─────────────────────────────────────────────
# STEP 5 — NET WORTH
# ─────────────────────────────────────────────
def step_networth():
    render_header(); render_progress()
    st.markdown('<p class="step-title">Net Worth Calculation</p>', unsafe_allow_html=True)
    st.markdown('<p class="step-subtitle">Your net worth (assets minus liabilities) is a foundational measure of financial health.</p>', unsafe_allow_html=True)

    nw = ss("nw")

    st.markdown("#### 🟢 Assets")
    c1, c2 = st.columns(2)
    asset_fields = [
        ("cash",            "Cash & Checking accounts", c1),
        ("savings_nw",      "Savings accounts / CDs",   c2),
        ("investments",     "Taxable brokerage / investments", c1),
        ("retirement_accts","All retirement accounts (401k, IRA, Roth, etc.)", c2),
        ("home",            "Primary home / real estate value", c1),
        ("vehicle",         "Vehicle(s) value",          c2),
    ]
    for key, label, col in asset_fields:
        with col:
            nw[key] = st.number_input(label, 0, 50_000_000, nw.get(key, 0),
                                      step=500, format="%d", key=f"nw_{key}")

    st.markdown("#### 🔴 Liabilities")
    c1, c2 = st.columns(2)
    liab_fields = [
        ("cc_debt",      "Credit card debt",          c1),
        ("student",      "Student loans",              c2),
        ("auto_loan",    "Auto loan(s)",               c1),
        ("mortgage",     "Mortgage balance",           c2),
        ("personal_loan","Personal / other loans",     c1),
        ("other_debt",   "Other debts (HELOC, etc.)",  c2),
    ]
    for key, label, col in liab_fields:
        with col:
            nw[key] = st.number_input(label, 0, 10_000_000, nw.get(key, 0),
                                      step=500, format="%d", key=f"nw_{key}")

    ss_set("nw", nw)
    assets, liabs, total = net_worth()
    bracket = age_bracket(ss("age"))
    bench_med, bench_p75 = NW_BENCH[bracket]
    scf_ret = SCF_RET[bracket]

    nw_color = "#1E5C3A" if total > bench_med else "#7A4F00"
    tier = ("Top 25%" if total > bench_p75
            else "Above median" if total > bench_med
            else "Below median")

    st.markdown(f"""
    <div class="card" style="border-left:4px solid {nw_color};margin-top:1.5rem;">
        <div class="kpi-grid">
            <div class="kpi-box"><div class="label">Total Assets</div><div class="value">{fmt_dollar(assets)}</div></div>
            <div class="kpi-box"><div class="label">Total Liabilities</div><div class="value" style="color:#8B1A1A">{fmt_dollar(liabs)}</div></div>
            <div class="kpi-box"><div class="label">Net Worth</div><div class="value" style="color:{nw_color}">{fmt_dollar(total)}</div></div>
        </div>
        <div style="margin-top:1rem;font-size:0.88rem;color:#3D2C5C;">
            <strong>Your position among {bracket}-year-olds:</strong> {tier}
            &nbsp;·&nbsp; Peer median: <strong>{fmt_dollar(bench_med)}</strong>
            &nbsp;·&nbsp; 75th percentile: <strong>{fmt_dollar(bench_p75)}</strong>
        </div>
        <div style="margin-top:0.5rem;font-size:0.82rem;color:#7A6A94;">
            ⚠️ Descriptive benchmark: reflects what peers <em>have</em>, not what is needed for financial security.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Full benchmark table
    st.markdown("**Net Worth Benchmarks by Age — Federal Reserve SCF 2022**")
    rows = ""
    for ag, (med, p75) in NW_BENCH.items():
        hl = ' class="highlight"' if ag == bracket else ""
        rows += f'<tr{hl}><td>{"▶ " if ag==bracket else ""}{ag}</td><td>{fmt_dollar(med)}</td><td>{fmt_dollar(p75)}</td></tr>'
    st.markdown(f"""
    <table class="bench-table">
        <thead><tr><th>Age Group</th><th>Median Net Worth</th><th>75th Percentile</th></tr></thead>
        <tbody>{rows}</tbody>
    </table>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="citation">
        <strong>Source:</strong><br>
        Board of Governors of the Federal Reserve System. (2023). <em>Survey of Consumer Finances, 2022.</em>
        <a href="https://www.federalreserve.gov/econres/scfindex.htm">https://www.federalreserve.gov/econres/scfindex.htm</a>
    </div>
    """, unsafe_allow_html=True)

    nav_buttons()

# ─────────────────────────────────────────────
# STEP 6 — CASH FLOW
# ─────────────────────────────────────────────
def step_cashflow():
    render_header(); render_progress()
    st.markdown('<p class="step-title">Cash Flow Analysis</p>', unsafe_allow_html=True)
    st.markdown('<p class="step-subtitle">Understanding where your money goes is the foundation of financial planning.</p>', unsafe_allow_html=True)

    income = st.number_input("Monthly net (take-home) income after taxes ($)",
                             0, 100_000, ss("income_net"), step=100, format="%d")
    ss_set("income_net", income)

    gross_mo = ss("salary") / 12
    st.caption(f"Your estimated gross monthly income: {fmt_dollar(gross_mo)}")

    exp = ss("exp")

    st.markdown("#### Fixed Expenses *(same each month)*")
    c1, c2 = st.columns(2)
    fixed_fields = [
        ("housing",    "Housing (rent or mortgage)", "25–35% of gross", c1),
        ("transport",  "Transportation / car payment", "10–15%", c2),
        ("insurance",  "Insurance (health, auto, life)", "5–10%", c1),
        ("debt_min",   "Minimum debt payments", "varies", c2),
    ]
    for key, label, tip, col in fixed_fields:
        with col:
            exp[key] = st.number_input(f"{label} *(typical: {tip})*",
                                       0, 20_000, exp.get(key, 0), step=50, format="%d", key=f"exp_{key}")

    st.markdown("#### Flexible Expenses *(variable each month)*")
    c1, c2 = st.columns(2)
    flex_fields = [
        ("groceries",    "Groceries & household supplies", "5–10%", c1),
        ("utilities",    "Utilities & phone", "3–6%", c2),
        ("personal",     "Personal care & clothing", "2–4%", c1),
        ("entertainment","Entertainment & dining out", "5–10%", c2),
        ("other_flex",   "Other variable expenses", "varies", c1),
    ]
    for key, label, tip, col in flex_fields:
        with col:
            exp[key] = st.number_input(f"{label} *(typical: {tip})*",
                                       0, 10_000, exp.get(key, 0), step=25, format="%d", key=f"exp_{key}")

    st.markdown("#### Occasional / Annual Expenses")
    occ = st.number_input("Annual total (gifts, travel, subscriptions, car maintenance, etc.)",
                          0, 200_000, ss("occ_annual"), step=100, format="%d")
    ss_set("occ_annual", occ)
    ss_set("exp", exp)

    total_exp = monthly_expenses()
    surplus, sr = savings_rate()

    if sr >= 20:
        sr_color, sr_msg = "#1E5C3A", "🌟 Excellent savings rate — on track for long-term security."
    elif sr >= 15:
        sr_color, sr_msg = "#1E5C3A", "✅ Good savings rate — meeting the 15% guideline."
    elif sr >= 10:
        sr_color, sr_msg = "#7A4F00", "⚠️ Moderate — try to reach 15–20% by trimming flexible spending."
    else:
        sr_color, sr_msg = "#8B1A1A", "🚨 Low savings rate — focus on increasing income or reducing expenses."

    st.markdown(f"""
    <div class="card" style="border-left:4px solid {sr_color};margin-top:1.5rem;">
        <div class="kpi-grid">
            <div class="kpi-box"><div class="label">Net Income</div><div class="value">{fmt_dollar(income)}/mo</div></div>
            <div class="kpi-box"><div class="label">Total Expenses</div><div class="value" style="color:#8B1A1A">{fmt_dollar(total_exp)}/mo</div></div>
            <div class="kpi-box"><div class="label">Monthly Surplus</div><div class="value" style="color:{sr_color}">{fmt_dollar(surplus)}</div></div>
            <div class="kpi-box"><div class="label">Savings Rate</div><div class="value" style="color:{sr_color}">{sr:.1f}%</div></div>
        </div>
        <p style="margin-top:1rem;font-size:0.88rem;">{sr_msg}</p>
    </div>
    """, unsafe_allow_html=True)

    # Housing ratio check
    housing_ratio = (exp.get("housing", 0) / gross_mo * 100) if gross_mo else 0
    if housing_ratio > 30:
        st.markdown(f"""
        <div class="card card-amber">
            ⚠️ <strong>Housing cost alert:</strong> Your housing expense is
            <strong>{housing_ratio:.0f}% of gross income</strong>.
            Financial planning guidelines recommend keeping housing below 28–30%.
            High housing costs compress your ability to save and build wealth.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("""
    <div class="citation">
        <strong>Sources:</strong><br>
        Garman, E. T., &amp; Forgue, R. E. (2018). <em>Personal finance</em> (13th ed.). Cengage Learning.<br>
        U.S. Department of Housing and Urban Development. (2023). <em>Affordable housing.</em>
        <a href="https://www.hud.gov/program_offices/comm_planning/affordablehousing">
        https://www.hud.gov/program_offices/comm_planning/affordablehousing</a>
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
        color, tier = "#1E5C3A", "✅ Fully funded"
    elif months_covered >= 3:
        color, tier = "#7A4F00", "⚠️ Partially funded"
    else:
        color, tier = "#8B1A1A", "🚨 Underfunded"

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
             else f" — Gap to 3-month minimum: <strong style='color:#8B1A1A'>{fmt_dollar(gap_3mo)}</strong>" if months_covered < 3
             else f" — Gap to 6-month goal: <strong style='color:#7A4F00'>{fmt_dollar(gap_6mo)}</strong>"}
        </div>
        <div style="margin-top:0.75rem;font-size:0.85rem;color:#3D2C5C;">
            Cover $400 emergency: <strong>{can_cover_400}</strong>
            &nbsp;|&nbsp; Cover $2,000 emergency: <strong>{can_cover_2k}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Progress bar
    metric_bar("Progress toward 6-month goal", min(months_covered, 6), 6,
               color="#1E5C3A" if months_covered >= 6 else "#7A4F00" if months_covered >= 3 else "#8B1A1A",
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

    ret_return = st.slider("Expected annual return (%)", 3.0, 12.0, ss("ret_return"), step=0.5)
    ss_set("ret_return", ret_return)

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

    color_now  = "#1E5C3A" if ret_saved >= goal_now  else "#8B1A1A"
    color_proj = "#1E5C3A" if projected  >= goal_ret else "#8B1A1A"

    st.markdown(f"""
    <div class="card card-blue">
        <strong>Your Fidelity Milestone (Prescriptive — What You Need)</strong><br>
        <span style="font-size:0.85rem;color:#3D1A5C;">
        Goal at your age ({age}): <strong>{mult_now:.1f}× salary = {fmt_dollar(goal_now)}</strong><br>
        Goal at retirement ({ret_age}): <strong>{mult_at_ret:.1f}× salary = {fmt_dollar(goal_ret)}</strong>
        </span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card" style="border-left:4px solid {color_now};margin-top:0.75rem;">
        <div class="kpi-grid">
            <div class="kpi-box">
                <div class="label">Current Savings</div>
                <div class="value">{fmt_dollar(ret_saved)}</div>
            </div>
            <div class="kpi-box">
                <div class="label">Goal Today</div>
                <div class="value" style="color:{color_now}">{fmt_dollar(goal_now)}</div>
            </div>
            <div class="kpi-box">
                <div class="label">Gap / Surplus Today</div>
                <div class="value" style="color:{color_now}">
                    {"+" if gap_now <= 0 else "-"}{fmt_dollar(abs(gap_now))}
                </div>
            </div>
            <div class="kpi-box">
                <div class="label">Peer Median (SCF)</div>
                <div class="value">{fmt_dollar(scf_peer)}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="card" style="border-left:4px solid {color_proj};margin-top:0.75rem;">
        <div style="font-size:0.9rem;font-weight:600;margin-bottom:0.5rem;">
            Retirement Projection at Age {ret_age} (with {ret_return:.1f}% annual return)
        </div>
        <div class="kpi-grid">
            <div class="kpi-box">
                <div class="label">Projected Savings</div>
                <div class="value" style="color:{color_proj}">{fmt_dollar(projected)}</div>
            </div>
            <div class="kpi-box">
                <div class="label">Goal at Retirement</div>
                <div class="value">{fmt_dollar(goal_ret)}</div>
            </div>
            <div class="kpi-box">
                <div class="label">Projected Gap/Surplus</div>
                <div class="value" style="color:{color_proj}">
                    {"+" if projected >= goal_ret else "-"}{fmt_dollar(abs(gap_proj))}
                </div>
            </div>
            <div class="kpi-box">
                <div class="label">Years to Retirement</div>
                <div class="value">{years_left}</div>
            </div>
        </div>
        <p style="font-size:0.78rem;color:#7A6A94;margin-top:0.75rem;">
            ⚠️ Projection assumes constant {ret_return:.1f}% return and consistent contributions.
            Actual returns vary. This does not account for inflation (~3%/year), taxes on withdrawals,
            or Social Security income. Consult a CFP® for personalized projections.
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
        rows2 += f'<tr{hl}><td>{"▶ " if ag==bracket else ""}{ag}</td><td>{fmt_dollar(med)}</td><td style="font-size:0.78rem;color:#7A6A94;">What peers have — not a sufficiency target</td></tr>'
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
    ef_color  = "#1E5C3A" if ef_months >= 6 else "#7A4F00" if ef_months >= 3 else "#8B1A1A"
    sr_color  = "#1E5C3A" if sr >= 15 else "#7A4F00" if sr >= 10 else "#8B1A1A"
    ret_color = "#1E5C3A" if projected >= goal_ret else "#8B1A1A"
    cfpb_color= "#1E5C3A" if cfpb_score >= 61 else "#7A4F00" if cfpb_score >= 41 else "#8B1A1A"

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

    if goals:
        st.markdown("#### 🎯 Your Selected Goals")
        goal_html = "".join(f"<li>{g}</li>" for g in goals[:5])
        st.markdown(f"""
        <div class="card card-amber">
            <ul style="margin:0;padding-left:1.2rem;font-size:0.9rem;color:#7A4F00;">{goal_html}</ul>
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
        <ul style="margin:0;padding-left:1.2rem;font-size:0.88rem;color:#3D2C5C;line-height:2;">
            <li>📊 <a href="https://www.consumerfinance.gov/consumer-tools/financial-well-being/" target="_blank">CFPB Financial Well-Being Tools</a> — validated assessment & planning resources</li>
            <li>🎓 <a href="https://www.smartaboutmoney.org" target="_blank">SmartAboutMoney.org (NEFE)</a> — free, research-based financial education</li>
            <li>🏛️ <a href="https://www.mymoney.gov" target="_blank">MyMoney.gov</a> — U.S. federal financial literacy portal</li>
            <li>📞 <a href="https://www.nfcc.org" target="_blank">NFCC.org</a> — nonprofit credit counseling (free or low-cost)</li>
            <li>👤 <a href="https://www.napfa.org/find-an-advisor" target="_blank">NAPFA.org</a> — fee-only fiduciary financial advisors</li>
            <li>📱 <a href="https://www.consumerfinance.gov/consumer-tools/your-money-your-goals/" target="_blank">CFPB "Your Money, Your Goals" Toolkit</a></li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # ── Download ─────────────────────────────
    st.markdown("#### 💾 Save Your Results")
    _, _, total_nw = net_worth()
    summary = {
        "date": date.today().isoformat(),
        "demographics": {"age": age, "salary": salary, "retirement_age": ret_age, "region": ss("region")},
        "goals": goals,
        "cfpb_wellbeing_score": cfpb_score,
        "avg_financial_confidence": round(avg_conf, 2),
        "net_worth": total_nw,
        "emergency_fund_months": round(ef_months, 1),
        "savings_rate_pct": round(sr, 1),
        "retirement_current": ret_saved,
        "retirement_projected": round(projected),
        "retirement_goal": round(goal_ret),
        "priority_actions": [a["title"] for a in actions],
    }
    st.download_button(
        label="⬇️ Download Summary (JSON)",
        data=json.dumps(summary, indent=2),
        file_name=f"financial-wellness-{date.today().isoformat()}.json",
        mime="application/json",
    )

    st.markdown("""
    <div class="card card-purple" style="text-align:center;margin-top:1.5rem;">
        <strong style="font-size:1.05rem;">Financial wellness is a journey, not a destination.</strong><br>
        <span style="font-size:0.88rem;color:#6d28d9;">
        Small, consistent improvements compound over time — in your savings and in your well-being.
        Re-take this assessment quarterly to track your progress.
        </span>
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
        <a href="https://doi.org/10.7208/chicago/9780226903286.001.0001">https://doi.org/10.7208/chicago/9780226903286.001.0001</a>
    </div>
    """, unsafe_allow_html=True)

    nav_buttons(next_label="Complete ✓")

# ─────────────────────────────────────────────
# ROUTER
# ─────────────────────────────────────────────
STEP_FNS = [
    step_welcome, step_demographics, step_goals, step_cfpb,
    step_confidence, step_networth, step_cashflow,
    step_emergency, step_retirement, step_action_plan,
]

STEP_FNS[ss("step")]()
