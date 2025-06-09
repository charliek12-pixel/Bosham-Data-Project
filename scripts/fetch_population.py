import pandas as pd
import requests
from io import StringIO
import os

# Constants
NOMIS_URL = (
    "https://www.nomisweb.co.uk/api/v01/dataset/NM_17_5.data.csv"
    "?geography=1946157341...1946157341&date=latest-15"
)
OUTPUT_PATH = "data/processed/employment_chichester_summary.csv"

# Only include these employment metrics
TARGET_VARIABLES = [
    "Employment rate - aged 16+",
    "% who are economically inactive - aged 16+",
    "% aged 16-64 economically inactive who want a job",
    "% aged 16-64 economically inactive who do not want a job"
]

def fetch_employment_data():
    print("📡 Downloading employment data...")
    response = requests.get(NOMIS_URL)
    response.raise_for_status()

    content = response.text
    if not content.strip():
        raise ValueError("Downloaded file is empty.")

    df = pd.read_csv(StringIO(content))
    print(f"✅ Raw data shape: {df.shape}")

    # Filter for full calendar year ranges and "Variable" measure
    df = df[
        df["DATE_NAME"].str.contains("Jan") &
        df["DATE_NAME"].str.contains("Dec") &
        (df["MEASURES_NAME"] == "Variable")
    ]

    df = df[df["VARIABLE_NAME"].isin(TARGET_VARIABLES)]
    df = df[["DATE_NAME", "VARIABLE_NAME", "OBS_VALUE"]]
    df.columns = ["Year", "Category", "Value"]
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    df = df.dropna()

    # Pivot to wide format: one row per year, each variable in its own column
    df_wide = df.pivot(index="Year", columns="Category", values="Value").reset_index()

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df_wide.to_csv(OUTPUT_PATH, index=False)
    print(f"💾 Saved cleaned data to: {OUTPUT_PATH}")

if __name__ == "__main__":
    fetch_employment_data()




