"""Usage: python3 build_post.py <topic_id> <screens_dir> <out_dir>
Renders the slides of one topic (from topics.json) to 1080x1350 JPEGs."""
import sys,json,base64,os
from playwright.sync_api import sync_playwright
HERE=os.path.dirname(os.path.abspath(__file__))
tid,SCR,OUT=sys.argv[1],sys.argv[2],sys.argv[3]
topic=[t for t in json.load(open(HERE+'/topics.json')) if t['id']==tid][0]
logo=open(HERE+'/logo.svg').read().replace('id="bg"','id="lbg"').replace('url(#bg)','url(#lbg)').replace('id="glow"','id="lglow"').replace('url(#glow)','url(#lglow)')
def img(k): return "data:image/png;base64,"+base64.b64encode(open(f'{SCR}/{k}.png','rb').read()).decode()
CSS="""*{box-sizing:border-box;margin:0}
body{width:1080px;height:1350px;overflow:hidden;font-family:'Inter','Segoe UI',Roboto,Helvetica,Arial,sans-serif;position:relative;color:#fff;
background:radial-gradient(900px 700px at 15% 0%,#8b5cf6 0%,rgba(139,92,246,0) 60%),linear-gradient(160deg,#6d28d9 0%,#4c1d95 55%,#2e1065 100%)}
.top{position:absolute;left:80px;right:80px;top:70px;display:flex;justify-content:space-between;align-items:center}
.brand{display:flex;align-items:center;gap:16px;font-weight:800;font-size:34px}.brand svg{width:56px;height:56px}
.pill{background:rgba(255,255,255,.16);border-radius:40px;padding:10px 24px;font-size:26px;font-weight:700}
.step{position:absolute;left:80px;top:190px;font-size:28px;font-weight:700;letter-spacing:3px;color:#ddd1ff;text-transform:uppercase}
h1{position:absolute;left:80px;right:80px;top:238px;font-size:84px;line-height:1.04;font-weight:800;letter-spacing:-1.5px}
p.sub{position:absolute;left:80px;right:120px;top:476px;font-size:36px;line-height:1.3;color:#e6dcff;font-weight:500}
.phone{position:absolute;left:50%;top:700px;width:610px;margin-left:-305px;border:12px solid #140b2b;border-bottom:0;border-radius:78px 78px 0 0;overflow:hidden;background:#f6f5f1;box-shadow:0 30px 80px rgba(10,0,40,.55),0 0 0 3px rgba(255,255,255,.14)}
.phone img{display:block;width:100%}"""
N=len(topic['slides'])
def head(n): return f"<div class='top'><div class='brand'>{logo}Gharwise</div><div class='pill'>{n} / {N}</div></div>"
def build(n,s):
    t=s['type']
    if t=='cover':
        return head(n)+f"<div class='step'>{s['kicker']}</div><h1 style='font-size:{s.get('size',88)}px;top:260px;line-height:1.06'>{s['title']}</h1><p class='sub' style='top:{s.get('subtop',560)}px;font-size:44px'>{s['sub']}</p><div style='position:absolute;right:80px;bottom:70px;font-size:32px;font-weight:700;color:#ddd1ff'>Swipe →</div>"
    if t=='list':
        items=''.join(f"<div style='margin-bottom:34px'>{x}</div>" for x in s['items'])
        return head(n)+f"<div class='step'>{s['step']}</div><h1 style='font-size:88px;top:250px'>{s['title']}</h1><div style='position:absolute;left:80px;right:80px;top:600px;font-size:46px;line-height:1.45;font-weight:600'>{items}<div style='color:#c9b6ff'>{s.get('foot','')}</div></div>"
    if t=='shot':
        return head(n)+f"<div class='step'>{s['step']}</div><h1>{s['title']}</h1><p class='sub'>{s['sub']}</p><div class='phone'><img src='{img(s['screen'])}'></div>"
    if t=='cta':
        return head(n)+f"<div style='position:absolute;left:0;right:0;top:290px;text-align:center'><div style='width:220px;height:220px;margin:0 auto 50px;filter:drop-shadow(0 20px 40px rgba(0,0,0,.4))'>{logo}</div><div style='font-size:92px;font-weight:800;letter-spacing:-2px;line-height:1.05;padding:0 70px'>{s['title']}</div><div style='font-size:38px;color:#e6dcff;margin:40px 100px 0;line-height:1.35;font-weight:500'>{s['sub']}</div><div style='display:inline-block;margin-top:70px;background:#fff;color:#4c1d95;font-size:44px;font-weight:800;padding:28px 64px;border-radius:70px'>gharwise.net</div><div style='margin-top:50px;font-size:30px;color:#ddd1ff;font-weight:600'>{s['foot']}</div></div>"
os.makedirs(OUT,exist_ok=True)
with sync_playwright() as p:
    try: b=p.chromium.launch(args=["--no-sandbox"])
    except Exception: b=p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"])
    pg=b.new_page(viewport={"width":1080,"height":1350})
    for i,s in enumerate(topic['slides'],1):
        pg.set_content(f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{build(i,s)}</body></html>");pg.wait_for_timeout(300)
        f=f"{OUT}/slide{i}.png";pg.screenshot(path=f)
        from PIL import Image
        Image.open(f).convert('RGB').save(f"{OUT}/{topic['slug']}_slide{i}.jpg",quality=95);os.remove(f)
    b.close()
print(len(topic['slides']),"slides ->",OUT)
