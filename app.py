
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Savings Growth What‑If", page_icon="💵", layout="wide")
st.title("💵 Savings Growth What‑If Model")
st.caption("Adjust inputs to run quick scenario analyses.")

with st.sidebar:
    st.header("Assumptions — Scenario A")
    pv_a = st.number_input("Starting Savings Balance (PV)", min_value=0.0, value=20000.0, step=100.0, format="%.2f")
    pmt_a = st.number_input("Monthly Savings Payments", min_value=0.0, value=700.0, step=50.0, format="%.2f")
    r_annual_a = st.number_input("Annual Interest Rate", min_value=0.0, max_value=1.0, value=0.06, step=0.005, format="%.3f")
    years_a = st.number_input("Savings Period (years)", min_value=1, max_value=60, value=int(15.0), step=1)

    st.divider()
    compare = st.checkbox("Compare with Scenario B")
    if compare:
        st.header("Assumptions — Scenario B")
        pv_b = st.number_input("Starting Savings Balance (PV) — B", min_value=0.0, value=20000.0, step=100.0, format="%.2f", key="pv_b")
        pmt_b = st.number_input("Monthly Savings Payments— B", min_value=0.0, value=700.0, step=50.0, format="%.2f", key="pmt_b")
        r_annual_b = st.number_input("Annual Interest Rate — B", min_value=0.0, max_value=1.0, value=0.06, step=0.005, format="%.3f", key="r_b")
        years_b = st.number_input("Savings Period (years) — B", min_value=1, max_value=60, value=int(15.0), step=1, key="yrs_b")

def simulate(pv, pmt, r_annual, years):
    n = int(years * 12)
    r_m = r_annual / 12.0
    balance = pv
    rows = []
    total_contrib = 0.0
    total_interest = 0.0
    for m in range(1, n+1):
        # interest accrues on current balance
        interest = balance * r_m
        balance += interest
        # deposit at month end
        balance += pmt
        total_contrib += pmt
        total_interest += interest
        rows.append({
            "Month": m,
            "Year": (m-1)//12 + 1,
            "Contribution": total_contrib,
            "Interest Accrued": total_interest,
            "Balance": balance
        })
    return pd.DataFrame(rows)

tab1, tab2 = st.tabs(["📈 Growth", "📊 Breakdown"])

df_a = simulate(pv_a, pmt_a, r_annual_a, years_a)
summary_a = {
    "Final Balance": df_a["Balance"].iloc[-1],
    "Total Contributions": df_a["Contribution"].iloc[-1],
    "Total Interest": df_a["Interest Accrued"].iloc[-1],
    "Months": len(df_a),
    "Years": years_a
}

if compare:
    df_b = simulate(pv_b, pmt_b, r_annual_b, years_b)
    summary_b = {
        "Final Balance": df_b["Balance"].iloc[-1],
        "Total Contributions": df_b["Contribution"].iloc[-1],
        "Total Interest": df_b["Interest Accrued"].iloc[-1],
        "Months": len(df_b),
        "Years": years_b
    }

# KPI row
c1, c2, c3, c4 = st.columns(4)
c1.metric("Final Balance — A", f"${summary_a['Final Balance']:,.0f}")
c2.metric("Total Contributions — A", f"${summary_a['Total Contributions']:,.0f}")
c3.metric("Total Interest — A", f"${summary_a['Total Interest']:,.0f}")
c4.metric("Horizon — A", f"{summary_a['Years']} years ({summary_a['Months']} mo)")

if compare:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Final Balance — B", f"${summary_b['Final Balance']:,.0f}")
    c2.metric("Total Contributions — B", f"${summary_b['Total Contributions']:,.0f}")
    c3.metric("Total Interest — B", f"${summary_b['Total Interest']:,.0f}")
    c4.metric("Horizon — B", f"{summary_b['Years']} years ({summary_b['Months']} mo)")

with tab1:
    df_plot_a = df_a.copy()
    df_plot_a["Scenario"] = "A"
    if compare:
        df_plot_b = df_b.copy()
        df_plot_b["Scenario"] = "B"
        df_plot = pd.concat([df_plot_a, df_plot_b], ignore_index=True)
    else:
        df_plot = df_plot_a

    fig_bal = px.line(df_plot, x="Month", y="Balance", color="Scenario", title="Balance Over Time")
    st.plotly_chart(fig_bal, use_container_width=True)

    st.download_button("Download Scenario A Data (CSV)", data=df_a.to_csv(index=False).encode("utf-8"), file_name="scenario_a.csv", mime="text/csv")
    if compare:
        st.download_button("Download Scenario B Data (CSV)", data=df_b.to_csv(index=False).encode("utf-8"), file_name="scenario_b.csv", mime="text/csv")

    st.dataframe(df_plot if compare else df_a, use_container_width=True)

with tab2:
    # Stacked area of contributions vs interest for each scenario
    df_a_area = df_a.melt(id_vars=["Month"], value_vars=["Contribution", "Interest Accrued"], var_name="Component", value_name="Amount")
    df_a_area["Scenario"] = "A"
    if compare:
        df_b_area = df_b.melt(id_vars=["Month"], value_vars=["Contribution", "Interest Accrued"], var_name="Component", value_name="Amount")
        df_b_area["Scenario"] = "B"
        df_area = pd.concat([df_a_area, df_b_area], ignore_index=True)
    else:
        df_area = df_a_area

    fig_area = px.area(df_area, x="Month", y="Amount", color="Component", facet_row="Scenario" if compare else None, title="Contributions vs. Interest Over Time")
    st.plotly_chart(fig_area, use_container_width=True)

with st.expander("Model notes"):
    st.markdown(
        "- Interest is compounded monthly: **r_m = annual_rate / 12**.\n"
        "- Contributions occur at **end of each month**.\n"
        "- Final balance = PV grown + monthly deposits + accrued interest.\n"
        "- Use the comparison toggle to run A/B scenarios."
    )

st.caption("Made with Streamlit · Ready for GitHub and Streamlit Community Cloud.")
