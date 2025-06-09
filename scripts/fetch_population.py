import pandas as pd
import requests
from io import StringIO
import os
import traceback

# Constants
NOMIS_URL = "https://www.nomisweb.co.uk/api/v01/dataset/NM_17_5.data.csv?geography=1946157341...1946157341&date=latest-15"
OUTPUT_PATH = "data/processed/employment_chichester_summary.csv"

TARGET_VARIABLES = [
    "Employment rate - aged 16+",
    "% who are economically inactive - aged 16+",
    "% aged 16-64 economically inactive who want a job",
    "% aged 16-64 economically inactive who do not want a job",
    "% in employment who are employees - aged 16+",
    "% in employment who are self employed - aged 16+",
    "% all in employment who work in - A-B:agriculture and fishing (SIC 92/03)",
    "% all in employment who work in - C,E:energy and water (SIC 92/03)",
    "% all in employment who work in - D:manufacturing (SIC 92/03)",
    "% all in employment who work in - F:construction (SIC 92/03)",
    "% all in employment who work in - G-H:distribution, hotels and restaurants (SIC 92/03)",
    "% all in employment who work in - I:transport and communications (SIC 92/03)",
    "% all in employment who work in - J-K:banking, finance and insurance (SIC 92/03)",
    "% all in employment who work in - L-N:public admin. education and health (SIC 92/03)",
    "% all in employment who work in - O-Q:other services (SIC 92/03)",
    "% all in employment who work in - G-Q:total services (SIC 92/03)"
]

def fetch_employment_data():
    try:
        print("📡 Fetching employment data...")
        response = requests.get(NOMIS_URL)
        response.raise_for_status()
        print("✅ Data downloaded successfully.")

        df = pd.read_csv(StringIO(response.text))
        print(f"📊 Raw data shape: {df.shape}")
        
        # Filter only full calendar years
        df = df[df["DATE_NAME"].str.contains("Jan") & df["DATE_NAME"].str.contains("Dec")]
        print(f"📆 After filtering by calendar years: {df.shape}")

        df = df[(df["MEASURES_NAME"] == "Variable") & df["VARIABLE_NAME"].isin(TARGET_VARIABLES)]
        print(f"🎯 After filtering by variable names: {df.shape}")

        df = df.rename(columns={
            "DATE_NAME": "Year",
            "VARIABLE_NAME": "Category",
            "OBS_VALUE": "Value"
        })[["Year", "Category", "Value"]]

        df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
        df = df.dropna()
        print(f"🧹 After cleaning nulls: {df.shape}")

        df_wide = df.pivot(index="Year", columns="Category", values="Value").reset_index()
        print(f"📐 Final wide format shape: {df_wide.shape}")

        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        df_wide.to_csv(OUTPUT_PATH, index=False)
        print(f"💾 File saved to {OUTPUT_PATH}")
    except Exception as e:
        print("❌ An error occurred during execution:")
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    fetch_employment_data()



