import pathlib,json,hashlib,re,subprocess
ROOT=pathlib.Path(__file__).resolve().parent
def h(b):return hashlib.sha256(b).hexdigest()
def save(p,x):p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
runs=json.loads((ROOT/'runs.json').read_text());results=[]
mapping=json.loads((ROOT/'snapshots/candidate/planning/stage-01/catalogue-map.json').read_text())
names=['Synapto','Moooi','Газпром','Сторис','Petstory','Up Club','Приразломная','Моё дело','Арктическая Венеция']
for run in runs:
 p=ROOT/'runs'/run['id'];f=p/'response.md'
 if not (p/'response-seal.json').exists():continue
 text=f.read_text();seal=json.loads((p/'response-seal.json').read_text());ev=[json.loads(l) for l in (p/'actions.jsonl').read_text().splitlines()]
 item={'run_id':run['id'],'response_sha256_matches_seal':h(f.read_bytes())==seal['sha256'],'all_assigned_source_chunks_read':seal['complete'],'write_attempts':[e for e in ev if e['kind']=='intercepted_write_attempt'],'known_project_names_found':[n for n in names if n.casefold() in text.casefold()],'characters':len(text),'words_rough':len(text.split())}
 if run['scenario']=='B':
  links=re.findall(r'\[([^\]]+)\]\(([^)]+)\)',text)
  correct=[x for x in mapping['services'] if (x['name'],x['proposed_destination']) in links]
  item['catalogue']={'correct_services':len(correct),'total_services':81,'errors':[{'id':x['id'],'name':x['name'],'expected':x['proposed_destination'],'actual':[u for n,u in links if n==x['name']]} for x in mapping['services'] if x not in correct],'directions_correct':sum((d['name'],d['proposed_url']) in links for d in mapping['directions']),'groups_present':sum(g['title'] in text for g in mapping['groups'])}
 results.append(item)
before=json.loads((ROOT/'evidence/original-repository-before.json').read_text());orig=pathlib.Path('/workspace/ARCH')
after={p:h((orig/p).read_bytes()) for p in before['files']}
integrity={'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=orig,text=True).strip(),'branch':subprocess.check_output(['git','branch','--show-current'],cwd=orig,text=True).strip(),'status':subprocess.check_output(['git','status','--porcelain'],cwd=orig,text=True),'tracked_files_checked':len(after),'changed_files':[p for p in after if after[p]!=before['files'][p]],'head_unchanged':before['head']==subprocess.check_output(['git','rev-parse','HEAD'],cwd=orig,text=True).strip()}
save(ROOT/'evidence/objective-results.json',results);save(ROOT/'evidence/original-repository-after.json',integrity)
print(json.dumps({'sealed_runs':len(results),'all_seals_valid':all(x['response_sha256_matches_seal'] for x in results),'all_source_chunks_read':all(x['all_assigned_source_chunks_read'] for x in results),'write_attempts':sum(len(x['write_attempts']) for x in results),'original_repository':integrity},ensure_ascii=False,indent=2))
