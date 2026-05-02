import internetarchive as ia
import json
import os
import shutil

with open('config.json', 'r') as f:
    config = json.load(f)

search_query = config.get("search", "archive")
count = config.get("count", 1)
target_folder = config.get("folder", "downloads")

if not os.path.exists(target_folder):
    os.makedirs(target_folder)

history = json.load(open('history.json')) if os.path.exists('history.json') else []

for col_id in config['collections']:
    print(f"Searching for '{search_query}' in collection '{col_id}'...")
    query = f"collection:{col_id} AND ({search_query})"
    search = ia.search_items(query)
    
    items = [item['identifier'] for item in search]
    new_items = [i for i in items if i not in history]
    
    import random
    selected = random.sample(new_items, min(count, len(new_items)))
    
    for identifier in selected:
        print(f"Downloading {identifier} to {target_folder}...")
        ia.download(identifier, glob_pattern='*.mp4', destdir=target_folder)
        history.append(identifier)

with open('history.json', 'w') as f:
    json.dump(history, f)
