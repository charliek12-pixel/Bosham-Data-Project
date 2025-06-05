import requests
import pandas as pd
import os

def fetch_and_clean_crime():
    url = "https://data.police.uk/api/crimes-street/all-crime?lat=50.8319&lng=-0.8632&date=2023-03"
    r = requests.get(url)
    data = r.json()

    df = pd.json_normalize(data)
    if not df.empty:
        df = df[["category", "location.street.name", "month"]]
        df.columns = ["CrimeType", "Street", "Month"]

    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/crime_bosham.csv", index=False)
    print("✅ Crime data saved.")

if __name__ == "__main__":
    fetch_and_clean_crime()
