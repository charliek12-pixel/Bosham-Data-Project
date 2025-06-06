import streamlit as st
import pandas as pd
import os

# Load data
@st.cache_data
def load_data():
    filepath = "data/processed/population_chichester_counts.csv"
    if not os.path.exists(filepath):
        st.error("Population data not found. Please run the data fetch script.")
        return pd.DataFrame()
    import streamlit as st
import pandas as pd
import os

# Load data
@st.cache_data
def load_data():
    filepath = "data/processed/population_chichester_counts.csv"
    if not os.path.exists(filepath):
        st.error("Population data not found. Please run the data fetch script.")
        return pd.DataFrame()
    df = pd.read_csv(filepath)
    df = df.rename(columns={"Value": "Population"})
    return df
df = load_data()

st.title("📊 Chichester Population Dashboard")

if not df.empty:
    # Sidebar filters
    years = df["Year"].unique()
    age_groups = df["Age Group"].unique()

    selected_year = st.sidebar.selectbox("Select year", sorted(years, reverse=True))
    selected_group = st.sidebar.selectbox("Select age group", sorted(age_groups))

    filtered = df[(df["Year"] == selected_year) & (df["Age Group"] == selected_group)]

    st.subheader(f"Population in {selected_year} for {selected_group}")
    st.dataframe(filtered)

    st.bar_chart(filtered.set_index("Gender")["Population"])
else:
    st.info("Waiting for data...")
    return df

df = load_data()

st.title("📊 Chichester Population Dashboard")

if not df.empty:
    # Sidebar filters
    years = df["Year"].unique()
    age_groups = df["Age Group"].unique()

    selected_year = st.sidebar.selectbox("Select year", sorted(years, reverse=True))
    selected_group = st.sidebar.selectbox("Select age group", sorted(age_groups))

    filtered = df[(df["Year"] == selected_year) & (df["Age Group"] == selected_group)]

    st.subheader(f"Population in {selected_year} for {selected_group}")
    st.dataframe(filtered)

    st.bar_chart(filtered.set_index("Gender")["Population"])
else:
    st.info("Waiting for data...")

