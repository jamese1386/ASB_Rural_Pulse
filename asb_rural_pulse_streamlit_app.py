import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="ASB Rural Pulse", layout="wide")

# -----------------------------
# PAGE STYLING
# -----------------------------
st.markdown(
    """
    <style>
        .main {
            background-color: #f7f8fa;
        }
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }
        .hero {
            background: linear-gradient(135deg, #0e2a47 0%, #1f5d8a 100%);
            padding: 1.4rem 1.6rem;
            border-radius: 18px;
            color: white;
            margin-bottom: 1rem;
            box-shadow: 0 10px 25px rgba(0,0,0,0.08);
        }
        .hero h1 {
            margin: 0;
            font-size: 2rem;
        }
        .hero p {
            margin: 0.35rem 0 0 0;
            color: #d9e6f1;
            font-size: 0.98rem;
        }
        .section-card {
            background: white;
            padding: 1rem 1rem 0.5rem 1rem;
            border-radius: 16px;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
            border: 1px solid #e7edf3;
            margin-bottom: 1rem;
        }
        .insight-box {
            background: #eef6fb;
            padding: 0.9rem 1rem;
            border-radius: 12px;
            border-left: 5px solid #1f5d8a;
            margin-top: 0.5rem;
            margin-bottom: 0.5rem;
        }
        .stMetric {
            background: white;
            border: 1px solid #e7edf3;
            padding: 0.5rem;
            border-radius: 14px;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.04);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# MOCK CLIENT DATA
# -----------------------------
clients_data = [
    {
        "client": "Waikato Dairy Ltd",
        "farm_type": "Dairy",
        "region": "Waikato",
        "relationship_manager": "R. Dykes",
        "annual_revenue_nzd": 2450000,
        "annual_expenses_nzd": 1780000,
        "debt_nzd": 3200000,
        "overdraft_limit_nzd": 450000,
        "overdraft_used_nzd": 315000,
        "commodity_index": 82,
        "weather_risk": "Medium",
        "financials_status": "Up to date",
        "review_due_days": 18,
        "seasonal_pressure": "High",
    },
    {
        "client": "Southland Sheep & Beef Co",
        "farm_type": "Sheep & Beef",
        "region": "Southland",
        "relationship_manager": "A. Chen",
        "annual_revenue_nzd": 1680000,
        "annual_expenses_nzd": 1190000,
        "debt_nzd": 1750000,
        "overdraft_limit_nzd": 250000,
        "overdraft_used_nzd": 110000,
        "commodity_index": 74,
        "weather_risk": "Low",
        "financials_status": "Pending",
        "review_due_days": 9,
        "seasonal_pressure": "Medium",
    },
    {
        "client": "Bay Orchards Partnership",
        "farm_type": "Horticulture",
        "region": "Bay of Plenty",
        "relationship_manager": "J. Morgan",
        "annual_revenue_nzd": 2140000,
        "annual_expenses_nzd": 1610000,
        "debt_nzd": 2280000,
        "overdraft_limit_nzd": 320000,
        "overdraft_used_nzd": 260000,
        "commodity_index": 88,
        "weather_risk": "High",
        "financials_status": "Up to date",
        "review_due_days": 35,
        "seasonal_pressure": "High",
    },
    {
        "client": "Canterbury Mixed Farming",
        "farm_type": "Mixed Farming",
        "region": "Canterbury",
        "relationship_manager": "R. Dykes",
        "annual_revenue_nzd": 1910000,
        "annual_expenses_nzd": 1450000,
        "debt_nzd": 2020000,
        "overdraft_limit_nzd": 300000,
        "overdraft_used_nzd": 145000,
        "commodity_index": 79,
        "weather_risk": "Medium",
        "financials_status": "Overdue",
        "review_due_days": 4,
        "seasonal_pressure": "Medium",
    },
    {
        "client": "Otago Hill Country Farming",
        "farm_type": "Sheep & Beef",
        "region": "Otago",
        "relationship_manager": "S. Patel",
        "annual_revenue_nzd": 1390000,
        "annual_expenses_nzd": 1085000,
        "debt_nzd": 1490000,
        "overdraft_limit_nzd": 210000,
        "overdraft_used_nzd": 178000,
        "commodity_index": 70,
        "weather_risk": "Medium",
        "financials_status": "Pending",
        "review_due_days": 12,
        "seasonal_pressure": "High",
    },
    {
        "client": "Taranaki Dairy Holdings",
        "farm_type": "Dairy",
        "region": "Taranaki",
        "relationship_manager": "A. Chen",
        "annual_revenue_nzd": 2580000,
        "annual_expenses_nzd": 1880000,
        "debt_nzd": 3480000,
        "overdraft_limit_nzd": 500000,
        "overdraft_used_nzd": 210000,
        "commodity_index": 86,
        "weather_risk": "Low",
        "financials_status": "Up to date",
        "review_due_days": 42,
        "seasonal_pressure": "Low",
    },
]

clients_df = pd.DataFrame(clients_data)

# -----------------------------
# MONTHLY CASH FLOW DATA
# -----------------------------
months = [
    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
    "Jan", "Feb", "Mar", "Apr", "May", "Jun"
]

cashflow_map = {
    "Waikato Dairy Ltd": {
        "income": [110000, 125000, 145000, 165000, 190000, 240000, 260000, 255000, 240000, 220000, 180000, 130000],
        "costs": [135000, 132000, 138000, 145000, 148000, 154000, 159000, 163000, 158000, 151000, 145000, 142000],
    },
    "Southland Sheep & Beef Co": {
        "income": [80000, 85000, 93000, 101000, 109000, 135000, 175000, 200000, 184000, 156000, 130000, 108000],
        "costs": [98000, 94000, 96000, 99000, 102000, 106000, 110000, 116000, 112000, 107000, 103000, 101000],
    },
    "Bay Orchards Partnership": {
        "income": [92000, 89000, 97000, 112000, 145000, 210000, 285000, 330000, 290000, 220000, 145000, 125000],
        "costs": [118000, 122000, 127000, 131000, 135000, 145000, 151000, 158000, 150000, 142000, 136000, 130000],
    },
    "Canterbury Mixed Farming": {
        "income": [89000, 93000, 101000, 109000, 126000, 152000, 185000, 178000, 172000, 149000, 128000, 112000],
        "costs": [104000, 105000, 108000, 111000, 115000, 121000, 126000, 129000, 124000, 119000, 116000, 110000],
    },
    "Otago Hill Country Farming": {
        "income": [71000, 76000, 82000, 93000, 101000, 125000, 152000, 171000, 162000, 141000, 116000, 95000],
        "costs": [91000, 94000, 96000, 99000, 101000, 106000, 111000, 118000, 114000, 109000, 104000, 99000],
    },
    "Taranaki Dairy Holdings": {
        "income": [118000, 132000, 148000, 171000, 205000, 248000, 272000, 265000, 250000, 232000, 192000, 148000],
        "costs": [138000, 141000, 145000, 149000, 154000, 160000, 165000, 171000, 167000, 158000, 149000, 145000],
    },
}

# -----------------------------
# HELPERS
# -----------------------------
def utilisation_pct(row: pd.Series) -> float:
    return (row["overdraft_used_nzd"] / row["overdraft_limit_nzd"]) * 100


def margin_pct(row: pd.Series) -> float:
    return ((row["annual_revenue_nzd"] - row["annual_expenses_nzd"]) / row["annual_revenue_nzd"]) * 100


def credit_risk_score(row: pd.Series) -> int:
    score = 0
    score += 3 if utilisation_pct(row) >= 80 else 2 if utilisation_pct(row) >= 60 else 1
    score += 3 if row["weather_risk"] == "High" else 2 if row["weather_risk"] == "Medium" else 1
    score += 3 if row["financials_status"] == "Overdue" else 2 if row["financials_status"] == "Pending" else 1
    score += 3 if row["seasonal_pressure"] == "High" else 2 if row["seasonal_pressure"] == "Medium" else 1
    score += 3 if row["review_due_days"] <= 7 else 2 if row["review_due_days"] <= 21 else 1
    return score


def risk_band(score: int) -> str:
    if score >= 13:
        return "High"
    if score >= 10:
        return "Medium"
    return "Low"


def monthly_cashflow_df(client_name: str) -> pd.DataFrame:
    data = cashflow_map[client_name]
    df = pd.DataFrame({
        "month": months,
        "income": data["income"],
        "costs": data["costs"],
    })
    df["net_cashflow"] = df["income"] - df["costs"]
    df["cumulative_cashflow"] = df["net_cashflow"].cumsum()
    return df


def create_action_list(clients: pd.DataFrame) -> pd.DataFrame:
    actions = []
    for _, row in clients.iterrows():
        util = utilisation_pct(row)
        score = row["credit_risk_score"]

        if util >= 80:
            actions.append({
                "client": row["client"],
                "priority": "High",
                "action": "Discuss seasonal working capital needs",
            })

        if row["financials_status"] in ["Pending", "Overdue"]:
            actions.append({
                "client": row["client"],
                "priority": "High" if row["financials_status"] == "Overdue" else "Medium",
                "action": "Request updated financial statements",
            })

        if row["review_due_days"] <= 14:
            actions.append({
                "client": row["client"],
                "priority": "High",
                "action": "Prepare upcoming credit review pack",
            })

        if row["weather_risk"] == "High":
            actions.append({
                "client": row["client"],
                "priority": "Medium",
                "action": "Check weather-related operational impacts",
            })

        if score >= 13:
            actions.append({
                "client": row["client"],
                "priority": "High",
                "action": "Schedule proactive banker call this week",
            })

    actions_df = pd.DataFrame(actions)
    if not actions_df.empty:
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        actions_df["sort"] = actions_df["priority"].map(priority_order)
        actions_df = actions_df.sort_values(["sort", "client"]).drop(columns="sort")
    return actions_df


def generate_credit_summary(row: pd.Series) -> str:
    util = utilisation_pct(row)
    margin = margin_pct(row)
    return (
        f"{row['client']} is a {row['farm_type'].lower()} client based in {row['region']}. "
        f"Annual revenue is approximately NZD {row['annual_revenue_nzd']:,.0f} against expenses of NZD {row['annual_expenses_nzd']:,.0f}, "
        f"implying an operating margin of about {margin:.1f}%. Total debt sits at NZD {row['debt_nzd']:,.0f}. "
        f"Overdraft utilisation is {util:.1f}% of the approved limit. Current key considerations include {row['seasonal_pressure'].lower()} seasonal pressure, "
        f"{row['weather_risk'].lower()} weather risk, and financials status marked as {row['financials_status'].lower()}. "
        f"Recommended next step: review servicing resilience and confirm whether any short-term working capital support or updated credit information is needed."
    )


clients_df["overdraft_utilisation_pct"] = clients_df.apply(utilisation_pct, axis=1)
clients_df["operating_margin_pct"] = clients_df.apply(margin_pct, axis=1)
clients_df["credit_risk_score"] = clients_df.apply(credit_risk_score, axis=1)
clients_df["risk_band"] = clients_df["credit_risk_score"].apply(risk_band)
actions_df = create_action_list(clients_df)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("ASB Rural Pulse")
st.sidebar.caption("Rural Banking Relationship Dashboard")

selected_farm_types = st.sidebar.multiselect(
    "Farm Type",
    options=sorted(clients_df["farm_type"].unique().tolist()),
    default=sorted(clients_df["farm_type"].unique().tolist()),
)

selected_regions = st.sidebar.multiselect(
    "Region",
    options=sorted(clients_df["region"].unique().tolist()),
    default=sorted(clients_df["region"].unique().tolist()),
)

selected_risk = st.sidebar.multiselect(
    "Risk Band",
    options=["High", "Medium", "Low"],
    default=["High", "Medium", "Low"],
)

filtered_clients = clients_df[
    clients_df["farm_type"].isin(selected_farm_types)
    & clients_df["region"].isin(selected_regions)
    & clients_df["risk_band"].isin(selected_risk)
]

filtered_actions = actions_df[actions_df["client"].isin(filtered_clients["client"])] if not actions_df.empty else actions_df

# -----------------------------
# HERO
# -----------------------------
st.markdown(
    """
    <div class='hero'>
        <h1>ASB Rural Pulse</h1>
        <p>Helping rural bankers stay ahead of seasonal pressure, client risk, and proactive support opportunities.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# KPIs
# -----------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric("Clients in Portfolio", len(filtered_clients))
col2.metric("Total Debt", f"NZD {filtered_clients['debt_nzd'].sum():,.0f}")
col3.metric("Avg OD Utilisation", f"{filtered_clients['overdraft_utilisation_pct'].mean():.1f}%")
col4.metric("Action Items", len(filtered_actions))

st.markdown("<div class='section-card'>", unsafe_allow_html=True)
st.subheader("Executive Snapshot")
summary_text = (
    "Portfolio pressure is concentrated among clients with high overdraft utilisation, pending or overdue financials, "
    "and upcoming credit reviews. Priority should be proactive outreach and updated information gathering."
)
st.markdown(f"<div class='insight-box'>{summary_text}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# TOP CHARTS
# -----------------------------
left, right = st.columns(2)

with left:
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.subheader("Overdraft Utilisation by Client")
    fig, ax = plt.subplots(figsize=(8, 4))
    util_chart = filtered_clients.sort_values("overdraft_utilisation_pct", ascending=True)
    ax.barh(util_chart["client"], util_chart["overdraft_utilisation_pct"])
    ax.set_xlabel("Utilisation %")
    ax.set_ylabel("Client")
    ax.set_title("Working Capital Pressure")
    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.subheader("Debt by Farm Type")
    fig, ax = plt.subplots(figsize=(8, 4))
    debt_by_type = filtered_clients.groupby("farm_type", as_index=False)["debt_nzd"].sum()
    ax.bar(debt_by_type["farm_type"], debt_by_type["debt_nzd"])
    ax.set_xlabel("Farm Type")
    ax.set_ylabel("Debt (NZD)")
    ax.set_title("Portfolio Debt Mix")
    plt.xticks(rotation=15)
    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# TABS
# -----------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "Portfolio Overview",
    "Client Drilldown",
    "Cash Flow & Credit",
    "Banker Action Centre",
])

with tab1:
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.subheader("Credit Risk Score by Client")
        fig, ax = plt.subplots(figsize=(8, 4))
        risk_chart = filtered_clients.sort_values("credit_risk_score", ascending=True)
        ax.barh(risk_chart["client"], risk_chart["credit_risk_score"])
        ax.set_xlabel("Credit Risk Score")
        ax.set_ylabel("Client")
        ax.set_title("Priority Ranking")
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.subheader("Margin vs Overdraft Utilisation")
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.scatter(filtered_clients["operating_margin_pct"], filtered_clients["overdraft_utilisation_pct"])
        for _, row in filtered_clients.iterrows():
            ax.annotate(row["client"], (row["operating_margin_pct"], row["overdraft_utilisation_pct"]), fontsize=8)
        ax.set_xlabel("Operating Margin %")
        ax.set_ylabel("Overdraft Utilisation %")
        ax.set_title("Client Resilience Snapshot")
        st.pyplot(fig)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.subheader("Rural Portfolio Table")
    st.dataframe(
        filtered_clients[[
            "client",
            "farm_type",
            "region",
            "relationship_manager",
            "debt_nzd",
            "overdraft_limit_nzd",
            "overdraft_used_nzd",
            "overdraft_utilisation_pct",
            "financials_status",
            "review_due_days",
            "risk_band",
            "credit_risk_score",
        ]],
        use_container_width=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.subheader("Client Drilldown")

    selected_client = st.selectbox("Select a client", filtered_clients["client"].tolist())
    client_row = filtered_clients[filtered_clients["client"] == selected_client].iloc[0]

    a, b, c, d = st.columns(4)
    a.metric("Farm Type", client_row["farm_type"])
    b.metric("Debt", f"NZD {client_row['debt_nzd']:,.0f}")
    c.metric("OD Utilisation", f"{client_row['overdraft_utilisation_pct']:.1f}%")
    d.metric("Risk Band", client_row["risk_band"])

    st.write(f"**Region:** {client_row['region']}")
    st.write(f"**Relationship Manager:** {client_row['relationship_manager']}")
    st.write(f"**Financials Status:** {client_row['financials_status']}")
    st.write(f"**Review Due In:** {client_row['review_due_days']} days")
    st.write(f"**Weather Risk:** {client_row['weather_risk']}")
    st.write(f"**Seasonal Pressure:** {client_row['seasonal_pressure']}")

    st.markdown(
        f"<div class='insight-box'>{selected_client} shows overdraft utilisation of {client_row['overdraft_utilisation_pct']:.1f}% and an operating margin of {client_row['operating_margin_pct']:.1f}%. This suggests a {'higher' if client_row['credit_risk_score'] >= 13 else 'moderate' if client_row['credit_risk_score'] >= 10 else 'lower'} need for proactive relationship management.</div>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    left_col, right_col = st.columns(2)

    with left_col:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.subheader("Monthly Cash Flow")
        cash_df = monthly_cashflow_df(selected_client)

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(cash_df["month"], cash_df["income"], label="Income")
        ax.plot(cash_df["month"], cash_df["costs"], label="Costs")
        ax.set_title("Seasonal Income vs Costs")
        ax.set_xlabel("Month")
        ax.set_ylabel("NZD")
        ax.legend()
        st.pyplot(fig)

        fig2, ax2 = plt.subplots(figsize=(8, 4))
        ax2.bar(cash_df["month"], cash_df["net_cashflow"])
        ax2.set_title("Monthly Net Cash Flow")
        ax2.set_xlabel("Month")
        ax2.set_ylabel("NZD")
        st.pyplot(fig2)
        st.markdown("</div>", unsafe_allow_html=True)

    with right_col:
        st.markdown("<div class='section-card'>", unsafe_allow_html=True)
        st.subheader("Credit Submission Support")
        st.write("### Draft Client Summary")
        st.info(generate_credit_summary(client_row))

        covenant_buffer = client_row["overdraft_limit_nzd"] - client_row["overdraft_used_nzd"]
        st.write("### Quick Credit Indicators")
        st.write(f"- Overdraft headroom: NZD {covenant_buffer:,.0f}")
        st.write(f"- Commodity index: {client_row['commodity_index']}")
        st.write(f"- Operating margin: {client_row['operating_margin_pct']:.1f}%")
        st.write(f"- Review due in: {client_row['review_due_days']} days")
        st.markdown("</div>", unsafe_allow_html=True)

with tab4:
    st.markdown("<div class='section-card'>", unsafe_allow_html=True)
    st.subheader("Banker Action Centre")
    if filtered_actions.empty:
        st.success("No immediate action items.")
    else:
        st.dataframe(filtered_actions, use_container_width=True)

        priority_counts = filtered_actions["priority"].value_counts().reindex(["High", "Medium", "Low"], fill_value=0)
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(priority_counts.index, priority_counts.values)
        ax.set_xlabel("Priority")
        ax.set_ylabel("Number of Actions")
        ax.set_title("Action Queue")
        st.pyplot(fig)

        top_action = filtered_actions.iloc[0]
        st.markdown(
            f"<div class='insight-box'><strong>Next best action:</strong> {top_action['action']} for {top_action['client']}.</div>",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

st.caption(f"Last updated: {datetime.now().strftime('%d %b %Y %H:%M:%S')}")
