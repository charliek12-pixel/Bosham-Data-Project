import requests
import pandas as pd

# Example: Get employment data
url = "https://www.nomisweb.co.uk/api/v01/dataset/NM_17_5.csv"
params = {
    'geography': 'E07000226',  # Chichester
    'date': 'latest',
    'variable': '45',  # Employment rate
    'measures': '20599'  # Percentage
}

response = requests.get(url, params=params)
df = pd.read_csv(StringIO(response.text))
print(df)


