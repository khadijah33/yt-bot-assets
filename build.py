import os, json, subprocess, datetime, random
from PIL import Image, ImageDraw, ImageFont
from bot import db, topic, script

d = datetime.date.today().isoformat()
p = f"output/{d}"
os.makedirs(p, exist_ok=True)

t = topic()
s = script(t)

open(f"{p}/TITLE.txt", "w").write(t)
open(f"{p}/TAGS.txt", "w").write("business,tech,ai,fintech,saas,uk,usa,canada,side-hustle")
open(f"{p}/SCRIPT.ssml", "w").write(s)

from gtts import gTTS
gTTS(s, lang="en").save(f"{p}/VOICE.mp3")

COLORS = {'bg': (15, 15, 35), 'accent1': (100, 200, 255), 'accent2': (255, 150, 100), 'text': (255, 255, 255), 'highlight': (255, 200, 100)}
W, H = 1920, 1080
OUT_DIR = "out"
os.makedirs(OUT_DIR, exist_ok=True)

# HOOK
for i in range(30):
    img = Image.new('RGB', (W, H), color=COLORS['bg'])
    draw = ImageDraw.Draw(img)
    draw.rectangle([(0, 0), (W, 150)], fill=COLORS['accent1'])
    draw.text((W//2, H//2), t, fill=COLORS['highlight'], anchor="mm")
    img.save(f"{OUT_DIR}/frame_{i:04d}.png")

# CONTENT (10 sections)
frame_idx = 30
for sec_idx in range(10):
    for slide in range(56):
        img = Image.new('RGB', (W, H), color=COLORS['bg'])
        draw = ImageDraw.Draw(img)
        draw.rectangle([(0, 0), (W, 120)], fill=COLORS['accent1'])
        draw.text((W//2, H//2), f"Section {sec_idx+1}", fill=COLORS['highlight'], anchor="mm")
        img.save(f"{OUT_DIR}/frame_{frame_idx:04d}.png")
        frame_idx += 1

# CTA
for i in range(30):
    img = Image.new('RGB', (W, H), color=COLORS['bg'])
    draw = ImageDraw.Draw(img)
    draw.text((W//2, H//2), "Subscribe", fill=COLORS['highlight'], anchor="mm")
    img.save(f"{OUT_DIR}/frame_{frame_idx:04d}.png")
    frame_idx += 1

# Video
out_path = f"{OUT_DIR}/video_{d}.mp4"
subprocess.run(["ffmpeg", "-framerate", "1", "-i", f"{OUT_DIR}/frame_%04d.png", "-i", f"{p}/VOICE.mp3", "-c:v", "libx264", "-c:a", "aac", "-shortest", "-y", out_path], check=True)

print(f"✓ Video: {out_path}")

# YouTube Upload
import requests
REFRESH_TOKEN = os.getenv('YOUTUBE_REFRESH_TOKEN')
CLIENT_SECRET = os.getenv('YOUTUBE_CLIENT_SECRET')
CLIENT_ID = '1095280161816-e91th9rqian0qvc3qdsa0ulloefurpe5.apps.googleusercontent.com'

print(f"Token: {REFRESH_TOKEN[:20]}..." if REFRESH_TOKEN else "NO TOKEN")
print(f"Secret: {CLIENT_SECRET[:20]}..." if CLIENT_SECRET else "NO SECRET")

if REFRESH_TOKEN and CLIENT_SECRET:
    try:
        # Get access token
        r = requests.post('https://oauth2.googleapis.com/token', data={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'refresh_token': REFRESH_TOKEN,
            'grant_type': 'refresh_token'
        })
        print(f"Token request status: {r.status_code}")
        token_data = r.json()
        print(f"Token response: {token_data}")
        
        access_token = token_data.get('access_token')
        if access_token:
            print(f"✓ Got access token")
            with open(out_path, 'rb') as video:
                r = requests.post('https://www.googleapis.com/upload/youtube/v3/videos?uploadType=multipart&part=snippet,status',
                    headers={'Authorization': f'Bearer {access_token}'},
                    json={'snippet': {'title': t, 'description': t, 'tags': ['business', 'tech'], 'categoryId': '27'}, 'status': {'privacyStatus': 'public'}},
                    files={'video': video})
            print(f"✓ Upload status: {r.status_code}")
            print(f"Upload response: {r.text[:200]}")
        else:
            print(f"✗ No access token: {token_data}")
    except Exception as e:
        print(f"✗ Error: {e}")
else:
    print("✗ Missing credentials")
