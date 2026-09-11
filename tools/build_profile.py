from pathlib import Path
from html import escape
import argparse

parser=argparse.ArgumentParser(description='Generate the original profile SVG artwork.')
parser.add_argument('--out',type=Path,default=Path(__file__).resolve().parents[1])
args=parser.parse_args(); ROOT=args.out
PALETTES={
 'light':dict(bg='#f4f2ea',panel='#eeeee6',ink='#20251e',muted='#535b4b',line='#bfc5b5',accent='#435c18'),
 'dark':dict(bg='#101310',panel='#171c17',ink='#f2f1e8',muted='#b3bbaa',line='#3e4938',accent='#d4e896')}

def text(x,y,value,size=28,fill=None,weight=400,anchor=None):
    return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}"'+(f' style="fill:{fill}"' if fill else '')+(f' text-anchor="{anchor}"' if anchor else '')+'>'+escape(value)+'</text>'
def line(x1,y1,x2,y2,color,width=2,extra=''):
    return f'<path d="M{x1} {y1}H{x2}" stroke="{color}" stroke-width="{width}" {extra}/>' if y1==y2 else f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{color}" stroke-width="{width}" {extra}/>'
def svg(path,w,h,p,title,desc,body,style=''):
    dest=ROOT/path;dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>
<style>text{{font-family:Arial,Helvetica,sans-serif;fill:{p['ink']}}}{style}</style>
<rect width="{w}" height="{h}" rx="10" fill="{p['bg']}"/>
{body}
</svg>''')
def gate(x,y,s,p):
    return f'<g transform="translate({x} {y}) scale({s})" fill="none" stroke="{p["accent"]}" stroke-width="2.5"><path d="M42 0V100 M62 0V100 M0 50H108"/><circle cx="108" cy="50" r="5" fill="{p["accent"]}" stroke="none"/></g>'

for theme,p in PALETTES.items():
    for mobile in [False,True]:
        suffix=('-mobile' if mobile else '')+'-'+theme
        w,h=(400,156) if mobile else (800,224)
        b=text(24 if mobile else 30,29 if mobile else 36,'AI PRODUCT BUILDER',18 if mobile else 26,p['muted'])
        b+=text(24 if mobile else 30,82 if mobile else 115,'AI that earns',40 if mobile else 64,weight=700)
        b+=text(24 if mobile else 30,130 if mobile else 188,'the next step.',40 if mobile else 64,weight=700)
        b+=gate(325 if mobile else 648,19 if mobile else 61,.46 if mobile else 1.24,p)
        svg(f'assets/profile/hero{suffix}.svg',w,h,p,'AI that earns the next step.','Abdulelah Alkhathami — AI Product Builder. A paired-line gate represents the boundary between a model request and an authorized action.',b)
        w,h=(400,184) if mobile else (800,222)
        b=text(22 if mobile else 30,29 if mobile else 37,'THE PERMISSION MOMENT',17 if mobile else 26,p['muted'])
        b+=text(22 if mobile else 30,69 if mobile else 91,'“Return my order.”',26 if mobile else 38,weight=700)
        y=111 if mobile else 143; a=35 if mobile else 42; z=366 if mobile else 752; gx=195 if mobile else 400
        b+=line(a,y,z,y,p['line'],3)
        b+=line(gx-7,y-22,gx-7,y+22,p['accent'],3)+line(gx+7,y-22,gx+7,y+22,p['accent'],3)
        b+=f'<circle cx="{a}" cy="{y}" r="6" fill="{p["accent"]}"/><circle cx="{z}" cy="{y}" r="6" fill="{p["accent"]}"/>'
        b+=f'<circle class="signal" cx="{z}" cy="{y}" r="7" fill="{p["accent"]}"/>'
        b+=text(22 if mobile else 30,153 if mobile else 192,'PROPOSE',18 if mobile else 28)
        b+=text(gx,153 if mobile else 192,'AUTHORIZE',18 if mobile else 28,anchor='middle')
        b+=text(376 if mobile else 768,153 if mobile else 192,'ACT',18 if mobile else 28,anchor='end')
        # Motion ends after one 4.6-second pass. Static fallback retains every label.
        distance=z-a; pause=z-gx
        style=f'.signal{{animation:pass 4.6s ease-in-out 1 both}}@keyframes pass{{0%{{transform:translateX(-{distance}px)}}35%,60%{{transform:translateX(-{pause}px)}}100%{{transform:translateX(0)}}}}@media(prefers-reduced-motion:reduce){{.signal{{animation:none}}}}'
        svg(f'assets/profile/permission{suffix}.svg',w,h,p,'The permission moment: propose, authorize, act.','Illustrative Raqmi return request. A signal pauses at an application-controlled authorization boundary before proceeding. Ownership and explicit return consent are required. This is a design illustration, not live execution.',b,style)
    p2=dict(p)
    p2['accent']='#8c442b' if theme=='light' else '#edb7a0'
    b=text(24,35,'DIFFERENT OWNER',18,p2['muted'])+text(24,77,'No permission. No action.',27,weight=700)
    b+=line(24,111,224,111,p2['line'],3)+line(230,92,230,130,p2['accent'],4)+line(240,92,240,130,p2['accent'],4)
    b+=text(270,119,'DENIED',20,p2['accent'],700)
    svg(f'assets/profile/denied-{theme}.svg',400,150,p2,'Different owner: denied. No return is created.','Illustrative ownership denial. The model request cannot grant access to someone else’s order.',b)

PROJECTS=[
 ('raqmi','Raqmi','AGENTIC AI','Retail support, with bounded actions.','Arabic retail support.','Tools with boundaries.','#435c18','#d4e896'),
 ('portfolio','Abdulelah.de','AI PRODUCT / WEB','A bilingual portfolio you can ask.','A bilingual portfolio','you can ask.','#54519d','#b4b8f5'),
 ('chatub','ChatUB','LOCAL AI / PROTOTYPE','Arabic FAQs. Local AI assistance.','Arabic FAQ retrieval.','Local AI assistance.','#8c4a25','#e4b899'),
 ('absher-insight','Absher Insight','SECURITY / PROTOTYPE','Synthetic signals. Visible decisions.','Synthetic signals.','Visible decisions.','#206674','#99cbd3'),
 ('stadium','Stadium','COMPUTER VISION','From camera frames to gate counts.','From camera frames','to gate counts.','#86436b','#dba6c9')]

def motif(kind,x,y,s,color):
    top=f'<g transform="translate({x} {y}) scale({s})" stroke="{color}" stroke-width="2.4" fill="none">'
    if kind=='raqmi': body='<path d="M30 0V104 M54 0V104 M0 52H108 M90 36L106 52 90 68"/>'
    elif kind=='portfolio':body='<path d="M6 18H72V69H40L24 85V69H6Z M42 43H108V94H90L75 109V94H42"/><path d="M18 36H52 M61 60H91 M66 77H91"/>'
    elif kind=='chatub':body='<circle cx="8" cy="20" r="5"/><circle cx="8" cy="51" r="5"/><circle cx="8" cy="82" r="5"/><path d="M13 20H35L58 51H106 M13 51H106 M13 82H35L58 51"/><rect x="81" y="34" width="30" height="34" fill="none"/>'
    elif kind=='absher-insight':body=''.join(f'<rect x="{i*28}" y="{j*28}" width="17" height="17" opacity="{.3+((i*3+j)%4)*.2}"/>' for i in range(4) for j in range(4))+'<path d="M0 94L25 66 53 79 82 22 110 38"/>'
    else:body='<path d="M0 95A54 54 0 0 1 108 95 M19 95A35 35 0 0 1 89 95 M40 95A14 14 0 0 1 68 95 M54 0V37 M0 25L20 45 M108 25L88 45"/><circle cx="41" cy="67" r="4"/><circle cx="72" cy="61" r="4"/>'
    return top+body+'</g>'

for idx,(slug,name,category,value,m1,m2,light,dark) in enumerate(PROJECTS):
    if idx<3:
        for theme,p0 in PALETTES.items():
            p=dict(p0);p['accent']=light if theme=='light' else dark
            p['bg']=({'raqmi':'#f0f2e7','portfolio':'#efedf5','chatub':'#f5eee7'} if theme=='light' else {'raqmi':'#171d13','portfolio':'#191923','chatub':'#211b16'})[slug]
            for mobile in [False,True]:
                w,h=(400,136) if mobile else (800,152)
                b=text(22 if mobile else 30,36 if mobile else 47,name,28 if mobile else 39,weight=700)
                b+=text(22 if mobile else 30,61 if mobile else 79,category,18 if mobile else 22,p['muted'])
                if mobile:b+=text(22,97,m1,19)+text(22,122,m2,19)
                else:b+=text(30,126,value,28)
                b+=motif(slug,308 if mobile else 659,25 if mobile else 19,.66 if mobile else 1,p['accent'])
                suffix=('-mobile' if mobile else '')+'-'+theme
                svg(f'assets/projects/{slug}{suffix}.svg',w,h,p,f'{name} — {category}. {value}',f'Open the public {name} repository. '+value,b)
    p=dict(PALETTES['dark']);p['accent']=dark
    b=text(56,65,'ABDULELAH / SELECTED WORK',24,p['muted'])
    b+=text(56,170,category,28,p['accent'])
    b+=text(56,300,name,104 if len(name)<13 else 86,weight=700)
    b+=text(56,382,m1,42)+text(56,438,m2,42)
    b+=line(56,541,1224,541,p['line'])+text(56,587,'Arabic-first AI. Product-minded engineering.',25,p['muted'])
    b+=motif(slug,922,177,2.5,p['accent'])
    svg(f'assets/social/{slug}.svg',1280,640,p,f'{name} by Abdulelah',value,b)

p=PALETTES['dark'];b=text(56,65,'ABDULELAH ALKHATHAMI',26,p['muted'])+text(56,169,'AI PRODUCT BUILDER',30,p['accent'])
b+=text(56,301,'AI that earns',105,weight=700)+text(56,421,'the next step.',105,weight=700)
b+=gate(990,242,1.8,p)+line(56,541,1224,541,p['line'])+text(56,587,'Arabic-first systems. Thoughtful product UX.',28,p['muted'])
svg('assets/social/profile.svg',1280,640,p,'Abdulelah Alkhathami — AI Product Builder','AI that earns the next step. Arabic-first systems and thoughtful product UX.',b)
print('Generated responsive profile and project SVGs plus six social-preview masters.')
