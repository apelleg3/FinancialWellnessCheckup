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

- Board of Governors of the Federal Reserve System. (2023). Survey of consumer finances, 2022. https://www.federalreserve.gov/econres/scfindex.htm
- Board of Governors of the Federal Reserve System. (2024). Report on the economic well-being of U.S. households in 2023. https://www.federalreserve.gov/publications/report-economic-well-being-us-households.htm
- Choi, J. J., Laibson, D., Madrian, B. C., & Metrick, A. (2004). For better or for worse: Default effects and 401(k) savings behavior. In D. A. Wise (Ed.), Perspectives on the economics of aging (pp. 81–126). University of Chicago Press. https://doi.org/10.7208/chicago/9780226903286.001.0001
- Consumer Financial Protection Bureau. (2017a). CFPB financial well-being scale. https://www.consumerfinance.gov/data-research/research-reports/financial-well-being-scale/
- Consumer Financial Protection Bureau. (2017b). CFPB financial well-being scale: Scale development technical report. https://www.consumerfinance.gov/data-research/research-reports/financial-well-being-scale/
- Consumer Financial Protection Bureau. (2017c). Financial well-being in America. https://www.consumerfinance.gov/data-research/research-reports/financial-well-being-in-america/
- Fidelity Investments. (2024). How much do I need to retire? https://www.fidelity.com/viewpoints/retirement/how-much-do-i-need-to-retire
- Fisher, P. J., & Montalto, C. P. (2010). Effect of saving motives and horizon on saving behaviors. Journal of Economic Psychology, 31(1), 92–105. https://doi.org/10.1016/j.joep.2009.10.001
- Garman, E. T., & Forgue, R. E. (2018). Personal finance (13th ed.). Cengage Learning.
- Lusardi, A., & Mitchell, O. S. (2014). The economic importance of financial literacy: Theory and evidence. Journal of Economic Literature, 52(1), 5–44. https://doi.org/10.1257/jel.52.1.5
- Madrian, B. C., & Shea, D. F. (2001). The power of suggestion: Inertia in 401(k) participation and savings behavior. Quarterly Journal of Economics, 116(4), 1149–1187. https://doi.org/10.1162/003355301753265543
- Munnell, A. H., & Chen, A. (2021). 401(k)/IRA holdings in 2019: An update from the SCF (Issue Brief No. 21-5). Center for Retirement Research at Boston College. https://crr.bc.edu/briefs/401kira-holdings-in-2019-an-update-from-the-scf/
- National Endowment for Financial Education. (2023). Financial education and decision-making. https://www.nefe.org/research
- Parker, A. M., de Bruin, W. B., Yoong, J., & Willis, R. (2012). Inappropriate confidence and retirement planning: Four studies with a national sample. Journal of Behavioral Decision Making, 25(4), 382–389. https://doi.org/10.1002/bdm.745
- Sin, R., Murphy, R. O., & Lamas, S. (2019). Goals-based financial planning: How simple lists can overcome cognitive blind spots. Journal of Financial Planning, 32(7), 32–43.
- U.S. Department of Housing and Urban Development. (2023). Affordable housing. https://www.hud.gov/program_offices/comm_planning/affordablehousing
