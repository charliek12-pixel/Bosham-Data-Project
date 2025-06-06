import pandas as pd
import requests
from io import StringIO
import os
from datetime import datetime

# Constants
NOMIS_URL = "https://www.nomisweb.co.uk/api/v01/dataset/NM_2002_1.csv"
CHICHESTER_CODE = "1946157341"
YEARS_BACK = 15
OUTPUT_PATH = "data/processed/population_chichester_summary.csv"

# Age brackets to include (exact match from NOMIS)
TARGET_AGE_GROUPS = [
    "Aged 0 to 15",
    "Aged 16 to 24",
    "Aged 25 to 49",
    "Aged 50 to 64",
    "Aged 65+"
]

def fetch_and_process_population():
    print("📡 Fetching population data from NOMIS...")

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

    # Rename for clarity
    df = df.rename(columns={
        "DATE_NAME": "Year",
        "GEOGRAPHY_NAME": "Location",
        "GENDER_NAME": "Gender",
        "C_AGE_NAME": "Age Group",
        "MEASURES_NAME": "Measure Type",
        "OBS_VALUE": "Population"
    })

    # Filter for value rows only and drop exact duplicates
    df = df[df["Measure Type"] == "Value"].drop_duplicates()
    df["Population"] = pd.to_numeric(df["Population"], errors="coerce")

    # AGE GROUPS (Gender = "All persons" or "Total")
    age_df = df[
        df["Gender"].str.lower().isin(["all persons", "total"]) &
        df["Age Group"].isin(TARGET_AGE_GROUPS)
    ][["Year", "Age Group", "Population"]].copy()
    age_df = age_df.rename(columns={"Age Group": "Category"})
    age_df["Type"] = "Age Group"

    # GENDER (Age Group = "All Ages")
    gender_df = df[
        df["Age Group"].str.lower() == "all ages" &
        df["Gender"].isin(["Male", "Female"])
    ][["Year", "Gender", "Population"]].copy()
    gender_df = gender_df.rename(columns={"Gender": "Category"})
    gender_df["Type"] = "Gender"

    # TOTAL POPULATION (All persons + All Ages)
    total_df = df[
        df["Age Group"].str.lower() == "all ages" &
        df["Gender"].str.lower().isin(["all persons", "total"])
    ][["Year", "Population"]].copy()
    total_df["Category"] = "Total Population"
    total_df["Type"] = "Total"
    total_df = total_df[["Year", "Category", "Type", "Population"]]

    # Combine
    combined = pd.concat([age_df, gender_df, total_df], ignore_index=True)
    combined = combined[["Year", "Category", "Type", "Population"]]
    combined = combined.sort_values(by=["Year", "Type", "Category"])

    # Save
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    combined.to_csv(OUTPUT_PATH, index=False)

    print(f"✅ Population summary saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    fetch_and_process_population()



