import internetarchive as ia
import json
import os
import random
import sys

sys.stdout.reconfigure(line_buffering=True)

print("Loading config...")
with open('config.json', 'r') as f:
    config = json.load(f)

target_folder = config.get("folder", "downloads")
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

history_path = 'history.json'
history = json.load(open(history_path)) if os.path.exists(history_path) else []

for col_id in config['collections']:
    print(f"Working on collection: {col_id}")
    
    try:
        search = ia.search_items(f"collection:{col_id}")
        
        items = [item['identifier'] for item in search][:200]
        
        print(f"Found {len(items)} items in {col_id}")
        
        new_items = [i for i in items if i not in history]
        if not new_items:
            print(f"No new items in {col_id}")
            continue
            
        selected = random.sample(new_items, min(config.get('count', 1), len(new_items)))
        
        for identifier in selected:
            print(f"Attempting download: {identifier}")
            ia.download(identifier, glob_pattern='*.mp4', destdir=target_folder, verbose=False)
            history.append(identifier)
            print(f"Successfully downloaded: {identifier}")
            
    except Exception as e:
        print(f"Search/Download failed for {col_id}: {str(e)}")

with open(history_path, 'w') as f:
    json.dump(history, f)

print("Finished.")
