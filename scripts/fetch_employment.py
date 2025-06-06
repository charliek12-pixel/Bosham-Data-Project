import pandas as pd
import requests
from io import StringIO
import os

def fetch_all_employment_data():
    url = "https://www.nomisweb.co.uk/api/v01/dataset/NM_1_1.data.csv"
    params = {
        "date": "latest",
        "employment_status": "0",    # All statuses
        "measures": "20100",        # Count
        "select": "date,geography_code,geography_name,employment_status_name,variable_name,obs_value"
    }

    print("📡 Downloading full NOMIS employment dataset...")
    r = requests.get(url, params=params)
    if r.status_code != 200 or not r.text.strip():
        raise RuntimeError(f"❌ Error fetching data: {r.status_code}\n{r.text[:500]}")

    df = pd.read_csv(StringIO(r.text))

    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/nomis_employment_full.csv", index=False)
    print("✅ Full employment dataset saved to data/raw/nomis_employment_full.csv")

if __name__ == "__main__":
    fetch_all_employment_data()



