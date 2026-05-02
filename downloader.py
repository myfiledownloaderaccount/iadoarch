import internetarchive as ia
import json
import os
import subprocess
import random
from datetime import datetime

with open('config.json', 'r') as f:
    config = json.load(f)

target_folder = config.get("folder", "downloads")
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

history = json.load(open('history.json')) if os.path.exists('history.json') else []
log_entries = []

for col_id in config['collections']:
    search_term = config.get("search", "")
    query = f"collection:{col_id}"
    if search_term:
        query += f" AND ({search_term})"
        
    try:
        print(f"Searching: {query}")
        search = ia.search_items(query)
        items = [item['identifier'] for item in search]
        new_items = [i for i in items if i not in history]
        selected = random.sample(new_items, min(config.get('count', 1), len(new_items)))
        
        for identifier in selected:
            print(f"Downloading: {identifier}")
            ia.download(identifier, glob_pattern='*.mp4', destdir=target_folder)
            
            item_path = os.path.join(target_folder, identifier)
            if os.path.exists(item_path):
                for root, dirs, files in os.walk(item_path):
                    for file in files:
                        if file.endswith('.mp4'):
                            full_path = os.path.join(root, file)
                            if os.path.getsize(full_path) > 90 * 1024 * 1024:
                                subprocess.run(['split', '-b', '90M', full_path, f"{full_path}.part_"])
                                os.remove(full_path)
            
            history.append(identifier)
            log_entries.append(f"{datetime.now()}: Downloaded {identifier} from {col_id}")
            
    except Exception as e:
        log_entries.append(f"{datetime.now()}: Error in {col_id} - {str(e)}")

with open('history.json', 'w') as f:
    json.dump(history, f)

with open('download_log.txt', 'a') as f:
    for entry in log_entries:
        f.write(entry + "\n")
