import requests
import internetarchive as ia
import json
import os
import random
import sys

sys.stdout.reconfigure(line_buffering=True)

with open('config.json', 'r') as f:
    config = json.load(f)

def get_items_from_collection(col_id):
    url = f"https://archive.org/advancedsearch.php?q=collection:{col_id}&fl[]=identifier&rows=50&page=1&output=json"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()
        return [doc['identifier'] for doc in data['response']['docs']]
    except:
        return []

target_folder = config.get("folder", "downloads")
history = json.load(open('history.json')) if os.path.exists('history.json') else []

for col_id in config['collections']:
    print(f"Fetching from collection: {col_id} via API...")
    items = get_items_from_collection(col_id)
    print(f"Found {len(items)} items.")
    
    new_items = [i for i in items if i not in history]
    selected = random.sample(new_items, min(config.get('count', 1), len(new_items)))
    
    for identifier in selected:
        print(f"Downloading: {identifier}")
        try:
            ia.download(identifier, glob_pattern='*.mp4', destdir=target_folder, verbose=False)
            history.append(identifier)
        except Exception as e:
            print(f"Download failed: {e}")

with open('history.json', 'w') as f:
    json.dump(history, f)
