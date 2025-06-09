import pandas as pd
import requests
from io import StringIO
import os
from datetime import datetime

# Constants
NOMIS_URL = "https://www.nomisweb.co.uk/api/v01/dataset/NM_17_5.data.csv?geography=1946157341...1946157341&date=latest-15"
CHICHESTER_CODE = "1946157341"
YEARS_BACK = 15
OUTPUT_PATH = "data/processed/employment_chichester_summary.csv"

# List of variables to keep (must match exactly)
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

def fetch_and_process_employment():
    print("📡 Fetching employment data from NOMIS...")

    current_year = datetime.now().year
    start_year = current_year - (YEARS_BACK - 1)
    date_range = f"{start_year}-{current_year}"

    params = {
        "geography": CHICHESTER_CODE,
        "date": date_range
    }

    response = requests.get(NOMIS_URL, params=params)
    if response.status_code != 200 or not response.text.strip():
        raise RuntimeError(f"❌ Error fetching data: {response.status_code}\n{response.text[:500]}")

    df = pd.read_csv(StringIO(response.text))

    # Filter for Variable type rows only
    df = df[df["MEASURES_NAME"] == "Variable"]

    # Filter for specific variables
    df = df[df["VARIABLE_NAME"].isin(TARGET_VARIABLES)]

    # Clean up column names
    df = df.rename(columns={
        "DATE_NAME": "Year",
        "VARIABLE_NAME": "Category",
        "OBS_VALUE": "Value"
    })

    # Narrow to relevant columns and drop NA
    df = df[["Year", "Category", "Value"]].dropna()
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")

    # Pivot to wide format
    df_wide = df.pivot(index="Year", columns="Category", values="Value").reset_index()

    # Save to output
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df_wide.to_csv(OUTPUT_PATH, index=False)

    print(f"✅ Pivoted employment summary saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    fetch_and_process_employment()





