"""Static site generator: data/tools.json -> dist/. Run: python3 build.py"""
import json, os, re, html, shutil, datetime
SITE_NAME = os.environ.get("SITE_NAME", "AX Intel Tools")
SITE_URL = os.environ.get("SITE_URL", "https://tools.axi68.com").rstrip("/")
import config
LINKS = {k: os.environ.get(k) or getattr(config, k) for k in
         ["SQUARE_LINK_FEATURED", "SQUARE_LINK_BANNER", "SQUARE_LINK_EMAIL", "CONTACT_EMAIL", "SUBSCRIBE_FORM_ACTION"]}
SUB_URL = "https://americankx.com/page/#!/Intel-Individual/p/464053610"
BRIEF = "The Early Bird™ Intelligence Brief"
OUT = "dist"
e = html.escape
slug = lambda s: re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
FEAT = {l.strip() for l in open("data/featured.txt")} if os.path.exists("data/featured.txt") else set()
_t = json.load(open("data/tools.json"))
for t in _t: t["featured"] = t["name"] in FEAT
tools = sorted(_t, key=lambda t: (not t.get("featured"), t["name"].lower()))
cats = sorted({t["category"] for t in tools})
today = datetime.date.today().isoformat()

CSS = """*{box-sizing:border-box}body{margin:0;font:16px/1.55 system-ui,-apple-system,Segoe UI,Roboto,sans-serif;color:#1c2430;background:#f5f7fa}
a{color:#0b5cad}.promo{background:#0a1422;border-bottom:1px solid #22344d;text-align:center;font-size:.85rem;line-height:1.3;padding:7px 14px}.promo a{color:#dce6f2;text-decoration:none}.promo a:hover b{text-decoration:underline}.promo b{color:#f2b544;font-weight:600}.promo .s{display:none}@media(max-width:640px){.promo .l{display:none}.promo .s{display:inline}}header{background:#0f1c2e;color:#fff}header .w{display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:space-between;padding:14px 18px}
header a{color:#fff;text-decoration:none}.brand{font-weight:700;font-size:1.15rem;display:flex;align-items:center;gap:10px}.brand img{width:44px;height:44px;flex:none}.brand small{display:block;font-weight:400;font-size:.75rem;opacity:.7}
nav a{margin-left:16px;font-size:.95rem;opacity:.9}nav a:hover{opacity:1;text-decoration:underline}.w{max-width:1100px;margin:0 auto;padding:0 18px}
.hero{background:linear-gradient(135deg,#0f1c2e,#1d3b5f);color:#fff;padding:36px 0 30px}.hero h1{margin:0 0 8px;font-size:1.9rem}.hero p{margin:0;opacity:.85}
.banner{background:#fff8e1;border:1px dashed #d9a400;padding:12px;border-radius:8px;margin:18px 0;text-align:center;font-size:.9rem}
#q{width:100%;padding:13px 14px;font-size:1rem;border:1px solid #c9d2dc;border-radius:8px;margin:18px 0 10px}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:14px}.chip{border:1px solid #c9d2dc;background:#fff;border-radius:99px;padding:5px 12px;font-size:.85rem;cursor:pointer}
.chip.on{background:#0f1c2e;color:#fff;border-color:#0f1c2e}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px;padding-bottom:30px}
.card{background:#fff;border:1px solid #e1e6ec;border-radius:10px;padding:16px;display:flex;flex-direction:column}.card h3{margin:0 0 4px;font-size:1.05rem}
.card h3 a{text-decoration:none}.meta{font-size:.78rem;color:#5a6676;margin-bottom:8px}.tag{display:inline-block;padding:1px 8px;border-radius:99px;background:#eef2f7;margin-right:4px}
.free{background:#e3f6e8;color:#1b6b34}.paid{background:#fdeee3;color:#8a4b12}.card p{margin:0;font-size:.92rem}.feat{border:2px solid #d9a400}
footer{background:#0f1c2e;color:#aab6c5;font-size:.85rem;padding:24px 0;margin-top:20px}footer a{color:#dfe7f0}
.page{background:#fff;border:1px solid #e1e6ec;border-radius:10px;padding:24px;margin:24px 0}.price{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}
.price div{border:1px solid #e1e6ec;border-radius:10px;padding:18px}.price b{font-size:1.6rem;display:block}.btn{display:inline-block;background:#0b5cad;color:#fff!important;padding:10px 18px;border-radius:8px;text-decoration:none;margin-top:10px}
.cta{background:#0f1c2e;color:#fff;border-radius:10px;padding:18px;margin:18px 0}.cta a{color:#ffd65a}#count{font-size:.85rem;color:#5a6676}
input,textarea,select{width:100%;padding:10px;border:1px solid #c9d2dc;border-radius:6px;margin:4px 0 12px;font:inherit}
@media(max-width:640px){nav a{margin:0 12px 0 0}.hero h1{font-size:1.45rem}}"""

def layout(title, desc, path, body):
    canon = SITE_URL + "/" + path
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{canon}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="website">
<meta property="og:image" content="{SITE_URL}/og.png"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" type="image/png" href="/logo-64.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="stylesheet" href="/style.css"></head><body>
<div class="promo"><a href="{SUB_URL}" target="_blank" rel="noopener"><span class="l">{e(BRIEF)} — weekday intel, in your inbox before sunrise. <b>Subscribe →</b></span><span class="s">{e(BRIEF)} · <b>Subscribe</b></span></a></div>
<header><div class="w" style="max-width:1100px;margin:0 auto"><a class="brand" href="/" aria-label="{e(SITE_NAME)} home"><img src="/logo-64.png" srcset="/logo-64.png 1x, /logo-128.png 2x" width="44" height="44" alt="American Kinetix logo"><span>{e(SITE_NAME)}<small>An AX Global resource</small></span></a>
<nav><a href="/">Directory</a><a href="/submit/">Submit a Tool</a><a href="/advertise/">Advertise</a><a href="/subscribe/">Subscribe</a></nav></div></header>
{body}
<footer><div class="w">© {datetime.date.today().year} AX Global · {e(SITE_NAME)} · Listings are editorial; inclusion is not endorsement. Featured listings are marked.
· <a href="/advertise/">Advertise</a> · <a href="/subscribe/">{e(BRIEF)}</a></div></footer></body></html>"""

def card(t):
    p = t["pricing"].lower()
    return (f'<div class="card{" feat" if t.get("featured") else ""}" data-cat="{e(t["category"])}" data-s="{e((t["name"]+" "+t["note"]+" "+t["category"]).lower())}">'
            f'<h3><a href="{e(t["url"])}" target="_blank" rel="noopener">{e(t["name"])}</a></h3>'
            f'<div class="meta"><a class="tag" href="/category/{slug(t["category"])}/">{e(t["category"])}</a><span class="tag {p}">{e(t["pricing"])}</span></div>'
            f'<p>{e(t["note"])}</p>{"<div class=meta style=margin-top:8px>★ Featured</div>" if t.get("featured") else ""}</div>')

SUBCTA = f'<div class="cta"><b>Get the daily intel picture.</b> {e(BRIEF)} lands in your inbox every morning. <a href="/subscribe/">Subscribe →</a></div>'
BANNER = f'<div class="banner">Top banner slot available: reach OSINT and security practitioners. <a href="/advertise/">Advertise here ($199/mo)</a></div>'
JS = """<script>(function(){var q=document.getElementById('q'),cs=document.querySelectorAll('.chip'),cards=document.querySelectorAll('.card'),c=document.getElementById('count'),cat='';
function run(){var v=q.value.toLowerCase().trim(),n=0;cards.forEach(function(k){var ok=(!cat||k.dataset.cat===cat)&&(!v||v.split(/\\s+/).every(function(w){return k.dataset.s.indexOf(w)>-1}));k.style.display=ok?'':'none';if(ok)n++});c.textContent=n+' tools'}
q.addEventListener('input',run);cs.forEach(function(b){b.onclick=function(){cs.forEach(function(x){x.classList.remove('on')});b.classList.add('on');cat=b.dataset.cat;run()}});
var h=new URLSearchParams(location.search).get('q');if(h){q.value=h}run()})();</script>"""

def write(path, content):
    fp = os.path.join(OUT, path, "index.html") if not path.endswith((".xml", ".txt", ".css")) else os.path.join(OUT, path)
    os.makedirs(os.path.dirname(fp), exist_ok=True); open(fp, "w").write(content)

shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
for _f in ("logo-64.png","logo-128.png","favicon.ico","apple-touch-icon.png","og.png","icon-512.png"): shutil.copy(os.path.join(os.path.dirname(os.path.abspath(__file__)),"assets",_f), os.path.join(OUT,_f))
write("style.css", CSS)
chips = '<button class="chip on" data-cat="">All</button>' + "".join(f'<button class="chip" data-cat="{e(c)}">{e(c)}</button>' for c in cats)
home = (f'<section class="hero"><div class="w"><h1>The OSINT & Threat-Intel Tool Directory</h1><p>{len(tools)} vetted tools for open-source intelligence, threat intel, OPSEC and security training, each with a practitioner note.</p></div></section>'
        f'<main class="w">{BANNER}<input id="q" type="search" placeholder="Search tools, e.g. satellite, breach, ransomware, username" aria-label="Search tools">'
        f'<div class="chips">{chips}</div><div id="count"></div><div class="grid">{"".join(map(card, tools))}</div>{SUBCTA}</main>{JS}')
write("", layout(f"{SITE_NAME}: OSINT, Threat Intelligence & OPSEC Tools Directory",
                 f"Searchable directory of {len(tools)} OSINT, threat intelligence, OPSEC and security training tools with expert notes. Free and paid.", "", home))
for c in cats:
    ts = [t for t in tools if t["category"] == c]
    body = (f'<section class="hero"><div class="w"><h1>{e(c)} Tools</h1><p>{len(ts)} tools in this category. <a style="color:#ffd65a" href="/">Back to all tools</a></p></div></section>'
            f'<main class="w">{BANNER}<input id="q" type="search" placeholder="Search {e(c)}" aria-label="Search"><div class="chips" hidden><button class="chip on" data-cat=""></button></div>'
            f'<div id="count"></div><div class="grid">{"".join(map(card, ts))}</div>{SUBCTA}</main>{JS}')
    write(f"category/{slug(c)}", layout(f"Best {c} Tools ({len(ts)}) | {SITE_NAME}", f"Curated {c.lower()} tools for OSINT and security professionals: {', '.join(t['name'] for t in ts[:5])} and more.", f"category/{slug(c)}/", body))
L = LINKS
adv = f"""<main class="w"><div class="page"><h1>Advertise to OSINT & Security Practitioners</h1>
<p>{e(SITE_NAME)} is read by investigators, threat analysts, SOC teams and trainers looking for tools. Put your product in front of them.</p>
<div class="price"><div><h3>Featured Listing</h3><b>$49/mo</b>Highlighted card pinned at the top of your category, marked "Featured".<br><a class="btn" href="{L['SQUARE_LINK_FEATURED']}" target="_blank" rel="noopener">Subscribe monthly</a><small style="display:block;margin-top:6px;font-size:.8rem;color:#5a6676">At checkout, choose 'Subscription' for automatic monthly billing.</small></div>
<div><h3>Top Banner</h3><b>$199/mo</b>The single site-wide banner slot on every page. Only one sponsor at a time.<br><a class="btn" href="{L['SQUARE_LINK_BANNER']}" target="_blank" rel="noopener">Subscribe monthly</a><small style="display:block;margin-top:6px;font-size:.8rem;color:#5a6676">At checkout, choose 'Subscription' for automatic monthly billing.</small></div>
<div><h3>Weekly Email Mention</h3><b>$99</b>A sponsored mention in our weekly new-tools email.<br><a class="btn" href="{L['SQUARE_LINK_EMAIL']}" target="_blank" rel="noopener">Book a mention</a></div></div>
<p>After paying, email <a href="mailto:{L['CONTACT_EMAIL']}">{L['CONTACT_EMAIL']}</a> with your logo, link and copy. Sponsored placements are always labeled. We don't accept stalkerware or illegal-data vendors.</p></div></main>"""
write("advertise", layout(f"Advertise | {SITE_NAME}", "Sponsor the OSINT and threat-intel tools directory: featured listings $49/mo, top banner $199/mo, weekly email $99.", "advertise/", adv))
sub = f"""<main class="w"><div class="page"><h1>Suggest a Tool</h1><p>Know a tool that belongs here? Listing is free and editorial; we review every submission and write our own note. Vendors who want guaranteed placement can buy a <a href="/advertise/">featured listing</a>.</p>
<form action="mailto:{L['CONTACT_EMAIL']}?subject=Tool%20submission" method="post" enctype="text/plain">
<label>Tool name<input name="name" required></label><label>URL<input name="url" type="url" required></label>
<label>Category<select name="category">{"".join(f"<option>{e(c)}</option>" for c in cats)}</select></label>
<label>Free or paid<select name="pricing"><option>Free</option><option>Paid</option><option>Freemium</option></select></label>
<label>What does it do?<textarea name="description" rows="4"></textarea></label><label>Your email<input name="email" type="email"></label>
<button class="btn" type="submit">Submit</button></form></div></main>"""
write("submit", layout(f"Submit a Tool | {SITE_NAME}", "Suggest an OSINT, threat intelligence, OPSEC or security training tool for the directory.", "submit/", sub))
SIGNUP = (f'<form action="{L["SUBSCRIBE_FORM_ACTION"]}" method="post"><input type="email" name="email" placeholder="Your email address" required><button class="btn" type="submit">Join the weekly email</button></form>' if L["SUBSCRIBE_FORM_ACTION"] else f'<a class="btn" href="mailto:{L["CONTACT_EMAIL"]}?subject=Subscribe%20to%20the%20weekly%20new-tools%20email">Join the weekly email</a>')
subs = f"""<main class="w"><div class="page"><h1>{e(BRIEF)}</h1>
<p>A concise daily intelligence brief for people who need to know what happened overnight: security, threats and world events, delivered before your day starts.</p>
<div class="price"><div><h3>Annual subscription</h3><b>$107.50/yr</b>Delivered every morning by email.<br><a class="btn" href="{SUB_URL}" target="_blank" rel="noopener">Subscribe to {e(BRIEF)}</a></div></div>
<h2>Free weekly new-tools email</h2><p>Get the tools we added this week.</p>
{SIGNUP}</div></main>"""
write("subscribe", layout(f"Subscribe: {BRIEF} | {SITE_NAME}", f"Subscribe to {BRIEF}, a daily intelligence brief, for $107.50 per year.", "subscribe/", subs))
urls = ["", "advertise/", "submit/", "subscribe/"] + [f"category/{slug(c)}/" for c in cats]
write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + "".join(f"<url><loc>{SITE_URL}/{u}</loc><lastmod>{today}</lastmod></url>" for u in urls) + "</urlset>\n")
write("robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
print(f"Built {len(tools)} tools, {len(cats)} categories -> {OUT}/")
