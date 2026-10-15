"""Build data/tools.json from data/raw.txt (name|url|category|pricing|note), keeping only URLs that resolve."""
import json, sys, concurrent.futures as cf, urllib.request, ssl
UA={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/124 Safari/537.36"}
def check(url):
    for m in ("HEAD","GET"):
        try:
            r=urllib.request.urlopen(urllib.request.Request(url,headers=UA,method=m),timeout=20)
            return r.status
        except urllib.error.HTTPError as e:
            if e.code in (401,403,405,429,503) and m=="GET": return e.code  # alive, bot-blocked
            if m=="GET": return e.code
        except Exception as e:
            if m=="GET": return str(e)[:60]
rows=[l.rstrip("\n").split("|",4) for l in open("data/raw.txt") if l.strip()]
with cf.ThreadPoolExecutor(32) as ex: res=list(ex.map(lambda r: check(r[1]), rows))
keep,dead=[],[]
for r,s in zip(rows,res):
    ok = isinstance(s,int) and (s<400 or s in (401,403,405,429,503))
    (keep if ok else dead).append(r if ok else (r[0],r[1],s))
    
tools=[dict(name=r[0],url=r[1],category=r[2],pricing=r[3],note=r[4]) for r in keep]
json.dump(tools,open("data/tools.json","w"),indent=1,ensure_ascii=False)
print("kept",len(tools),"dead",len(dead)); [print("DEAD",*d) for d in dead]
