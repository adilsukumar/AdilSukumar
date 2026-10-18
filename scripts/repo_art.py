"""Small animated vector scenes, chosen for each repository's actual subject."""
from html import escape
import math
KINDS={
 'KAN-ECG-Research_Paper':'ecg','SCLC-Somatic-Variant-Analysis':'dna','Zebrafish-Formaldehyde-Toxicity':'fish',
 'Portiva':'rover','Smart-Helmet-Vision':'helmet','Posture-Detection':'pose','SoftSpace':'headphones',
 'Atlas-Voice-Assistant':'microphone','Whisper-for-Windows':'desktop-voice','SciGenius-Research_Paper_Builder':'knowledge-graph',
 'Pawsitive_Diagnostics_v1':'paw-heart','Pawsitive_Diagnostics_v2':'pet-dashboard','Pawsitive_Diagnostics_Website':'pet-browser','Moomentum':'collar',
 'Finly_Personal_Finance':'coins','SplitSmart-Smart_Expense_Splitter':'split','Spendture_Website':'finance-browser','CardSavvy':'cards',
 'ATS_Resume-to-Job_Fit_Analyzer':'resume-scan','AI-Mock-Interviewer':'conversation','Lead-Radar':'radar','LeadForge-Pro_Website':'shop-browser',
 'AMOM-A_Map_Of_Memories':'memory-map','SkillNests':'learning-tree','CyberSHE-WiCyS-Hackathon':'shield',
 'DSA_Data-Structures-and-Algorithms':'sorting','A2Z-DataSheet-Replica':'checklist','leetcode-company-wise-problems-2022':'fork-code',
 'Website':'portfolio','AdilSukumar':'signature'}
STYLE='''
@keyframes mini-scan{0%,100%{transform:translateY(0)}50%{transform:translateY(42px)}}
@keyframes mini-dash{to{stroke-dashoffset:-180}}
@keyframes mini-turn{to{transform:rotate(360deg)}}
@keyframes mini-twist{50%{transform:scaleX(-1)}}
@keyframes mini-swim{0%,100%{transform:translateX(-8px)}50%{transform:translateX(18px)}}
@keyframes mini-flap{50%{transform:scaleX(.5)}}
@keyframes mini-route{0%,100%{transform:translateX(-12px)}50%{transform:translateX(18px)}}
@keyframes mini-level{0%,100%{transform:scaleY(.28)}50%{transform:scaleY(1)}}
@keyframes mini-bob{50%{transform:translateY(-9px)}}
@keyframes mini-blink{0%,100%{opacity:.2}50%{opacity:1}}
@keyframes mini-fan{50%{transform:rotate(11deg)}}
@keyframes mini-progress{0%,10%{stroke-dashoffset:140}75%,100%{stroke-dashoffset:0}}
@keyframes mini-sort{0%,100%{transform:translateY(0)}50%{transform:translateY(-22px)}}
.mini-scan{animation:mini-scan 4s ease-in-out infinite}
.mini-dash{stroke-dasharray:9 12;animation:mini-dash 5s linear infinite}
.mini-turn{transform-box:fill-box;transform-origin:center;animation:mini-turn 9s linear infinite}
.mini-twist{transform-origin:100px 60px;animation:mini-twist 7s ease-in-out infinite}
.mini-swim{animation:mini-swim 5s ease-in-out infinite}.mini-flap{transform-box:fill-box;transform-origin:right;animation:mini-flap 1s ease-in-out infinite}
.mini-route{animation:mini-route 7s ease-in-out infinite}
.mini-level{transform-box:fill-box;transform-origin:bottom;animation:mini-level 2s ease-in-out infinite}
.mini-bob{animation:mini-bob 4s ease-in-out infinite}.mini-blink{animation:mini-blink 4s ease-in-out infinite}
.mini-fan{transform-origin:100px 100px;animation:mini-fan 5s ease-in-out infinite}
.mini-progress{stroke-dasharray:140;animation:mini-progress 5s ease-in-out infinite}
.mini-sort{animation:mini-sort 5s ease-in-out infinite}
@media(prefers-reduced-motion:reduce){.mini-scan,.mini-dash,.mini-turn,.mini-twist,.mini-swim,.mini-flap,.mini-route,.mini-level,.mini-bob,.mini-blink,.mini-fan,.mini-progress,.mini-sort{animation:none!important}}
'''
C='#FF4081';B='#A783F7';W='#BCFCF6';G='#F3D962';DIM='#40364D'
ALIASES={'leadforge-pro-website':'leadforge-pro','splitsmart-smart-expense-splitter':'splitsmart-expense-splitter','ats-resume-to-job-fit-analyzer':'ats-resume-job-fit-analyzer'}
def canonical(name):
 key=name.lower().replace('_','-')
 return ALIASES.get(key,key)
def kind_for(name):return {canonical(k):v for k,v in KINDS.items()}.get(canonical(name),'code')
def p(d,c=C,w=2,cl=''):return f'<path d="{d}" stroke="{c}" fill="none" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" class="{cl}"/>'
def r(x,y,w,h,c=DIM,fill='none',rad=4):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rad}" stroke="{c}" stroke-width="1.6" fill="{fill}"/>'
def o(x,y,rad,c=C,fill='none',cl=''):return f'<circle cx="{x}" cy="{y}" r="{rad}" stroke="{c}" fill="{fill}" stroke-width="1.7" class="{cl}"/>'
def g(body,cl='',extra=''):return f'<g class="{cl}" {extra}>{body}</g>'
def bars(x=69,y=35,count=5):return ''.join(f'<rect x="{x+i*12}" y="{y+8*(i%2)}" width="5" height="{45-8*(i%2)}" rx="2" fill="{C if i%2 else B}" class="mini-level" style="animation-delay:-{i*.3}s"/>' for i in range(count))
def browser():return r(39,20,123,78,B)+p('M39 34H162',DIM,1)+o(46,27,1.2,G,G)+o(53,27,1.2,C,C)+o(60,27,1.2,B,B)
def paw(x=100,y=55):
 s=f'<path d="M{x-17} {y+17}Q{x-23} {y+5} {x-10} {y-3}Q{x} {y-16} {x+12} {y-3}Q{x+24} {y+8} {x+18} {y+18}Q{x+12} {y+24} {x} {y+18}Q{x-13} {y+25} {x-17} {y+17}Z" fill="none" stroke="{C}" stroke-width="2"/>'
 for dx,dy in [(-23,-9),(-8,-22),(8,-22),(23,-9)]:s+=f'<ellipse cx="{x+dx}" cy="{y+dy}" rx="4" ry="7" fill="none" stroke="{C}" stroke-width="1.7"/>'
 return s
def art(kind):
 s=''
 if kind=='ecg':
  s=p('M20 62H49L60 52L71 76L84 21L99 100L114 62H139L153 50L166 62H185',DIM,1.5)+p('M20 62H49L60 52L71 76L84 21L99 100L114 62H139L153 50L166 62H185',C,2.5,'mini-dash')
 elif kind=='dna':
  for y in range(20,105,8):
   x=100+28*math.sin((y-20)/84*math.pi*2);xx=200-x
   s+=p(f'M{x:.1f} {y}H{xx:.1f}',DIM,1)+o(x,y,2,C,C)+o(xx,y,2,B,B)
  s=g(s,'mini-twist')
 elif kind=='fish':
  s=p('M22 86Q42 79 62 86T102 86T142 86T182 86',DIM,1,'mini-dash')
  fish=p('M58 59Q98 25 143 59Q100 92 58 59Z',C)+p('M60 59L37 42V76Z',B)+p('M86 43L102 28L117 42M89 74L106 89L119 73',B)+o(128,55,2,W,W)
  s+=g(fish,'mini-swim')
 elif kind=='rover':
  s=p('M20 95H180',DIM,1,'mini-dash')+g(r(64,42,73,38,B)+r(83,27,35,15,C)+o(80,86,9,C)+o(124,86,9,C)+g(p('M80 80V92M74 86H86',G),'mini-turn')+g(p('M124 80V92M118 86H130',G),'mini-turn')+p('M99 26V17',C)+o(99,14,3,C,C),'mini-route')
 elif kind=='helmet':
  s=p('M57 71V62C57 15 141 15 141 62V71ZM48 72H150M79 29V54M120 29V54',C)+p('M42 96H158',DIM)+g(p('M47 41H152',G,2),'mini-scan')
 elif kind=='pose':
  s=o(100,25,9,C)+p('M100 34V69M100 45L70 57L58 40M100 45L128 57L141 41M100 69L79 98M100 69L122 99',B)+g(p('M48 33H153',G,1),'mini-scan')
 elif kind=='headphones':
  s=p('M58 67V55C58 5 141 5 141 55V67',B,4)+r(48,55,20,40,C,rad=9)+r(132,55,20,40,C,rad=9)+p('M81 66H94L100 73L106 66H120',W)+g(p('M35 58Q23 75 35 92M165 58Q178 75 165 92',C,2),'mini-blink')
 elif kind=='microphone':
  s=r(87,20,26,49,C,rad=13)+p('M76 50V57C76 88 124 88 124 57V50M100 81V100M83 100H117',B)+g(p('M56 44V67M145 41V70',G,3),'mini-level')
 elif kind=='desktop-voice':s=browser()+p('M82 109H120M101 97V109',B)+bars(67,44,6)
 elif kind=='knowledge-graph':
  for d in ['M45 60L99 24L150 60L100 96L45 60M99 24V96M45 60H150']:s+=p(d,DIM)
  s+=p('M45 60L99 24L150 60L100 96L45 60',C,2,'mini-dash')
  for i,(x,y) in enumerate([(45,60),(99,24),(150,60),(100,96)]):s+=g(o(x,y,6,B,'#0E1116'),'mini-blink',f'style="animation-delay:-{i}s"')
 elif kind=='paw-heart':s=paw()+p('M31 101H68L78 91L88 109L99 100H169',G,2,'mini-dash')
 elif kind=='pet-dashboard':s=browser()+g(paw(),'mini-blink')+p('M47 88H78M126 88H154',G,2,'mini-progress')
 elif kind=='pet-browser':s=browser()+g(paw(),'mini-bob')+p('M59 108H143',G,2,'mini-dash')
 elif kind=='collar':
  s=f'<ellipse cx="100" cy="65" rx="58" ry="25" fill="none" stroke="{B}" stroke-width="5"/>'+r(87,49,26,33,C,rad=6)+o(100,63,4,G,G)
  s+=g(p('M75 33Q100 9 125 33M84 39Q100 24 116 39',C),'mini-blink')
 elif kind=='coins':
  for i,(x,y) in enumerate([(62,83),(91,69),(121,54)]):s+=g(r(x,y-29,28,31,B,rad=12)+p(f'M{x+14} {y-23}V{y-4}',C),'mini-bob',f'style="animation-delay:-{i*.8}s"')
  s+=p('M38 103H167',DIM)
 elif kind=='split':
  s=o(49,61,15,B)+p('M64 61H91L132 28H163M91 61L132 94H163',C)+p('M64 61H91L132 28H163M91 61L132 94H163',G,3,'mini-dash')+p('M155 20L164 28L155 36M155 86L164 94L155 102',B)
 elif kind=='finance-browser':s=browser()+p('M55 82L77 65L94 75L122 47L149 54',C,2,'mini-progress')+p('M55 88H148',DIM)
 elif kind=='cards':s=g(r(63,33,89,57,B,rad=7)+r(73,43,20,11,C)+p('M77 77H102M110 77H135',G),'mini-fan')+r(47,48,90,57,C,rad=7)+p('M47 63H137',B,5)
 elif kind=='resume-scan':s=r(62,15,69,92,B)+p('M76 30H115M76 44H117M76 58H112M76 72H111M76 86H100',DIM,2)+g(p('M51 28H142',C,2),'mini-scan')+g(p('M137 81L146 91L165 67',G,3),'mini-blink')
 elif kind=='conversation':s=r(28,23,93,47,B,rad=8)+p('M47 70L39 86L68 70',B)+r(90,61,84,40,C,rad=8)+p('M151 101L159 111L135 101',C)+g(p('M43 44H105M104 80H159',G,2),'mini-dash')
 elif kind=='radar':
  s=o(100,62,45,DIM)+o(100,62,29,DIM)+o(100,62,13,DIM)+p('M50 62H150M100 12V112',DIM,1)
  s+=g(p('M100 62V17L119 22Z',C,2),'mini-turn')+g(o(119,40,4,G,G),'mini-blink')
 elif kind=='shop-browser':s=browser()+p('M66 76V58H135V76M60 57H141L130 43H71ZM82 76V63H95V76M107 63H122',C)+g(p('M68 89H135',G,2),'mini-progress')
 elif kind=='memory-map':
  s=p('M30 37L77 21L126 37L173 21V89L126 105L77 89L30 105ZM77 21V89M126 37V105',DIM)
  s+=g(p('M100 34C80 34 77 56 90 69L100 82L111 69C126 53 119 34 100 34Z',C)+o(100,49,5,G),'mini-bob')
 elif kind=='learning-tree':s=p('M100 99V62M100 62L55 37M100 62L145 37M100 62V20',DIM)+p('M100 99V62L55 37M100 62L145 37M100 62V20',C,2,'mini-dash')+o(55,37,9,B)+o(145,37,9,B)+o(100,20,9,G)
 elif kind=='shield':s=p('M100 16L144 33V65Q143 92 100 108Q56 91 56 65V33Z',B)+p('M77 60L94 78L124 45',C,3,'mini-progress')+g(p('M26 45H44M26 61H44M26 77H44',G,2),'mini-blink')
 elif kind=='sorting':
  for i,h in enumerate([24,51,33,66,43]):s+=g(r(45+i*23,97-h,14,h,C if i%2 else B,rad=2),'mini-sort',f'style="animation-delay:-{i*.9}s"')
  s+=p('M37 103H165',DIM)
 elif kind=='checklist':
  s=r(48,16,106,92,B)
  for i in range(3):
   y=35+i*25;s+=r(60,y-8,14,14,DIM)+p(f'M63 {y-1}L67 {y+3}L73 {y-5}',C,2,'mini-progress')+p(f'M85 {y}H139',B,2)
 elif kind=='fork-code':s=p('M58 26V92M58 65Q58 50 100 50H141V27',B)+o(58,23,6,C)+o(58,95,6,C)+o(141,23,6,G)+p('M58 65Q58 50 100 50H141V27',C,3,'mini-dash')+g(p('M116 78L106 86L116 94M136 78L146 86L136 94',G),'mini-blink')
 elif kind=='portfolio':s=browser()+r(50,44,28,39,C)+p('M89 48H145M89 60H137M89 73H124',B,2,'mini-progress')+g(p('M144 77V87',C,2),'mini-blink')
 elif kind=='signature':s=p('M29 94L62 26L93 94M44 65H80M165 34C132 12 105 39 125 53C138 64 174 56 170 81C165 109 127 105 112 88',DIM,3)+p('M29 94L62 26L93 94M44 65H80M165 34C132 12 105 39 125 53C138 64 174 56 170 81C165 109 127 105 112 88',C,2,'mini-dash')
 else:s=browser()+p('M72 51L59 63L72 76M126 51L139 63L126 76',C,2,'mini-dash')
 return f'<svg x="0" y="0" width="200" height="120" viewBox="0 0 200 120" data-motion-kind="{escape(kind,quote=True)}">{s}</svg>'
