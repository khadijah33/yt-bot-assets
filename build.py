import os, subprocess, textwrap, datetime
from moviepy.editor import TextClip, CompositeVideoClip, ColorClip, AudioFileClip

OUT_DIR = "out"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. SCRIPT - Edit this daily or we can pull from ChatGPT later
title = f"Daily Video {datetime.date.today()}"
script = textwrap.dedent("""
    0-10s: Hook - Did you know?
    10-30s: Part 1 
    30-50s: Part 2
    50-60s: CTA - Follow for more
""")

W, H, FPS = 1080, 1920, 24
DURATION = 600 # 10 minutes total

# 2. VIDEO - Simple black background + text for now. We’ll add AI voice + stock footage next.
clips = []
for i in range(0, DURATION, 10):
    txt = TextClip(f"{title}\n{script[:40]}...", fontsize=70, color='white', size=(W-100, H), method='caption')
    txt = txt.set_duration(10
cat > build.py << 'EOF'
import os, textwrap, datetime
from moviepy.editor import TextClip, CompositeVideoClip, ColorClip

OUT_DIR = "out"
os.makedirs(OUT_DIR, exist_ok=True)

title = f"Daily Video {datetime.date.today()}"
script = textwrap.dedent("0-10s: Hook\n10-30s: Part 1\n30-50s: Part 2\n50-60s: CTA")

W, H, FPS = 1080, 1920, 24
DURATION = 600 

clips = []
for i in range(0, DURATION, 10):
    txt = TextClip(f"{title}\n{script[:40]}...", fontsize=70, color='white', size=(W-100, H), method='caption')
    txt = txt.set_duration(10).set_position('center')
    bg = ColorClip(size=(W,H), color=(0,0,0), duration=10)
    clips.append(CompositeVideoClip([bg, txt]))

video = CompositeVideoClip(clips, size=(W,H))
out_path = os.path.join(OUT_DIR, f"video_{datetime.date.today()}.mp4")
video.write_videofile(out_path, fps=FPS, codec="libx264", audio=False, logger=None)
print(f"Made {out_path}")
