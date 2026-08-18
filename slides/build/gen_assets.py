import os, random, math, cairosvg
A="/sessions/inspiring-eloquent-brown/mnt/outputs/slides_build/assets"
random.seed(11)
INDIGO="#1E3A8A"; BLUE="#2563EB"; VIOLET="#7C3AED"; LIGHT="#BFDBFE"; MINT="#93C5FD"; WHITE="#FFFFFF"; INK="#0F172A"; SLATE="#334155"
def defs():
    return (f'<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{INDIGO}"/><stop offset="0.55" stop-color="{BLUE}"/>'
            f'<stop offset="1" stop-color="{VIOLET}"/></linearGradient>'
            f'<radialGradient id="glow" cx="0.5" cy="0.4" r="0.6">'
            f'<stop offset="0" stop-color="#FFFFFF" stop-opacity="0.18"/>'
            f'<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient></defs>')
def dots(cx,cy,spread,n,base=5,color=MINT,query=None,op=(0.5,0.95)):
    pts=[]
    for _ in range(n):
        a=random.uniform(0,2*math.pi); r=abs(random.gauss(0,spread*0.5)); pts.append((cx+r*math.cos(a),cy+r*math.sin(a)))
    s=""
    if query:
        qx,qy=query
        for x,y in sorted(pts,key=lambda p:(p[0]-qx)**2+(p[1]-qy)**2)[:5]:
            s+=f'<line x1="{qx:.0f}" y1="{qy:.0f}" x2="{x:.0f}" y2="{y:.0f}" stroke="{WHITE}" stroke-opacity="0.45" stroke-width="2"/>'
    for x,y in pts:
        s+=f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{base*random.uniform(0.6,1.6):.1f}" fill="{color}" fill-opacity="{random.uniform(*op):.2f}"/>'
    if query:
        qx,qy=query; s+=f'<circle cx="{qx:.0f}" cy="{qy:.0f}" r="13" fill="{WHITE}"/><circle cx="{qx:.0f}" cy="{qy:.0f}" r="22" fill="none" stroke="{WHITE}" stroke-opacity="0.7" stroke-width="2"/>'
    return s
def out(svg,name,w,h):
    cairosvg.svg2png(bytestring=svg.encode(),write_to=os.path.join(A,name),output_width=w,output_height=h); print("wrote",name)

# --- title/closing background (dark) 2560x1440 ---
W,H=2560,1440
s=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{defs()}'
s+=f'<rect width="{W}" height="{H}" fill="url(#bg)"/><rect width="{W}" height="{H}" fill="url(#glow)"/>'
s+=dots(1950,470,360,120,base=6,query=(1780,410))
s+='</svg>'; out(s,"bg_title.png",W,H)

# --- content background (light, subtle corner motif) ---
s=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="{W}" height="{H}" fill="#FFFFFF"/>'
s+=dots(2360,150,180,34,base=5,color=BLUE,op=(0.05,0.14))
s+='</svg>'; out(s,"bg_content.png",W,H)

# --- inverted index diagram ---
w,h=1500,1020
def box(x,y,bw,bh,fill,txt,tcol=WHITE,fs=40,rx=16,bold=True):
    return (f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="{rx}" fill="{fill}"/>'
            f'<text x="{x+bw/2:.0f}" y="{y+bh/2+fs*0.35:.0f}" font-family="DejaVu Sans" font-weight="{"bold" if bold else "normal"}" font-size="{fs}" fill="{tcol}" text-anchor="middle">{txt}</text>')
s=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" fill="none"/>'
rows=[("grass","{D0}"),("blue","{D1, D4}"),("whale","{D4}"),("sky","{D1}")]
y=60
s+=f'<text x="40" y="40" font-family="DejaVu Sans" font-weight="bold" font-size="34" fill="{INK}">term</text>'
s+=f'<text x="640" y="40" font-family="DejaVu Sans" font-weight="bold" font-size="34" fill="{INK}">postings (docs containing it)</text>'
for term,post in rows:
    s+=box(40,y,360,120,BLUE,term,fs=44)
    s+=f'<line x1="410" y1="{y+60}" x2="620" y2="{y+60}" stroke="{SLATE}" stroke-width="6"/><polygon points="620,{y+48} 650,{y+60} 620,{y+72}" fill="{SLATE}"/>'
    s+=box(660,y,780,120,"#EEF3FF",post,tcol=INK,fs=42,rx=60)
    y+=200
s+='</svg>'; out(s,"diagram_index.png",w,h)

# --- pipeline diagram (query -> index+BM25 -> ranked results) ---
w,h=2000,430
s=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" fill="none"/>'
def pbox(x,txt,sub,fill,tcol=WHITE):
    bw,bh,y=520,220,100
    r=(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="26" fill="{fill}"/>'
       f'<text x="{x+bw/2:.0f}" y="{y+95}" font-family="DejaVu Sans" font-weight="bold" font-size="52" fill="{tcol}" text-anchor="middle">{txt}</text>'
       f'<text x="{x+bw/2:.0f}" y="{y+150}" font-family="DejaVu Sans" font-size="30" fill="{tcol}" text-anchor="middle" opacity="0.9">{sub}</text>')
    return r
s+=pbox(20,"Query","what color is the grass","#334155")
s+=pbox(740,"Match + score","inverted index + BM25",BLUE)
s+=pbox(1460,"Ranked results","most relevant first",VIOLET)
for x in (600,1320):
    s+=f'<line x1="{x}" y1="210" x2="{x+120}" y2="210" stroke="{SLATE}" stroke-width="8"/><polygon points="{x+120},195 {x+155},210 {x+120},225" fill="{SLATE}"/>'
s+='</svg>'; out(s,"diagram_pipeline.png",w,h)
print("assets done")
