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

# CONTENT
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

# Build video
out_path = f"{OUT_DIR}/video_{d}.mp4"
subprocess.run(["ffmpeg", "-framerate", "1", "-i", f"{OUT_DIR}/frame_%04d.png", "-i", f"{p}/VOICE.mp3", "-c:v", "libx264", "-c:a", "aac", "-shortest", "-y", out_path], check=True)

print(f"✓ Video saved: {out_path}")
print(f"✓ Title: {t}")
print(f"✓ Ready to upload to YouTube manually")
