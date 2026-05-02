import internetarchive as ia
import json
import os
import subprocess

with open('config.json', 'r') as f:
    config = json.load(f)

target_folder = config.get("folder", "downloads")
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

history = json.load(open('history.json')) if os.path.exists('history.json') else []

for col_id in config['collections']:
    query = f"collection:{col_id} AND ({config.get('search', 'archive')})"
    items = [item['identifier'] for item in ia.search_items(query)]
    
    import random
    selected = random.sample([i for i in items if i not in history], min(config['count'], len(items)))
    
    for identifier in selected:
        print(f"Processing: {identifier}")
        ia.download(identifier, glob_pattern='*.mp4', destdir=target_folder)
        
        item_path = os.path.join(target_folder, identifier)
        for root, dirs, files in os.walk(item_path):
            for file in files:
                if file.endswith('.mp4'):
                    full_path = os.path.join(root, file)
                    if os.path.getsize(full_path) > 90 * 1024 * 1024:
                        print(f"Splitting {file}...")
                        subprocess.run(['split', '-b', '90M', full_path, f"{full_path}.part_"])
                        os.remove(full_path)
        
        history.append(identifier)

with open('history.json', 'w') as f:
    json.dump(history, f)
