import requests
import pandas as pd

# Base URL (DOGE Grants API)
base_url = "https://api.doge.gov/savings/grants"
headers = {"accept": "application/json"}

all_grants = []
page = 1
per_page = 100

print("Fetching all grant data...")

while True:
    # Fetch one page at a time
    url = f"{base_url}?sort_by=date&sort_order=desc&page={page}&per_page={per_page}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        break

    data = response.json()

    # Extract grants from this page
    grants = data.get("result", {}).get("grants", [])
    if not grants:
        break  # stop if no more pages

    all_grants.extend(grants)
    print(f"Page {page} fetched with {len(grants)} records.")
    page += 1

# Convert all pages into a single DataFrame
df = pd.DataFrame(all_grants)

print("\n📊 Full Grants Data:")
print(df.head())

# Ensure date is in datetime format
df['date'] = pd.to_datetime(df['date'], errors='coerce')

# Extract year and month for grouping
df['Year'] = df['date'].dt.year
df['Month'] = df['date'].dt.month

# Some entries might not have savings — drop NAs
if 'savings' in df.columns:
    df['savings'] = pd.to_numeric(df['savings'], errors='coerce')
else:
    raise KeyError("No 'savings' column found in the API data. Check field names.")

# Summarize savings by Year and Month
summary = (
    df.groupby(['Year', 'Month'])['savings']
    .sum()
    .reset_index()
    .sort_values(['Year', 'Month'])
)

print("\n💰 Monthly Savings Summary:")
print(summary)

# Optionally save to CSV
df.to_csv("doge_grants_full.csv", index=False)
summary.to_csv("doge_grants_summary.csv", index=False)

print("\n Data saved as:")
print(" - doge_grants_full.csv")
print(" - doge_grants_summary.csv")
