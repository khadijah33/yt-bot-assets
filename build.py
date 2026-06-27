import os, json, subprocess, datetime
from bot import topic, script, job

# Use your existing bot system
job()

# Get the generated files
d = datetime.date.today().isoformat()
p = f"output/{d}"

# Read the audio and metadata
with open(f"{p}/VOICE.mp3", "rb") as audio:
    audio_data = audio.read()

out_path = f"out/video_{d}.mp4"
os.makedirs("out", exist_ok=True)

# Combine audio (you have) with simple video
subprocess.run(["ffmpeg", "-f", "lavfi", "-i", "color=c=black:s=1080x1920:d=600", "-i", f"{p}/VOICE.mp3", "-c:v", "libx264", "-c:a", "aac", "-y", out_path], check=True)

print(f"Made {out_path}")

# Upload
import requests, os
REFRESH_TOKEN = os.getenv('YOUTUBE_REFRESH_TOKEN')
if REFRESH_TOKEN:
    with open(f"{p}/TITLE.txt") as f: title = f.read().strip()
    r = requests.post('https://oauth2.googleapis.com/token', data={
        'client_id': '1095280161816-e91th9rqian0qvc3qdsa0ulloefurpe5.apps.googleusercontent.com',
        'client_secret': os.getenv('YOUTUBE_CLIENT_SECRET'),
        'refresh_token': REFRESH_TOKEN,
        'grant_type': 'refresh_token'
    })
    access_token = r.json().get('access_token')
    if access_token:
        with open(out_path, 'rb') as f:
            requests.post('https://www.googleapis.com/upload/youtube/v3/videos?uploadType=multipart&part=snippet,status',
                headers={'Authorization': f'Bearer {access_token}'},
                json={'snippet': {'title': title, 'description': 'Daily tech insights', 'categoryId': '27'}, 'status': {'privacyStatus': 'unlisted'}},
                files={'video': f})
