import pandas as pd
import os
import requests
from io import StringIO

def fetch_and_clean_employment():
    print("📡 Fetching Chichester employment data from NOMIS API...")

    # NOMIS API URL for employment & unemployment estimates (model-based)
    url = (
        "https://www.nomisweb.co.uk/api/v01/dataset/NM_1_1.data.csv?"
    )

    try:
        # Fetch and read the CSV from the API
        response = requests.get(url)
        response.raise_for_status()
        df = pd.read_csv(StringIO(response.text))

        # Optional cleaning & formatting
        df = df.rename(columns={
            "date": "Date",
            "geography_name": "Location",
            "employment_status_name": "Status",
            "variable_name": "Variable",
            "obs_value": "Value"
        })

        # Pivot to show key indicators as columns
        df = df.pivot_table(index="Date", columns="Variable", values="Value", aggfunc="first").reset_index()
        df.insert(1, "Location", "Chichester")

        # Save
        os.makedirs("data/processed", exist_ok=True)
        df.to_csv("data/processed/employment_chichester.csv", index=False)

        print("✅ Employment data saved to data/processed/employment_chichester.csv")

    except requests.exceptions.RequestException as e:
        print("❌ Error fetching from NOMIS:", e)

if __name__ == "__main__":
    fetch_and_clean_employment()

