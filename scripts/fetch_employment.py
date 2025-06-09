import pandas as pd
import requests
from io import StringIO
import os

# Constants (same as before)
NOMIS_URL = "https://www.nomisweb.co.uk/api/v01/dataset/NM_17_5.data.csv"
CHICHESTER_CODE = "1946157341"
OUTPUT_PATH = "data/processed/employment_chichester_summary.csv"

# List of variables to keep (same as before)
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
    params = {
        "geography": CHICHESTER_CODE,
        "time": "latestMINUS14-latest",
        "measures": "20100",  # ensures we get values
    }

    print("📡 Fetching employment data (last 15 years)...")
    response = requests.get(NOMIS_URL, params=params)
    if response.status_code != 200:
        raise RuntimeError(f"❌ API error: {response.status_code}")

    df = pd.read_csv(StringIO(response.text))
    print("✅ Raw download complete. Years present:", df["DATE_NAME"].unique())

    # Filter and simplify
    df = df[df["MEASURES_NAME"] == "Variable"]
    df = df[df["VARIABLE_NAME"].isin(TARGET_VARIABLES)]
    df = df.rename(columns={"DATE_NAME": "Year", "VARIABLE_NAME": "Category", "OBS_VALUE": "Value"})
    df = df[["Year", "Category", "Value"]].dropna()
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")

    # Pivot wide
    df_wide = df.pivot(index="Year", columns="Category", values="Value").reset_index()

    # Save
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df_wide.to_csv(OUTPUT_PATH, index=False)
    print(f"✅ Employment data saved with {len(df_wide)} rows")

if __name__ == "__main__":
    fetch_and_process_employment()


