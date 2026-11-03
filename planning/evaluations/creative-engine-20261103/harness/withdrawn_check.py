"""Read revoked text into auditor memory only. Never restore it to a file or feed it to writers."""
import pathlib,subprocess,re,json,hashlib,unicodedata,collections
ROOT=pathlib.Path(__file__).resolve().parent
repo=pathlib.Path('/workspace/ARCH')
archived_commit=subprocess.check_output(['git','rev-parse','0701bc6^'],cwd=repo,text=True).strip()
paths=['planning/stage-02/'+x+'-page.md' for x in ['home','services','about','process','contact','client-workspace']]+['references/project/'+x for x in ['06_Architektonica_Reference_Texts.md','07_Architektonica_Copy_Registry.md','08_Architektonica_Site_Content_Plan.md','09_Engine_Home_Copy.md']]
def tokens(s):return re.findall(r'[\w]+',unicodedata.normalize('NFKC',s).casefold())
def grams(s,n=12):
 result=set()
 s=re.sub(r'\]\([^)]*\)',']',s)
 s=re.sub(r'<[^>]*>','',s)
 for paragraph in re.split(r'\n\s*\n',s):
  t=tokens(paragraph);result.update(tuple(t[i:i+n]) for i in range(len(t)-n+1))
 return result
archive={};manifest=[]
for name in paths:
 b=subprocess.check_output(['git','show',archived_commit+':'+name],cwd=repo)
 archive[name]=grams(b.decode());manifest.append({'path':name,'source_commit':archived_commit,'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)})
current=set()
for sub in ['references/project','methods','planning/stage-01']:
 for p in (ROOT/'snapshots/candidate'/sub).rglob('*'):
  if p.is_file() and p.suffix in ['.md','.json']:current.update(grams(p.read_text()))
results=[]
for run in json.loads((ROOT/'runs.json').read_text()):
 p=ROOT/'runs'/run['id']/'response.md'
 if not p.exists():continue
 observed=grams(p.read_text());matches=[]
 for name,gg in archive.items():
  suspicious=(observed & gg)-current
  if suspicious:matches.append({'archive_path':name,'unique_12_word_matches':[' '.join(x) for x in sorted(suspicious)]})
 results.append({'run_id':run['id'],'legacy_only_exact_matches':matches})
data={'method':'Exact normalized 12-word sequences within paragraphs, ignoring Markdown URLs and HTML tags, against 10 revoked documents immediately before reset 0701bc6; exclude sequences also present in current canonical references/methods/IA. Auditor-only in-memory git show. No restoration or writer access.','initial_scan_note':'The initial unsegmented scan flagged candidate-B-1 for concatenated canonical service labels plus URL fragments spanning paragraph boundaries. That is shared IA, not reproduced editorial prose. The initial result is retained separately; refined matching does not concatenate paragraphs or compare URL syntax.','archived_sources':manifest,'results':results,'limitations':['Does not detect paraphrase, semantic reuse, or unavailable revisions.','Shared factual names, service lists and current canonical descriptions are excluded; they are not evidence of restoring revoked copy.']}
(ROOT/'evidence/withdrawn-copy-check.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'runs_checked':len(results),'revoked_documents':len(manifest),'runs_with_legacy_only_exact_matches':sum(bool(x['legacy_only_exact_matches']) for x in results)},indent=2))
