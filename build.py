import os, json, subprocess, datetime
from bot import topic, script, job

job()

d = datetime.date.today().isoformat()
p = f"output/{d}"

out_path = f"out/video_{d}.mp4"
os.makedirs("out", exist_ok=True)

subprocess.run(["ffmpeg", "-f", "lavfi", "-i", "color=c=black:s=1080x1920:d=60", "-i", f"{p}/VOICE.mp3", "-c:v", "libx264", "-c:a", "aac", "-y", out_path], check=True)

print(f"Made {out_path}")

import requests
REFRESH_TOKEN = os.getenv('YOUTUBE_REFRESH_TOKEN')
CLIENT_SECRET = os.getenv('YOUTUBE_CLIENT_SECRET')

print(f"Token exists: {bool(REFRESH_TOKEN)}")
print(f"Secret exists: {bool(CLIENT_SECRET)}")

if REFRESH_TOKEN and CLIENT_SECRET:
    try:
        with open(f"{p}/TITLE.txt") as f: title = f.read().strip()
        r = requests.post('https://oauth2.googleapis.com/token', data={
            'client_id': '1095280161816-e91th9rqian0qvc3qdsa0ulloefurpe5.apps.googleusercontent.com',
            'client_secret': CLIENT_SECRET,
            'refresh_token': REFRESH_TOKEN,
            'grant_type': 'refresh_token'
        })
        print(f"Token response: {r.json()}")
        access_token = r.json().get('access_token')
        if access_token:
            with open(out_path, 'rb') as f:
                r = requests.post('https://www.googleapis.com/upload/youtube/v3/videos?uploadType=multipart&part=snippet,status',
                    headers={'Authorization': f'Bearer {access_token}'},
                    json={'snippet': {'title': title, 'description': 'Daily tech', 'categoryId': '27'}, 'status': {'privacyStatus': 'unlisted'}},
                    files={'video': f})
                print(f"Upload: {r.status_code}")
    except Exception as e:
        print(f"Error: {e}")
else:
    print("No credentials found")
