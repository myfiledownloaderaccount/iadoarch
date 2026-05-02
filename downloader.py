import requests
import json
import os
import random
import sys
import subprocess

sys.stdout.reconfigure(line_buffering=True)

with open('config.json', 'r') as f:
    config = json.load(f)

target_folder = config.get("folder", "downloads")
if not os.path.exists(target_folder):
    os.makedirs(target_folder)

history = json.load(open('history.json')) if os.path.exists('history.json') else []

for col_id in config['collections']:
    print(f"Fetching {col_id}...")
    url = f"https://archive.org/advancedsearch.php?q=collection:{col_id}&fl[]=identifier&rows=20&page=1&output=json"
    ids = [d['identifier'] for d in requests.get(url).json()['response']['docs'] if d['identifier'] not in history]
    
    selected = random.sample(ids, min(config.get('count', 1), len(ids)))
    
    for identifier in selected:
        print(f"Downloading {identifier}...")
        cmd = [
            'curl', '-L', '--max-time', '60', 
            f'https://archive.org/download/{identifier}/{identifier}.mp4', 
            '-o', os.path.join(target_folder, f"{identifier}.mp4")
        ]
        res = subprocess.run(cmd)
        
        if res.returncode == 0:
            history.append(identifier)
            print(f"Done: {identifier}")
        else:
            print(f"Failed to download {identifier}")

with open('history.json', 'w') as f:
    json.dump(history, f)
