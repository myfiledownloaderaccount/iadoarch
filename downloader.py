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

history = json.load(open('history.json')) if os.path.exists('history.json') else []

for col_id in config['collections']:
    print(f"Working on collection: {col_id}")
    
    try:
        search = ia.search_items(f"collection:{col_id}", limit=20)
        items = [item['identifier'] for item in search]
        print(f"Found {len(items)} items in {col_id}")
    except Exception as e:
        print(f"Search failed for {col_id}: {e}")
        continue
        
    selected = random.sample(items, min(config.get('count', 1), len(items)))
    
    for identifier in selected:
        if identifier in history:
            print(f"Skipping {identifier} (already in history)")
            continue
            
        print(f"Attempting download: {identifier}")
        try:
            ia.download(identifier, glob_pattern='*.mp4', destdir=target_folder, verbose=False)
            history.append(identifier)
            print(f"Successfully downloaded: {identifier}")
        except Exception as e:
            print(f"Failed to download {identifier}: {e}")

with open('history.json', 'w') as f:
    json.dump(history, f)
print("Finished.")
