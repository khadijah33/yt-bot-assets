import json,os,random,datetime,time,threading
from http.server import BaseHTTPRequestHandler,HTTPServer
from gtts import gTTS
DB="db.json";OUT="output"
NICHES=["AI for Business","Fintech SaaS","Remote Work Tools","Side Hustle Tech","AI vs Human Jobs"]
HOOKS1=["Stop Using {} in 2026","The Best {} for UK/US/CA","How I Automated {} in 7 Days"]
HOOKS2=["{} vs {}: I Tested Both"]
BROLL=["office desk","laptop code","stock chart","AI brain"]
def db():return json.load(open(DB))if os.path.exists(DB)else{"u":[]}
def save(d):json.dump(d,open(DB,"w"))
def topic():
 d=db()
 if random.random()<0.5: t=random.choice(HOOKS1).format(random.choice(NICHES))
 else: n1,n2=random.sample(NICHES,2); t=random.choice(HOOKS2).format(n1,n2)
 if t in d["u"]:return topic()
 d["u"].append(t);save(d);return t
def script(t):return f"<speak><prosody rate=\"105%\">HOOK: {t}. <break time=\"400ms\"/> If you care about Business Tech in US UK CA MY, stay. <break time=\"300ms\"/> POINT 1: Why it matters now. POINT 2: Top 3 tools. POINT 3: How to start today. OUTRO: Subscribe.</prosody></speak>"
def job():
 t=topic();s=script(t);d=datetime.date.today().isoformat();p=f"{OUT}/{d}";os.makedirs(p,exist_ok=True)
 open(f"{p}/TITLE.txt","w").write(t);open(f"{p}/TAGS.txt","w").write("business,tech,ai,fintech,saas,uk,usa,canada,malaysia,side hustle")
 open(f"{p}/BROLL.txt","w").write("\n".join(random.sample(BROLL,4)))
 open(f"{p}/SCRIPT.ssml","w").write(s)
 gTTS(s,lang="en").save(f"{p}/VOICE.mp3")
 print(f"[OK] {d} | {t}")
def scheduler():
 while True:
  n=datetime.datetime.now()
  if n.hour==9 and n.minute==0:job();time.sleep(60)
  time.sleep(30)
class H(BaseHTTPRequestHandler):
 def _s(self,c,b):self.send_response(c);self.send_header("Content-type","text/plain");self.end_headers();self.wfile.write(b)
 def do_GET(self):self._s(200,b"Bot is running")
if __name__=="__main__":
 threading.Thread(target=scheduler,daemon=True).start()
 threading.Thread(target=lambda:HTTPServer(("0.0.0.0",5001),H).serve_forever(),daemon=True).start()
 print("* BOT LIVE 09:00 Lagos")
 while True:time.sleep(60)
