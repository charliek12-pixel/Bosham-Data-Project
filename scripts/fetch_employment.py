import pandas as pd
import requests
from io import StringIO
import os

def get_geography_code(name):
    """
    Pull geography code by name from the same NOMIS dataset (NM_1_1),
    using the official base geography list.
    """
    geo_url = "https://www.nomisweb.co.uk/api/v01/dataset/NM_1_1.geography.csv"
    r = requests.get(geo_url)
    df = pd.read_csv(StringIO(r.text))

    # Find the geography code that best matches the location name
    matches = df[df["GEOGRAPHY_NAME"].str.contains(name, case=False, na=False)]
    if matches.empty:
        raise ValueError(f"No geography code found for: {name}")
    
    code = matches.iloc[0]["GEOGRAPHY_CODE"]
    print(f"📍 Found geography code for {name}: {code}")
    return code

def fetch_employment(location_name):
    # Use your fixed base NOMIS API dataset URL
    base_url = "https://www.nomisweb.co.uk/api/v01/dataset/NM_1_1.data.csv"

    # Look up correct area code
    geo_code = get_geography_code(location_name)

    # Build parameterised request
    params = {
        "geography": geo_code,
        "date": "latest",
        "employment_status": "0",
        "measures": "20100",
        "select": "date,geography_name,employment_status_name,variable_name,obs_value"
    }

    # Fetch from NOMIS
    r = requests.get(base_url, params=params)
    if r.status_code != 200 or not r.text.strip():
        raise RuntimeError(f"Error fetching data: {r.status_code}\n{r.text[:500]}")

    df = pd.read_csv(StringIO(r.text))
    df = df.rename(columns={
        "date": "Date",
        "geography_name": "Location",
        "employment_status_name": "Status",
        "variable_name": "Variable",
        "obs_value": "Value"
    })

    df = df.pivot_table(index="Date", columns="Variable", values="Value", aggfunc="first").reset_index()
    df.insert(1, "Location", location_name)

    # Save result
    os.makedirs("data/processed", exist_ok=True)
    filename = f"data/processed/employment_{location_name.lower().replace(' ', '_')}.csv"
    df.to_csv(filename, index=False)
    print(f"✅ Employment data saved to {filename}")

if __name__ == "__main__":
    fetch_employment("Chichester")


