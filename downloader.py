import internetarchive as ia
import json
import os
import subprocess
import random
import sys

ia.get_session().mount("https://", ia.requests.adapters.HTTPAdapter(max_retries=3))

with open('config.json', 'r') as f:
    config = json.load(f)

sys.stdout.reconfigure(line_buffering=True)

target_folder = config.get("folder", "downloads")
history = json.load(open('history.json')) if os.path.exists('history.json') else []

for col_id in config['collections']:
    print(f"DEBUG: Starting collection {col_id}")
    search = ia.search_items(f"collection:{col_id}", limit=50) 
    items = [item['identifier'] for item in search]
    
    selected = random.sample(items, min(config.get('count', 1), len(items)))
    
    for identifier in selected:
        if identifier in history: continue
        print(f"DEBUG: Attempting {identifier}")
        try:
            ia.download(identifier, glob_pattern='*.mp4', destdir=target_folder, verbose=False)
            history.append(identifier)
            print(f"DEBUG: Success {identifier}")
        except Exception as e:
            print(f"DEBUG: Error {identifier}: {e}")

with open('history.json', 'w') as f:
    json.dump(history, f)
