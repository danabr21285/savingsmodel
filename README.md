# 💵 Savings Growth What‑If (Streamlit)

Interactive web app for exploring savings growth over time with adjustable assumptions and optional A/B scenario comparisons.

## Features
- Adjustable inputs: starting balance, monthly savings, annual interest rate, horizon (years)
- Monthly compounding with end-of-month contributions
- KPI summaries
- Interactive charts (balance; contributions vs. interest)
- CSV export for each scenario
- Optional Scenario B for comparisons

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy (Streamlit Community Cloud)
1. Push this folder to a GitHub repo.
2. Go to https://share.streamlit.io and point to `app.py` in your repo.
3. (Optional) Add your original Excel file if you want the default values to be read from it.

## Notes
- The app will try to read defaults from `Savings Spreadsheet Model.xlsx` if present (sheet `Sheet1`). If not found, it falls back to sensible defaults.
- Interest is compounded monthly; contributions are added at month end.
