"""Help AG – Session Security carousel slides  (two-pass vertical centering)."""

from PIL import Image, ImageDraw, ImageFont
import os

W, H   = 1080, 1350
CREAM  = (250, 245, 238)
RED    = (212,  43,  47)
NAVY   = ( 27,  43,  91)
WHITE  = (255, 255, 255)
LTRED  = (240, 216, 218)
GRAY   = (140, 140, 160)

FB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

def f(sz, bold=True): return ImageFont.truetype(FB if bold else FR, sz)

# shared measurement draw (WxH so all rects/blobs won't crash on clip)
_M = ImageDraw.Draw(Image.new("RGB", (W*4, H*4), CREAM))

def tw(text, ft): b = _M.textbbox((0,0),text,font=ft); return b[2]-b[0]
def th(text, ft): b = _M.textbbox((0,0),text,font=ft); return b[3]-b[1]

# ── primitives ────────────────────────────────────────────
def rr(d,x1,y1,x2,y2,r,fill,outline=None,lw=0):
    d.rounded_rectangle([x1,y1,x2,y2],radius=r,fill=fill,
                         outline=outline,width=lw)

def _cx(d,y,text,ft,color):
    d.text(((W-tw(text,ft))//2,y),text,font=ft,fill=color)
    return y+th(text,ft)

def blob(d,cx,cy,r):
    d.ellipse([cx-r,cy-r,cx+r,cy+r],fill=RED)

# ── components (each returns new y) ──────────────────────
def c_gap(d,y,g): return y+g

def c_divider(d,y,w=90,color=RED):
    cx=W//2; rr(d,cx-w//2,y,cx+w//2,y+10,5,color); return y+10

def c_badge(d,y,text,bg=RED,fg=WHITE):
    ft=f(28); pw,ph=44,16
    bw=tw(text,ft)+pw*2; bh=th(text,ft)+ph*2
    x1=(W-bw)//2
    rr(d,x1,y,x1+bw,y+bh,bh//2,bg)
    d.text((x1+pw,y+ph),text,font=ft,fill=fg)
    return y+bh

def c_logo(d,y):
    r=44; cx=W//2
    d.ellipse([cx-r,y,cx+r,y+2*r],fill=RED)
    fi=f(36); t="(i)"
    d.text((cx-tw(t,fi)//2,y+r-th(t,fi)//2),t,font=fi,fill=WHITE)
    y+=2*r+14
    f2=f(52)
    d.text(((W-tw("HELP AG",f2))//2,y),"HELP AG",font=f2,fill=NAVY)
    y+=th("HELP AG",f2)+8
    f3=f(24,False); s="an e& enterprise company"
    d.text(((W-tw(s,f3))//2,y),s,font=f3,fill=GRAY)
    return y+th(s,f3)

def c_strip(d,y,text,bg=RED):
    sh=90; lm=58
    rr(d,lm,y,W-lm,y+sh,18,bg)
    ft=f(32)
    d.text(((W-tw(text,ft))//2,y+(sh-th(text,ft))//2),text,font=ft,fill=WHITE)
    return y+sh

def _wrap(text,ft,max_w):
    words=text.split(); lines=[]; cur=[]
    for w in words:
        t2=" ".join(cur+[w])
        if tw(t2,ft)<=max_w: cur.append(w)
        else:
            if cur: lines.append(" ".join(cur))
            cur=[w]
    if cur: lines.append(" ".join(cur))
    return lines

def c_icon_card(d,y,num,text,lm=62,rm=62):
    ft=f(34); tx_lm=lm+108
    lines=_wrap(text,ft,W-rm-tx_lm-8)
    row_h=th(lines[0],ft); lh=row_h
    ch=max(116,len(lines)*lh+(len(lines)-1)*5+44)
    rr(d,lm,y,W-rm,y+ch,18,LTRED)
    rr(d,lm,y,lm+8,y+ch,4,RED)
    icx=lm+55; icy=y+ch//2; ir=26
    d.ellipse([icx-ir,icy-ir,icx+ir,icy+ir],fill=RED)
    fn=f(28)
    d.text((icx-tw(num,fn)//2,icy-th(num,fn)//2),num,font=fn,fill=WHITE)
    tot_h=len(lines)*lh+(len(lines)-1)*5
    ty=y+(ch-tot_h)//2
    for line in lines:
        d.text((tx_lm,ty),line,font=ft,fill=RED); ty+=lh+5
    return y+ch

def c_bullet_card(d,y,text,lm=62,rm=62):
    ft=f(34); tx_lm=lm+80
    lines=_wrap(text,ft,W-rm-tx_lm-8)
    lh=th(lines[0],ft)
    ch=max(110,len(lines)*lh+(len(lines)-1)*5+44)
    rr(d,lm,y,W-rm,y+ch,18,LTRED)
    rr(d,lm,y,lm+8,y+ch,4,RED)
    bx=lm+46; by=y+ch//2
    d.ellipse([bx-9,by-9,bx+9,by+9],fill=RED)
    tot_h=len(lines)*lh+(len(lines)-1)*5
    ty=y+(ch-tot_h)//2
    for line in lines:
        d.text((tx_lm,ty),line,font=ft,fill=RED); ty+=lh+5
    return y+ch

def c_stats(d,y):
    bh=158; lm=62; bw=(W-lm*2-20)//2
    for i,(num,lbl) in enumerate([("80%","of breaches involve stolen credentials"),
                                   ("207","avg. days to detect a breach")]):
        x1=lm+i*(bw+20); x2=x1+bw
        rr(d,x1,y,x2,y+bh,18,RED)
        fn=f(60); fl=f(22,False)
        ny=y+14
        d.text(((x1+x2)//2-tw(num,fn)//2,ny),num,font=fn,fill=WHITE)
        ny+=th(num,fn)+8
        mw=bw-20
        for line in _wrap(lbl,fl,mw):
            d.text(((x1+x2)//2-tw(line,fl)//2,ny),line,font=fl,fill=WHITE)
            ny+=th(line,fl)+3
    return y+bh

def c_tri(d,y):
    for cx in [W//2-195,W//2,W//2+195]:
        s=42; pts=[(cx,y),(cx-s,y+s*2+10),(cx+s,y+s*2+10)]
        d.polygon(pts,fill=RED)
        fi=f(32)
        d.text((cx-tw("!",fi)//2,y+s-10),"!",font=fi,fill=WHITE)
    return y+s*2+10+20

# ── two-pass helper ───────────────────────────────────────
def make_slide(blobs_fn, content_fn, top_pad=80, bot_pad=80):
    """Measure content height, then render centered."""
    # measure
    actual_h = content_fn(_M, 0) - 0
    y0 = max(top_pad, (H-actual_h-top_pad-bot_pad)//2 + top_pad)
    # render
    img=Image.new("RGB",(W,H),CREAM)
    d=ImageDraw.Draw(img)
    blobs_fn(d)
    content_fn(d, y0)
    return img

GAP = 16   # gap between cards
LGP = 28   # larger gap

OUT="/home/user/Book/slides"
os.makedirs(OUT,exist_ok=True)

# ═══════════════════════════════════════════════════════════
# S1 – COVER  (logo pinned top, text centered in middle zone)
# ═══════════════════════════════════════════════════════════
def s1_blobs(d):
    blob(d,W+195,-195,380); blob(d,W+150,H+145,320); blob(d,-55,H+85,290)

def s1_content(d,y0):
    # logo at top
    ly=c_logo(d,y0)
    # measure middle block
    fA=f(86); fB=f(72)
    text_block_h=(th("You're already",fA)+10+th("logged in…",fA)+26
                  +th("…but is it",fB)+10+th("really you?",fB))
    zone_top=ly+30; zone_bot=H-92-50
    ty=zone_top+(zone_bot-zone_top-text_block_h)//2
    for line in ["You're already","logged in…"]:
        ty=_cx(d,ty,line,fA,RED)+10
    ty+=16
    _cx(d,ty,"…but is it",fB,NAVY); ty+=th("…but is it",fB)+10
    _cx(d,ty,"really you?",fB,RED)
    c_strip(d,H-92-44,"  Session hijacking is silent")
    return H  # fixed layout

img=make_slide(s1_blobs, s1_content, top_pad=80, bot_pad=80)
img.save(f"{OUT}/slide_01_cover.png"); print("✓ slide 1")

# ═══════════════════════════════════════════════════════════
# S2 – THE PROBLEM
# ═══════════════════════════════════════════════════════════
def s2_blobs(d): blob(d,-185,-185,355); blob(d,W+165,H+155,335)

def s2_content(d,y):
    fC=f(56); fD=f(68)
    y=c_badge(d,y,"THE PROBLEM",bg=NAVY); y=c_gap(d,y,30)
    for i,line in enumerate(["You checked","your account."]):
        y=_cx(d,y,line,fC,RED); y=c_gap(d,y,8 if i==0 else 28)
    y=c_divider(d,y); y=c_gap(d,y,30)
    for i,(line,col) in enumerate([("Everything looks",RED),("normal.",NAVY)]):
        y=_cx(d,y,line,fD,col); y=c_gap(d,y,8 if i==0 else 28)
    y=_cx(d,y,"No alerts. No warnings.",fC,RED); y=c_gap(d,y,28)
    y=c_divider(d,y,w=60,color=NAVY); y=c_gap(d,y,30)
    for i,(line,col) in enumerate([("Just… activity you",RED),("don't remember.",NAVY)]):
        y=_cx(d,y,line,fD,col); y=c_gap(d,y,8 if i==0 else 0)
    return y

img=make_slide(s2_blobs,s2_content)
img.save(f"{OUT}/slide_02_problem.png"); print("✓ slide 2")

# ═══════════════════════════════════════════════════════════
# S3 – HOW IT HAPPENS
# ═══════════════════════════════════════════════════════════
def s3_blobs(d): blob(d,W+175,-175,345); blob(d,-165,H+165,345)

def s3_content(d,y):
    fE=f(62); fF=f(34,False)
    y=c_badge(d,y,"HOW IT HAPPENS",bg=RED); y=c_gap(d,y,LGP)
    for i,line in enumerate(["Not all threats force","their way in."]):
        y=_cx(d,y,line,fE,RED); y=c_gap(d,y,10 if i==0 else 14)
    y=_cx(d,y,"Some simply walk through an open door.",fF,NAVY); y=c_gap(d,y,LGP+4)
    for num,text in [("1","You forget to log out"),
                     ("2","Sessions stay active too long"),
                     ("3","Access goes unnoticed"),
                     ("4","Unsecured public networks")]:
        y=c_icon_card(d,y,num,text); y=c_gap(d,y,GAP)
    return y

img=make_slide(s3_blobs,s3_content)
img.save(f"{OUT}/slide_03_how.png"); print("✓ slide 3")

# ═══════════════════════════════════════════════════════════
# S4 – WHAT HAPPENS NEXT
# ═══════════════════════════════════════════════════════════
def s4_blobs(d): blob(d,-185,-185,345); blob(d,W+175,H+165,335)

def s4_content(d,y):
    fG=f(64)
    y=c_badge(d,y,"WHAT HAPPENS NEXT",bg=NAVY); y=c_gap(d,y,LGP)
    for i,(line,col) in enumerate([("It doesn't look wrong…",RED),("until it is.",NAVY)]):
        y=_cx(d,y,line,fG,col); y=c_gap(d,y,10 if i==0 else 14)
    y=c_divider(d,y); y=c_gap(d,y,LGP+4)
    for text in ["Changes you didn't make",
                 "Actions taken in your name",
                 "Information accessed without you knowing"]:
        y=c_bullet_card(d,y,text); y=c_gap(d,y,GAP)
    y=c_gap(d,y,14)
    y=c_tri(d,y)
    return y

img=make_slide(s4_blobs,s4_content)
img.save(f"{OUT}/slide_04_what.png"); print("✓ slide 4")

# ═══════════════════════════════════════════════════════════
# S5 – HOW TO STAY SAFE
# ═══════════════════════════════════════════════════════════
def s5_blobs(d): blob(d,W+175,-175,345); blob(d,-165,H+165,345)

def s5_content(d,y):
    fH=f(82)
    y=c_badge(d,y,"STAY PROTECTED",bg=NAVY); y=c_gap(d,y,LGP)
    for i,line in enumerate(["How to","Stay Safe"]):
        y=_cx(d,y,line,fH,RED); y=c_gap(d,y,8 if i==0 else LGP+4)
    for num,text in [("1","Log out from shared devices"),
                     ("2","Enable login alerts"),
                     ("3","Review active sessions regularly"),
                     ("4","Use multi-factor authentication")]:
        y=c_icon_card(d,y,num,text); y=c_gap(d,y,GAP)
    y=c_gap(d,y,14)
    y=c_strip(d,y,"  Your identity is your first firewall",bg=NAVY)
    return y

img=make_slide(s5_blobs,s5_content)
img.save(f"{OUT}/slide_05_safe.png"); print("✓ slide 5")

# ═══════════════════════════════════════════════════════════
# S6 – CLOSING CTA
# ═══════════════════════════════════════════════════════════
def s6_blobs(d): blob(d,-185,-185,345); blob(d,W+175,H+165,335)

def s6_content(d,y):
    fI=f(80); fJ=f(46); fK=f(26,False); fL=f(24,False)
    y=c_stats(d,y); y=c_gap(d,y,LGP)
    y=c_divider(d,y); y=c_gap(d,y,LGP+4)
    for i,line in enumerate(["Stay secure.","Stay aware."]):
        y=_cx(d,y,line,fI,RED); y=c_gap(d,y,10 if i==0 else 22)
    for i,line in enumerate(["Cybersecurity starts","with the right awareness."]):
        y=_cx(d,y,line,fJ,NAVY); y=c_gap(d,y,8 if i==0 else LGP+8)
    y=c_logo(d,y); y=c_gap(d,y,18)
    y=_cx(d,y,"Protecting digital identities across the region.",fK,GRAY)
    y=c_gap(d,y,12)
    y=_cx(d,y,"#CyberSecurity  ·  #DigitalSafety  ·  #StaySecure",fL,GRAY)
    return y

img=make_slide(s6_blobs,s6_content)
img.save(f"{OUT}/slide_06_cta.png"); print("✓ slide 6")

print(f"\nAll slides → {OUT}/")
