import requests
import pandas as pd
from datetime import datetime
import os
from io import StringIO

def download_filtered_nomis_data(dataset_id="NM_17_5", years=None, api_key=None):
    """
    Download and combine Nomis data for multiple years with filters.
    """
    base_url = f"https://www.nomisweb.co.uk/api/v01/dataset/{dataset_id}.data.csv"

    # Full list of allowed variables (use your full list here)
    allowed_variables = [
        "% of all people aged 16+ who are male", "% of all people aged 16+ who are female",
        "% of all 16+ who are aged 16-19", "% of all 16+ who are aged 20-24", "% of all 16+ who are aged 25-34",
        "% of all 16+ who are aged 35-49", "% of all 16+ who are aged 50-64", "% of all 16+ who are aged 65+",
        "Economic activity rate - aged 16+", "Economic activity rate males - aged 16+", "Economic activity rate females - aged 16+",
        "% who are economically inactive - aged 16+", "% of  males who are economically inactive - aged 16+",
        "% of females who are economically inactive - aged 16+",
        "Employment rate - aged 16+", "Employment rate males - aged 16+", "Employment rate females - aged 16+",
        "% in employment who are employees - aged 16+", "% in employment who are self employed - aged 16+",
        "% of males aged 16-64 who are employees", "% of males aged 16-64 who are self employed",
        "% of females aged 16-64 who are employees", "% of females aged 16-64 who are self employed",
        "% all in employment who work in - A-B:agriculture and fishing (SIC 92/03)",
        "% all in employment who work in - C,E:energy and water (SIC 92/03)",
        "% all in employment who work in - D:manufacturing (SIC 92/03)",
        "% all in employment who work in - F:construction (SIC 92/03)",
        "% all in employment who work in - G-H:distribution, hotels and restaurants (SIC 92/03)",
        "% all in employment who work in - I:transport and communications (SIC 92/03)",
        "% all in employment who work in - J-K:banking, finance and insurance (SIC 92/03)",
        "% all in employment who work in - L-N:public admin. education and health (SIC 92/03)",
        "% all in employment who work in - O-Q:other services (SIC 92/03)",
        "% all in employment who work in - G-Q:total services (SIC 92/03)",
        "% all in employment who are - 1: managers and senior officials",
        "% all in employment who are - 2: professional occupations",
        "% all in employment who are - 3: associate prof & tech occupations",
        "% all in employment who are - 4: administrative and secretarial occupations",
        "% all in employment who are - 5: skilled trades occupations",
        "% all in employment who are - 6: personal service occupations",
        "% all in employment who are - 7: sales and customer service occupations",
        "% all in employment who are - 8: process, plant and machine operatives",
        "% all in employment who are - 9: elementary occupations",
        "% males in employment who are - 1: managers and senior officials",
        "% males in employment who are - 2: professional occupations",
        "% males in employment who are - 3: associate prof & tech occupations",
        "% males in employment who are - 4: administrative and secretarial occupations",
        "% males in employment who are - 5: skilled trades occupations",
        "% males in employment who are - 6: personal service occupations",
        "% males in employment who are - 7: sales and customer service occupations",
        "% males in employment who are - 8: process, plant and machine operatives",
        "% males in employment who are - 9: elementary occupations",
        "% females in employment who are - 1: managers and senior officials",
        "% females in employment who are - 2: professional occupations",
        "% females in employment who are - 3: associate prof & tech occupations",
        "% females in employment who are - 4: administrative and secretarial occupations",
        "% females in employment who are - 5: skilled trades occupations",
        "% females in employment who are - 6: personal service occupations",
        "% females in employment who are - 7: sales and customer service occupations",
        "% females in employment who are - 8: process, plant and machine operatives",
        "% females in employment who are - 9: elementary occupations",
        "% of white - aged 16+", "% of ethnic minority - aged 16+"
    ]

    all_filtered_data = []

    for year in years:
        print(f"Fetching data for {year}...")
        params = {
            "time": str(year),
            "geography": "1946157341",  # Chichester
            "uid": api_key
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()

            df = pd.read_csv(StringIO(response.text))

            df_filtered = df[
                (df["VARIABLE_NAME"].isin(allowed_variables)) &
                (df["MEASURES_NAME"] == "Variable") &
                (df["DATE_NAME"] == f"Jan {year}-Dec {year}")
            ]

            if not df_filtered.empty:
                all_filtered_data.append(df_filtered)
                print(f"✓ {len(df_filtered)} rows added")
            else:
                print("⚠ No matching data for this year")

        except Exception as e:
            print(f"✗ Failed to fetch {year}: {e}")

    if all_filtered_data:
        combined_df = pd.concat(all_filtered_data, ignore_index=True)
        os.makedirs("data/raw", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"data/raw/{dataset_id}_chichester_2009-2024_{timestamp}.csv"
        combined_df.to_csv(output_file, index=False)
        print(f"\n✓ Saved {len(combined_df)} total rows to: {output_file}")
        return combined_df, output_file
    else:
        print("\n✗ No data matched across selected years.")
        return None, None

def main():
    DATASET_ID = "NM_17_5"
    API_KEY = "0x1d0f3b40c2f71f619de2a87922dd8ada9ea5d1c2"
    YEARS = list(range(2024, 2008, -1))  # From 2024 back to 2009

    print("Nomis Filtered Multi-Year Downloader (2009–2024)")
    print("=" * 50)

    df, filename = download_filtered_nomis_data(
        dataset_id=DATASET_ID,
        years=YEARS,
        api_key=API_KEY
    )

    if df is not None:
        print("\nFinal DataFrame Preview:")
        print(df.head())

if __name__ == "__main__":
    main()

