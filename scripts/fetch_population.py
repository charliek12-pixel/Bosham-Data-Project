import pandas as pd
import os
import requests
from io import StringIO

def fetch_and_clean_population():
    url = "https://www.ons.gov.uk/file?uri=/peoplepopulationandcommunity/populationandmigration/populationestimates/datasets/populationestimatesforukenglandandwalesscotlandandnorthernireland/mid2021/ukmidyearestimates2021finalversion.xls"
    file_path = "data/raw/population_ons.xls"
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    r = requests.get(url)
    with open(file_path, "wb") as f:
        f.write(r.content)

    # ONS data usually starts from row 4 or 5
    df = pd.read_excel(file_path, sheet_name="MYE2 - Persons", skiprows=4)
    df = df[df["Name"].str.contains("Chichester", na=False)]
    df = df.melt(id_vars=["Code", "Name"], var_name="Year", value_name="Population")
    df = df[["Year", "Population", "Name"]]
    df.columns = ["Year", "Population", "Location"]

    df.to_csv("data/processed/population_chichester.csv", index=False)
    print("✅ Population data saved.")

if __name__ == "__main__":
    fetch_and_clean_population()
