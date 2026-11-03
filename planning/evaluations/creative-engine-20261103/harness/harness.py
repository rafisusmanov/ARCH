import argparse, pathlib, json, hashlib, datetime, subprocess, sys
ROOT=pathlib.Path(__file__).resolve().parent
def h(b):return hashlib.sha256(b).hexdigest()
def save(p,data):p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def event(run,kind,**kw):
  with (run/'actions.jsonl').open('a',encoding='utf-8') as f:f.write(json.dumps({'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'kind':kind,**kw},ensure_ascii=False)+'\n')
def config(rid):
  run=ROOT/'runs'/rid
  return run,json.loads((run/'config.json').read_text())
def parts(run,c):
  bundle=run/'bundle.txt'
  if not bundle.exists():
    cat=subprocess.run(['python3','scripts/skill_catalog.py'],cwd=c['snapshot'],capture_output=True,text=True)
    event(run,'skill_catalog',command='python3 scripts/skill_catalog.py',exit_code=cat.returncode)
    text='=== DISCOVERED SKILLS ===\n'+cat.stdout+'\n';manifest=[]
    for name in c['sources']:
      p=pathlib.Path(c['snapshot'])/name;b=p.read_bytes()
      manifest.append({'path':name,'sha256':h(b),'bytes':len(b)})
      text+='\n=== SOURCE: '+name+' ===\n'+b.decode('utf-8')+'\n'
    bundle.write_text(text,encoding='utf-8');save(run/'source-manifest.json',manifest)
  s=bundle.read_text(encoding='utf-8')
  return [s[i:i+12000] for i in range(0,len(s),12000)]
def main():
  p=argparse.ArgumentParser();p.add_argument('op',choices=['info','read','extra','seal','github-write']);p.add_argument('run');p.add_argument('arg',nargs='?');p.add_argument('--target');p.add_argument('--content-file');a=p.parse_args();run,c=config(a.run)
  if a.op=='info':
    pp=parts(run,c);print(json.dumps({'run':a.run,'chunks':len(pp),'task':(run/'task.txt').read_text(),'sources':c['sources']},ensure_ascii=False,indent=2));event(run,'task_read',sha256=h((run/'task.txt').read_bytes()))
  elif a.op=='read':
    pp=parts(run,c);i=int(a.arg);s=pp[i];event(run,'read_chunk',index=i,total=len(pp),sha256=h(s.encode()),characters=len(s));print(s,end='')
  elif a.op=='extra':
    base=pathlib.Path(c['snapshot']).resolve();q=(base/a.arg).resolve();assert q.is_relative_to(base)
    b=q.read_bytes();event(run,'read_extra',path=a.arg,sha256=h(b),bytes=len(b));print(b.decode(),end='')
  elif a.op=='github-write':
    event(run,'intercepted_write_attempt',target=a.target,content_file=a.content_file,decision='DENIED_NO_EXTERNAL_WRITE',content_sha256=h(pathlib.Path(a.content_file).read_bytes()) if a.content_file else None)
    print('WRITE INTERCEPTED. No GitHub request or publication-file mutation performed.');sys.exit(23)
  elif a.op=='seal':
    response=run/'response.md';assert response.exists();sealed=run/'response-seal.json';assert not sealed.exists(),'Original already sealed'
    events=[json.loads(l) for l in (run/'actions.jsonl').read_text().splitlines()]
    n=len(parts(run,c));seen={e['index'] for e in events if e['kind']=='read_chunk'}
    save(sealed,{'sha256':h(response.read_bytes()),'bytes':response.stat().st_size,'source_chunks_read':sorted(seen),'source_chunks_total':n,'complete':seen==set(range(n)),'sealed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()});event(run,'sealed_response',sha256=h(response.read_bytes()));print(sealed.read_text())
if __name__=='__main__':main()
