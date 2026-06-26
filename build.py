import os, datetime
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = "out"
os.makedirs(OUT_DIR, exist_ok=True)

W, H, FPS = 1080, 1920, 1 # 1 fps is fine for slides
DURATION = 600 # 10 minutes = 600 seconds
SECONDS_PER_SLIDE = 1

img = Image.new('RGB', (W, H), color=(0,0,0))
draw = ImageDraw.Draw(img)
font = ImageFont.load_default()

for i in range(0, DURATION, SECONDS_PER_SLIDE):
    txt = f"Daily Video {datetime.date.today()}\nSlide {i//10 + 1}"
    draw.rectangle([(0,0),(W,H)], fill=(0,0,0))
    draw.text((W//2, H//2), txt, font=font, fill=(255,255,255), anchor="mm")
    img.save(f"{OUT_DIR}/frame_{i:04d}.png")

# Make video from images. No ImageMagick needed.
import subprocess
out_path = os.path.join(OUT_DIR, f"video_{datetime.date.today()}.mp4")
subprocess.run([
    "ffmpeg", "-framerate", "1", "-i", f"{OUT_DIR}/frame_%04d.png", 
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30", out_path
], check=True)
print(f"Made {out_path}")
