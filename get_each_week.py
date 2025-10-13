from datetime import datetime
import requests
import json
import os

base_api_url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard"

def fetch_week_data(week: int):
    url = f"{base_api_url}?week={week}&seasontype=2&year=2025"
    response = requests.get(url)
    data = response.json()
    return data

def save_week_data(week: int, data: dict, directory="json_data"):
    os.makedirs(directory, exist_ok=True)

    file_path = os.path.join(directory, f"week{week}-espn-response.json")
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def main():
    directory = "data/json_data"
    if os.path.exists(directory):
        backup_dir = directory + datetime.now().strftime("%Y%m%d%H%M%S")
        print(f"Existing data directory found. Backing up to {backup_dir}...")
        os.rename(directory, backup_dir)

    for week in range(1, 19):
        print(f"Fetching data for week {week}...")
        week_data = fetch_week_data(week)
        save_week_data(week, week_data, directory)
        print(f"Data for week {week} saved.")

if __name__ == "__main__":
    main()