import pandas as pd
import requests
from io import StringIO
import os

from datetime import datetime

def fetch_population_chichester():
    url = "https://www.nomisweb.co.uk/api/v01/dataset/NM_2002_1.csv"

    current_year = datetime.now().year
    start_year = current_year - 14
    date_range = f"{start_year}-{current_year}"

    params = {
        "geography": "1946157341",  # Chichester
        "date": date_range
    }

    print("📡 Fetching population data from NOMIS...")
    response = requests.get(url, params=params)
    if response.status_code != 200 or not response.text.strip():
        raise RuntimeError(f"❌ Error fetching data: {response.status_code}\n{response.text[:500]}")

    df = pd.read_csv(StringIO(response.text))

    # Rename and keep only necessary columns
    df = df.rename(columns={
        "DATE_NAME": "Year",
        "GEOGRAPHY_NAME": "Location",
        "GENDER_NAME": "Gender",
        "C_AGE_NAME": "Age Group",
        "MEASURES_NAME": "Measure Type",
        "OBS_VALUE": "Population"
    })

    df = df[["Year", "Location", "Gender", "Age Group", "Measure Type", "Population"]]

    # Split into counts and percentages
    counts_df = df[df["Measure Type"] == "Value"].copy()
    perc_df = df[df["Measure Type"] == "Percent"].copy()

    # Save both
    os.makedirs("data/processed", exist_ok=True)
    counts_df.to_csv("data/processed/population_chichester_counts.csv", index=False)
    perc_df.to_csv("data/processed/population_chichester_percentages.csv", index=False)

if __name__ == "__main__":
    fetch_population_chichester()

