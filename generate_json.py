import os
import json
import requests
from bs4 import BeautifulSoup

def get_game_name_and_icon_name(full_icon_name):
    # Example full_icon_name: Castle-of-Shikigami-2-icon001-%5B010061E018D3C000%5D.jpg
    parts = full_icon_name.split('-')
    
    # Extract game name and icon name
    game_name = ' '.join(parts[:-3])
    icon_name = '-'.join(parts[-3:-1])
    
    # Extract title id from square brackets
    title_id = full_icon_name.split('[')[-1].split(']')[0]
    
    return game_name, icon_name, title_id

def fetch_icons(base_url, subdirectories):
    icons_data = []

    for subdirectory in subdirectories:
        subdirectory_url = os.path.join(base_url, subdirectory)
        
        # Fetch HTML content of subdirectory page
        response = requests.get(subdirectory_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract all image links
        image_links = [img['src'] for img in soup.find_all('img') if img['src'].endswith('.jpg')]
        
        # Extract game name, icon name, and title id for each image
        for image_link in image_links:
            game_name, icon_name, title_id = get_game_name_and_icon_name(image_link)
            author = "sodasoba"
            icon_url = os.path.join(base_url, subdirectory, image_link)
            
            icon_data = {"name": icon_name, "url": icon_url, "author": author}
            
            # Check if the game entry already exists in icons_data
            existing_entry = next((entry for entry in icons_data if entry["name"] == game_name), None)
            
            if existing_entry:
                existing_entry["icons"].append(icon_data)
            else:
                game_entry = {"name": game_name, "normalIcon": icon_url, "icons": [icon_data]}
                icons_data.append(game_entry)

    return icons_data

def main():
    base_url = "https://raw.githubusercontent.com/sodasoba1/NSW-Custom-Game-Icons-square/main/Default/"
    subdirectories = ["0-9", "A", "Arcade-archive", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", 
                      "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    
    icons_data = fetch_icons(base_url, subdirectories)

    # Add authors data
    icons_data.append({"authors": [{"name": "sodasoba", "link": "https://www.steamgriddb.com/profile/76561199237351291"}]})
    
    # Create JSON file
    output_file_path = "output.json"
    with open(output_file_path, "w") as json_file:
        json.dump(icons_data, json_file, indent=2)

if __name__ == "__main__":
    main()
