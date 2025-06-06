import streamlit as st
import pandas as pd
import os

# Load processed data
@st.cache_data
def load_data():
    path = "data/processed/population_chichester_summary.csv"
    if not os.path.exists(path):
        st.error("❌ Data not found. Please fetch the latest population data first.")
        return pd.DataFrame()
    return pd.read_csv(path)

df = load_data()

st.title("📊 Chichester Population Trends")

if df.empty:
    st.stop()

# --- Sidebar filter ---
type_options = ["Total only", "Age groups only", "All combined"]
selected_type = st.sidebar.radio("Select view:", type_options)

# Filter by type
if selected_type == "Total only":
    filtered = df[df["Type"] == "Total"]
elif selected_type == "Age groups only":
    filtered = df[df["Type"] == "Age Group"]
else:
    filtered = df[df["Type"].isin(["Total", "Age Group"])]

# Pivot for line chart
pivot = filtered.pivot(index="Year", columns="Category", values="Population").sort_index()

# Show chart
st.subheader("📈 Population Over Time")
st.line_chart(pivot)

# Optional: expandable data table
with st.expander("🔍 Show data table"):
    st.dataframe(pivot.style.format("{:,.0f}"))
