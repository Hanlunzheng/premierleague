import requests
import time
import pandas as pd
from bs4 import BeautifulSoup

# URL for Premier League Stats
BASE_URL = "https://fbref.com/en/comps/9/Premier-League-Stats"

# List to store all team stats
all_teams = []

# Fetch the main page
try:
    response = requests.get(BASE_URL)
    response.raise_for_status()  # Raise an error for failed requests
except requests.RequestException as e:
    print(f"Error fetching main page: {e}")
    exit()

# Parse the HTML
soup = BeautifulSoup(response.text, 'lxml')

# Extract tables with class 'stats_table'
tables = soup.find_all('table', class_='stats_table')
if not tables:
    print("No tables found on the page. Exiting...")
    exit()

# Find team links
links = [a.get("href") for a in tables[0].find_all('a') if a.get("href") and '/squads/' in a.get("href")]
team_urls = [f"https://fbref.com{link}" for link in links]

print(f"Found {len(team_urls)} teams. Scraping data...")

# Iterate over each team page
for idx, team_url in enumerate(team_urls, start=1):
    try:
        team_name = team_url.split("/")[-1].replace("-Stats", "")
        team_response = requests.get(team_url)
        team_response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {team_name}: {e}")
        continue

    # Parse the team's page
    team_soup = BeautifulSoup(team_response.text, 'lxml')
    team_tables = team_soup.find_all('table', class_='stats_table')

    if not team_tables:
        print(f"No stats table found for {team_name}. Skipping...")
        continue

    # Extract the first table (General team stats)
    try:
        team_data = pd.read_html(str(team_tables[0]))[0]
        if isinstance(team_data.columns, pd.MultiIndex):
            team_data.columns = team_data.columns.droplevel()  # Drop multi-index if present
        team_data["Team"] = team_name  # Add team name column
        all_teams.append(team_data)
        print(f"[{idx}/{len(team_urls)}] {team_name} data scraped successfully.")
    except Exception as e:
        print(f"Error processing data for {team_name}: {e}")

    time.sleep(3)  # Delay to prevent being blocked

# Save to CSV if data is collected
if all_teams:
    stat_df = pd.concat(all_teams, ignore_index=True)
    stat_df.to_csv("stats.csv", index=False)
    print("✅ Data saved to stats.csv")
else:
    print("❌ No data collected, CSV not created.")
