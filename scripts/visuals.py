"""Self-contained motion graphics shared by the identity and project directory."""
from html import escape
import math
from repo_art import art, STYLE as MINI_STYLE
BG='#0E1116'; WHITE='#F8F8F3'; SUB='#BCFCF6'; LINE='#343044'; COPPER='#FF4081'; STEEL='#A783F7'
STYLE='''
@keyframes traverse{from{stroke-dashoffset:0}to{stroke-dashoffset:-1700}}
@keyframes drift{50%{transform:translateX(22px)}}
@keyframes words{0%,18%{transform:translateY(0)}25%,43%{transform:translateY(-68px)}50%,68%{transform:translateY(-136px)}75%,93%{transform:translateY(-204px)}100%{transform:translateY(-272px)}}
@keyframes breathe{50%{opacity:.35}}
@keyframes unveil{0%,10%{stroke-dashoffset:1100}70%,100%{stroke-dashoffset:0}}
@keyframes cursor{50%{opacity:0}}
@keyframes sheen{0%,12%{transform:translateX(-1400px)}65%,100%{transform:translateX(1400px)}}
@keyframes lift{50%{transform:translateY(-7px)}}
.travel{display:none}
.drift{animation:drift 12s ease-in-out infinite}
.words{animation:words 24s cubic-bezier(.65,0,.2,1) infinite}
.pulse{animation:breathe 7s ease-in-out infinite}
.draw{stroke-dasharray:1100;animation:unveil 14s ease-in-out infinite}
.cursor{animation:cursor 1.4s steps(1,end) infinite}
.sheen{animation:sheen 15s cubic-bezier(.4,0,.2,1) infinite}
.lift{animation:lift 11s ease-in-out infinite}
@media(prefers-reduced-motion:reduce){.travel,.drift,.words,.pulse,.draw,.cursor,.field,.sheen,.lift{animation:none!important}}
'''
def txt(x,y,s,size=16,c=WHITE,weight=400,extra='',font='Arial, Helvetica, sans-serif'):
 return f'<text x="{x}" y="{y}" fill="{c}" font-size="{size}" font-weight="{weight}" font-family="{font}" {extra}>{escape(str(s))}</text>'
def mono(x,y,s,size=11,c=SUB,extra=''):return txt(x,y,s,size,c,400,extra,'Consolas, monospace')
def path(d,c=LINE,w=1,extra=''):return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" {extra}/>'
def rule(y,w=1120,delay=0):return path(f'M32 {y}H{w-32}',LINE)+path(f'M32 {y}H{w-32}','url(#prism)',2,extra=f'class="travel" style="animation-delay:-{delay}s"')
STYLE+=MINI_STYLE

def svg(w,h,body,title,desc='',css=''):
 defs='''<defs><linearGradient id="prism"><stop stop-color="#BCFCF6"/><stop offset=".4" stop-color="#FF4081"/><stop offset=".73" stop-color="#A783F7"/><stop offset="1" stop-color="#F3D962"/></linearGradient><linearGradient id="foil" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#F8F8F3"/><stop offset=".25" stop-color="#FF4081"/><stop offset=".52" stop-color="#BCFCF6"/><stop offset=".72" stop-color="#A783F7"/><stop offset="1" stop-color="#F3D962"/></linearGradient><radialGradient id="aura"><stop stop-color="#4E7AB5" stop-opacity=".2"/><stop offset="1" stop-color="#0E1116" stop-opacity="0"/></radialGradient></defs>'''
 return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">{escape(desc or title)}</desc>{defs}<style>{STYLE}{css}</style><rect width="100%" height="100%" fill="{BG}"/>{body}</svg>'
def wrap(s,length):
 words=s.split();out=[];line=''
 for word in words:
  if line and len(line)+len(word)+1>length:out.append(line);line=word
  else:line=(line+' '+word).strip()
 if line:out.append(line)
 return out
def field(x,y,w,h,lines=34):
 body='';css=''
 for i in range(lines):
  def shape(phase):
   pts=[]
   for n in range(65):
    u=n/64;v=i/(lines-1)
    yy=y+h*v+math.sin(u*math.pi*2+v*3+phase)*h*.42*math.sin(u*math.pi)
    xx=x+w*u+math.sin(v*math.pi)*math.sin(u*math.pi)*w*.05
    pts.append(f'{xx:.1f} {yy:.1f}')
   return 'M'+'L'.join(pts)
  d1,d2=shape(0),shape(1.5)
  color='url(#prism)'
  body+=path(d1,color,1.4 if i%6==0 else .9,extra=f'class="field" style="opacity:{.3+.5*i/lines:.3f};animation:field{i} {14+i%5}s ease-in-out infinite"')
  css+=f'@keyframes field{i}{{0%,100%{{d:path("{d1}")}}50%{{d:path("{d2}")}}}}'
 return body,css

def heading(label,subtitle='',mobile=False):
 w,h=(640,215) if mobile else (1120,190)
 b=rule(15,w)+mono(32,43,'FIELD / '+label.upper(),19,COPPER)
 if mobile:
  for i,s in enumerate(wrap(label,29)):b+=txt(30,91+i*37,s,32,WHITE,600)
 else:
  extra='letter-spacing="-1.5"'
  if len(label)>37:extra+=' textLength="1050" lengthAdjust="spacingAndGlyphs"'
  b+=txt(30,94,label,45,'url(#foil)',600,extra=extra)
  b+=txt(32,124,subtitle,16,SUB)
 for i in range(4):
  yy=h-18+i*3
  d=f'M32 {yy}C{w*.28} {yy-14-i*2} {w*.7} {yy+13+i*2} {w-32} {yy-1}'
  b+=path(d,'url(#prism)',1,extra=f'opacity="{.3+i*.14}"')+path(d,'url(#prism)',1.8,extra=f'class="travel" style="animation-delay:-{i*3}s"')
 return svg(w,h,b,label,subtitle)

def repo_row(title,description,flags='',mobile=False,phase=0,kind='code'):
 w,h=(640,240) if mobile else (1120,140)
 b=rule(h-2,w,phase)
 b+=path(f'M17 19V{h-22}','url(#prism)',2,extra='opacity=".65"')
 if mobile:
  for i,s in enumerate(wrap(title,24)):b+=txt(31,45+i*35,s,28,WHITE,600)
  for i,s in enumerate(wrap(description,55)[:2]):b+=txt(32,156+i*25,s,19,SUB)
  if flags:b+=mono(32,221,flags.strip(' ·').upper(),18,COPPER)
  b+='<g transform="translate(440 10) scale(.9)">'+art(kind)+'</g>'
 else:
  b+=txt(32,40,title,27,WHITE,600,extra='letter-spacing="-.6"')
  if flags:b+=mono(32,121,flags.strip(' ·').upper(),16,COPPER)
  for i,s in enumerate(wrap(description,99)[:2]):b+=txt(32,74+i*23,s,17,SUB)
  b+='<g transform="translate(904 5)">'+art(kind)+'</g>'
 return svg(w,h,b,title,description+flags)
