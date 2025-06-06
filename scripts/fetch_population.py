import pandas as pd
import requests
from io import StringIO
import os

def fetch_population_chichester():
    url = "https://www.nomisweb.co.uk/api/v01/dataset/NM_2002_1.csv"
    params = {
        "geography": "1946157341",  # Chichester
        "date": "2009-2023"
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
        "OBS_VALUE": "Population",
        "GENDER_NAME": "Gender",
        "C_AGE_NAME": "Age Group"
    })

    df = df[["Year", "Location", "Gender", "Age Group", "Population"]]

    # Save processed output
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/population_chichester.csv", index=False)
    print("✅ Population data saved to data/processed/population_chichester.csv")

if __name__ == "__main__":
    fetch_population_chichester()

