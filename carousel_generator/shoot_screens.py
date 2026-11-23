import os, json, re, threading, http.server, socketserver, functools, datetime as dt, random, sys
from playwright.sync_api import sync_playwright
WWW=sys.argv[1]
OUT=sys.argv[2]
today=dt.date.today()
random.seed(4)
P1,P2="Aarav","Meera"
def d(n): return (today-dt.timedelta(days=n)).isoformat()
# month start (salary day 1)
tx=[];i=0
def add(amt,typ,m,cat,day,p,note=None):
    global i;i+=1
    tx.append(dict(id=f"t{i}",amount=amt,type=typ,merchant=m,merchant_key=re.sub(r'[^a-z0-9]+','-',m.lower()).strip('-'),category=cat,note=note,txn_date=day,person=p,hidden=False,created_at=day+"T10:00:00Z"))
ms=today.replace(day=1)
def md(k): 
    x=ms+dt.timedelta(days=k); 
    return min(x,today).isoformat()
for off,label in [(0,'cur'),(-1,'prev')]:
    base=ms if off==0 else (ms-dt.timedelta(days=1)).replace(day=1)
    def dd(k):
        x=base+dt.timedelta(days=k)
        return min(x,today).isoformat() if off==0 else x.isoformat()
    add(95000,'in',"Salary – Aarav","Salary / Income",dd(0),P1)
    add(72000,'in',"Salary – Meera","Salary / Income",dd(0),P2)
    rows=[("BigBasket",2850,"Groceries – Online",P2,2),("D-Mart",3400,"Groceries – Offline",P1,4),("Swiggy",620,"Food – Online delivery",P1,3),("Zomato",780,"Food – Online delivery",P2,6),
     ("Uber",340,"Transport",P2,5),("Indian Oil",2200,"Fuel",P1,7),("Netflix",649,"Subscriptions",P1,2),("Amazon",3150,"Shopping – Online",P2,8),("PVR Cinemas",1100,"Entertainment",P1,9),
     ("Apollo Pharmacy",940,"Health",P2,10),("Cafe Coffee Day",450,"Food – Dining out",P1,11),("Reliance Fresh",1800,"Groceries – Offline",P2,12),("Myntra",2400,"Shopping – Online",P2,13),("Ola",260,"Transport",P1,14),("Zepto",890,"Groceries – Online",P2,15)]
    for m,a,c,p,k in rows:
        if off==0 and k>(today-ms).days+1: continue
        add(a,'out',m,c,dd(k),p)
tx.sort(key=lambda t:t['txn_date'],reverse=True)
cm=ms.strftime("%Y-%m")
budgets=[dict(category=c,amount=a) for c,a in [("Groceries – Online",6000),("Groceries – Offline",7000),("Food – Online delivery",3000),("Food – Dining out",2500),("Transport",2000),("Fuel",3500),("Shopping – Online",5000),("Entertainment",2000),("Subscriptions",1500),("Health",2000)]]
fixed=[dict(id="f1",name="Home loan EMI",amount=28500,day=5,freq="monthly",month=None,category="Home loan EMI"),
 dict(id="f2",name="Kid school fees",amount=12000,day=10,freq="monthly",month=None,category="Kid education"),
 dict(id="f3",name="Maid",amount=3500,day=1,freq="monthly",month=None,category="Maid"),
 dict(id="f4",name="Electricity bill",amount=2400,day=15,freq="monthly",month=None,category="Electricity bill"),
 dict(id="f5",name="Car insurance",amount=18500,day=20,freq="yearly",month=3,category=None)]
due=(today+dt.timedelta(days=300)).isoformat()
goals=[dict(id="g1",name="Goa trip",target=60000,saved=24000,due=(today+dt.timedelta(days=150)).isoformat()),
 dict(id="g2",name="Emergency fund",target=300000,saved=120000,due=due),
 dict(id="g3",name="New car down payment",target=250000,saved=60000,due=(today+dt.timedelta(days=420)).isoformat())]
gents=[dict(id="e1",goal_id="g1",amount=6000,created_at=today.isoformat()+"T09:00:00Z"),dict(id="e2",goal_id="g2",amount=10000,created_at=today.isoformat()+"T09:00:00Z")]
members=[dict(user_id="u1",display_name=P1,role="owner"),dict(user_id="u2",display_name=P2,role="member")]
profile=dict(user_id="u1",role="owner",household_id="demo",display_name=P1,email="aarav@example.com",invite_code="GW4K9X",can_edit=True)
def mock(route):
    u=route.request.url
    def ok(b): route.fulfill(status=200,content_type="application/json",headers={"access-control-allow-origin":"*"},body=json.dumps(b))
    if "rpc/family_overview" in u: return ok(dict(members=[dict(user_id="u1",name=P1,email="aarav@example.com",role="owner",can_edit=True),dict(user_id="u2",name=P2,email="meera@example.com",role="member",can_edit=True)],invites=[]))
    if "rpc/my_profile" in u: return ok(profile)
    if "rpc/app_txns" in u: return ok(tx)
    if "/members" in u: return ok(members)
    if "/budgets" in u: return ok(budgets)
    if "/fixed_items" in u: return ok(fixed)
    if "/goal_entries" in u: return ok(gents)
    if "/goals" in u: return ok(goals)
    if "household_categories" in u: return ok([])
    return ok([])
class H(http.server.SimpleHTTPRequestHandler):
    def __init__(s,*a,**k): super().__init__(*a,directory=WWW,**k)
    def log_message(s,*a): pass
socketserver.TCPServer.allow_reuse_address=True
srv=socketserver.TCPServer(("127.0.0.1",8791),H);threading.Thread(target=srv.serve_forever,daemon=True).start()
tabs=sys.argv[3:] or ["home","home_family","plan","goals","fam","track","list","rep","rep_next","fixed"]
os.makedirs(OUT,exist_ok=True)
with sync_playwright() as p:
    import os
    try: b=p.chromium.launch(args=["--no-sandbox"])
    except Exception: b=p.chromium.launch(executable_path="/usr/bin/google-chrome",args=["--no-sandbox"])
    ctx=b.new_context(viewport={"width":390,"height":844},device_scale_factor=3,color_scheme="light")
    ctx.route(re.compile(r"supabase\.co"),mock)
    pg=ctx.new_page()
    pg.add_init_script("localStorage.setItem('sb',JSON.stringify({access:'x',refresh:'y',exp:9999999999,email:'aarav@example.com'}));localStorage.setItem('theme','light')")
    pg.goto("http://127.0.0.1:8791/index.html");pg.wait_for_timeout(2500)
    acts={
     "home":"S.tab='home';render()",
     "home_family":"S.pf='__both';S.tab='home';render()",
     "plan":"S.tab='plan';render()",
     "budget_top":"S.tab='plan';render()",
     "budget_cat":"S.tab='plan';render();window.scrollTo(0,0)",
     "fixed":"S.tab='plan';render();var h=[].slice.call(document.querySelectorAll('h2')).filter(function(x){return /Fixed/.test(x.textContent)})[0];h.scrollIntoView();window.scrollBy(0,-90)",
     "goals":"S.tab='goals';render()",
     "fam":"S.tab='fam';S.fam=null;loadFam().then(render);",
     "track":"S.tab='track';render()",
     "rep":"S.tab='rep';render()",
     "rep_next":"S.tab='rep';S.rp='next';render()",
     "list":"S.tab='list';render()",
    }
    for t in tabs:
        pg.evaluate(acts[t]);pg.wait_for_timeout(1200)
        pg.screenshot(path=f"{OUT}/{t}.png")
        print("shot",t)
    b.close()
