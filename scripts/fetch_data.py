import pandas as pd
from datetime import datetime
import os

# Simulated data – later you’ll replace this with real data from APIs
data = {
    "Year": [2011, 2015, 2021, 2023],
    "Population": [3055, 3120, 3290, 3345]
}
df = pd.DataFrame(data)

# Create the folder if it doesn’t exist
os.makedirs("data/processed", exist_ok=True)

# Save CSV
df.to_csv("data/processed/population.csv", index=False)
print("✅ population.csv updated:", datetime.now())


