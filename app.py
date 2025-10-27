# Import libraries
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="📊 PhonePe Transaction Insights",
    layout="wide",
    page_icon="💸"
)

# ----------------------------
# Load Data
# ----------------------------
df = pd.read_csv("aggregated_transaction.csv")

# ----------------------------
# Title & Description
# ----------------------------
st.title("📊 PhonePe Transaction Insights Dashboard")
st.markdown("""
Explore the transaction data across **Indian states**, **years**, and **transaction types**.
Use the sidebar to filter your view.
""")

# ----------------------------
# Sidebar Filters
# ----------------------------
st.sidebar.header("Filter Options")

# Year filter
years = sorted(df["Year"].unique())
selected_year = st.sidebar.selectbox("Select Year", options=years, index=len(years)-1)

# State filter
states = df["State"].unique()
selected_states = st.sidebar.multiselect("Select State(s)", options=states, default=list(states))

# Transaction Type filter
transaction_types = df["Transaction_Type"].unique()
selected_txn_types = st.sidebar.multiselect(
    "Select Transaction Type(s)", options=transaction_types, default=list(transaction_types)
)

# Filter DataFrame based on selections
filtered_df = df[
    (df["Year"] == selected_year) &
    (df["State"].isin(selected_states)) &
    (df["Transaction_Type"].isin(selected_txn_types))
]

# ----------------------------
# Layout: Two Columns
# ----------------------------
col1, col2 = st.columns(2)

# Total Transaction Amount by Type
with col1:
    st.subheader("💰 Total Transaction Amount by Type")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(
        data=filtered_df,
        x="Transaction_Type",
        y="Transaction_Amount",
        estimator=sum,
        palette="mako",
        ax=ax
    )
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Transaction Count by Type
with col2:
    st.subheader("📈 Transaction Count by Type")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(
        data=filtered_df,
        x="Transaction_Type",
        y="Transaction_Count",
        estimator=sum,
        palette="rocket",
        ax=ax
    )
    plt.xticks(rotation=45)
    st.pyplot(fig)

# ----------------------------
# Yearly Trend
# ----------------------------
st.subheader("📆 Transaction Growth Over the Years")
yearly = df.groupby(["Year"])[["Transaction_Amount"]].sum().reset_index()

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=yearly, x="Year", y="Transaction_Amount", marker="o", ax=ax)
st.pyplot(fig)

# ----------------------------
# State-wise Total Transactions
# ----------------------------
st.subheader("📍 State-wise Transaction Amount")
state_summary = filtered_df.groupby("State")[["Transaction_Amount", "Transaction_Count"]].sum().reset_index()

fig, ax = plt.subplots(figsize=(12, 5))
sns.barplot(
    data=state_summary,
    x="State",
    y="Transaction_Amount",
    palette="viridis",
    ax=ax
)
plt.xticks(rotation=45)
st.pyplot(fig)

# ----------------------------
# Summary Metrics
# ----------------------------
st.subheader("🧠 Summary Insights")
total_amount = filtered_df["Transaction_Amount"].sum()
total_count = filtered_df["Transaction_Count"].sum()
st.metric("Total Transaction Amount", f"₹{total_amount:,.2f}")
st.metric("Total Transaction Count", f"{total_count:,}")

