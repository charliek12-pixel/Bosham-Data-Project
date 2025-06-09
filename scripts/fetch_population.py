import pandas as pd
import requests
from io import StringIO
import os

# Constants
NOMIS_URL = "https://www.nomisweb.co.uk/api/v01/dataset/NM_17_5.data.csv?geography=1946157341...1946157341&date=latest-15"
OUTPUT_PATH = "data/processed/employment_chichester_summary.csv"

# Target variable names
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
    print("📡 Fetching data from NOMIS...")
    response = requests.get(NOMIS_URL)
    response.raise_for_status()

    df = pd.read_csv(StringIO(response.text))

    # ✅ Filter to calendar year format
    df = df[df["DATE_NAME"].str.match(r"^Jan \d{4}-Dec \d{4}$")]

    # ✅ Filter by measure and variable
    df = df[(df["MEASURES_NAME"] == "Variable") & df["VARIABLE_NAME"].isin(TARGET_VARIABLES)]

    # ✅ Rename and select columns
    df = df.rename(columns={
        "DATE_NAME": "Year",
        "VARIABLE_NAME": "Category",
        "OBS_VALUE": "Value"
    })[["Year", "Category", "Value"]]

    # ✅ Clean values
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    df = df.dropna()

    # ✅ Pivot to wide format
    df_wide = df.pivot(index="Year", columns="Category", values="Value").reset_index()

    # ✅ Save output
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df_wide.to_csv(OUTPUT_PATH, index=False)
    print(f"✅ Data saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    fetch_employment_data()


