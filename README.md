# 💰 Financial Wellness Checkup

A research-based interactive financial wellness assessment built with Python and Streamlit.

## What It Does

This tool combines **subjective well-being** (how you feel about money) with **objective financial health** (net worth, cash flow, retirement readiness) to give users a more holistic picture of their financial capacity and empower financial planning. This is a tool for personal assessment and should not be used as advice. Always consult a financial professional for making informed financial decisions on critical topics.

### Assessment Modules

1. **Demographic Profile** — age-appropriate benchmarks and personalization
2. **Goal Setting** — structured financial goal identification (Fisher & Montalto, 2010)
3. **CFPB Financial Well-Being Scale** — validated 10-item instrument with full scoring
4. **Financial Confidence Self-Assessment** — 8 domains, calibrated feedback
5. **Net Worth Calculator** — Federal Reserve SCF 2022 benchmarks by age group
6. **Cash Flow Analysis** — savings rate, housing ratio, surplus/deficit
7. **Emergency Fund Assessment** — prescriptive 3–6 month benchmarks + peer data
8. **Retirement Readiness** — Fidelity prescriptive milestones + SCF descriptive data + projection model
9. **Personalized Action Plan** — priority-ranked, empirically informed recommendations

### Key Research Sources
- Consumer Financial Protection Bureau (CFPB) Financial Well-Being Scale
- Federal Reserve Survey of Consumer Finances (2022)
- Fidelity Investments retirement savings milestones
- Lusardi & Mitchell (2014) on financial literacy
- Madrian & Shea (2001) on savings automation
- National Endowment for Financial Education (NEFE)

---

## 📁 File Structure

```
financial-wellness/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies (streamlit only)
├── .streamlit/
│   └── config.toml         # Theme and server configuration
└── README.md               # This file
```

---

## 🔒 Privacy

All data is processed locally within the user's browser session. Nothing is stored, logged, or transmitted to external servers.

---

## 📖 APA Citations

All benchmarks and recommendations cite peer-reviewed research and government data sources in APA 7th edition format, with live hyperlinks. Sources include:

- Board of Governors of the Federal Reserve System. (2023). *Survey of Consumer Finances, 2022.* https://www.federalreserve.gov/econres/scfindex.htm
- Consumer Financial Protection Bureau. (2017). *CFPB Financial Well-Being Scale.* https://www.consumerfinance.gov/data-research/research-reports/financial-well-being-scale/
- Fidelity Investments. (2024). *How much do I need to retire?* https://www.fidelity.com/viewpoints/retirement/how-much-do-i-need-to-retire
- Lusardi, A., & Mitchell, O. S. (2014). The economic importance of financial literacy. *Journal of Economic Literature, 52*(1), 5–44.
