import internetarchive as ia
import json
import random
import os

MAX_SIZE_GB = 0.9  
config = {
    "collections": ["twitter-social-media-video", "facebook-social-video", "instagram-video-collection", "mirrortube", "reddit-social-media-video", "vice-video-mirror", "Arkive", "adultswimstreams", "odysee-social-media-video", "tiktoks"],
    "count_per_collection": 1,
    "download_dir": "downloads"
}

def get_dir_size(path):
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            total += os.path.getsize(os.path.join(dirpath, f))
    return total / (1024**3) 

history = json.load(open('history.json')) if os.path.exists('history.json') else []

if not os.path.exists(config['download_dir']):
    os.makedirs(config['download_dir'])

for col_id in config['collections']:
    if get_dir_size(config['download_dir']) > MAX_SIZE_GB:
        print("Limit reached. Stopping downloads.")
        break
        
    search = ia.search_items(f'collection:{col_id}')
    items = [item['identifier'] for item in search]
    new_items = [i for i in items if i not in history]
    
    selected = random.sample(new_items, min(config['count_per_collection'], len(new_items)))
    
    for identifier in selected:
        print(f"Downloading: {identifier}")
        ia.download(identifier, glob_pattern='*.mp4', destdir=config['download_dir'])
        history.append(identifier)

with open('history.json', 'w') as f:
    json.dump(history, f)
