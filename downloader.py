import internetarchive as ia
import json
import os
import subprocess
import random

with open('config.json', 'r') as f:
    config = json.load(f)

target_folder = config.get("folder", "downloads")
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

history = json.load(open('history.json')) if os.path.exists('history.json') else []

for col_id in config['collections']:
    print(f"--- Processing Collection: {col_id} ---")
    query = f"collection:{col_id} AND ({config.get('search', 'video')})"
    try:
        search = ia.search_items(query)
        items = [item['identifier'] for item in search]
        new_items = [i for i in items if i not in history]
        selected = random.sample(new_items, min(config.get('count', 1), len(new_items)))
    except Exception as e:
        print(f"Error searching collection {col_id}: {e}")
        continue
    
    for identifier in selected:
        print(f"Attempting to download: {identifier}")
        try:
            ia.download(identifier, glob_pattern='*.mp4', destdir=target_folder, verbose=True)
            
            item_path = os.path.join(target_folder, identifier)
            if os.path.exists(item_path):
                for file in os.listdir(item_path):
                    if file.endswith('.mp4'):
                        full_path = os.path.join(item_path, file)
                        if os.path.getsize(full_path) > 90 * 1024 * 1024:
                            print(f"Splitting {file}...")
                            subprocess.run(['split', '-b', '90M', full_path, f"{full_path}.part_"])
                            os.remove(full_path)
            
            history.append(identifier)
        except Exception as e:
            print(f"Failed to download {identifier}: {e}. Skipping...")
            continue

with open('history.json', 'w') as f:
    json.dump(history, f)
