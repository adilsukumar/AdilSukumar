"""Build the public project directory without changing handwritten README content."""
from pathlib import Path
from collections import defaultdict
from html import escape
import argparse, json, os, re, urllib.request, urllib.parse
import hashlib
from visuals import heading, repo_row
from repo_art import KINDS,canonical,kind_for

ROOT=Path(__file__).resolve().parents[1]
OWNER='adilsukumar'
EXCLUDED={'amazon-ml-challenge-2026'}
START='<!-- PROJECTS:START -->'
END='<!-- PROJECTS:END -->'
SECTORS=[('intelligence', 'Artificial Intelligence & Intelligent Systems', 'Models, language tools, voice assistants, research tools, and interview intelligence.'), ('vision', 'Computer Vision & Human Motion', 'Visual perception, helmet detection, and pose estimation.'), ('bio', 'Bioinformatics & Biomedical Research', 'Genomic pipelines, ECG modelling, and reproducible biomedical analysis.'), ('applications', 'Web & App Development', 'Finance, pet care, education, digital safety, community, and business applications.'), ('hardware', 'Robotics, Embedded & Product Design', 'Carrying robots, connected devices, and assistive physical-product research.'), ('dsa', 'Data Structures & Algorithms', 'Problem-solving practice, curriculum trackers, and reference collections.'), ('personal', 'Portfolio & Profile', 'My personal website and GitHub profile.'), ('new', 'Other & Emerging Work', 'New public projects awaiting a confident field match.')]
KNOWN={
 'Zebrafish-Formaldehyde-Toxicity':('bio','Zebrafish formaldehyde toxicity','Reproducible adult-zebrafish screening analysis with documented limitations.'),
 'CyberSHE-WiCyS-Hackathon':('community','CyberSHE','A hackathon project focused on women’s digital safety.'),
 'Moomentum':('pet','Moomentum','Animal-care interface prototypes and sensor-analysis experiments.'),
 'SCLC-Somatic-Variant-Analysis':('bio','SCLC somatic variant analysis','A sequencing-to-variant pipeline for CD56+ circulating tumor cells.'),
 'KAN-ECG-Research_Paper':('bio','KAN × ECG','Cross-dataset ECG classification and symbolic fidelity research.'),
 'Portiva':('robotics','Portiva','Android + Arduino carrying robot; hardware validation in progress.'),
 'Smart-Helmet-Vision':('vision','Smart Helmet Vision','Helmet-vision research, a web demo, and Python tooling.'),
 'SoftSpace':('design','SoftSpace','Passive-headphone and glasses-friendly cushion research prototypes.'),
 'Atlas-Voice-Assistant':('assistants','Atlas Voice Assistant','Python voice/text commands with optional speech recognition.'),
 'Whisper-for-Windows':('assistants','Whisper for Windows','Windows voice and screen assistant; developer prototype.'),
 'Amazon_ML_Challenge_2026':('ml','Amazon ML Challenge 2026','A team solution for business entity resolution.'),
 'SciGenius-Research_Paper_Builder':('ml','SciGenius','NLP knowledge graphs and research-writing tools.'),
 'Pawsitive_Diagnostics_v1':('pet','Pawsitive Diagnostics · v1','A pet-health monitoring web interface.'),
 'Pawsitive_Diagnostics_v2':('pet','Pawsitive Diagnostics · v2','A further pet-care application prototype.'),
 'Pawsitive_Diagnostics_Website':('pet','Pawsitive · website','The project’s public-facing landing page.'),
 'MOoomentum...':('pet','MOoomentum','A Japan-focused pet-care application concept.'),
 'Finly_Personal_Finance':('finance','Finly','Personal finance and expense tracking.'),
 'SplitSmart-Smart_Expense_Splitter':('finance','SplitSmart','Shared expenses and group balances.'),
 'Spendture_Website':('finance','Spendture · website','The Spendture finance platform’s website.'),
 'CardSavvy':('finance','CardSavvy','Credit-card comparison and wallet prototype with heuristic scoring.'),
 'ATS_Resume-to-Job_Fit_Analyzer':('career','Resume-to-Job Fit Analyzer','NLP-based resume and job-description comparison.'),
 'AI-Mock-Interviewer':('career','AI Mock Interviewer','Voice-based interview practice.'),
 'Lead-Radar':('career','Lead Radar','Startup lead discovery and qualification.'),
 'LeadForge-Pro_Website':('career','LeadForge Pro','Business discovery and agency lead-generation tools.'),
 'SkillNests':('community','SkillNests','A collaborative educational platform.'),
 'CyberSHE_WiCyS_Hackathon_.Saras-Hack-Squad':('community','CyberSHE','A hackathon project focused on women’s digital safety.'),
 'AMOM-A_Map_Of_Memories':('community','A Map of Memories','Personal stories pinned to places around the world.'),
 'Posture-Detection':('vision','Posture Monitor','Browser-based pose estimation and posture feedback.'),
 'DSA_Data-Structures-and-Algorithms':('dsa','DSA journey','My data-structures and algorithms practice.'),
 'A2Z-DataSheet-Replica':('dsa','A2Z DSA tracker','A curriculum tracker based on the A2Z problem sheet.'),
 'leetcode-company-wise-problems-2022':('dsa','Company-wise problem lists','An upstream reference collection, dated May 2022.'),
 'Website':('personal','Personal website','My web portfolio.'),
 'AdilSukumar':('personal','This profile','My GitHub introduction and public project directory.')}
TOPICS={'bioinformatics':'bio','ecg':'bio','genomics':'bio','robotics':'robotics','embedded-systems':'robotics','iot':'robotics','accessibility':'design','cad':'design','voice-assistant':'assistants','speech-recognition':'assistants','entity-resolution':'ml','nlp':'ml','pet-health':'pet','personal-finance':'finance','expense-tracker':'finance','interview-preparation':'dsa','data-structures':'dsa','lead-generation':'career','education':'community','digital-safety':'community','portfolio':'personal'}
RULES=[('bio',r'bioinformatics|genomic|\becg\b|somatic|sequencing'),('pet',r'pawsitive|pet.health|dog.collar|wancare'),('robotics',r'robot|arduino|esp32|embedded|helmet.vision'),('design',r'headphone|sensory.design|cushion|assistive.product'),('assistants',r'voice.assistant|desktop.assistant|screen.assistant|speech.recognition'),('finance',r'credit.card|personal.finance|expense|wallet'),('career',r'resume|job.fit|mock.interview|lead.generation|startup.lead'),('dsa',r'\bdsa\b|leetcode|algorithm.practice|data.structures'),('ml',r'entity.resolution|machine.learning|knowledge.graph|research.paper'),('community',r'education|digital.safety|community|memor(y|ies)')]
def _classify_original(repo):
 name=repo['name']
 known={canonical(k):v for k,v in KNOWN.items()}
 if canonical(name) in known:return known[canonical(name)]
 topics=repo.get('topics',[])
 valid={x[0] for x in SECTORS}|{'assistants','ml','finance','career','community','pet','robotics','design'}
 for topic in topics:
  if topic.startswith('sector-') and topic[7:] in valid:return topic[7:],name,None
 for topic in topics:
  if topic in TOPICS:return TOPICS[topic],name,None
 haystack=(name+' '+(repo.get('description') or '')).lower()
 for sector,pattern in RULES:
  if re.search(pattern,haystack):return sector,name,None
 return 'new',name,None

def classify(repo):
 sector,title,description=_classify_original(repo)
 mapping={'assistants':'intelligence','ml':'intelligence','finance':'applications','career':'applications','community':'applications','pet':'applications','robotics':'hardware','design':'hardware'}
 if canonical(repo['name']) in {'ats-resume-job-fit-analyzer','ai-mock-interviewer'}:sector='intelligence'
 return mapping.get(sector,sector),title,description

def fetch_public():
 result=[];page=1
 while True:
  url=f'https://api.github.com/users/{OWNER}/repos?type=owner&per_page=100&page={page}'
  headers={'Accept':'application/vnd.github+json','User-Agent':'Adil-profile-directory','X-GitHub-Api-Version':'2026-03-10'}
  if os.environ.get('GH_TOKEN'):headers['Authorization']='Bearer '+os.environ['GH_TOKEN']
  with urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=30) as response:batch=json.load(response)
  if not isinstance(batch,list):raise ValueError('Unexpected GitHub response; README preserved')
  result.extend(batch)
  if len(batch)<100:break
  page+=1
 if not result:raise ValueError('Empty repository response; README preserved')
 return result

def clean(s):return escape(re.sub(r'\s+',' ',s).strip(),quote=True)
def generate(repos):
 # The explicit public check also protects local fixtures and authenticated runs.
 public={r['name']:r for r in repos if r.get('private') is False and r.get('owner',{}).get('login','').lower()==OWNER and canonical(r['name']) not in EXCLUDED}
 if not public:raise ValueError('No verified public repositories; README preserved')
 groups=defaultdict(list)
 for r in public.values():
  sector,title,desc=classify(r)
  desc=desc or r.get('description') or 'Open the repository for details.'
  if len(desc)>160:desc=desc[:157].rsplit(' ',1)[0]+'…'
  flags=(' · upstream fork' if r.get('fork') else '')+(' · archived' if r.get('archived') else '')
  url=f'https://github.com/{OWNER}/'+urllib.parse.quote(r['name'],safe='-._')
  groups[sector].append((title.lower(),f'<li><a href="{url}"><strong>{clean(title)}</strong></a>{clean(flags)} — {clean(desc)}</li>'))
 active=[s for s in SECTORS if groups[s[0]]]
 counts={k:len(v) for k,v in groups.items()}
 nav=' &nbsp; · &nbsp; '.join(f'<a href="#sector-{key}">{clean(label)}</a>' for key,label,_ in active)
 chunks=[f'<p><strong>{len(public)} public repositories</strong> · organized by field · forks included and credited</p>',f'<p>{nav}</p>']
 for key,label,intro in active:
  chunks += [f'<h3 id="sector-{key}">{clean(label)} <sub>/{counts[key]}</sub></h3>',f'<p><em>{clean(intro)}</em></p>','<ul>',*[x[1] for x in sorted(groups[key])],'</ul>']
 return '\n\n'.join(chunks),public,counts

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--input',type=Path);args=parser.parse_args()
 repos=json.loads(args.input.read_text(encoding='utf-8')) if args.input else fetch_public()
 body,public,counts=generate(repos)
 body=generate_visual(public,counts)
 readme=ROOT/'README.md';s=readme.read_text(encoding='utf-8')
 if s.count(START)!=1 or s.count(END)!=1:raise ValueError('Missing or duplicate directory markers; README preserved')
 left,tail=s.split(START);_,right=tail.split(END)
 updated=left+START+'\n\n'+body+'\n\n'+END+right
 if updated!=s:readme.write_text(updated,encoding='utf-8')
 print(json.dumps({'public_repositories':len(public),'sectors':counts,'changed':updated!=s}))

def generate_visual(public,counts):
 directory=ROOT/'assets/directory';directory.mkdir(parents=True,exist_ok=True)
 def save(name,content):
  file=directory/name
  if not file.exists() or file.read_text(encoding='utf-8')!=content:file.write_text(content,encoding='utf-8')
 active=[s for s in SECTORS if counts.get(s[0])]
 nav=' &nbsp; · &nbsp; '.join(f'<a href="#sector-{key}">{clean(label)}</a>' for key,label,_ in active)
 chunks=[f'<p><strong>{len(public)} public repositories · {len(active)} fields</strong></p>']
 for key,label,intro in active:
  short={'intelligence':'Artificial Intelligence','applications':'Web & App Development','hardware':'Robotics, Embedded & Design','bio':'Biomedical Research','robotics':'Robotics & Embedded','vision':'Vision & Human Motion','design':'Assistive Product Design','assistants':'Voice & Desktop AI','ml':'ML & Research Tools','pet':'Pet Health & Monitoring','finance':'Finance & Decision Tools','career':'Career & Business Tools','community':'Community & Digital Safety','dsa':'Algorithms & DSA','personal':'Personal Web & Profile'}.get(key,label)
  from visuals import svg,txt,path
  graphic='<rect x="2" y="2" width="426" height="74" rx="12" fill="#141320" stroke="#40364D"/>'+txt(20,34,short,22,'#BCFCF6',600)+txt(20,60,str(counts[key])+' repositories',16,'#F3D962')+path('M390 26l12 12-12 12','#FF4081',2,extra='class="pulse"')
  save('nav-'+key+'.svg',svg(430,78,graphic,label))
 chunks+=['<p align="center">'+''.join(f'<a href="#sector-{key}"><img src="assets/directory/nav-{key}.svg" width="270" alt="{clean(label)}"/></a> ' for key,label,intro in active)+'</p>']
 def image(base,alt):
  return f'<picture><source media="(max-width: 600px)" srcset="assets/directory/{base}-mobile.svg" /><img src="assets/directory/{base}.svg" width="100%" alt="{clean(alt)}" /></picture>'
 for key,label,intro in active:
  name='sector-'+key
  save(name+'.svg',heading(label,intro))
  save(name+'-mobile.svg',heading(label,intro,True))
  chunks+=[f'<a id="sector-{key}"></a>',f'<p>{image(name,label+". "+intro)}</p>']
  entries=[r for r in public.values() if classify(r)[0]==key]
  for repo in sorted(entries,key=lambda r:classify(r)[1].lower()):
   _,title,desc=classify(repo);desc=desc or repo.get('description') or 'Open the repository for details.'
   if len(desc)>112:desc=desc[:109].rsplit(' ',1)[0]+'…'
   flags=(' · upstream fork' if repo.get('fork') else '')+(' · archived' if repo.get('archived') else '')
   digest=hashlib.sha256(repo['name'].encode()).hexdigest()
   base='repo-'+digest[:12]
   phase=int(digest[:2],16)/20
   kind=kind_for(repo['name'])
   save(base+'.svg',repo_row(title,desc,flags,False,phase,kind))
   save(base+'-mobile.svg',repo_row(title,desc,flags,True,phase,kind))
   url=f'https://github.com/{OWNER}/'+urllib.parse.quote(repo['name'],safe='-._')
   chunks+=[f'<p><a href="{url}">{image(base,title+flags+" — "+desc)}</a></p>']
 return '\n\n'.join(chunks)

if __name__=='__main__':main()
