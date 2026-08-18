# -*- coding: utf-8 -*-
"""Generate the project's brand graphics (banner, social preview, poster, PDF cover).

Authors SVG and rasterizes with cairosvg. One consistent identity:
deep indigo -> blue -> violet gradient, a 'semantic space' dot motif, and the pipeline.
"""
import os, random, math
import cairosvg

HERE = os.path.dirname(os.path.abspath(__file__))
random.seed(7)

def esc(t):
    return str(t).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

# ---- palette ----
INDIGO="#1E3A8A"; BLUE="#2563EB"; VIOLET="#7C3AED"
LIGHT="#BFDBFE"; MINT="#93C5FD"; WHITE="#FFFFFF"; INK="#0F172A"

def defs():
    return f'''
    <defs>
      <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0" stop-color="{INDIGO}"/>
        <stop offset="0.55" stop-color="{BLUE}"/>
        <stop offset="1" stop-color="{VIOLET}"/>
      </linearGradient>
      <radialGradient id="glow" cx="0.5" cy="0.5" r="0.5">
        <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.18"/>
        <stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
      </radialGradient>
    </defs>'''

def dot_cluster(cx, cy, spread, n, base_r=4, color=MINT, query=None):
    """Return SVG for a semantic-space cluster: dots + a highlighted query node with links."""
    pts=[]
    for _ in range(n):
        a=random.uniform(0,2*math.pi); r=abs(random.gauss(0,spread*0.5))
        pts.append((cx+r*math.cos(a), cy+r*math.sin(a)))
    s=""
    if query:
        qx,qy=query
        # nearest 4 links
        near=sorted(pts,key=lambda p:(p[0]-qx)**2+(p[1]-qy)**2)[:4]
        for (x,y) in near:
            s+=f'<line x1="{qx:.0f}" y1="{qy:.0f}" x2="{x:.0f}" y2="{y:.0f}" stroke="{WHITE}" stroke-opacity="0.5" stroke-width="2"/>'
    for (x,y) in pts:
        rr=base_r*random.uniform(0.6,1.6)
        s+=f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rr:.1f}" fill="{color}" fill-opacity="{random.uniform(0.5,0.95):.2f}"/>'
    if query:
        qx,qy=query
        s+=f'<circle cx="{qx:.0f}" cy="{qy:.0f}" r="11" fill="{WHITE}"/><circle cx="{qx:.0f}" cy="{qy:.0f}" r="19" fill="none" stroke="{WHITE}" stroke-opacity="0.7" stroke-width="2"/>'
    return s

def chip(x,y,w,h,label,fill="#FFFFFF",fillop="0.14",txt=WHITE,fs=26):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2:.0f}" fill="{fill}" fill-opacity="{fillop}" '
            f'stroke="{WHITE}" stroke-opacity="0.35"/>'
            f'<text x="{x+w/2:.0f}" y="{y+h/2+fs*0.35:.0f}" font-family="DejaVu Sans" font-weight="bold" '
            f'font-size="{fs}" fill="{txt}" text-anchor="middle">{esc(label)}</text>')

def render(svg, png_path, w, h, scale=2):
    cairosvg.svg2png(bytestring=svg.encode(), write_to=png_path,
                     output_width=int(w*scale), output_height=int(h*scale))
    print("wrote", os.path.relpath(png_path, HERE), f"{int(w*scale)}x{int(h*scale)}")

# =================== BANNER (1600x400) ===================
def banner():
    W,H=1600,400
    s=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{defs()}'
    s+=f'<rect width="{W}" height="{H}" rx="28" fill="url(#bg)"/>'
    s+=f'<rect width="{W}" height="{H}" rx="28" fill="url(#glow)"/>'
    # motif right
    s+=dot_cluster(1300,200,150,60,color=MINT,query=(1210,180))
    # text
    s+=f'<text x="80" y="150" font-family="DejaVu Sans" font-weight="bold" font-size="84" fill="{WHITE}">Search Semantically</text>'
    s+=f'<rect x="84" y="176" width="150" height="6" rx="3" fill="{MINT}"/>'
    s+=f'<text x="84" y="234" font-family="DejaVu Sans" font-size="34" fill="{LIGHT}">Large Language Models &amp; Semantic Search</text>'
    s+=f'<text x="84" y="286" font-family="DejaVu Sans" font-size="24" fill="#E0 E7FF">From keyword matching to embeddings, dense retrieval, re-ranking &amp; RAG</text>'.replace("E0 E7","E0E7")
    # pipeline chips
    labels=["Retrieve","Re-rank","Generate"]; x=84
    for i,l in enumerate(labels):
        s+=chip(x,318,150,46,l,fs=24); x+=170
        if i<len(labels)-1:
            s+=f'<text x="{x-34}" y="348" font-family="DejaVu Sans" font-size="30" fill="{WHITE}">&#8594;</text>'
    s+='</svg>'
    render(s, os.path.join(HERE,"banner.png"), W,H)

# =================== SOCIAL PREVIEW (1280x640) ===================
def social():
    W,H=1280,640
    s=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{defs()}'
    s+=f'<rect width="{W}" height="{H}" fill="url(#bg)"/>'
    s+=f'<rect width="{W}" height="{H}" fill="url(#glow)"/>'
    # faint scattered dots across
    s+=dot_cluster(220,150,180,40,base_r=3,color=WHITE)
    s+=dot_cluster(1150,430,120,28,base_r=3,color=WHITE)
    # center card
    s+=f'<text x="{W/2}" y="250" font-family="DejaVu Sans" font-weight="bold" font-size="96" fill="{WHITE}" text-anchor="middle">Search Semantically</text>'
    s+=f'<text x="{W/2}" y="312" font-family="DejaVu Sans" font-size="38" fill="{LIGHT}" text-anchor="middle">Large Language Models &amp; Semantic Search</text>'
    # pipeline chips centered
    labels=["Retrieve","Re-rank","Generate"]; cw=200; gap=70; total=len(labels)*cw+(len(labels)-1)*gap
    x=(W-total)/2; y=380
    for i,l in enumerate(labels):
        s+=chip(x,y,cw,58,l,fs=28); x+=cw
        if i<len(labels)-1:
            s+=f'<text x="{x+gap/2:.0f}" y="{y+40}" font-family="DejaVu Sans" font-size="40" fill="{WHITE}" text-anchor="middle">&#8594;</text>'; x+=gap
    s+=f'<text x="{W/2}" y="540" font-family="DejaVu Sans" font-weight="bold" font-size="30" fill="{MINT}" text-anchor="middle">14 chapters  •  runnable notebooks  •  free e-book  •  open-source</text>'
    s+='</svg>'
    render(s, os.path.join(HERE,"social-preview.png"), W,H)

# =================== POSTER (1600x2500) ===================
CHAPTERS=[
 ("0","Introduction"),("1","Foundations of IR"),("2","Keyword / Lexical Search"),
 ("3","From Text to Vectors"),("4","Embeddings Deep Dive"),("5","Dense Retrieval"),
 ("6","Vector Databases & ANN"),("7","Re-ranking"),("8","Hybrid Search"),
 ("9","Evaluating Search"),("10","RAG"),("11","Chunking & Pipelines"),
 ("12","Advanced Topics"),("13","Capstone Project"),
]
PARTS=[(0,"I","Foundations"),(2,"II","Classical Search"),(3,"III","The Vector Toolkit"),
 (5,"IV","Semantic Retrieval"),(7,"V","Better Results"),(9,"VI","Measuring Quality"),
 (10,"VII","Generation"),(12,"EXTRA","Mastery")]
def poster():
    W,H=1600,1640
    s=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{defs()}'
    s+=f'<rect width="{W}" height="{H}" fill="#F5F7FF"/>'
    # header band
    s+=f'<rect width="{W}" height="300" fill="url(#bg)"/>'
    s+=f'<rect width="{W}" height="300" fill="url(#glow)"/>'
    s+=dot_cluster(1380,150,120,45,color=MINT,query=(1300,130))
    s+=f'<text x="70" y="150" font-family="DejaVu Sans" font-weight="bold" font-size="76" fill="{WHITE}">Search Semantically</text>'
    s+=f'<text x="74" y="210" font-family="DejaVu Sans" font-size="34" fill="{LIGHT}">The learning path: from matching words to matching meaning</text>'
    s+=f'<text x="74" y="258" font-family="DejaVu Sans" font-size="26" fill="{MINT}">14 chapters  •  7 parts  •  runnable notebooks  •  free e-book</text>'
    # chapter cards, two columns
    top=360; cardw=690; cardh=118; gapx=40; gapy=26
    part_at={p[0]:p for p in PARTS}
    col_x=[70, 70+cardw+gapx]
    for i,(num,title) in enumerate(CHAPTERS):
        col=i%2; row=i//2
        x=col_x[col]; y=top+row*(cardh+gapy)
        # part label if a part starts at this chapter
        s+=f'<rect x="{x}" y="{y}" width="{cardw}" height="{cardh}" rx="18" fill="{WHITE}" stroke="#D6DEF5" stroke-width="2"/>'
        s+=f'<rect x="{x}" y="{y}" width="10" height="{cardh}" rx="5" fill="{BLUE}"/>'
        # number badge
        s+=f'<circle cx="{x+70}" cy="{y+cardh/2}" r="40" fill="url(#bg)"/>'
        s+=f'<text x="{x+70}" y="{y+cardh/2+14}" font-family="DejaVu Sans" font-weight="bold" font-size="40" fill="{WHITE}" text-anchor="middle">{num}</text>'
        s+=f'<text x="{x+135}" y="{y+cardh/2-2}" font-family="DejaVu Sans" font-weight="bold" font-size="34" fill="{INK}">{esc(title)}</text>'
        if num in part_at:
            _,roman,pname=part_at[num]
            s+=f'<text x="{x+135}" y="{y+cardh/2+34}" font-family="DejaVu Sans" font-size="24" fill="{VIOLET}">Part {esc(roman)} — {esc(pname)}</text>'
    # pipeline strip at bottom
    by=top+7*(cardh+gapy)+30
    s+=f'<rect x="70" y="{by}" width="{W-140}" height="150" rx="20" fill="url(#bg)"/>'
    s+=f'<text x="100" y="{by+52}" font-family="DejaVu Sans" font-weight="bold" font-size="30" fill="{WHITE}">The pipeline you build</text>'
    labels=["Query","Retrieve","Re-rank","Generate","Answer"]; x=100; y=by+95
    for i,l in enumerate(labels):
        w=200 if len(l)>6 else 150
        s+=chip(x,y,w,44,l,fs=22); x+=w
        if i<len(labels)-1:
            s+=f'<text x="{x+18}" y="{y+30}" font-family="DejaVu Sans" font-size="30" fill="{WHITE}">&#8594;</text>'; x+=52
    s+=f'<text x="{W/2}" y="{H-40}" font-family="DejaVu Sans" font-size="24" fill="#64748B" text-anchor="middle">© Dr. Mahdi Habibi  •  github.com/mdhabibi/llm-search-handbook  •  MIT + CC BY 4.0  •  v1.0.0</text>'
    s+='</svg>'
    render(s, os.path.join(HERE,"poster.png"), W,H, scale=1.5)

# =================== PDF COVER (A4 portrait) ===================
def pdf_cover():
    W,H=1654,2339  # ~A4 @200dpi
    s=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{defs()}'
    s+=f'<rect width="{W}" height="{H}" fill="url(#bg)"/>'
    s+=f'<rect width="{W}" height="{H}" fill="url(#glow)"/>'
    s+=dot_cluster(W/2,760,300,90,base_r=5,color=MINT,query=(W/2-120,700))
    s+=f'<rect x="{W/2-90}" y="960" width="180" height="8" rx="4" fill="{MINT}"/>'
    s+=f'<text x="{W/2}" y="1120" font-family="DejaVu Sans" font-weight="bold" font-size="132" fill="{WHITE}" text-anchor="middle">Search</text>'
    s+=f'<text x="{W/2}" y="1250" font-family="DejaVu Sans" font-weight="bold" font-size="132" fill="{WHITE}" text-anchor="middle">Semantically</text>'
    s+=f'<text x="{W/2}" y="1360" font-family="DejaVu Sans" font-size="52" fill="{LIGHT}" text-anchor="middle">Large Language Models &amp; Semantic Search</text>'
    s+=f'<text x="{W/2}" y="1440" font-family="DejaVu Sans" font-size="38" fill="{MINT}" text-anchor="middle">A beginner-to-expert, hands-on course</text>'
    # pipeline chips
    labels=["Retrieve","Re-rank","Generate"]; cw=300; gap=90; total=len(labels)*cw+(len(labels)-1)*gap
    x=(W-total)/2; y=1560
    for i,l in enumerate(labels):
        s+=chip(x,y,cw,80,l,fs=38); x+=cw
        if i<len(labels)-1:
            s+=f'<text x="{x+gap/2:.0f}" y="{y+56}" font-family="DejaVu Sans" font-size="52" fill="{WHITE}" text-anchor="middle">&#8594;</text>'; x+=gap
    s+=f'<text x="{W/2}" y="2120" font-family="DejaVu Sans" font-weight="bold" font-size="40" fill="{WHITE}" text-anchor="middle">14 chapters  •  runnable notebooks  •  open-source</text>'
    s+=f'<text x="{W/2}" y="2185" font-family="DejaVu Sans" font-size="34" fill="{LIGHT}" text-anchor="middle">Dr. Mahdi Habibi  ·  v1.0.0</text>'
    s+='</svg>'
    # PNG (preview) + PDF (for prepending to the ebook)
    render(s, os.path.join(HERE,"pdf-cover.png"), W,H, scale=1)
    cairosvg.svg2pdf(bytestring=s.encode(), write_to=os.path.join(HERE,"pdf-cover.pdf"))
    print("wrote pdf-cover.pdf")

if __name__=="__main__":
    banner(); social(); poster(); pdf_cover()
    print("all graphics generated")
