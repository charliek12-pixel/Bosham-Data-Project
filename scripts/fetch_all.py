from fetch_population import fetch_and_clean_population
from fetch_employment import fetch_and_clean_employment
from fetch_crime import fetch_and_clean_crime

if __name__ == "__main__":
    fetch_and_clean_population()
    fetch_and_clean_employment()
    fetch_and_clean_crime()
    print("🎉 All datasets updated.")
