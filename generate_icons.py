import os
import requests
from bs4 import BeautifulSoup
import json

github_url = "https://github.com/sodasoba1/NSW-Custom-Game-Icons-square/tree/main/Default"
raw_github_url = "https://raw.githubusercontent.com/sodasoba1/NSW-Custom-Game-Icons-square/main/Default"

# Function to get subdirectories with icons
def get_subdirectories_with_icons():
    response = requests.get(github_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    subdirectories = [a['href'] for a in soup.find_all('a', href=True) if a.text and a.text not in ["..", "."]]

    return subdirectories

# Function to generate JSON data
def generate_json_data(subdirectories):
    data = {"games": [], "authors": [{"name": "sodasoba", "link": "https://www.steamgriddb.com/profile/76561199237351291"}]}

    for subdirectory in subdirectories:
        subdir_url = f"{raw_github_url}/{subdirectory}"
        icons = []

        # Get icons in the subdirectory
        icons_response = requests.get(subdir_url)
        icons_soup = BeautifulSoup(icons_response.text, 'html.parser')
        icon_files = [a['href'] for a in icons_soup.find_all('a', href=True) if a.text and a.text.endswith(".jpg")]

        for icon_file in icon_files:
            # Extract game name, icon name, and title id from the icon file name
            parts = icon_file.split('-')
            game_name = parts[0].replace("#", "").replace("-", " ").title()
            icon_name = parts[-2]
            title_id = parts[-1].split('[')[-1].split(']')[0]

            icon_url = f"{raw_github_url}/{subdirectory}/{icon_file}"
            icon_data = {"name": f"{icon_name}-{title_id}", "url": icon_url, "author": "sodasoba"}
            icons.append(icon_data)

        # Create game entry in the JSON data
        game_entry = {"name": game_name, "normalIcon": icons[0]["url"], "icons": icons}
        data["games"].append(game_entry)

    return data

# Write JSON data to a file
def write_json_file(data):
    with open('output.json', 'w') as json_file:
        json.dump(data, json_file, indent=2)

if __name__ == "__main__":
    subdirectories = get_subdirectories_with_icons()
    json_data = generate_json_data(subdirectories)
    write_json_file(json_data)
