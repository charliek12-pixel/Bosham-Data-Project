import requests
import pandas as pd
import time
from datetime import datetime
import os
import subprocess

def download_nomis_data(dataset_id="NM_17_5", start_year=2009, end_year=2024, api_key=None, delay=1):
    """
    Download Nomis data year by year and combine into a single CSV.
    
    Parameters:
    - dataset_id: Nomis dataset ID (default: "NM_17_5")
    - start_year: First year to download (default: 2009)
    - end_year: Last year to download (default: 2024) 
    - api_key: Your Nomis API key (optional, increases rate limits)
    - delay: Seconds to wait between requests (default: 1)
    """
    
    base_url = f"https://www.nomisweb.co.uk/api/v01/dataset/{dataset_id}.data.csv"
    all_data = []
    failed_years = []
    
    print(f"Downloading data for {dataset_id} from {start_year} to {end_year}")
    print(f"API Key provided: {'Yes' if api_key else 'No'}")
    print("-" * 50)
    
    for year in range(start_year, end_year + 1):
        try:
            # Build URL with parameters
            params = {"time": str(year)}
            if api_key:
                params["uid"] = api_key
            
            print(f"Downloading {year}... ", end="")
            
            # Make request
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            
            # Check if we got actual data (not just headers)
            if len(response.text.strip()) > 100:  # Assuming headers are less than 100 chars
                # Read CSV data
                from io import StringIO
                df = pd.read_csv(StringIO(response.text))
                
                if len(df) > 0:
                    all_data.append(df)
                    print(f"✓ ({len(df)} rows)")
                else:
                    print("✗ (No data)")
                    failed_years.append(year)
            else:
                print("✗ (Empty response)")
                failed_years.append(year)
                
        except requests.exceptions.RequestException as e:
            print(f"✗ (Request failed: {e})")
            failed_years.append(year)
        except pd.errors.EmptyDataError:
            print("✗ (No data returned)")
            failed_years.append(year)
        except Exception as e:
            print(f"✗ (Error: {e})")
            failed_years.append(year)
        
        # Be polite to the API
        time.sleep(delay)
    
    # Combine all data
    if all_data:
        print("-" * 50)
        print("Combining data...")
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Create data/raw directory if it doesn't exist
        os.makedirs("data/raw", exist_ok=True)
        
        # Create output filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"data/raw/{dataset_id}_data_{start_year}-{end_year}_{timestamp}.csv"
        
        # Save to CSV
        combined_df.to_csv(output_file, index=False)
        
        print(f"✓ Saved {len(combined_df)} total rows to: {output_file}")
        print(f"✓ Data covers {len(all_data)} years successfully downloaded")
        
        if failed_years:
            print(f"⚠ Failed to download: {failed_years}")
        
        # Git operations
        try:
            print("-" * 50)
            print("Pushing to GitHub...")
            
            # Add the file to git
            subprocess.run(["git", "add", output_file], check=True)
            
            # Commit with descriptive message
            commit_message = f"Add Nomis data {dataset_id} ({start_year}-{end_year}) - {len(combined_df)} rows"
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            
            # Push to GitHub
            subprocess.run(["git", "push"], check=True)
            
            print("✓ Successfully pushed to GitHub!")
            
        except subprocess.CalledProcessError as e:
            print(f"⚠ Git operation failed: {e}")
            print("File saved locally but not pushed to GitHub")
            print("You may need to manually commit and push, or check your git configuration")
        
        return combined_df, output_file
    else:
        print("✗ No data was successfully downloaded")
        return None, None

def main():
    """
    Main function - customize these parameters as needed
    """
    
    # Configuration - EDIT THESE VALUES
    DATASET_ID = "NM_17_5"  # Your dataset ID
    START_YEAR = 2009       # First year to download
    END_YEAR = 2024         # Last year to download
    API_KEY = None          # Your API key (get from https://www.nomisweb.co.uk/myaccount/userdefined.aspx)
    DELAY = 1               # Seconds between requests (be nice to the API!)
    
    # Uncomment and add your API key here if you have one:
    # API_KEY = "your_api_key_here"
    
    print("Nomis Data Downloader")
    print("=" * 50)
    
    # Download the data
    df, filename = download_nomis_data(
        dataset_id=DATASET_ID,
        start_year=START_YEAR, 
        end_year=END_YEAR,
        api_key=API_KEY,
        delay=DELAY
    )
    
    if df is not None:
        print("\nData summary:")
        print(f"Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        
        # Show first few rows
        print("\nFirst 5 rows:")
        print(df.head())
        
        # Show data by year if there's a date/time column
        if 'DATE' in df.columns:
            print(f"\nData count by year:")
            year_counts = df['DATE'].value_counts().sort_index()
            print(year_counts)
    
    print("\nDone!")

if __name__ == "__main__":
    main()


