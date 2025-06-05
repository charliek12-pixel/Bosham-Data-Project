import pandas as pd
import os

def fetch_and_clean_employment():
    # Nomis download link (manual export link required for full automation)
    url = "https://www.nomisweb.co.uk/output/download/nomis_lmp_chichester.csv"
    os.makedirs("data/processed", exist_ok=True)

    # Placeholder since Nomis doesn’t provide a persistent downloadable link without interaction
    print("⚠️ Nomis auto-download not supported without scraping. Please manually download to data/raw/")

    # Assume local file exists
    try:
        df = pd.read_csv("data/raw/nomis_lmp_chichester.csv")
        df = df[["Date", "Variable", "Value"]]  # Simplify to a structure
        df = df.pivot(index="Date", columns="Variable", values="Value").reset_index()
        df.insert(1, "Location", "Chichester")
        df.to_csv("data/processed/employment_chichester.csv", index=False)
        print("✅ Employment data saved.")
    except FileNotFoundError:
        print("❌ Nomis CSV not found. Please download manually.")

if __name__ == "__main__":
    fetch_and_clean_employment()
